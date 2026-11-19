"""P10.2 — valeurs extrêmes non stationnaires en Gironde (cadrage, critères X1-X7 et décisions D-AM à D-AO du
19/11/2026, validés par Grég avant tout ajustement ; docs/phases.md, section P10.2).

TXx (maximum annuel de TX) à Bordeaux-Mérignac, 1953-fin : années homogénéisées (correction B de P2a) prolongées par
les années brutes postérieures, si l'écart corrigé − brut après la dernière rupture le permet (X1). GEV dont la
position suit la température mondiale GISTEMP lissée sur 4 ans (etl/stats/gev.py). Les choix (station, années,
covariable, climats comparés, événements, nombre de tirages) sont ceux du cadrage, pas ajustés aux données.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np

from etl.schema import (Criterion, Estimate, ExtremeEvent, Extremes, ExtremeSeries, ExtremeVariant, GevCurve,
                        InputSource, Period, Unbounded)
from etl.stats import gev

MAIN = "33281001"                                   # Bordeaux-Mérignac
OTHERS = ("33236002", "33529001", "33550001", "33063001")  # Cap-Ferret, Cazaux, Villenave-d'Ornon, Bordeaux-Paulin
START = 1953
PAST_YEAR = 1960
PRE = (1880, 1900)
EVENT_YEAR = 2025                                   # record du 11/08/2025 (D-AN)
N_PAST = 20                                         # « 20 ans en 1960 » (D-AN)
SMOOTH = 4                                          # années a − 3 à a
N_BOOT = 1000
SEED = 1002
MAX_EXT_DIFF = 0.1                                  # X1
XI_RANGE = (-0.5, 0.2)                              # X2
KS_MIN = 0.05                                       # X2
ALPHA_LEVEL = 0.05                                  # X3
REFERENCE = (3.3, 2.5, 4.2)                         # R-X1
REFERENCE_SOURCE = ("Weather and Climate Dynamics 7, 439 (2026) : maximum des TX d'été en Europe de l'Ouest, "
                    "1950-2023, 3,3 [2,5 ; 4,2] fois le réchauffement mondial ; Vautard et al. (2023), Nature "
                    "Communications 14, 6803 : 3,4 °C par degré de réchauffement mondial (information)")
PERIODS = [1.1, 1.5, 2, 3, 5, 7, 10, 15, 20, 30, 50, 70, 100, 150, 200, 300, 500, 1000]
GISTEMP, HADCRUT = "temperature-gistemp-monde", "temperature-hadcrut5-monde"


@dataclass(frozen=True)
class Year:
    txx: float
    date: str
    tx3x: float | None
    status: str              # "homogenized" | "raw"
    txx_raw: float


@dataclass(frozen=True)
class StationMaxima:
    sid: str
    name: str
    last_break_regime: int | None
    years: dict[int, Year]

    def ext_diff(self) -> float:
        """Plus grand écart |TXx corrigé − brut| des années homogénéisées après la dernière rupture (X1)."""
        reg = self.last_break_regime or 0
        d = [abs(v.txx - v.txx_raw) for y, v in self.years.items() if v.status == "homogenized" and y > reg]
        return max(d) if d else 0.0

    def series(self, extend: bool = True, index: str = "txx", end: int | None = None) -> tuple[dict[int, float], list[int]]:
        """Années homogénéisées depuis START, prolongées (si `extend`) par les années brutes postérieures à la
        dernière année homogénéisée. Renvoie (valeurs, années prises brutes)."""
        hom = [y for y, v in self.years.items() if v.status == "homogenized" and y >= START]
        if not hom:
            return {}, []
        last = max(hom)
        out, raw = {}, []
        for y, v in sorted(self.years.items()):
            if y < START or (end is not None and y > end):
                continue
            val = v.txx if index == "txx" else v.tx3x
            if val is None:
                continue
            if v.status == "homogenized":
                out[y] = val
            elif extend and y > last:
                out[y] = val
                raw.append(y)
        return out, raw


# ---------------------------------------------------------------- lecture


def tx3(series: dict[str, float], year: int) -> float | None:
    """Maximum annuel de la moyenne de TX sur 3 jours consécutifs, sans trou."""
    best = None
    d = date(year, 1, 1)
    while d.year == year:
        keys = [(d + timedelta(days=k)).isoformat() for k in range(3)]
        if all(k in series for k in keys):
            v = sum(series[k] for k in keys) / 3
            best = v if best is None or v > best else best
        d += timedelta(days=1)
    return best


def load_station(sid: str, raw_dir: Path) -> StationMaxima:
    from etl.indicators import extremes as X  # import tardif : données Météo-France

    sd = X.station_daily("TX", sid, raw_dir)
    years = {}
    for y, st in sd.year_status.items():
        src = sd.corrected if st == "homogenized" else sd.raw
        days = {d: v for d, v in src.items() if d.startswith(f"{y}-")}
        raw_days = [v for d, v in sd.raw.items() if d.startswith(f"{y}-")]
        dmax = max(days, key=days.get)
        years[y] = Year(days[dmax], dmax, tx3(src, y), st, max(raw_days))
    return StationMaxima(sid, sd.station.name, sd.last_break_regime, years)


def smoothed(annual: dict[int, float], n: int = SMOOTH) -> dict[int, float]:
    """Moyenne glissante sur n ans, années a − n + 1 à a (aucune année future)."""
    return {y: sum(annual[y - k] for k in range(n)) / n for y in annual if all(y - k in annual for k in range(n))}


def published(out_dir: Path, iid: str) -> dict[int, float]:
    ind = json.loads((out_dir / "monde" / f"{iid}.json").read_text(encoding="utf-8"))
    return {int(t[:4]): v for t, v in zip(ind["series"]["time"], ind["series"]["value"]) if v is not None}


# ---------------------------------------------------------------- calcul


def arrays(values: dict[int, float], g: dict[int, float]) -> tuple[list[int], np.ndarray, np.ndarray]:
    years = [y for y in sorted(values) if y in g]
    return years, np.array([values[y] for y in years]), np.array([g[y] for y in years])


def pr(p_now: float, p_then: float) -> float:
    if p_then > 0:
        return p_now / p_then
    return np.inf if p_now > 0 else np.nan


def rp(p: float) -> float:
    return np.inf if p <= 0 else 1 / p


def unbounded(central: float, samples: np.ndarray) -> Unbounded:
    s = np.asarray(samples, float)
    undefined = int(np.sum(np.isnan(s)))
    s = s[~np.isnan(s)]
    lo, hi = gev.interval(s) if len(s) else (np.nan, np.nan)
    f = lambda v: None if (v is None or not np.isfinite(v)) else float(v)  # noqa: E731
    return Unbounded(value=f(central), ci_low=f(lo), ci_high=f(hi), undefined_draws=undefined)


def est(central: float, samples: np.ndarray | None = None) -> Estimate:
    if samples is None:
        return Estimate(value=float(central))
    lo, hi = gev.interval(np.asarray(samples, float))
    return Estimate(value=float(central), ci_low=float(lo), ci_high=float(hi))


def analyse(main: StationMaxima, others: list[StationMaxima], gis: dict[int, float], had: dict[int, float],
            n_boot: int = N_BOOT) -> dict:
    """Tout le calcul de P10.2, sans écriture. Renvoie les pièces du résultat publié."""
    G, GH = smoothed(gis), smoothed(had)
    g_now, g_past = G[EVENT_YEAR], G[PAST_YEAR]
    g_pre = float(np.mean([gis[y] for y in range(PRE[0], PRE[1] + 1)]))
    values, raw_years = main.series()
    years, x, g = arrays(values, G)
    if EVENT_YEAR not in values:
        raise ValueError(f"P10.2 : année de l'événement {EVENT_YEAR} absente")
    rec = values[EVENT_YEAR]
    rec_date = main.years[EVENT_YEAR].date

    f = gev.fit(x, g)
    lrt = gev.likelihood_ratio_p(x, g)
    ks = gev.ks_p(f, x, g)

    def stats_of(ff: gev.GevFit) -> np.ndarray:
        x20 = float(ff.return_level(N_PAST, g_past))
        p_now, p_past, p_pre = (ff.exceedance(rec, gg) for gg in (g_now, g_past, g_pre))
        q_now, q_pre = ff.exceedance(x20, g_now), ff.exceedance(x20, g_pre)
        x20_pre = float(ff.return_level(N_PAST, g_pre))
        return np.array([
            ff.alpha, ff.sigma, ff.xi,
            rp(p_now), rp(p_past), rp(p_pre), pr(p_now, p_past), pr(p_now, p_pre),
            ff.alpha * (g_now - g_past), ff.alpha * (g_now - g_pre),
            x20, rp(q_now), rp(q_pre), pr(q_now, 1 / N_PAST), pr(q_now, q_pre), x20_pre,
            *ff.return_level(PERIODS, g_now), *ff.return_level(PERIODS, g_past),
        ])

    central = stats_of(f)
    boot, failed = gev.bootstrap(x, g, n_boot, SEED, stats_of)
    col = lambda i: boot[:, i]  # noqa: E731
    k = len(PERIODS)

    events = [
        ExtremeEvent(id="record-2025", label=f"Record de {EVENT_YEAR} ({rec_date})", value=est(rec), date=rec_date,
                     return_period_today=unbounded(central[3], col(3)), return_period_past=unbounded(central[4], col(4)),
                     return_period_preindustrial=unbounded(central[5], col(5)),
                     probability_ratio=unbounded(central[6], col(6)),
                     probability_ratio_preindustrial=unbounded(central[7], col(7)),
                     intensity_change=est(central[8], col(8)), intensity_change_preindustrial=est(central[9], col(9))),
        ExtremeEvent(id="vingt-ans-1960", label=f"Chaleur de période de retour {N_PAST} ans en {PAST_YEAR}",
                     value=est(central[10], col(10)), date=None,
                     return_period_today=unbounded(central[11], col(11)),
                     return_period_past=Unbounded(value=float(N_PAST), ci_low=float(N_PAST), ci_high=float(N_PAST)),
                     return_period_preindustrial=unbounded(central[12], col(12)),
                     probability_ratio=unbounded(central[13], col(13)),
                     probability_ratio_preindustrial=unbounded(central[14], col(14)),
                     intensity_change=est(central[8], col(8)), intensity_change_preindustrial=est(central[9], col(9))),
    ]

    lv_now, lv_past = central[16:16 + k], central[16 + k:16 + 2 * k]
    b_now, b_past = boot[:, 16:16 + k], boot[:, 16 + k:16 + 2 * k]
    order = np.argsort(x)
    n = len(x)
    obs_periods = [(n + 1) / (n - r) for r in range(n)]           # rang de Weibull, du plus petit au plus grand
    curve = GevCurve(
        periods=PERIODS, today=_r(lv_now), past=_r(lv_past),
        today_low=_r(np.quantile(b_now, 0.025, axis=0, method="inverted_cdf")),
        today_high=_r(np.quantile(b_now, 0.975, axis=0, method="inverted_cdf")),
        past_low=_r(np.quantile(b_past, 0.025, axis=0, method="inverted_cdf")),
        past_high=_r(np.quantile(b_past, 0.975, axis=0, method="inverted_cdf")),
        obs_periods=_r(obs_periods),
        obs_today=_r(np.sort(x + f.alpha * (g_now - g))),
        obs_past=_r(np.sort(x + f.alpha * (g_past - g))),
    )
    series = ExtremeSeries(years=years, values=_r(x), raw_years=raw_years, mu=_r(f.mu(g)),
                           level20=_r(f.return_level(N_PAST, 0.0) + f.alpha * g))

    # X5 — robustesse (estimations centrales)
    variants: list[ExtremeVariant] = []

    def variant(label: str, vals: dict[int, float], cov: dict[int, float], event: float | None,
                group: str = "robustesse") -> ExtremeVariant:
        ys, xv, gv = arrays(vals, cov)
        ff = gev.fit(xv, gv)
        p = None if event is None else pr(ff.exceedance(event, cov[EVENT_YEAR]), ff.exceedance(event, cov[PAST_YEAR]))
        ok = ff.alpha > 0 and (p is None or (not np.isnan(p) and p > 1))
        status = "sans_objet" if p is None else "indefini" if np.isnan(p) else "infini" if np.isinf(p) else "fini"
        return ExtremeVariant(group=group, label=label, period=Period(start=ys[0], end=ys[-1]), n=len(ys),
                              alpha=est(ff.alpha), xi=float(ff.xi),
                              probability_ratio=float(p) if status == "fini" else None,
                              probability_ratio_status=status, ok=bool(ok))

    variants.append(variant("Covariable HadCRUT5", values, GH, rec))
    hom_only, _ = main.series(extend=False)
    variants.append(variant(f"Années homogénéisées seules ({min(hom_only)}-{max(hom_only)})", hom_only, G, rec))
    variants.append(variant(f"Sans l'année {EVENT_YEAR}", {y: v for y, v in values.items() if y != EVENT_YEAR}, G, rec))
    tx3v, _ = main.series(index="tx3x")
    variants.append(variant("Indice TX3x (moyenne de TX sur 3 jours)", tx3v, G, tx3v.get(EVENT_YEAR)))

    # X6 — cohérence régionale (intervalles bootstrap de α)
    a_lo, a_hi = gev.interval(col(0))
    station_rows = []
    for st in others:
        vals, _ = st.series()
        ys, xs, gs = arrays(vals, G)
        ff = gev.fit(xs, gs)
        bs, _ = gev.bootstrap(xs, gs, n_boot, SEED, lambda q: q.alpha)
        lo, hi = gev.interval(bs)
        ok = ff.alpha > 0 and lo <= a_hi and a_lo <= hi
        station_rows.append((st, ff, lo, hi, ok))
        variants.append(ExtremeVariant(group="station", label=st.name, period=Period(start=ys[0], end=ys[-1]),
                                       n=len(ys), alpha=Estimate(value=ff.alpha, ci_low=lo, ci_high=hi),
                                       xi=float(ff.xi), probability_ratio=None,
                                       probability_ratio_status="sans_objet", ok=bool(ok)))

    gaps = [y for y in range(START, years[-1] + 1) if y not in values]
    return {
        "fit": f, "lrt": lrt, "ks": ks, "central": central, "boot": boot, "failed": failed, "events": events,
        "curve": curve, "series": series, "variants": variants, "years": years, "raw_years": raw_years,
        "gaps": gaps, "ext_diff": main.ext_diff(), "g_now": g_now, "g_past": g_past, "g_pre": g_pre,
        "alpha_ci": (a_lo, a_hi), "sigma_ci": gev.interval(col(1)), "xi_ci": gev.interval(col(2)),
        "station_rows": station_rows,
    }


def _r(a) -> list[float]:
    return [round(float(v), 4) + 0.0 for v in a]


def _f(x: float, nd: int, sign: bool = False) -> str:
    from etl.demonstration import _f as fmt
    return fmt(x, nd, sign)


def _rp(u: Unbounded, nd: int = 0) -> str:
    def one(v):
        if v is None:
            return "infinie"
        return f"{_f(v, nd)} ans" if v < 10_000 else "plus de 10 000 ans"
    return one(u.value)


def _ratio(u: Unbounded) -> str:
    if u.value is None:
        return "infini"
    return _f(u.value, 0 if u.value >= 10 else 1)


def _variant_ratio(v: ExtremeVariant) -> str:
    if v.probability_ratio_status == "fini":
        return _f(v.probability_ratio, 0 if v.probability_ratio >= 10 else 1)
    return {"infini": "infini", "indefini": "indéfini (0/0)", "sans_objet": "—"}[v.probability_ratio_status]


def build(main: StationMaxima, others: list[StationMaxima], gis: dict[int, float], had: dict[int, float],
          ctx_version: str, extracted_at, n_boot: int = N_BOOT) -> Extremes:
    r = analyse(main, others, gis, had, n_boot)
    f = r["fit"]
    a_lo, a_hi = r["alpha_ci"]
    ev_rec, ev_20 = r["events"]
    criteria = [
        Criterion(id="X1", label="Données", satisfied=not r["gaps"] and r["ext_diff"] <= MAX_EXT_DIFF,
                  detail=f"{main.name} {r['years'][0]}-{r['years'][-1]}, {len(r['years'])} années, "
                         f"{'aucune manquante' if not r['gaps'] else 'manquantes : ' + ', '.join(map(str, r['gaps']))} ; "
                         f"années brutes {', '.join(map(str, r['raw_years'])) or 'aucune'} ; écart maximal |corrigé − brut| "
                         f"après la rupture de {main.last_break_regime} : {_f(r['ext_diff'], 2)} °C (seuil {_f(MAX_EXT_DIFF, 1)})"),
        Criterion(id="X2", label="Ajustement", satisfied=XI_RANGE[0] <= f.xi <= XI_RANGE[1] and r["ks"] >= KS_MIN,
                  detail=f"ξ = {_f(f.xi, 2)} (bornes {_f(XI_RANGE[0], 1)} et {_f(XI_RANGE[1], 1, True)}) ; "
                         f"Kolmogorov-Smirnov p = {_f(r['ks'], 2)} (seuil {_f(KS_MIN, 2)}) ; "
                         f"{r['failed']} tirage(s) bootstrap sans convergence sur {n_boot}"),
        Criterion(id="X3", label="Détection", satisfied=f.alpha > 0 and r["lrt"] < ALPHA_LEVEL and a_lo > 0,
                  detail=f"α = {_f(f.alpha, 2)} [{_f(a_lo, 2)} ; {_f(a_hi, 2)}] °C par °C ; rapport de vraisemblance "
                         f"p {'< 0,001' if r['lrt'] < 0.001 else '= ' + _f(r['lrt'], 3)}"),
        Criterion(id="X4", label="Plausibilité", satisfied=a_lo <= REFERENCE[2] and REFERENCE[1] <= a_hi,
                  detail=f"intervalle de α [{_f(a_lo, 2)} ; {_f(a_hi, 2)}] contre la référence "
                         f"[{_f(REFERENCE[1], 1)} ; {_f(REFERENCE[2], 1)}]"),
        Criterion(id="X5", label="Robustesse", satisfied=all(v.ok for v in r["variants"] if v.group == "robustesse"),
                  detail=" ; ".join(f"{v.label} : α = {_f(v.alpha.value, 2)}, rapport de probabilité du record "
                                    f"{_variant_ratio(v)} {'✓' if v.ok else '✗'}"
                                    for v in r["variants"] if v.group == "robustesse")),
        Criterion(id="X6", label="Cohérence régionale", satisfied=all(v.ok for v in r["variants"] if v.group == "station"),
                  detail=" ; ".join(f"{v.label} {v.period.start}-{v.period.end} : α = {_f(v.alpha.value, 2)} "
                                    f"[{_f(v.alpha.ci_low, 2)} ; {_f(v.alpha.ci_high, 2)}] {'✓' if v.ok else '✗'}"
                                    for v in r["variants"] if v.group == "station")),
    ]
    ok = {c.id: c.satisfied for c in criteria}
    if all(ok[f"X{i}"] for i in range(1, 7)):
        confidence, reason = "elevee", ("Critères X1 à X6 conformes (règle D-AO). L'analyse relie les maxima au "
                                        "réchauffement mondial ; elle n'en attribue pas la cause.")
    elif ok["X3"]:
        failed = ", ".join(f"{c.id} ({c.label.lower()})" for c in criteria if not c.satisfied)
        confidence, reason = "moyenne", (f"Hausse détectée (X3), mais critère non conforme, d'où la confiance "
                                         f"« moyenne » (règle D-AO) : {failed}. Détail : docs/validation-p10.md.")
    else:
        confidence, reason = "non_etabli", "La hausse des maxima avec le réchauffement mondial n'est pas détectée (X3)."

    g_txt = _f(r["g_now"] - r["g_past"], 2)
    pr_rec = ev_rec.probability_ratio
    if ev_rec.return_period_past.value is None:
        past_txt = (f"Dans le climat de {PAST_YEAR}, il dépassait la borne supérieure de la loi ajustée : il y était "
                    "pratiquement impossible")
        if pr_rec.ci_low is not None:
            past_txt += (f" (période de retour d'au moins {_f(ev_rec.return_period_past.ci_low, 0)} ans et "
                         f"probabilité multipliée par au moins {_f(pr_rec.ci_low, 0)}, bornes basses des intervalles)")
        past_txt += "."
    else:
        past_txt = (f"Dans le climat de {PAST_YEAR}, sa période de retour était de {_rp(ev_rec.return_period_past)} : "
                    f"il est devenu {_ratio(pr_rec)} fois plus probable.")
    finding = (
        f"À {main.name}, sur {r['years'][0]}-{r['years'][-1]}, la journée la plus chaude de l'année gagne "
        f"{_f(f.alpha, 1)} °C [{_f(a_lo, 1)} ; {_f(a_hi, 1)}] par degré de réchauffement mondial. Le monde s'étant "
        f"réchauffé de {g_txt} °C entre {PAST_YEAR} et {EVENT_YEAR} (moyennes sur 4 ans, GISTEMP), une chaleur qui "
        f"revenait tous les {N_PAST} ans en {PAST_YEAR} ({_f(ev_20.value.value, 1)} °C) revient aujourd'hui en moyenne "
        f"tous les {_rp(ev_20.return_period_today, 1)}, et une chaleur de rareté donnée est "
        f"{_f(ev_rec.intensity_change.value, 1)} °C [{_f(ev_rec.intensity_change.ci_low, 1)} ; "
        f"{_f(ev_rec.intensity_change.ci_high, 1)}] plus forte. Le record du {_date(ev_rec.date)} "
        f"({_f(ev_rec.value.value, 1)} °C) a une période de retour d'environ {_rp(ev_rec.return_period_today)} "
        f"[{_rp(Unbounded(value=ev_rec.return_period_today.ci_low, ci_low=None, ci_high=None))} ; "
        f"{_rp(Unbounded(value=ev_rec.return_period_today.ci_high, ci_low=None, ci_high=None))}] dans le climat "
        f"d'aujourd'hui. " + past_txt
    )

    return Extremes(
        question=(f"Une forte chaleur qui revenait tous les {N_PAST} ans dans le climat de {PAST_YEAR} à Bordeaux "
                  "revient-elle plus souvent aujourd'hui, et de combien les maxima ont-ils augmenté par degré de "
                  "réchauffement mondial ?"),
        model="TXx(a) ~ GEV(μ₀ + α·G(a), σ, ξ), G = température mondiale lissée sur 4 ans",
        finding=finding, confidence=confidence, confidence_reason=reason,
        method_note=(
            "Maximum annuel de la température maximale quotidienne (TXx) à Bordeaux-Mérignac : années homogénéisées "
            "(correction mensuelle B de la phase P2a) prolongées par les années brutes postérieures, autorisées parce "
            "que corrigé et brut coïncident depuis la dernière rupture. Loi généralisée des valeurs extrêmes dont la "
            "position suit la température mondiale GISTEMP v4 lissée sur 4 ans (années a − 3 à a), échelle et forme "
            "constantes, ajustée par maximum de vraisemblance (protocole du World Weather Attribution, Philip et al., "
            f"2020). Intervalles à 95 % par rééchantillonnage des années ({n_boot} tirages). Climats comparés : "
            f"{EVENT_YEAR} contre {PAST_YEAR}, et pour information contre la moyenne {PRE[0]}-{PRE[1]}. Une "
            "période de retour « infinie » signifie que la valeur dépasse la borne supérieure de la loi ajustée pour "
            "ce climat (forme ξ négative)."),
        limitations=[
            "La covariable représente tout ce qui suit le réchauffement mondial (gaz à effet de serre, aérosols, "
            "changements de circulation) : l'analyse relie les maxima au réchauffement mondial, elle n'attribue pas "
            "leur cause à l'homme, ce qui demanderait des modèles de climat.",
            "Une seule station principale ; quatre autres postes de Gironde servent de contrôle, mais partagent le "
            "même climat régional et ne sont pas indépendants.",
            f"Le record de {EVENT_YEAR} a été choisi après coup et figure dans l'ajustement : la variante sans "
            f"{EVENT_YEAR} mesure ce biais de sélection.",
            "Les longues périodes de retour extrapolent la loi au-delà des 73 années observées ; la borne supérieure "
            "de la loi (ξ < 0) est mal connue, d'où des intervalles très larges, parfois infinis.",
            "La correction B décale chaque mois sans corriger la forme de la distribution quotidienne ; Mérignac est "
            "un aéroport en lisière d'agglomération, un effet urbain lent n'est pas exclu.",
            "Le rééchantillonnage suppose les années indépendantes.",
        ],
        inputs=[
            InputSource(name="Météo-France — données climatologiques de base quotidiennes, TX", license="Licence Ouverte 2.0 (Etalab)",
                        url="https://www.data.gouv.fr/datasets/6569b51ae64326786e4e8e1a",
                        note="homogénéisation mensuelle par les séries LSH (correction B, phase P2a)"),
            InputSource(name="GISTEMP v4 — température mondiale annuelle, telle que publiée sur le site",
                        url=f"https://projet-evolution-climat.vercel.app/monde/{GISTEMP}", license="voir la page de l'indicateur"),
            InputSource(name="HadCRUT5 — contrôle de la covariable (X5)",
                        url=f"https://projet-evolution-climat.vercel.app/monde/{HADCRUT}", license="voir la page de l'indicateur"),
        ],
        station=main.name, index_label="TXx, maximum annuel de la température maximale quotidienne",
        period=Period(start=r["years"][0], end=r["years"][-1]), n=len(r["years"]),
        covariate="GISTEMP v4, moyenne glissante sur 4 ans", today_year=EVENT_YEAR, past_year=PAST_YEAR,
        g_today=r["g_now"], g_past=r["g_past"], g_preindustrial=r["g_pre"], mu0=f.mu0,
        alpha=Estimate(value=f.alpha, ci_low=a_lo, ci_high=a_hi),
        sigma=Estimate(value=f.sigma, ci_low=r["sigma_ci"][0], ci_high=r["sigma_ci"][1]),
        xi=Estimate(value=f.xi, ci_low=r["xi_ci"][0], ci_high=r["xi_ci"][1]),
        lrt_p=r["lrt"], ks_p=r["ks"], n_boot=n_boot, n_failed=r["failed"],
        reference=Estimate(value=REFERENCE[0], ci_low=REFERENCE[1], ci_high=REFERENCE[2]), reference_source=REFERENCE_SOURCE,
        events=r["events"], curve=r["curve"], series=r["series"], variants=r["variants"], criteria=criteria,
        script="etl/demo_extremes.py", etl_version=ctx_version, extracted_at=extracted_at,
    )


MONTHS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
          "novembre", "décembre")


def _date(iso: str | None) -> str:
    if not iso:
        return ""
    y, m, d = (int(v) for v in iso.split("-"))
    return f"{d}{'er' if d == 1 else ''} {MONTHS[m - 1]} {y}"
