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
          "la vapeur d'eau intégrée a augmenté depuis 1979 à un rythme globalement cohérent avec ce taux (GIEC AR6 GT1, "
          "ch. 2) ; fourchette retenue 6 à 8 % par °C."),
    "S": ("R-B2 : basse stratosphère refroidie depuis le milieu du XXe siècle, « pratiquement certain », stable depuis "
          "le milieu des années 1990 ; troposphère réchauffée (GIEC AR6 GT1, ch. 2)."),
    "N": ("R-B3 : niveau marin 1993-2018 3,1 ± 0,3 mm/an ; dilatation 42 %, glaciers 21 %, Groenland 15 %, "
          "Antarctique 8 % ; depuis 2005, avec la masse de l'océan mesurée par GRACE, bilan fermé à 0,3 mm/an près "
          "(1 σ) (WCRP Global Sea Level Budget Group, ESSD 10, 1551, 2018)."),
    "E": ("R-B4 : hausse du déséquilibre de 0,50 ± 0,47 W/m² par décennie (intervalle à 90 %) de mi-2005 à mi-2019, "
          "indiscernable entre satellites et mesures in situ (Loeb et al., 2021, GRL 48) ; environ 91 % de l'excédent "
          "réchauffe l'océan (GIEC AR6)."),
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


def est(v: float, lo: float | None = None, hi: float | None = None) -> Estimate:
    """Pleine précision (règle de P10.1) : l'arrondi est fait une seule fois, à l'affichage."""
    r = lambda x: None if x is None else float(x) + 0.0  # noqa: E731
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
    """Pente des moindres carrés et son erreur type de Newey-West (Bartlett, décalage ⌊4·(n/100)^(2/9)⌋, au moins 1).

    Calcul direct plutôt que R.ols_newey_west, qui refuse les séries de moins de 12 points : les sous-périodes de
    P10.4b (2005-2015, 2016-2024) en ont 11 et 9. L'erreur type n'est qu'une information (D-AU)."""
    x, y = np.asarray(t, float), np.asarray(v, float)
    if len(x) < 5 or not (np.all(np.isfinite(x)) and np.all(np.isfinite(y))):
        raise ValueError("tendance : moins de 5 points ou valeur non finie")
    X = np.column_stack([np.ones(len(x)), x])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ beta
    n, k = X.shape
    lag = max(1, R.newey_west_lag(n))
    xe = X * e[:, None]
    S = xe.T @ xe
    for j in range(1, lag + 1):
        G_ = xe[j:].T @ xe[:-j]
        S += (1 - j / (lag + 1)) * (G_ + G_.T)
    bread = np.linalg.inv(X.T @ X)
    cov = bread @ S @ bread * n / (n - k)
    return Slope(float(beta[1]), float(np.sqrt(cov[1, 1])), n)


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


def budget(gmsl: dict[int, float], thermo: dict[int, float], mass: list[tuple[float, float]],
           p: tuple[int, int] = N_SPAN) -> Budget:
    ys = span(p)
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
        note=(f"Écarts à la moyenne {V_SPAN[0]}-{V_SPAN[1]} : vapeur d'eau en %, et ce que donnerait le taux théorique "
              "de 7 % par °C appliqué à la température moyenne de la mer du globe. La vapeur est mesurée entre 60° S et "
              "60° N, la température sur tout l'océan : les deux courbes ne portent pas sur la même région. Cette "
              "différence n'explique pas l'écart : sur un même domaine, la pente est encore plus forte (P10.4b)."))
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
                    "moyenne mondiale de la mer, la vapeur celle de 60° S-60° N (différence testée en P10.4b : elle "
                    "n'explique pas l'écart)."))

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
        result=(f"Sur {N_SPAN[0]}-{N_SPAN[1]}, la mer monte de {_f(tot, 2)} mm par an (altimétrie corrigée de "
                f"l'ajustement isostatique) ; la dilatation de l'eau (0-2000 m) en explique {_f(b.thermo.value, 2)} et "
                f"l'eau ajoutée à l'océan, pesée par GRACE, {_f(b.mass.value, 2)}. Il reste {_f(b.resid, 2, True)} mm par "
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
                    "isostatique, celle ajoutée à l'altimétrie (0,3 mm/an) et celle déjà appliquée par JPL à GRACE "
                    "(ICE6G-D), d'incertitude comparable à la tolérance ; les intervalles supposent les trois mesures "
                    "indépendantes et reposent sur peu de points : ils sont probablement trop étroits."))

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
                f"par décennie {_ci(te.lo, te.hi, 2, True)} et le flux de chaleur entrant dans l'océan de "
                f"{_f(to.value, 2, True)} {_ci(to.lo, to.hi, 2, True)}"
                + (" : les deux tendances ne se contredisent pas, mais le contrôle est peu exigeant"
                   + (" (la hausse du flux océanique n'est pas établie)." if to.lo <= 0 else ".")
                   if e_ok else " : les deux évolutions ne concordent pas selon le critère.")),
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
        limitation=("Vingt ans seulement : le flux océanique, obtenu par différence, est bruité. L'océan sous 2000 m, "
                    "non mesuré ici, le réchauffement des terres (environ 5 % de l'excédent selon le GIEC AR6), la fonte "
                    "des glaces (3 %) et l'atmosphère (1 %) ne sont pas comptés : le rapport des moyennes ne peut pas "
                    "atteindre 100 %."))

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
        rule="D-AT",
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


# ================================================================ P10.4b : recadrage de V et N (D-AV, D-AW, D-AX)
# Cadré le 20/11/2026 APRÈS le calcul officiel de P10.4 (écarts C2 et C4), en connaissant ses résultats ; les seuils
# ne sont pas élargis (D-AW). Critères B1-B5, règle de confiance D-AX.

VB_SPAN = (1988, 2025)
NB_SPAN = (2005, 2015)
NB_INFO = (2016, 2024)
COMMON_MIN = 0.5                     # B1 : part de la bande 60° S-60° N couverte par le masque commun


def annual_common(monthly: dict[str, tuple[float, float]]) -> tuple[dict[int, float], dict[int, float]]:
    per: dict[int, list[tuple[float, float]]] = {}
    for m, v in monthly.items():
        per.setdefault(int(m[:4]), []).append(v)
    full = {y: v for y, v in per.items() if len(v) == 12}
    return ({y: sum(a for a, _ in v) / 12 for y, v in full.items()}, {y: sum(b for _, b in v) / 12 for y, v in full.items()})


def _thousands(n) -> str:
    return "?" if n is None else f"{int(n):,}".replace(",", "\u202f")


def build_b(*, common_monthly: dict[str, tuple[float, float]], vapor_meta: dict, gmsl: dict[int, float],
            thermo: dict[int, float], grace_rows: list[dict], ctx_version: str, extracted_at,
            grace_meta: dict | None = None) -> Coherence:
    crit: list[Criterion] = []
    vy = span(VB_SPAN)
    tpw, sst = annual_common(common_monthly)
    frac = float(vapor_meta["common_area_fraction"])
    v_miss = missing(tpw, vy)
    ny = span(NB_SPAN)
    n_miss = sorted(set(missing(gmsl, span((NB_SPAN[0], NB_INFO[1])))) | set(missing(thermo, span((NB_SPAN[0], NB_INFO[1])))))
    mass = mass_months(grace_rows, NB_SPAN)
    n_cov, n_months = month_count(mass), 12 * len(ny)
    b1 = not v_miss and frac >= COMMON_MIN and not n_miss and n_cov >= MASS_MIN * n_months
    crit.append(Criterion(id="B1", label="Données", satisfied=b1, detail=(
        f"V′ : {VB_SPAN[0]}-{VB_SPAN[1]}, {'aucune année manquante' if not v_miss else 'manquantes : ' + ', '.join(map(str, v_miss))}, "
        f"masque commun RSS et ERSST couvrant {_f(frac * 100, 1)} % de la bande 60° S-60° N (seuil {_f(COMMON_MIN * 100, 0)} %, "
        f"{_thousands(vapor_meta.get('common_cells'))} mailles de 1°) ; N′ : altimétrie et dilatation {NB_SPAN[0]}-{NB_INFO[1]} "
        f"{'complètes' if not n_miss else 'manquantes : ' + ', '.join(map(str, n_miss))}, masse GRACE {n_cov} mois sur "
        f"{n_months} en {NB_SPAN[0]}-{NB_SPAN[1]} ({_f(n_cov / n_months * 100, 0)} %, seuil {_f(MASS_MIN * 100, 0)} %)")))

    # ---------- V′
    try:
        cc, cc_err = fit_cc(tpw, sst, vy), ""
    except ValueError as exc:
        cc, cc_err = None, str(exc)
    ob, olo, ohi = fit_cc_ols(tpw, sst, vy)
    ols_ok = olo > 0 and overlap((olo, ohi), CC_RANGE)
    b2 = cc is not None and cc.ok
    rng = f"[{_f(CC_RANGE[0], 0)} ; {_f(CC_RANGE[1], 0)}]"
    crit.append(Criterion(id="B2", label="Vapeur d'eau, même domaine", satisfied=b2, detail=(
        (f"β = {_f(cc.beta, 1)} % par °C {_ci(cc.lo, cc.hi, 1)} ({VB_SPAN[0]}-{VB_SPAN[1]}, ERSST v5 sur le masque commun, "
         f"Prais-Winsten, ρ = {_f(cc.rho, 2)})" if cc is not None else f"{cc_err}")
        + f" ; attendu : intervalle recoupant {rng} (D-AW), borne basse > 0")))
    mean_t = sum(sst[y] for y in vy) / len(vy)
    mean_w = sum(tpw[y] for y in vy) / len(vy)
    beta_txt = (f"{_f(cc.beta, 1)} % par °C de température de la mer (intervalle à 95 % : {_f(cc.lo, 1)} à "
                f"{_f(cc.hi, 1)})" if cc is not None
                else "selon une pente que l'estimateur AR(1) ne parvient pas à estimer")
    v_check = CoherenceCheck(
        id="vapeur-domaine", letter="V′", title="Vapeur d'eau et température de la mer du même domaine",
        question="Sur un même domaine océanique, la vapeur d'eau croît-elle d'environ 7 % par degré de la mer ?",
        criterion="B2", satisfied=b2,
        result=(f"Sur le même domaine (60° S-60° N, mailles valides pour les deux jeux), la vapeur d'eau augmente de "
                f"{beta_txt}, "
                + ("compatible avec le taux de Clausius-Clapeyron." if b2 else f"hors de la fourchette {rng} retenue.")),
        reference=(REFERENCES["V"] + " Fourchette conservée après le premier calcul (D-AW). Rapports de tendances publiés "
                   "contre la température de la mer plus élevés : 9,9 % par K sur 20° S-20° N (Fu et al., 2025, ESSD "
                   "17, 4651), environ 11 % par K pour le radiomètre TMR de Topex, 1992-2005 (Keihm et al., 2009)."),
        values=[value("β, vapeur d'eau par °C de la mer (même domaine)", "% par °C", VB_SPAN,
                      est(cc.beta, cc.lo, cc.hi) if cc is not None else est(ob))],
        information=[value("β en moindres carrés, erreurs de Newey-West (B4)", "% par °C", VB_SPAN, est(ob, olo, ohi)),
                     *([value("Part de la variance expliquée", "%", VB_SPAN, est(cc.r2 * 100))] if cc is not None else [])],
        charts=[CoherenceChart(
            title=f"Vapeur d'eau et température de la mer sur le même domaine ({VB_SPAN[0]}-{VB_SPAN[1]})", unit="%",
            years=vy,
            lines=[CoherenceLine(name="Vapeur d'eau RSS (écart à la moyenne)",
                                 values=[round((tpw[y] / mean_w - 1) * 100, 3) for y in vy]),
                   CoherenceLine(name="7 % par °C de la température de mer ERSST (même domaine)",
                                 values=[round(7 * (sst[y] - mean_t), 3) for y in vy])],
            note=(f"Écarts à la moyenne {VB_SPAN[0]}-{VB_SPAN[1]}, sur les mêmes mailles : vapeur d'eau en %, et ce que "
                  "donnerait le taux de 7 % par °C appliqué à la température de la mer de ces mailles."))],
        limitation=("Température de la mer et non de l'air : la troposphère tropicale se réchauffe plus que la mer, ce "
                    "qui pousse le rapport au-dessus de 7 % ; ERSST (2°) est lue à la maille la plus proche de chaque "
                    "maille RSS (1°)."))

    # ---------- N′
    b = budget(gmsl, thermo, mass, NB_SPAN)
    late = budget(gmsl, thermo, mass_months(grace_rows, NB_INFO), NB_INFO)
    tot, tot_late = b.obs.value + GIA, late.obs.value + GIA
    b3 = b.ok
    crit.append(Criterion(id="B3", label="Bilan marin 2005-2015", satisfied=b3, detail=(
        f"{NB_SPAN[0]}-{NB_SPAN[1]}, moindres carrés : observé {_f(b.obs.value, 2)} + {_f(GIA, 1)} = {_f(tot, 2)} mm/an ; "
        f"dilatation 0-2000 m {_f(b.thermo.value, 2)} ; masse {_f(b.mass.value, 2)} ; résidu {_f(b.resid, 2, True)} mm/an "
        f"(information : {_ci(b.resid_lo, b.resid_hi, 2, True)}) ; attendu |résidu| ≤ {_f(RESID_MAX, 1)}")))
    per: dict[int, list[float]] = {}
    for t, v in mass_months(grace_rows, (NB_SPAN[0], NB_INFO[1])):
        per.setdefault(int(t), []).append(v)
    ma = {y: sum(v) / len(v) for y, v in per.items() if len(v) >= 6}
    yall = span((NB_SPAN[0], NB_INFO[1]))

    def centred(d: dict[int, float]) -> dict[int, float]:
        m = sum(d.values()) / len(d)
        return {y: v - m for y, v in d.items()}

    obs_c = centred({y: gmsl[y] + GIA * (y - NB_SPAN[0]) for y in yall})
    th_c, ma_c = centred({y: thermo[y] for y in yall}), centred(ma)
    n_check = CoherenceCheck(
        id="niveau-marin-2005-2015", letter="N′", title="Bilan du niveau marin avant 2016",
        question="Avant les difficultés instrumentales connues de 2016, la hausse mesurée est-elle la somme de la "
                 "dilatation et de l'eau ajoutée ?",
        criterion="B3", satisfied=b3,
        result=(f"Sur {NB_SPAN[0]}-{NB_SPAN[1]}, la mer monte de {_f(tot, 1)} mm par an ; dilatation {_f(b.thermo.value, 1)}, "
                f"masse {_f(b.mass.value, 1)} ; résidu {_f(b.resid, 2, True)} mm par an, "
                + ("dans la tolérance de ± 0,5." if b3 else "hors de la tolérance de ± 0,5.")
                + f" Sur {NB_INFO[0]}-{NB_INFO[1]}, pour information, le résidu est de {_f(late.resid, 2, True)} mm par an."),
        reference=REFERENCES["N"] + " Non-fermeture après 2016 : Chen et al. (2020) ; Barnoud et al. (2021, GRL 48).",
        values=[value("Résidu observé − (dilatation + masse)", "mm/an", NB_SPAN, est(b.resid, b.resid_lo, b.resid_hi))],
        information=[value("Niveau observé + 0,3 (ajustement isostatique)", "mm/an", NB_SPAN, est(tot)),
                     value("Dilatation thermique 0-2000 m (NCEI)", "mm/an", NB_SPAN, est(b.thermo.value)),
                     value("Masse de l'océan (GRACE, JPL)", "mm/an", NB_SPAN, est(b.mass.value)),
                     value("Résidu avec les pentes de Sen (B4)", "mm/an", NB_SPAN, est(b.sen_resid)),
                     value("Résidu après 2016 (information)", "mm/an", NB_INFO, est(late.resid, late.resid_lo, late.resid_hi)),
                     value("Niveau observé + 0,3, après 2016", "mm/an", NB_INFO, est(tot_late)),
                     value("Dilatation 0-2000 m, après 2016", "mm/an", NB_INFO, est(late.thermo.value)),
                     value("Masse de l'océan, après 2016", "mm/an", NB_INFO, est(late.mass.value))],
        charts=[CoherenceChart(
            title=f"Niveau marin observé et ses deux composantes ({NB_SPAN[0]}-{NB_INFO[1]})", unit="mm", years=yall,
            lines=[CoherenceLine(name="Observé + ajustement isostatique", values=[round(obs_c[y], 2) for y in yall]),
                   CoherenceLine(name="Dilatation + masse", values=[round(th_c[y] + ma_c[y], 2) if y in ma_c else None for y in yall]),
                   CoherenceLine(name="Dilatation 0-2000 m", values=[round(th_c[y], 2) for y in yall]),
                   CoherenceLine(name="Masse (GRACE)", values=[round(ma_c[y], 2) if y in ma_c else None for y in yall])],
            note=("Séries centrées sur leur moyenne 2005-2024 ; la masse, sur la moyenne de ses seules années affichées "
                  "(moyenne annuelle des mois désaisonnalisés, affichée si l'année en compte au moins 6). Le critère "
                  "porte sur les tendances de 2005-2015 ; 2016-2024 est publié pour information."))],
        limitation=("Onze ans seulement pour le critère, et un intervalle plus large que la tolérance : le contrôle ne "
                    "peut que ne pas rejeter la fermeture ; l'océan sous 2000 m n'est pas mesuré ; les corrections "
                    "isostatiques (altimétrie et GRACE) pèsent sur le résultat ; le découpage en 2016 a été choisi après le "
                    "premier calcul."))

    # ---------- B4 et confiance (D-AX)
    b4 = ols_ok and b.sen_ok
    crit.append(Criterion(id="B4", label="Robustesse", satisfied=b4, detail=(
        f"B2 en moindres carrés, erreurs de Newey-West : β = {_f(ob, 1)} % par °C {_ci(olo, ohi, 1)} "
        f"({'conforme' if ols_ok else 'non conforme'}) ; B3 avec les pentes de Sen : résidu {_f(b.sen_resid, 2, True)} mm/an "
        f"({'conforme' if b.sen_ok else 'non conforme'})")))
    ok = {c.id: c.satisfied for c in crit}
    if all(ok.values()):
        conf, reason = "elevee", "B1 à B4 conformes (règle D-AX)."
    elif b2 or b3:
        bad = ", ".join(k for k, v in ok.items() if not v)
        good = "B2" if b2 else "B3"
        conf, reason = "moyenne", (f"{good} conforme ; non conformes : {bad}"
                                   + (" : un contrôle recadré sur deux" if not (b2 and b3) else "")
                                   + " (règle D-AX).")
    else:
        conf, reason = "non_etabli", "Aucun des deux contrôles recadrés n'est conforme (règle D-AX)."
    half = max(abs(b.resid_hi - b.resid), abs(b.resid - b.resid_lo))
    parts = [("la vapeur d'eau suit le taux de Clausius-Clapeyron sur un même domaine" if b2 else
              "la vapeur d'eau croît plus vite que 7 % par °C de la mer, même sur un même domaine"),
             (f"le résidu du bilan marin est dans la tolérance sur {NB_SPAN[0]}-{NB_SPAN[1]} ({_f(b.resid, 2, True)} mm/an"
              + (f", mais son incertitude, ± {_f(half, 1)}, dépasse la tolérance)"
                 if b.resid_lo < -RESID_MAX or b.resid_hi > RESID_MAX else ")") if b3 else
              f"le résidu du bilan marin sort de la tolérance sur {NB_SPAN[0]}-{NB_SPAN[1]} ({_f(b.resid, 2, True)} mm/an)")
             + (f", et {'en sort nettement' if b3 else 'aussi'} sur {NB_INFO[0]}-{NB_INFO[1]} ({_f(late.resid, 2, True)}, information)"
                if abs(late.resid) > RESID_MAX else
                f", et y reste sur {NB_INFO[0]}-{NB_INFO[1]} ({_f(late.resid, 2, True)}, information)")]
    finding = "Recadrés après le premier calcul : " + " ; ".join(parts) + "."
    inputs = [
        InputSource(name=RV.SOURCE_NAME, url=RV.DIR_URL, license=RV.LICENSE,
                    note=f"fichier {vapor_meta.get('file', '?')}, masque commun avec ERSST"),
        InputSource(name=RV.ERSST_NAME, url=RV.ERSST_PAGE, license=RV.ERSST_LICENSE),
        InputSource(name=G.SOURCES["thermosteric-2000"].name, url=G.SOURCES["thermosteric-2000"].url,
                    license=G.SOURCES["thermosteric-2000"].license),
        InputSource(name=GR.SOURCE_NAME, url=GR.PAGE, license=GR.LICENSE, note=(grace_meta or {}).get("granule")),
        InputSource(name="Niveau moyen de la mer NOAA STAR, tel que publié sur le site", url=SITE.format(GMSL),
                    license="voir la page de l'indicateur"),
    ]
    return Coherence(
        rule="D-AX",
        question="Recadrés après le premier calcul, les contrôles de la vapeur d'eau et du niveau marin tiennent-ils ?",
        model=("V′ : ln W = c + β·T + u, u AR(1), W vapeur d'eau RSS et T température de la mer ERSST v5 sur les mêmes "
               "mailles ; N′ : tendance(observé + 0,3) − tendance(dilatation 0-2000 m) − tendance(masse GRACE), 2005-2015."),
        finding=finding, confidence=conf, confidence_reason=reason,
        method_note=("Sous-phase cadrée après le calcul officiel de P10.4, en connaissant ses résultats (décision D-AV du "
                     "20/11/2026) ; critères B1-B5 et seuils fixés avant ce nouveau calcul (D-AW, D-AX), sans élargir la "
                     "fourchette de 6 à 8 % par °C. Le résultat de P10.4 reste publié tel quel."),
        limitations=[
            "Contrôles recadrés après avoir vu un premier résultat : un succès ici a moins de poids qu'un succès prévu "
            "d'avance.", v_check.limitation, n_check.limitation],
        inputs=inputs, checks=[v_check, n_check], criteria=crit, script=SCRIPT, etl_version=ctx_version,
        extracted_at=extracted_at)


def load_and_build_b(out_dir: Path, raw_dir: Path, ctx_version: str, extracted_at) -> Coherence:
    _, meta = RV.load()
    gmeta = json.loads((GR.OUT_DIR / "meta.json").read_text(encoding="utf-8"))
    return build_b(common_monthly=RV.load_common(), vapor_meta=meta, gmsl=published(out_dir, GMSL),
                   thermo=G.load("thermosteric-2000", raw_dir), grace_rows=GR.load(), ctx_version=ctx_version,
                   extracted_at=extracted_at, grace_meta=gmeta)
