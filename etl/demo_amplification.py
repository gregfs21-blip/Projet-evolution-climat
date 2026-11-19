"""P10.3 — amplification régionale : de combien la France et la Gironde se réchauffent pour 1 °C mondial.

Cadrage, critères A1-A7 et décisions D-AP et D-AQ validés par Grég le 19/11/2026, avant tout calcul
(docs/phases.md, section P10.3 ; sonde docs/sonde-p10c.md).

Modèle : T_rég(a) = c + k·G(a) + u(a), u AR(1) (Prais-Winsten itéré, etl/stats/regression.py), G = GISTEMP v4 en
moyenne glissante sur 4 ans (années a − 3 à a). France : composite LSH des 217 postes du réseau P5 complets jusqu'en
2024 (moyenne des départements), 1959-2024, 2022-2024 en partie bruts. Gironde : composite publié (4 postes),
1953-2024, 2023-2024 bruts. Informations sans critère : facteur contre la température des seules terres (CRUTEM5),
facteurs d'été et d'hiver, rapport des pentes de Sen.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import stats

from etl import demo_extremes as E
from etl.indicators import france as F
from etl.indicators import temperature as T
from etl.schema import (Amplification, AmplificationFit, AmplificationScale, AmplificationSeries, AmplificationVariant,
                        Criterion, Estimate, InputSource, Period)
from etl.sources import globaux as G
from etl.stats.regression import prais_winsten
from etl.stats.trend import annual_trend

FRANCE_SPAN = (1959, 2024)
FRANCE_HOM_END = 2021                 # fin du réseau constant homogénéisé de P5 (D-N), variante A5
GIRONDE_SPAN = (1953, 2024)
BASE = (1961, 1990)
SUB_START = 1979                      # A5
MIN_YEARS = 60                        # A1
RHO_MAX = 0.9                         # A2
LB_LAGS = 10                          # A2 (Ljung-Box)
LB_MIN = 0.05
REF_RANGE = (1.3, 2.0)                # R-A1 (A4)
REF_SOURCE = ("TRACC (ministère de la Transition écologique) : + 4 °C en France pour + 3 °C mondial en 2100, "
              "+ 2 °C pour + 1,5 °C en 2030 (rapport ≈ 1,33) ; Copernicus (C3S) et OMM, European State of the Climate "
              "2024 : l'Europe se réchauffe deux fois plus vite que la moyenne mondiale depuis les années 1980")
LAND_REF = ("GIEC AR6 GT1, SPM A.1.2 : 2011-2020 contre 1850-1900, + 1,09 °C pour le globe, + 1,59 °C sur les terres, "
            "+ 0,88 °C sur les océans")
STATIONS = (("bordeaux-merignac", "Bordeaux-Mérignac"), ("cap-ferret", "Cap-Ferret"), ("cazaux", "Cazaux"),
            ("villenave-d-ornon", "Villenave-d'Ornon"), ("bordeaux-paulin", "Bordeaux-Paulin"))
SEASONS = {"ete": ("été (juin-août)", ((0, 6), (0, 7), (0, 8))),
           "hiver": ("hiver (décembre-février)", ((-1, 12), (0, 1), (0, 2)))}

CRUTEM5 = G.Source("crutem5", "Met Office Hadley Centre / CRU — CRUTEM5, température moyenne des terres émergées",
                   "https://www.metoffice.gov.uk/hadobs/crutem5/data/CRUTEM.5.0.2.0/diagnostics/"
                   "CRUTEM.5.0.2.0.summary_series.global.annual.csv",
                   "https://www.metoffice.gov.uk/hadobs/crutem5/", "Open Government Licence v3", "°C",
                   G.parse_hadcrut5, drop_current_year=True)
BERKELEY = "temperature-berkeley-monde"


# ---------------------------------------------------------------- données


@dataclass(frozen=True)
class Regional:
    values: dict[int, float]
    hom: set[int]
    stations: int


def season_values(monthly: dict[tuple[int, int], float], hom: dict[tuple[int, int], bool], season: str
                  ) -> tuple[dict[int, float], set[int]]:
    """Moyenne saisonnière par année (hiver de l'année a : décembre a − 1, janvier et février a) ; saison complète
    seulement ; homogénéisée si ses trois mois le sont."""
    months = SEASONS[season][1]
    out, h = {}, set()
    for y in sorted({y for y, _ in monthly}):
        ks = [(y + dy, m) for dy, m in months]
        if all(k in monthly for k in ks):
            out[y] = sum(monthly[k] for k in ks) / 3
            if all(hom.get(k) for k in ks):
                h.add(y)
    return out, h


def anomaly(series: dict[int, float]) -> dict[int, float]:
    base = [series[y] for y in range(BASE[0], BASE[1] + 1) if y in series]
    if len(base) != BASE[1] - BASE[0] + 1:
        raise ValueError("P10.3 : normale 1961-1990 incomplète")
    m = sum(base) / len(base)
    return {y: v - m for y, v in series.items()}


def france_network(raw_dir: Path) -> tuple[str, ...]:
    """Réseau P5 (220 postes homogénéisés 1959-2021) restreint aux postes complets (12 mois de TN et TX) jusqu'à la fin
    de FRANCE_SPAN (D-AP)."""
    tn, tx = F._all("TN", str(raw_dir)), F._all("TX", str(raw_dir))
    out = []
    for p in F.t_network(str(raw_dir)):
        ok = all((y, m) in tn[p].values and (y, m) in tx[p].values
                 for y in range(FRANCE_HOM_END + 1, FRANCE_SPAN[1] + 1) for m in range(1, 13))
        if ok:
            out.append(p)
    return tuple(out)


def france(raw_dir: Path) -> tuple[Regional, dict[str, Regional]]:
    """Composite France (moyenne des départements) annuel et saisonnier, anomalies 1961-1990."""
    tn, tx = F._all("TN", str(raw_dir)), F._all("TX", str(raw_dir))
    net = france_network(raw_dir)
    annual, seasons = {}, {s: {} for s in SEASONS}
    for p in net:
        series, hom = F.station_annual("TM", tn[p], tx[p])
        annual[p] = (anomaly(series), hom)
        keys = tn[p].values.keys() & tx[p].values.keys()
        mon = {k: (tn[p].values[k] + tx[p].values[k]) / 2 for k in keys}
        mh = {k: tn[p].homogenized[k] and tx[p].homogenized[k] for k in keys}
        for s in SEASONS:
            v, h = season_values(mon, mh, s)
            seasons[s][p] = (anomaly(v), h)

    def build(per: dict) -> Regional:
        vals, hom = F.composite(per)
        span = range(FRANCE_SPAN[0], FRANCE_SPAN[1] + 1)
        return Regional({y: vals[y] for y in span if y in vals}, {y for y in hom if y in span}, len(per))

    return build(annual), {s: build(seasons[s]) for s in SEASONS}


def gironde_seasons(raw_dir: Path) -> dict[str, Regional]:
    """Composite saisonnier de Gironde, mêmes postes et même pondération (égale) que le composite annuel publié."""
    members, _ = T.composite_members("TM", raw_dir)
    out = {}
    for s in SEASONS:
        per = []
        for sid in members:
            mon, hom, _st = T.monthly("TM", sid, raw_dir)
            v, h = season_values(mon, hom, s)
            per.append((anomaly(v), h))
        years = sorted(set.intersection(*(set(a) for a, _ in per)))
        span = range(GIRONDE_SPAN[0], GIRONDE_SPAN[1] + 1)
        out[s] = Regional({y: sum(a[y] for a, _ in per) / len(per) for y in years if y in span},
                          {y for y in years if y in span and all(y in h for _a, h in per)}, len(per))
    return out


def published(out_dir: Path, path: str) -> tuple[dict[int, float], set[int]]:
    d = json.loads((out_dir / f"{path}.json").read_text(encoding="utf-8"))
    s = d["series"]
    q = s.get("quality") or ["homogenized"] * len(s["time"])
    vals = {int(t[:4]): v for t, v in zip(s["time"], s["value"]) if v is not None}
    hom = {int(t[:4]) for t, k, v in zip(s["time"], q, s["value"]) if v is not None and k == "homogenized"}
    return vals, hom


def load_land(raw_dir: Path) -> dict[int, float]:
    series = CRUTEM5.parse(G.fetch(CRUTEM5, raw_dir))
    if len(series) < 100:
        raise ValueError("CRUTEM5 : moins de 100 années lues, format probablement changé")
    return series


# ---------------------------------------------------------------- calcul


def ljung_box_p(u: np.ndarray, lags: int = LB_LAGS, fitted_params: int = 1) -> float:
    """Ljung-Box sur des résidus déjà blanchis ; degrés de liberté = lags − paramètres AR estimés."""
    u = np.asarray(u, float) - np.mean(u)
    n = len(u)
    den = float(u @ u)
    q = n * (n + 2) * sum((float(u[h:] @ u[:-h]) / den) ** 2 / (n - h) for h in range(1, lags + 1))
    return float(stats.chi2.sf(q, lags - fitted_params))


@dataclass(frozen=True)
class KFit:
    years: list[int]
    k: float
    lo: float
    hi: float
    c: float
    rho: float
    r2: float
    lb_p: float
    fitted: list[float]
    cov: list[float]

    def model(self, label: str) -> AmplificationFit:
        return AmplificationFit(label=label, period=Period(start=self.years[0], end=self.years[-1]), n=len(self.years),
                                k=Estimate(value=self.k, ci_low=self.lo, ci_high=self.hi), constant=self.c,
                                rho=self.rho, r2=self.r2, ljung_box_p=self.lb_p)


def fit_k(reg: dict[int, float], cov: dict[int, float], years: list[int] | None = None) -> KFit:
    """k de T_rég = c + k·G + u, u AR(1). Années : celles de `reg` (ou `years`) ; toutes doivent avoir G."""
    ys = sorted(reg) if years is None else list(years)
    missing = [y for y in ys if y not in cov or y not in reg]
    if missing:
        raise ValueError(f"P10.3 : années sans valeur régionale ou mondiale : {missing[:5]}")
    if any(b - a != 1 for a, b in zip(ys, ys[1:])):
        raise ValueError("P10.3 : années non consécutives")
    y = np.array([reg[a] for a in ys])
    x = np.array([cov[a] for a in ys])
    f = prais_winsten(y, x, ["G"])
    k, se = f.get("G")
    lo, hi = f.ci()
    e = f.resid
    w = np.sqrt(1 - f.rho ** 2)
    u = np.concatenate([[w * e[0]], e[1:] - f.rho * e[:-1]])
    return KFit(ys, k, float(lo[1]), float(hi[1]), float(f.coef[0]), f.rho, f.r2, ljung_box_p(u),
                [float(v) for v in f.fitted], [float(v) for v in x])


def overlap(a: tuple[float, float], b: tuple[float, float]) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]


def contiguous_raw_tail(years: list[int], hom: set[int]) -> bool:
    """Les années non homogénéisées sont toutes en fin de série (A1)."""
    raw = [y for y in years if y not in hom]
    return not raw or all(y not in hom for y in years if y >= raw[0])


def sen_ratio(reg: dict[int, float], glob: dict[int, float], years: list[int]) -> tuple[float, float, float]:
    r = annual_trend(years, [reg[y] for y in years]).slope_per_decade
    g = annual_trend(years, [glob[y] for y in years]).slope_per_decade
    return r, g, r / g


def analyse(fr: Regional, fr_seasons: dict[str, Regional], fr_published: tuple[dict[int, float], set[int]],
            gi: tuple[dict[int, float], set[int]], gi_seasons: dict[str, Regional],
            stations: dict[str, dict[int, float]], gis: dict[int, float], had: dict[int, float],
            berk: dict[int, float], land: dict[int, float]) -> dict:
    """Tout le calcul de P10.3, sans écriture."""
    Gs, Hs, Bs, Ls = E.smoothed(gis), E.smoothed(had), E.smoothed(berk), E.smoothed(land)
    gi_vals, gi_hom = gi
    scales = {
        "france": dict(label="France métropolitaine", vals=fr.values, hom=fr.hom, n_st=fr.stations,
                       seasons=fr_seasons, hom_only=(fr_published[0], fr_published[1]),
                       source=f"composite LSH de {fr.stations} postes, moyenne des départements"),
        "gironde": dict(label="Gironde", vals=gi_vals, hom=gi_hom, n_st=4, seasons=gi_seasons, hom_only=gi,
                        source="composite LSH publié de 4 postes"),
    }
    out = {"scales": {}, "variants": [], "land_global": None}
    lg_years = [y for y in range(min(min(s["vals"]) for s in scales.values()),
                                 max(max(s["vals"]) for s in scales.values()) + 1)]
    # Terres annuelles (non lissées) contre G lissé, comme les séries régionales : lisser les deux côtés rendrait les
    # résidus très autocorrélés (fenêtres qui se chevauchent).
    out["land_global"] = fit_k({y: land[y] for y in lg_years}, Gs)
    for sid, s in scales.items():
        years = sorted(s["vals"])
        main = fit_k(s["vals"], Gs)
        land_fit = fit_k(s["vals"], Ls)
        seas = {k: fit_k(r.values, Gs) for k, r in s["seasons"].items()}
        sr = sen_ratio(s["vals"], gis, years)
        out["scales"][sid] = dict(s, years=years, main=main, land=land_fit, seas=seas, sen=sr,
                                  raw=[y for y in years if y not in s["hom"]])
        hv, hh = s["hom_only"]
        hom_years = sorted(y for y in hv if y in hh and y >= years[0])
        for label, reg, cov, ys in (
            ("Covariable HadCRUT5", s["vals"], Hs, None),
            ("Covariable Berkeley Earth", s["vals"], Bs, None),
            ("Température mondiale annuelle, non lissée", s["vals"], gis, None),
            (f"Sous-période {SUB_START}-{years[-1]}", s["vals"], Gs, [y for y in years if y >= SUB_START]),
            (f"Années homogénéisées seules ({hom_years[0]}-{hom_years[-1]})", hv, Gs, hom_years),
        ):
            f = fit_k(reg, cov, ys)
            out["variants"].append(AmplificationVariant(
                scale=sid, group="robustesse", label=label, period=Period(start=f.years[0], end=f.years[-1]),
                n=len(f.years), k=Estimate(value=f.k, ci_low=f.lo, ci_high=f.hi), ok=bool(f.k > 1)))
    gmain = out["scales"]["gironde"]["main"]
    for slug, name in STATIONS:
        vals = stations[slug]
        f = fit_k(vals, Gs)
        ok = f.k > 0 and overlap((f.lo, f.hi), (gmain.lo, gmain.hi))
        out["variants"].append(AmplificationVariant(
            scale="gironde", group="poste", label=name, period=Period(start=f.years[0], end=f.years[-1]),
            n=len(f.years), k=Estimate(value=f.k, ci_low=f.lo, ci_high=f.hi), ok=bool(ok)))
    return out


def _f(x: float, nd: int, sign: bool = False) -> str:
    from etl.demonstration import _f as fmt
    return fmt(x, nd, sign)


def _k(f: KFit, nd: int = 2) -> str:
    return f"{_f(f.k, nd)} [{_f(f.lo, nd)} ; {_f(f.hi, nd)}]"


def build(fr: Regional, fr_seasons: dict[str, Regional], fr_published, gi, gi_seasons, stations, gis, had, berk,
          land, ctx_version: str, extracted_at) -> Amplification:
    r = analyse(fr, fr_seasons, fr_published, gi, gi_seasons, stations, gis, had, berk, land)
    S = r["scales"]
    F_, Gi = S["france"], S["gironde"]

    def a1(s) -> tuple[bool, str]:
        ys = s["years"]
        gaps = [y for y in range(ys[0], ys[-1] + 1) if y not in s["vals"]]
        tail = contiguous_raw_tail(ys, s["hom"])
        ok = not gaps and tail and len(ys) >= MIN_YEARS
        return ok, (f"{s['label']} {ys[0]}-{ys[-1]}, {len(ys)} années, "
                    f"{'aucune manquante' if not gaps else 'manquantes : ' + ', '.join(map(str, gaps))} ; "
                    f"{s['n_st']} postes à réseau constant ; années non homogénéisées "
                    f"{', '.join(map(str, s['raw'])) or 'aucune'}{'' if tail else ' (pas toutes en fin de série)'}")

    def a2(s) -> tuple[bool, str]:
        m = s["main"]
        ok = -RHO_MAX < m.rho < RHO_MAX and m.lb_p >= LB_MIN
        return ok, f"{s['label']} : ρ = {_f(m.rho, 2)}, Ljung-Box ({LB_LAGS} ans) p = {_f(m.lb_p, 2)}"

    c1 = [a1(F_), a1(Gi)]
    c2 = [a2(F_), a2(Gi)]
    a3 = [(s["main"].lo > 1, f"{s['label']} : k = {_k(s['main'])}") for s in (F_, Gi)]
    fm, gm = F_["main"], Gi["main"]
    a4_ok = overlap((fm.lo, fm.hi), REF_RANGE)
    rob = [v for v in r["variants"] if v.group == "robustesse"]
    posts = [v for v in r["variants"] if v.group == "poste"]
    a6_scale = overlap((gm.lo, gm.hi), (fm.lo, fm.hi))
    criteria = [
        Criterion(id="A1", label="Données", satisfied=all(ok for ok, _ in c1), detail=" | ".join(d for _, d in c1)),
        Criterion(id="A2", label="Ajustement", satisfied=all(ok for ok, _ in c2),
                  detail=" | ".join(d for _, d in c2) + f" (seuils : |ρ| < {_f(RHO_MAX, 1)}, p ≥ {_f(LB_MIN, 2)})"),
        Criterion(id="A3", label="Amplification", satisfied=all(ok for ok, _ in a3),
                  detail=" | ".join(f"{d} {'✓' if ok else '✗'}" for ok, d in a3) + " (borne basse > 1)"),
        Criterion(id="A4", label="Plausibilité", satisfied=a4_ok,
                  detail=f"intervalle de k France [{_f(fm.lo, 2)} ; {_f(fm.hi, 2)}] contre la fourchette "
                         f"[{_f(REF_RANGE[0], 1)} ; {_f(REF_RANGE[1], 1)}]"),
        Criterion(id="A5", label="Robustesse", satisfied=all(v.ok for v in rob),
                  detail=" | ".join(f"{S[v.scale]['label']}, {v.label} : k = {_f(v.k.value, 2)} "
                                    f"{'✓' if v.ok else '✗'}" for v in rob)),
        Criterion(id="A6", label="Cohérence", satisfied=a6_scale and all(v.ok for v in posts),
                  detail=f"intervalle Gironde [{_f(gm.lo, 2)} ; {_f(gm.hi, 2)}] contre France [{_f(fm.lo, 2)} ; "
                         f"{_f(fm.hi, 2)}] {'✓' if a6_scale else '✗'} | " + " ; ".join(
                             f"{v.label} {v.period.start}-{v.period.end} : k = {_f(v.k.value, 2)} "
                             f"[{_f(v.k.ci_low, 2)} ; {_f(v.k.ci_high, 2)}] {'✓' if v.ok else '✗'}" for v in posts)),
    ]
    ok = {c.id: c.satisfied for c in criteria}
    if all(ok[f"A{i}"] for i in range(1, 7)):
        confidence, reason = "elevee", ("Critères A1 à A6 conformes (règle D-AQ). k est un rapport observé : il ne dit "
                                        "pas pourquoi la région se réchauffe plus vite.")
    elif ok["A3"]:
        failed = ", ".join(f"{c.id} ({c.label.lower()})" for c in criteria if not c.satisfied)
        confidence, reason = "moyenne", (f"Amplification établie (A3), mais critère non conforme, d'où la confiance "
                                         f"« moyenne » (règle D-AQ) : {failed}. Détail : docs/validation-p10.md.")
    else:
        confidence, reason = "non_etabli", ("L'amplification n'est pas établie (A3) : la borne basse de l'intervalle "
                                            "de k ne dépasse pas 1 pour la France et la Gironde.")

    lg = r["land_global"]

    def land_class(s) -> str:
        lf = s["land"]
        return "egal" if lf.lo <= 1 <= lf.hi else ("plus" if lf.lo > 1 else "moins")

    land_words = {
        "egal": ("compatible avec 1 : {qui} se réchauffe{nt} comme la moyenne des terres, et {son} écart avec le monde "
                 "tient pour l'essentiel au contraste terres-océans"),
        "plus": ("au-dessus de 1 : {qui} se réchauffe{nt} aussi plus vite que la moyenne des terres, et le contraste "
                 "terres-océans n'explique qu'une partie de {son} écart avec le monde"),
        "moins": "sous 1 : {qui} se réchauffe{nt} moins que la moyenne des terres",
    }
    cF, cG = land_class(F_), land_class(Gi)
    if cF == cG:
        land_sentence = (f"Mesurés contre elles, les facteurs valent {_k(F_['land'])} pour la France et "
                         f"{_k(Gi['land'])} pour la Gironde, "
                         + land_words[cF].format(qui="toutes deux", nt="nt", son="leur") + ".")
    else:
        land_sentence = (f"Mesuré contre elles, le facteur vaut {_k(F_['land'])} pour la France, "
                         + land_words[cF].format(qui="elle", nt="", son="son") + f" ; il vaut {_k(Gi['land'])} pour la "
                         "Gironde, " + land_words[cG].format(qui="elle", nt="", son="son") + ".")
    fa, ga = fm.lo > 1, gm.lo > 1
    if fa and ga:
        amp_sentence = "toutes deux se réchauffent plus vite que le monde"
    elif not fa and not ga:
        amp_sentence = "ni l'une ni l'autre ne se réchauffe de façon établie plus vite que le monde"
    else:
        amp_sentence = (f"{'la France' if fa else 'la Gironde'} se réchauffe plus vite que le monde, "
                        f"{'la Gironde' if fa else 'la France'} pas de façon établie")
    def season_sentence() -> str:
        parts = []
        for name, sc in (("la France", F_), ("la Gironde", Gi)):
            e, h = sc["seas"]["ete"], sc["seas"]["hiver"]
            if e.lo > h.hi:
                rel = "nettement plus fort en été qu'en hiver"
            elif h.lo > e.hi:
                rel = "nettement plus fort en hiver qu'en été"
            elif abs(e.k - h.k) < 0.005:
                rel = "du même ordre en été et en hiver"
            else:
                rel = ("plus élevé en été qu'en hiver, sans que l'écart soit établi (intervalles qui se recoupent)"
                       if e.k > h.k else "plus élevé en hiver qu'en été, sans que l'écart soit établi (intervalles qui "
                       "se recoupent)")
            parts.append(f"pour {name}, {_k(e)} en été et {_k(h)} en hiver : {rel}")
        return "Saisons : " + " ; ".join(parts) + "."

    finding = (
        f"Pour 1 °C de réchauffement mondial (GISTEMP, moyenne sur 4 ans), la France se réchauffe de {_k(fm)} °C sur "
        f"{fm.years[0]}-{fm.years[-1]} et la Gironde de {_k(gm)} °C sur {gm.years[0]}-{gm.years[-1]} : "
        f"{amp_sentence}. Sur {lg.years[0]}-{lg.years[-1]}, les terres émergées dans leur ensemble (CRUTEM5) se "
        f"réchauffent de {_k(lg)} °C par °C mondial. {land_sentence} {season_sentence()}"
    )

    def scale_model(sid: str) -> AmplificationScale:
        s = S[sid]
        m = s["main"]
        return AmplificationScale(
            id=sid, label=s["label"], source=s["source"], stations=s["n_st"], fit=m.model("Contre le monde (GISTEMP lissé)"),
            land=s["land"].model("Contre les terres émergées (CRUTEM5 lissé)"),
            summer=s["seas"]["ete"].model(SEASONS["ete"][0]), winter=s["seas"]["hiver"].model(SEASONS["hiver"][0]),
            slope_regional=s["sen"][0], slope_global=s["sen"][1], slope_ratio=s["sen"][2],
            series=AmplificationSeries(years=m.years, values=[float(s["vals"][y]) for y in m.years], fitted=m.fitted,
                                       covariate=m.cov, raw_years=s["raw"]),
        )

    return Amplification(
        question="Pour 1 °C de réchauffement mondial, de combien la France et la Gironde se réchauffent-elles ?",
        model="T_rég(a) = c + k·G(a) + u(a), u AR(1) ; G = température mondiale lissée sur 4 ans",
        finding=finding, confidence=confidence, confidence_reason=reason,
        method_note=(
            "Anomalies annuelles de température moyenne (TM) par rapport à 1961-1990. France : composite des séries "
            f"homogénéisées de Météo-France (LSH), {fr.stations} postes du réseau de la phase P5 complets jusqu'en "
            f"{FRANCE_SPAN[1]}, moyenne des départements ; années postérieures à {FRANCE_HOM_END} en partie non "
            "homogénéisées. Gironde : composite publié de 4 postes. G : GISTEMP v4 en moyenne glissante sur 4 ans "
            "(années a − 3 à a), qui retire l'essentiel d'El Niño : une covariable bruitée sous-estimerait k. "
            "Estimation par moindres carrés généralisés avec erreurs autorégressives d'ordre 1 (Prais-Winsten itéré), "
            "intervalles à 95 %. Contrôle : même modèle contre la température moyenne des terres émergées (CRUTEM5). "
            "Saisons : anomalie de la saison contre le même G annuel. Rapport des pentes : pentes de Sen de la série "
            "régionale et de GISTEMP annuel sur la même période."),
        limitations=[
            "k est un rapport observé, pas une réponse forcée : il contient le contraste terres-océans, la baisse des "
            "aérosols européens depuis les années 1980, les changements de circulation et la variabilité propre de la "
            "région ; il n'attribue aucune cause, et la régression mondiale ci-dessus ne se transpose pas à la France.",
            f"k peut dépendre de la période : la variante {SUB_START}-fin le mesure.",
            f"France : années {FRANCE_HOM_END + 1}-{FRANCE_SPAN[1]} en partie non homogénéisées ; Gironde : "
            f"{', '.join(map(str, Gi['raw']))} non homogénéisées ; la variante « années homogénéisées seules » mesure "
            "leur effet.",
            "La Gironde ne compte que quatre postes au composite, dont trois proches du littoral ou du bassin "
            "d'Arcachon.",
            "Les références ne mesurent pas exactement k (périodes, bases et méthodes différentes) : le contrôle A4 est "
            "un recoupement avec une fourchette, pas une comparaison à une valeur.",
        ],
        inputs=[
            InputSource(name="Météo-France — Longues Séries Homogénéisées (LSH), TN et TX mensuelles",
                        url="https://www.data.gouv.fr/datasets/6569b2c4f1937611d4c8b1a3", license="Licence Ouverte 2.0 (Etalab)",
                        note=f"France : {fr.stations} postes ; Gironde : composite et postes publiés sur le site"),
            InputSource(name="GISTEMP v4, HadCRUT5, Berkeley Earth — température mondiale annuelle, telle que publiée sur le site",
                        url="https://projet-evolution-climat.vercel.app/monde", license="voir les pages des indicateurs"),
            InputSource(name=CRUTEM5.name, url=CRUTEM5.page, license=CRUTEM5.license, note="contrôle « terres », sans critère"),
        ],
        covariate="GISTEMP v4, moyenne glissante sur 4 ans", land_covariate="CRUTEM5, moyenne glissante sur 4 ans",
        land_global=lg.model("Terres émergées (CRUTEM5) contre le monde (GISTEMP)"), land_reference=LAND_REF,
        scales=[scale_model("france"), scale_model("gironde")], variants=r["variants"],
        reference_low=REF_RANGE[0], reference_high=REF_RANGE[1], reference_source=REF_SOURCE,
        criteria=criteria, script="etl/demo_amplification.py", etl_version=ctx_version, extracted_at=extracted_at,
    )


def load_and_build(out_dir: Path, raw_dir: Path, ctx_version: str, extracted_at) -> Amplification:
    fr, fr_seasons = france(raw_dir)
    stations = {slug: published(out_dir, f"gironde/tm-annuelle-{slug}")[0] for slug, _ in STATIONS}
    return build(fr, fr_seasons, published(out_dir, "france/tm-france"), published(out_dir, "gironde/tm-annuelle-gironde"),
                 gironde_seasons(raw_dir), stations, E.published(out_dir, E.GISTEMP), E.published(out_dir, E.HADCRUT),
                 E.published(out_dir, BERKELEY), load_land(raw_dir), ctx_version, extracted_at)
