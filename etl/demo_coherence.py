"""P10.4 — cohérence physique : des grandeurs mesurées indépendamment évoluent-elles comme la physique l'impose ?

Cadrage, critères C1-C7 et décisions D-AS, D-AT et D-AU validés par Grég le 20/11/2026, avant tout calcul
(docs/phases.md, section P10.4). Quatre contrôles, chacun confrontant deux jeux de mesures de natures différentes :

- V, vapeur d'eau et température (Clausius-Clapeyron) : ln W = c + β·T + u, u AR(1) (Prais-Winsten), W vapeur d'eau
  intégrée RSS (océans, 60° S-60° N, masque constant), T température de surface de la mer HadSST4 publiée ;
  β (% par °C) contre [6 ; 8] (C2).
- S, troposphère contre stratosphère : tendances de Sen 1979-2025 de la basse troposphère (TLT, publiées) et de la
  basse stratosphère (TLS), RSS et UAH (C3).
- N, bilan du niveau marin 2005-2024, par tendances (D-AU) : tendance(niveau observé + 0,3 mm/an d'ajustement
  isostatique) − tendance(dilatation 0-2000 m) − tendance(masse de l'océan GRACE) ; |résidu| ≤ 0,5 mm/an (C4).
- E, déséquilibre énergétique contre chaleur stockée par l'océan : tendances (Prais-Winsten) du déséquilibre CERES et
  du flux de chaleur dans l'océan 0-2000 m (différence centrée du contenu thermique annuel, rapportée à la surface de
  la Terre) ; positives, intervalles qui se recoupent (C5). Les niveaux moyens ne sont pas indépendants (CERES est
  calé sur Argo) : leur rapport n'est qu'une information.

Aucun contrôle n'attribue une cause. Les choix (périodes, seuils, masque, estimateurs) sont ceux du cadrage.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import stats

from etl.schema import (Coherence, CoherenceChart, CoherenceCheck, CoherenceLine, CoherenceValue, Criterion, Estimate,
                        InputSource, Period)
from etl.sources import globaux as G
from etl.sources import grace as GR
from etl.sources import rss_vapor as RV
from etl.stats import regression as R
from etl.stats.trend import annual_trend

SCRIPT = "etl/demo_coherence.py"
CI_LEVEL = 0.95
SITE = "https://projet-evolution-climat.vercel.app/monde/{}"

# ---------------------------------------------------------------- choix fixés par le cadrage (20/11/2026)
V_SPAN = (1988, 2025)
CC_RANGE = (6.0, 8.0)                 # R-B1, % par °C (C2)
MASK_MIN = 0.5                        # C1 : part de la bande 60° S-60° N couverte par le masque constant
S_SPAN = (1979, 2025)
S_SUB = ((1979, 1997), (1998, 2025))  # information
N_SPAN = (2005, 2024)
GIA = 0.3                             # mm/an ajoutés à l'altimétrie NOAA STAR (non corrigée)
RESID_MAX = 0.5                       # C4, mm/an
MASS_MIN = 0.8                        # D-AU : part minimale des mois GRACE présents
E_SPAN = (2006, 2024)                 # années du flux océanique (différence centrée de 2005-2025)
EARTH_AREA = 4 * math.pi * 6.371e6 ** 2   # m²
YEAR_S = 365.25 * 86400
TLT = {"rss": "tlt-rss-monde", "uah": "tlt-uah-monde"}
TLS = {"rss": "tls-rss", "uah": "tls-uah"}
NAMES = {"rss": "RSS 4.0", "uah": "UAH 6.1"}
SST, SST_ALT = "sst-hadsst-monde", "sst-noaa-monde"
GMSL, OHC, EEI = "niveau-mer-monde", "ohc-2000-monde", "desequilibre-energetique-monde"

REFERENCES = {
    "V": ("R-B1 : la capacité de l'air à contenir de la vapeur d'eau croît d'environ 7 % par °C (Clausius-Clapeyron) ; "
          "la vapeur d'eau intégrée observée suit ce taux (GIEC AR6 GT1, ch. 2) ; fourchette retenue 6 à 8 % par °C."),
    "S": ("R-B2 : basse stratosphère refroidie depuis le milieu du XXe siècle, « pratiquement certain », stable depuis "
          "le milieu des années 1990 ; troposphère réchauffée (GIEC AR6 GT1, ch. 2)."),
    "N": ("R-B3 : niveau marin 1993-2018 3,1 ± 0,3 mm/an, budget fermé à 0,3 mm/an près (1 σ) ; dilatation 42 %, "
          "glaciers 21 %, Groenland 15 %, Antarctique 8 % (WCRP Global Sea Level Budget Group, ESSD 10, 1551, 2018)."),
    "E": ("R-B4 : hausse du déséquilibre de 0,50 ± 0,47 W/m² par décennie sur 2005-2019, indiscernable entre satellites "
          "et mesures in situ (Loeb et al., 2021, GRL 48) ; environ 91 % de l'excédent réchauffe l'océan (GIEC AR6)."),
}


def _f(x: float, nd: int, sign: bool = False) -> str:
    from etl.demonstration import _f as fmt
    return fmt(x, nd, sign)


def _ci(lo: float, hi: float, nd: int, sign: bool = False) -> str:
    return f"[{_f(lo, nd, sign)} ; {_f(hi, nd, sign)}]"


def published(out_dir: Path, iid: str) -> dict[int, float]:
    d = json.loads((out_dir / "monde" / f"{iid}.json").read_text(encoding="utf-8"))
    return {int(t[:4]): v for t, v in zip(d["series"]["time"], d["series"]["value"]) if v is not None}


def span(a: tuple[int, int]) -> list[int]:
    return list(range(a[0], a[1] + 1))


def missing(series: dict, years: list[int]) -> list[int]:
    return [y for y in years if y not in series]


def overlap(a: tuple[float, float], b: tuple[float, float]) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]


def est(v: float, lo: float | None = None, hi: float | None = None, nd: int = 4) -> Estimate:
    r = lambda x: None if x is None else round(float(x), nd) + 0.0  # noqa: E731
    return Estimate(value=r(v), ci_low=r(lo), ci_high=r(hi))


def value(label: str, unit: str, p: tuple[int, int], e: Estimate) -> CoherenceValue:
    return CoherenceValue(label=label, unit=unit, period=Period(start=p[0], end=p[1]), estimate=e)


# ---------------------------------------------------------------- V : vapeur d'eau


def annual_tpw(monthly: dict[str, float]) -> dict[int, float]:
    per: dict[int, list[float]] = {}
    for m, v in monthly.items():
        per.setdefault(int(m[:4]), []).append(v)
    return {y: sum(v) / 12 for y, v in per.items() if len(v) == 12}


@dataclass(frozen=True)
class CCFit:
    beta: float           # % par °C
    lo: float
    hi: float
    rho: float
    r2: float
    years: list[int]
    fitted: list[float]   # W reconstruit (kg/m²)

    @property
    def ok(self) -> bool:
        return self.lo > 0 and overlap((self.lo, self.hi), CC_RANGE)


def fit_cc(tpw: dict[int, float], sst: dict[int, float], years: list[int]) -> CCFit:
    y = np.log([tpw[a] for a in years])
    x = np.array([sst[a] for a in years])
    f = R.prais_winsten(y, x, ["T"])
    lo, hi = f.ci(1 - CI_LEVEL)
    return CCFit(float(f.coef[1]) * 100, float(lo[1]) * 100, float(hi[1]) * 100, f.rho, f.r2, years,
                 [float(v) for v in np.exp(f.fitted)])


def fit_cc_ols(tpw: dict[int, float], sst: dict[int, float], years: list[int]) -> tuple[float, float, float]:
    """Information seulement, si Prais-Winsten ne converge pas : moindres carrés, erreurs de Newey-West (% par °C)."""
    f = R.ols_newey_west(np.log([tpw[a] for a in years]), np.array([sst[a] for a in years]), ["T"])
    lo, hi = f.ci(1 - CI_LEVEL)
    return float(f.coef[1]) * 100, float(lo[1]) * 100, float(hi[1]) * 100


# ---------------------------------------------------------------- N : bilan du niveau marin


@dataclass(frozen=True)
class Slope:
    value: float          # mm/an
    se: float             # erreur type (Newey-West), information
    n: int


def ols_slope(t: list[float], v: list[float]) -> Slope:
    f = R.ols_newey_west(np.array(v, float), np.array(t, float), ["t"])
    return Slope(float(f.coef[1]), float(f.se[1]), len(t))


def sen_slope(t: list[float], v: list[float]) -> float:
    return float(stats.theilslopes(v, t)[0])


def mass_months(rows: list[dict], p: tuple[int, int]) -> list[tuple[float, float]]:
    """Mesures GRACE désaisonnalisées de la période (temps décimal, mm), telles que publiées par JPL."""
    return [(r["time"], r["deseasoned_mm"]) for r in rows if p[0] <= r["time"] < p[1] + 1]


def month_count(mass: list[tuple[float, float]]) -> int:
    """Nombre de mois civils distincts couverts (une solution JPL est datée au milieu de sa fenêtre)."""
    return len({(int(t), min(11, int((t - int(t)) * 12))) for t, _ in mass})


@dataclass(frozen=True)
class Budget:
    obs: Slope
    thermo: Slope
    mass: Slope
    resid: float
    resid_lo: float
    resid_hi: float
    sen_obs: float
    sen_thermo: float
    sen_mass: float
    sen_resid: float
    mass_count: int

    @property
    def ok(self) -> bool:
        return abs(self.resid) <= RESID_MAX

    @property
    def sen_ok(self) -> bool:
        return abs(self.sen_resid) <= RESID_MAX


def budget(gmsl: dict[int, float], thermo: dict[int, float], mass: list[tuple[float, float]]) -> Budget:
    ys = span(N_SPAN)
    o = ols_slope(ys, [gmsl[y] for y in ys])
    th = ols_slope(ys, [thermo[y] for y in ys])
    mt, mv = [t for t, _ in mass], [v for _, v in mass]
    ma = ols_slope(mt, mv)
    resid = o.value + GIA - th.value - ma.value
    half = stats.norm.ppf(0.5 + CI_LEVEL / 2) * math.sqrt(o.se ** 2 + th.se ** 2 + ma.se ** 2)
    so, st, sm = sen_slope(ys, [gmsl[y] for y in ys]), sen_slope(ys, [thermo[y] for y in ys]), sen_slope(mt, mv)
    return Budget(o, th, ma, resid, resid - half, resid + half, so, st, sm, so + GIA - st - sm, len(mass))


# ---------------------------------------------------------------- E : énergie


def ocean_flux(ohc: dict[int, float], years: list[int]) -> dict[int, float]:
    """Flux de chaleur dans l'océan 0-2000 m (W/m² de surface terrestre) : (H(a+1) − H(a−1)) / 2 ans, H en 10²² J."""
    return {y: (ohc[y + 1] - ohc[y - 1]) * 1e22 / (2 * YEAR_S * EARTH_AREA) for y in years}


def smooth3(s: dict[int, float]) -> dict[int, float]:
    return {y: (s[y - 1] + s[y] + s[y + 1]) / 3 for y in s if y - 1 in s and y + 1 in s}


@dataclass(frozen=True)
class DTrend:
    value: float          # par décennie
    lo: float
    hi: float
    rho: float


def pw_trend(s: dict[int, float], years: list[int]) -> DTrend:
    f = R.prais_winsten(np.array([s[y] for y in years]), np.array(years, float), ["t"])
    lo, hi = f.ci(1 - CI_LEVEL)
    return DTrend(float(f.coef[1]) * 10, float(lo[1]) * 10, float(hi[1]) * 10, f.rho)


def energy_ok(a: DTrend, b: DTrend) -> bool:
    return a.value > 0 and b.value > 0 and overlap((a.lo, a.hi), (b.lo, b.hi))


# ---------------------------------------------------------------- assemblage


def _count(n: int) -> str:
    return ("aucun", "un", "deux", "trois", "quatre")[n]


def build(*, tpw_monthly: dict[str, float], tpw_meta: dict, sst: dict[int, float], sst_alt: dict[int, float],
          tlt: dict[str, dict[int, float]], tls: dict[str, dict[int, float]], gmsl: dict[int, float],
          thermo: dict[int, float], grace_rows: list[dict], ohc: dict[int, float], eei: dict[int, float],
          ctx_version: str, extracted_at, grace_meta: dict | None = None) -> Coherence:
    crit: list[Criterion] = []

    # ---------- C1 : données
    vy = span(V_SPAN)
    tpw = annual_tpw(tpw_monthly)
    frac = float(tpw_meta["mask_area_fraction"])
    v_miss = sorted(set(missing(tpw, vy)) | set(missing(sst, vy)) | set(missing(sst_alt, vy)))
    sy = span(S_SPAN)
    s_miss = {f"{k} {NAMES[n]}": missing(d[n], sy) for k, d in (("TLT", tlt), ("TLS", tls)) for n in NAMES}
    s_miss = {k: v for k, v in s_miss.items() if v}
    ny = span(N_SPAN)
    n_miss = sorted(set(missing(gmsl, ny)) | set(missing(thermo, ny)))
    mass = mass_months(grace_rows, N_SPAN)
    n_cov = month_count(mass)
    n_months = 12 * len(ny)
    ey = span(E_SPAN)
    e_miss = sorted(set(missing(eei, ey)) | set(missing(ohc, span((E_SPAN[0] - 1, E_SPAN[1] + 1)))))
    c1 = (not v_miss and frac >= MASK_MIN and not s_miss and not n_miss and n_cov >= MASS_MIN * n_months
          and not e_miss)
    crit.append(Criterion(id="C1", label="Données", satisfied=c1, detail=(
        f"V : {V_SPAN[0]}-{V_SPAN[1]}, {'aucune année manquante' if not v_miss else 'manquantes : ' + ', '.join(map(str, v_miss))}, "
        f"masque constant couvrant {_f(frac * 100, 1)} % de la bande 60° S-60° N (seuil {_f(MASK_MIN * 100, 0)} %) ; "
        f"S : {S_SPAN[0]}-{S_SPAN[1]}, {'séries complètes' if not s_miss else '; '.join(f'{k} manque {v}' for k, v in s_miss.items())} ; "
        f"N : altimétrie et dilatation {N_SPAN[0]}-{N_SPAN[1]} {'complètes' if not n_miss else 'manquantes : ' + ', '.join(map(str, n_miss))}, "
        f"masse GRACE {n_cov} mois sur {n_months} ({_f(n_cov / n_months * 100, 0)} %, seuil {_f(MASS_MIN * 100, 0)} %, D-AU) ; "
        f"E : déséquilibre {E_SPAN[0]}-{E_SPAN[1]} et contenu thermique {E_SPAN[0] - 1}-{E_SPAN[1] + 1} "
        f"{'complets' if not e_miss else 'manquants : ' + ', '.join(map(str, e_miss))}")))

    # ---------- V
    cc = fit_cc(tpw, sst, vy)
    try:
        cc_alt, alt_err = fit_cc(tpw, sst_alt, vy), ""
    except ValueError as exc:          # estimateur AR(1) qui ne converge pas : la variante échoue, sans arrêter l'ETL
        cc_alt, alt_err = None, str(exc)
    alt_ok = cc_alt is not None and cc_alt.ok
    if cc_alt is not None:
        alt_txt = f"β = {_f(cc_alt.beta, 1)} % par °C {_ci(cc_alt.lo, cc_alt.hi, 1)}"
        alt_val = value("β avec la température de mer NOAA (C6)", "% par °C", V_SPAN, est(cc_alt.beta, cc_alt.lo, cc_alt.hi))
    else:
        ob, olo, ohi = fit_cc_ols(tpw, sst_alt, vy)
        alt_txt = (f"{alt_err} ; pour information, moindres carrés et erreurs de Newey-West : β = {_f(ob, 1)} % par °C "
                   f"{_ci(olo, ohi, 1)}")
        alt_val = value("β avec la température de mer NOAA, moindres carrés (C6 : Prais-Winsten ne converge pas)",
                        "% par °C", V_SPAN, est(ob, olo, ohi))
    crit.append(Criterion(id="C2", label="Vapeur d'eau", satisfied=cc.ok, detail=(
        f"β = {_f(cc.beta, 1)} % par °C {_ci(cc.lo, cc.hi, 1)} ({V_SPAN[0]}-{V_SPAN[1]}, HadSST4, Prais-Winsten, "
        f"ρ = {_f(cc.rho, 2)}) ; attendu : intervalle recoupant [{_f(CC_RANGE[0], 0)} ; {_f(CC_RANGE[1], 0)}], borne basse > 0")))
    mean_t = sum(sst[y] for y in vy) / len(vy)
    mean_w = sum(tpw[y] for y in vy) / len(vy)
    v_chart = CoherenceChart(
        title=f"Vapeur d'eau observée et taux de Clausius-Clapeyron ({V_SPAN[0]}-{V_SPAN[1]})", unit="%", years=vy,
        lines=[CoherenceLine(name="Vapeur d'eau RSS (écart à la moyenne)",
                             values=[round((tpw[y] / mean_w - 1) * 100, 3) for y in vy]),
               CoherenceLine(name="7 % par °C de la température de mer HadSST4",
                             values=[round(7 * (sst[y] - mean_t), 3) for y in vy])],
        note=(f"Écarts à la moyenne {V_SPAN[0]}-{V_SPAN[1]} : vapeur d'eau en %, température de mer convertie au taux "
              "théorique de 7 % par °C. Si la physique est respectée, les deux courbes se superposent, y compris "
              "pendant les épisodes El Niño (1998, 2016, 2024)."))
    v_check = CoherenceCheck(
        id="vapeur", letter="V", title="Vapeur d'eau et température (Clausius-Clapeyron)",
        question="L'atmosphère au-dessus des océans contient-elle environ 7 % de vapeur d'eau en plus par degré ?",
        criterion="C2", satisfied=cc.ok,
        result=(f"La vapeur d'eau au-dessus des océans augmente de {_f(cc.beta, 1)} % par °C de température de mer "
                f"(intervalle à 95 % : {_f(cc.lo, 1)} à {_f(cc.hi, 1)}), "
                + ("compatible avec le taux de Clausius-Clapeyron." if cc.ok else "hors du taux de Clausius-Clapeyron.")),
        reference=REFERENCES["V"],
        values=[value("β, vapeur d'eau par °C (HadSST4)", "% par °C", V_SPAN, est(cc.beta, cc.lo, cc.hi))],
        information=[alt_val,
                     value("Part de la variance expliquée", "%", V_SPAN, est(cc.r2 * 100))],
        charts=[v_chart],
        limitation=("Océans sans glace seulement (pas de mesure micro-onde sur les continents) ; la température est la "
                    "moyenne mondiale de la mer, la vapeur celle de 60° S-60° N."))

    # ---------- S
    tr = {(k, n): annual_trend(sy, [d[n][y] for y in sy], f"{k} {NAMES[n]}") for k, d in (("TLT", tlt), ("TLS", tls))
          for n in NAMES}
    s_ok = all(tr[("TLT", n)].slope_ci_low > 0 and tr[("TLS", n)].slope_ci_high < 0 for n in NAMES)
    crit.append(Criterion(id="C3", label="Stratosphère", satisfied=s_ok, detail=" ; ".join(
        f"{NAMES[n]} : TLT {_f(tr[('TLT', n)].slope_per_decade, 3, True)} °C/déc. "
        f"{_ci(tr[('TLT', n)].slope_ci_low, tr[('TLT', n)].slope_ci_high, 3, True)}, "
        f"TLS {_f(tr[('TLS', n)].slope_per_decade, 3, True)} °C/déc. "
        f"{_ci(tr[('TLS', n)].slope_ci_low, tr[('TLS', n)].slope_ci_high, 3, True)}" for n in NAMES)
        + f" (Sen, {S_SPAN[0]}-{S_SPAN[1]}) ; attendu : TLT borne basse > 0 et TLS borne haute < 0"))
    sub = {(n, p): annual_trend(span(p), [tls[n][y] for y in span(p)], f"TLS {NAMES[n]} {p[0]}-{p[1]}")
           for n in NAMES for p in S_SUB}
    s_check = CoherenceCheck(
        id="stratosphere", letter="S", title="Troposphère contre stratosphère",
        question="La basse troposphère se réchauffe-t-elle pendant que la basse stratosphère se refroidit ?",
        criterion="C3", satisfied=s_ok,
        result=(f"Sur {S_SPAN[0]}-{S_SPAN[1]}, la basse troposphère {'se réchauffe' if s_ok else 'évolue'} "
                f"({_f(tr[('TLT', 'rss')].slope_per_decade, 2, True)} °C par décennie selon RSS, "
                f"{_f(tr[('TLT', 'uah')].slope_per_decade, 2, True)} selon UAH) et la basse stratosphère "
                f"{'se refroidit' if s_ok else 'évolue'} ({_f(tr[('TLS', 'rss')].slope_per_decade, 2, True)} et "
                f"{_f(tr[('TLS', 'uah')].slope_per_decade, 2, True)})"
                + (", comme prévu." if s_ok else " : les signes attendus ne sont pas nets pour les deux jeux.")),
        reference=REFERENCES["S"],
        values=[value(f"{k} {NAMES[n]}", "°C par décennie", S_SPAN,
                      est(tr[(k, n)].slope_per_decade, tr[(k, n)].slope_ci_low, tr[(k, n)].slope_ci_high))
                for n in NAMES for k in ("TLT", "TLS")],
        information=[value(f"TLS {NAMES[n]}, {p[0]}-{p[1]}", "°C par décennie", p,
                           est(sub[(n, p)].slope_per_decade, sub[(n, p)].slope_ci_low, sub[(n, p)].slope_ci_high))
                     for n in NAMES for p in S_SUB],
        charts=[CoherenceChart(
            title=f"Basse troposphère et basse stratosphère ({S_SPAN[0]}-{S_SPAN[1]})", unit="°C", years=sy,
            lines=[CoherenceLine(name=f"{k} {NAMES[n]}", values=[round(d[n][y], 3) for y in sy])
                   for k, d in (("TLT", tlt), ("TLS", tls)) for n in NAMES],
            note=("Anomalies annuelles publiées par chaque producteur (périodes de référence propres). Les pics de la "
                  "stratosphère en 1982-1983 et 1991-1992 sont les éruptions d'El Chichón et du Pinatubo, dont les "
                  "aérosols absorbent le rayonnement."))],
        limitation=("Un signe attendu d'avance : ce contrôle vérifie surtout les données. Le refroidissement de la "
                    "stratosphère vient pour beaucoup de la perte d'ozone, et en partie du CO₂ ; il ne les sépare pas."))

    # ---------- N
    b = budget(gmsl, thermo, mass)
    tot = b.obs.value + GIA
    crit.append(Criterion(id="C4", label="Niveau marin", satisfied=b.ok, detail=(
        f"{N_SPAN[0]}-{N_SPAN[1]}, moindres carrés : observé {_f(b.obs.value, 2)} + {_f(GIA, 1)} = {_f(tot, 2)} mm/an ; "
        f"dilatation 0-2000 m {_f(b.thermo.value, 2)} ; masse {_f(b.mass.value, 2)} ; résidu {_f(b.resid, 2, True)} mm/an "
        f"(information : {_ci(b.resid_lo, b.resid_hi, 2, True)}) ; attendu |résidu| ≤ {_f(RESID_MAX, 1)}")))
    mass_annual: dict[int, float] = {}
    per: dict[int, list[float]] = {}
    for t, v in mass:
        per.setdefault(int(t), []).append(v)
    mass_annual = {y: sum(v) / len(v) for y, v in per.items() if len(v) >= 6}

    def centred(s: dict[int, float]) -> dict[int, float]:
        m = sum(s.values()) / len(s)
        return {y: v - m for y, v in s.items()}

    obs_c = centred({y: gmsl[y] + GIA * (y - N_SPAN[0]) for y in ny})
    th_c = centred({y: thermo[y] for y in ny})
    ma_c = centred(mass_annual)
    n_check = CoherenceCheck(
        id="niveau-marin", letter="N", title="Bilan du niveau marin",
        question="La hausse mesurée par satellite est-elle la somme de la dilatation de l'eau et de l'eau ajoutée ?",
        criterion="C4", satisfied=b.ok,
        result=(f"Sur {N_SPAN[0]}-{N_SPAN[1]}, la mer monte de {_f(tot, 1)} mm par an (altimétrie corrigée de "
                f"l'ajustement isostatique) ; la dilatation de l'eau (0-2000 m) en explique {_f(b.thermo.value, 1)} et "
                f"l'eau ajoutée à l'océan, pesée par GRACE, {_f(b.mass.value, 1)}. Il reste {_f(b.resid, 2, True)} mm par "
                "an non expliqués, " + ("dans la tolérance de ± 0,5 mm par an." if b.ok else "hors de la tolérance de ± 0,5 mm par an.")),
        reference=REFERENCES["N"],
        values=[value("Résidu observé − (dilatation + masse)", "mm/an", N_SPAN, est(b.resid, b.resid_lo, b.resid_hi))],
        information=[value("Niveau observé + 0,3 (ajustement isostatique)", "mm/an", N_SPAN, est(tot)),
                     value("Dilatation thermique 0-2000 m (NCEI)", "mm/an", N_SPAN, est(b.thermo.value)),
                     value("Masse de l'océan (GRACE, JPL)", "mm/an", N_SPAN, est(b.mass.value)),
                     value("Part de la dilatation", "%", N_SPAN, est(b.thermo.value / tot * 100)),
                     value("Part de la masse", "%", N_SPAN, est(b.mass.value / tot * 100)),
                     value("Résidu avec les pentes de Sen (C6)", "mm/an", N_SPAN, est(b.sen_resid))],
        charts=[CoherenceChart(
            title=f"Niveau marin observé et ses deux composantes ({N_SPAN[0]}-{N_SPAN[1]})", unit="mm", years=ny,
            lines=[CoherenceLine(name="Observé + ajustement isostatique", values=[round(obs_c[y], 2) for y in ny]),
                   CoherenceLine(name="Dilatation + masse", values=[round(th_c[y] + ma_c[y], 2) if y in ma_c else None for y in ny]),
                   CoherenceLine(name="Dilatation 0-2000 m", values=[round(th_c[y], 2) for y in ny]),
                   CoherenceLine(name="Masse (GRACE)", values=[round(ma_c[y], 2) if y in ma_c else None for y in ny])],
            note=("Chaque série est centrée sur sa propre moyenne (seules les variations comptent). Masse : moyenne "
                  "annuelle des mois désaisonnalisés par JPL, affichée si l'année en compte au moins 6 ; le trou "
                  "GRACE / GRACE-FO (juillet 2017 à mai 2018) laisse 2017 et 2018 vides ou partielles. Le bilan "
                  "lui-même porte sur les tendances calculées sur tous les mois disponibles (D-AU)."))],
        limitation=("L'océan sous 2000 m n'est pas mesuré (environ 0,1 mm/an) ; le résultat dépend de la correction "
                    "isostatique retenue (0,3 mm/an) ; les intervalles supposent les trois mesures indépendantes."))

    # ---------- E
    flux = ocean_flux(ohc, ey)
    te, to = pw_trend(eei, ey), pw_trend(flux, ey)
    e_ok = energy_ok(te, to)
    fs = smooth3(flux)
    sy3 = sorted(fs)
    te3, to3 = pw_trend(eei, sy3), pw_trend(fs, sy3)
    e3_ok = energy_ok(te3, to3)
    crit.append(Criterion(id="C5", label="Énergie", satisfied=e_ok, detail=(
        f"{E_SPAN[0]}-{E_SPAN[1]}, Prais-Winsten : déséquilibre CERES {_f(te.value, 2, True)} W/m² par décennie "
        f"{_ci(te.lo, te.hi, 2, True)} ; flux de chaleur dans l'océan 0-2000 m {_f(to.value, 2, True)} "
        f"{_ci(to.lo, to.hi, 2, True)} ; attendu : deux valeurs positives, intervalles qui se recoupent")))
    mean_e = sum(eei[y] for y in ey) / len(ey)
    mean_o = sum(flux[y] for y in ey) / len(ey)
    e_check = CoherenceCheck(
        id="energie", letter="E", title="Déséquilibre énergétique contre chaleur de l'océan",
        question="L'énergie en excès mesurée au sommet de l'atmosphère se retrouve-t-elle dans l'océan ?",
        criterion="C5", satisfied=e_ok,
        result=(f"Sur {E_SPAN[0]}-{E_SPAN[1]}, le déséquilibre mesuré par satellite augmente de {_f(te.value, 2, True)} W/m² "
                f"par décennie et le flux de chaleur entrant dans l'océan de {_f(to.value, 2, True)} : "
                + ("les deux hausses sont compatibles." if e_ok else "les deux évolutions ne concordent pas selon le critère.")),
        reference=REFERENCES["E"],
        values=[value("Déséquilibre CERES", "W/m² par décennie", E_SPAN, est(te.value, te.lo, te.hi)),
                value("Flux de chaleur dans l'océan 0-2000 m", "W/m² par décennie", E_SPAN, est(to.value, to.lo, to.hi))],
        information=[value("Déséquilibre CERES, moyenne", "W/m²", E_SPAN, est(mean_e)),
                     value("Flux océanique 0-2000 m, moyenne", "W/m²", E_SPAN, est(mean_o)),
                     value("Rapport des moyennes (non indépendant)", "%", E_SPAN, est(mean_o / mean_e * 100)),
                     value(f"Flux océanique lissé sur 3 ans (C6), {sy3[0]}-{sy3[-1]}", "W/m² par décennie",
                           (sy3[0], sy3[-1]), est(to3.value, to3.lo, to3.hi)),
                     value(f"Déséquilibre CERES (C6), {sy3[0]}-{sy3[-1]}", "W/m² par décennie",
                           (sy3[0], sy3[-1]), est(te3.value, te3.lo, te3.hi))],
        charts=[CoherenceChart(
            title=f"Énergie reçue en excès et chaleur entrant dans l'océan ({E_SPAN[0]}-{E_SPAN[1]})", unit="W/m²",
            years=ey,
            lines=[CoherenceLine(name="Déséquilibre au sommet de l'atmosphère (CERES)", values=[round(eei[y], 3) for y in ey]),
                   CoherenceLine(name="Flux de chaleur dans l'océan 0-2000 m", values=[round(flux[y], 3) for y in ey])],
            note=("Les deux grandeurs sont rapportées à toute la surface de la Terre. Le niveau moyen de CERES est calé "
                  "sur la chaleur de l'océan mesurée par Argo : seules les variations sont une comparaison "
                  "indépendante. Le flux océanique est la différence centrée du contenu thermique annuel."))],
        limitation=("Vingt ans seulement : le flux océanique, obtenu par différence, est bruité ; l'océan sous 2000 m, "
                    "la fonte des glaces et le réchauffement des terres (environ 10 % de l'excédent) ne sont pas comptés."))

    # ---------- C6 et confiance
    c6 = alt_ok and b.sen_ok and e3_ok
    crit.append(Criterion(id="C6", label="Robustesse", satisfied=c6, detail=(
        f"C2 avec la température de mer NOAA : {alt_txt} "
        f"({'conforme' if alt_ok else 'non conforme'}) ; C4 avec les pentes de Sen : résidu {_f(b.sen_resid, 2, True)} mm/an "
        f"({'conforme' if b.sen_ok else 'non conforme'}) ; C5 avec le flux lissé sur 3 ans ({sy3[0]}-{sy3[-1]}) : "
        f"CERES {_f(te3.value, 2, True)} {_ci(te3.lo, te3.hi, 2, True)}, océan {_f(to3.value, 2, True)} "
        f"{_ci(to3.lo, to3.hi, 2, True)} ({'conforme' if e3_ok else 'non conforme'})")))
    ok = {c.id: c.satisfied for c in crit}
    physical = sum(ok[k] for k in ("C2", "C3", "C4", "C5"))
    if all(ok.values()):
        conf, reason = "elevee", "C1 à C6 conformes : les quatre contrôles et leur robustesse tiennent."
    elif physical >= 3:
        bad = ", ".join(k for k, v in ok.items() if not v)
        conf, reason = "moyenne", f"{physical} contrôles physiques sur 4 conformes ; non conforme : {bad} (règle D-AT)."
    else:
        conf, reason = "non_etabli", f"{physical} contrôles physiques sur 4 conformes seulement (règle D-AT)."
    checks = [v_check, s_check, n_check, e_check]
    passed = [c.title.split(" (")[0].lower() for c in checks if c.satisfied]
    failed = [c.title.split(" (")[0].lower() for c in checks if not c.satisfied]
    if physical == 4:
        finding = ("Les quatre contrôles physiques sont cohérents : des mesures indépendantes (satellites, flotteurs "
                   "Argo, gravimétrie) s'accordent sur une atmosphère et un océan qui se réchauffent. Ces contrôles "
                   "n'attribuent pas de cause.")
    else:
        head = {0: "Aucun des quatre contrôles physiques n'est cohérent",
                1: "Un des quatre contrôles physiques est cohérent"}.get(
            physical, f"{_count(physical).capitalize()} des quatre contrôles physiques sont cohérents")
        finding = head + (f" ({', '.join(passed)})" if passed else "") + f" ; écart pour : {', '.join(failed)}."
    inputs = [
        InputSource(name=RV.SOURCE_NAME, url=RV.DIR_URL, license=RV.LICENSE,
                    note=f"fichier {tpw_meta.get('file', '?')}, masque constant 60° S-60° N"),
        InputSource(name=G.SOURCES["tls-rss"].name, url=G.SOURCES["tls-rss"].url, license=G.SOURCES["tls-rss"].license),
        InputSource(name=G.SOURCES["tls-uah"].name, url=G.SOURCES["tls-uah"].url, license=G.SOURCES["tls-uah"].license),
        InputSource(name=G.SOURCES["thermosteric-2000"].name, url=G.SOURCES["thermosteric-2000"].url,
                    license=G.SOURCES["thermosteric-2000"].license),
        InputSource(name=GR.SOURCE_NAME, url=GR.PAGE, license=GR.LICENSE,
                    note=(grace_meta or {}).get("granule")),
        *[InputSource(name=f"{lab}, telle que publiée sur le site", url=SITE.format(iid), license="voir la page de l'indicateur")
          for iid, lab in ((SST, "Température de surface de la mer HadSST4"), (SST_ALT, "Température de surface de la mer NOAA"),
                           (TLT["rss"], "Basse troposphère RSS"), (TLT["uah"], "Basse troposphère UAH"),
                           (GMSL, "Niveau moyen de la mer NOAA STAR"), (OHC, "Contenu thermique de l'océan 0-2000 m NOAA NCEI"),
                           (EEI, "Déséquilibre énergétique CERES EBAF"))],
    ]
    return Coherence(
        question="Les grandeurs mesurées indépendamment évoluent-elles comme la physique l'impose ?",
        model=("Quatre contrôles : vapeur d'eau contre température de mer (Clausius-Clapeyron) ; basse troposphère "
               "contre basse stratosphère ; niveau marin contre dilatation plus masse ajoutée ; déséquilibre énergétique "
               "contre chaleur entrant dans l'océan."),
        finding=finding, confidence=conf, confidence_reason=reason,
        method_note=("Critères, seuils et périodes fixés avant tout calcul (décisions D-AS à D-AU du 20/11/2026). Les "
                     "séries déjà publiées sur le site sont relues telles quelles ; les nouvelles sont relevées chez "
                     "leur producteur. Tendances de Sen (stratosphère), moindres carrés (bilan marin, D-AU), régression "
                     "à erreurs AR(1) de Prais-Winsten (vapeur d'eau, énergie) ; intervalles à 95 %."),
        limitations=[
            "Cohérence n'est pas attribution : ces contrôles vérifient que les mesures s'accordent entre elles, pas ce "
            "qui cause le réchauffement (voir P10.1).",
            v_check.limitation, s_check.limitation, n_check.limitation, e_check.limitation],
        inputs=inputs, checks=checks, criteria=crit, script=SCRIPT, etl_version=ctx_version, extracted_at=extracted_at)


def load_and_build(out_dir: Path, raw_dir: Path, ctx_version: str, extracted_at) -> Coherence:
    tpw, meta = RV.load()
    gmeta = json.loads((GR.OUT_DIR / "meta.json").read_text(encoding="utf-8"))
    return build(tpw_monthly=tpw, tpw_meta=meta, sst=published(out_dir, SST), sst_alt=published(out_dir, SST_ALT),
                 tlt={n: published(out_dir, iid) for n, iid in TLT.items()},
                 tls={n: G.load(sid, raw_dir) for n, sid in TLS.items()},
                 gmsl=published(out_dir, GMSL), thermo=G.load("thermosteric-2000", raw_dir), grace_rows=GR.load(),
                 ohc=published(out_dir, OHC), eei=published(out_dir, EEI), ctx_version=ctx_version,
                 extracted_at=extracted_at, grace_meta=gmeta)
