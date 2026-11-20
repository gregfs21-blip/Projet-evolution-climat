"""P10 — démonstration de l'évolution du climat (cadrage, critères O1-O9 et décisions D-AD à D-AH du 17/11/2026,
validés par Grég avant tout calcul ; docs/phases.md, section P10).

P10.1, régression multiple : pour chaque jeu de températures mondiales publié (HadCRUT5, GISTEMP, Berkeley),
    T(a) = c + βₐ·A(a) + βᵥ·V(a) + βₛ·S(a) + βₑ·E(a) + ε(a),  ε AR(1) (Prais-Winsten itéré),
A forçage anthropique, V forçage volcanique décalé de 6 mois, S forçage solaire (IGCC 2025), E indice ENSO décalé de
3 mois (Niño 3.4 HadISST1.1 moins sa climatologie mobile de 30 ans). Les températures sont relues dans les JSON publiés
(data/processed/monde) : la régression porte exactement sur les séries affichées par le site.

Les choix (décalages, période de base, fenêtres, fourchettes) sont ceux du cadrage ; ils ne sont pas ajustés aux
données. Leur effet est mesuré par le critère O8.

Usage : python -m etl.demonstration   → data/processed/demonstration.json
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from etl.context import PROCESSED_DIR, RAW_DIR, ROOT, make_context
from etl.schema import (Attribution, Coefficient, Criterion, Demonstration, DemonstrationAnalysis, Estimate,
                        InputSource, Period, Regression, RegressionDataset, RegressionSeries, RobustnessCase)
from etl.sources import globaux as G
from etl.sources import igcc as I
from etl.stats import regression as R
from etl.stats.trend import annual_trend

OUT = PROCESSED_DIR / "demonstration.json"
SCRIPT = "etl/demonstration.py"

# ---------------------------------------------------------------- choix fixés par le cadrage (17/11/2026)
BASELINE = (1850, 1900)
LAG_ENSO, LAG_VOLC = 3, 6                   # mois (Foster et Rahmstorf, 2011)
ENSO_LAGS, VOLC_LAGS = (2, 3, 4), (0, 6, 12)  # O8 a
CLIM_YEARS = 30                             # climatologie mobile de l'indice ENSO
SUB_START = 1951                            # O8 c : sous-période avec l'ONI
F2X = 3.93                                  # W/m², forçage d'un doublement du CO₂ (GIEC AR6, ch. 7)
TCR_RANGE = (1.2, 2.4)                      # R-O4 (GIEC AR6, très probable)
NATURAL_RANGE = (-0.1, 0.2)                 # R-O3 (IGCC 2025)
TREND_START = 1979
ONI_MIN_R = 0.95                            # O2
ALPHA = 0.05
# (fenêtre, réchauffement humain publié [central, bas, haut], naturel publié) — IGCC 2025, Assessment-Update-2025
WINDOWS = (
    ((2010, 2019), (1.07, 0.9, 1.3), (0.05, -0.1, 0.2)),
    ((2016, 2025), (1.24, 1.0, 1.5), (0.04, -0.1, 0.2)),
)
CONTROL = (2016, 2025)                      # fenêtre de contrôle de O8
REFERENCE_SOURCE = ("IGCC 2025 (Forster et al., 2026, ESSD 18, 3889-3933), évaluation « Assessment-Update-2025 » ; "
                    "2010-2019 : GIEC AR6 GT1, SPM A.1.3 (1,07 °C, probable 0,8 à 1,3)")
DATASETS = (
    ("hadcrut5", "temperature-hadcrut5-monde", "HadCRUT5"),
    ("gistemp", "temperature-gistemp-monde", "GISTEMP v4"),
    ("berkeley", "temperature-berkeley-monde", "Berkeley Earth"),
)
NAMES = ["anthropique", "volcans", "soleil", "enso"]
LABELS = {
    "constante": ("Constante", "°C"),
    "anthropique": ("Forçage anthropique", "°C par W/m²"),
    "volcans": ("Forçage volcanique (décalé de 6 mois)", "°C par W/m²"),
    "soleil": ("Forçage solaire", "°C par W/m²"),
    "enso": ("ENSO, Niño 3.4 (décalé de 3 mois)", "°C par °C"),
}


# ---------------------------------------------------------------- indice ENSO et décalages


def enso_index(anom: dict[tuple[int, int], float], years: int = CLIM_YEARS) -> dict[tuple[int, int], float]:
    """Anomalie moins sa climatologie mobile de `years` ans, mois par mois (années a − 15 à a + 14).

    La fenêtre est décalée pour rester entière aux deux bouts ; seules les années complètes (12 mois) servent de base.
    """
    full = sorted(y for y in {y for y, _ in anom} if all((y, m) in anom for m in range(1, 13)))
    if len(full) < years or full != list(range(full[0], full[-1] + 1)):
        raise ValueError("indice ENSO : années complètes insuffisantes ou non consécutives")
    first, last = full[0], full[-1]
    half = years // 2
    out = {}
    for (y, m), v in anom.items():
        start = y - half
        start = min(max(start, first), last - years + 1)
        base = [anom[(b, m)] for b in range(start, start + years)]
        out[(y, m)] = v - sum(base) / years
    return out


def lagged_mean(monthly: dict[tuple[int, int], float], year: int, lag: int) -> float | None:
    """Moyenne des 12 mois de janvier − lag à décembre − lag (ex. lag 3 : octobre a − 1 à septembre a)."""
    vals = []
    for k in range(12):
        t = 12 * year + k - lag
        key = (t // 12, t % 12 + 1)
        if key not in monthly:
            return None
        vals.append(monthly[key])
    return sum(vals) / 12


def volcanic_lagged(v: dict[int, float], year: int, lag: int) -> float | None:
    """Forçage annuel décalé de `lag` mois (0, 6 ou 12) : (1 − lag/12)·v(a) + (lag/12)·v(a − 1)."""
    w = lag / 12
    if year not in v or (w > 0 and year - 1 not in v):
        return None
    return (1 - w) * v[year] + (w * v[year - 1] if w > 0 else 0.0)


def window_mean(f, years: range) -> float:
    vals = [f(y) for y in years]
    if any(x is None for x in vals):
        raise ValueError(f"moyenne {years.start}-{years.stop - 1} incomplète")
    return sum(vals) / len(vals)


# ---------------------------------------------------------------- régression d'un jeu


@dataclass
class Inputs:
    erf: dict[int, dict[str, float]]
    anthro: dict[int, float]                     # forçage anthropique retenu (meilleure estimation, ou 5 % / 95 %)
    enso: dict[tuple[int, int], float]


@dataclass
class Run:
    years: list[int]
    T: np.ndarray
    X: np.ndarray
    fit: R.Fit
    lag_e: int
    lag_v: int
    inputs: Inputs

    def A(self, y): return self.inputs.anthro.get(y)
    def V(self, y): return volcanic_lagged({k: r["volcanic"] for k, r in self.inputs.erf.items()}, y, self.lag_v)
    def S(self, y): return self.inputs.erf[y]["solar"] if y in self.inputs.erf else None

    def deltas(self, window: tuple[int, int]) -> dict[str, float]:
        w, b = range(window[0], window[1] + 1), range(BASELINE[0], BASELINE[1] + 1)
        return {n: window_mean(f, w) - window_mean(f, b) for n, f in (("anthropique", self.A), ("volcans", self.V),
                                                                      ("soleil", self.S))}

    def attributable(self, window: tuple[int, int]) -> tuple[float, float, float]:
        d = self.deltas(window)
        return self.fit.combination({"anthropique": d["anthropique"]})

    def natural(self, window: tuple[int, int]) -> tuple[float, float, float]:
        d = self.deltas(window)
        return self.fit.combination({"volcans": d["volcans"], "soleil": d["soleil"]})


def regress(temp: dict[int, float], inputs: Inputs, lag_e: int = LAG_ENSO, lag_v: int = LAG_VOLC,
            start: int | None = None) -> Run:
    volc = {k: r["volcanic"] for k, r in inputs.erf.items()}
    rows = []
    for y in sorted(temp):
        if start is not None and y < start:
            continue
        xs = (inputs.anthro.get(y), volcanic_lagged(volc, y, lag_v), inputs.erf.get(y, {}).get("solar"),
              lagged_mean(inputs.enso, y, lag_e))
        if all(x is not None for x in xs):
            rows.append((y, temp[y], *xs))
    years = [r[0] for r in rows]
    if not years or years != list(range(years[0], years[-1] + 1)):
        raise ValueError("régression : années non consécutives (donnée manquante au milieu de la période)")
    arr = np.array([r[1:] for r in rows], dtype=float)
    T, X = arr[:, 0], arr[:, 1:]
    return Run(years, T, X, R.prais_winsten(T, X, NAMES), lag_e, lag_v, inputs)


def coefficients(fit: R.Fit) -> list[Coefficient]:
    lo, hi = fit.ci(ALPHA)
    p = fit.p_values()
    return [Coefficient(name=_slug(n), label=LABELS[n][0], unit=LABELS[n][1], value=float(fit.coef[i]),
                        ci_low=float(lo[i]), ci_high=float(hi[i]), p_value=float(p[i]))
            for i, n in enumerate(fit.names)]


def _slug(name: str) -> str:
    return {"constante": "constante", "anthropique": "anthropique", "volcans": "volcans", "soleil": "soleil",
            "enso": "enso"}[name]


def est(v: float, lo: float | None = None, hi: float | None = None) -> Estimate:
    """Pleine précision : le texte (etl) et le site n'arrondissent qu'une fois, au moment de l'affichage."""
    r = lambda x: None if x is None else float(x) + 0.0  # noqa: E731
    return Estimate(value=r(v), ci_low=r(lo), ci_high=r(hi))


def in_range(x: float, rng: tuple[float, float]) -> bool:
    return rng[0] <= x <= rng[1]


# ---------------------------------------------------------------- lecture des entrées


def load_temperatures(out_dir: Path) -> dict[str, dict[int, float]]:
    out = {}
    for _, iid, _ in DATASETS:
        ind = json.loads((out_dir / "monde" / f"{iid}.json").read_text(encoding="utf-8"))
        out[iid] = {int(t[:4]): v for t, v in zip(ind["series"]["time"], ind["series"]["value"]) if v is not None}
    return out


def oni_annual(out_dir: Path) -> dict[int, float]:
    ind = json.loads((out_dir / "monde" / "oni-monde.json").read_text(encoding="utf-8"))
    return {int(t[:4]): v for t, v in zip(ind["series"]["time"], ind["series"]["value"]) if v is not None}


# ---------------------------------------------------------------- jeu complet


def dataset_result(key: str, iid: str, label: str, temp: dict[int, float], best: Inputs, p05: Inputs, p95: Inputs,
                   oni: Inputs) -> tuple[RegressionDataset, dict]:
    run = regress(temp, best)
    fit = run.fit
    years = run.years
    ols = R.ols_newey_west(run.T, run.X, NAMES)
    b = {n: fit.get(n)[0] for n in fit.names}

    # Décomposition : forçages relatifs à 1850-1900, ENSO tel quel.
    base = range(BASELINE[0], BASELINE[1] + 1)
    ref = {n: window_mean(f, base) for n, f in (("anthropique", run.A), ("volcans", run.V), ("soleil", run.S))}
    ca = b["anthropique"] * (run.X[:, 0] - ref["anthropique"])
    cv = b["volcans"] * (run.X[:, 1] - ref["volcans"])
    cs = b["soleil"] * (run.X[:, 2] - ref["soleil"])
    ce = b["enso"] * run.X[:, 3]
    level = b["constante"] + sum(b[n] * ref[n] for n in ("anthropique", "volcans", "soleil"))
    rebased = run.T - level
    adjusted = run.T - (ce - ce.mean()) - (cv - cv.mean()) - (cs - cs.mean())
    assert np.allclose(rebased, ca + cv + cs + ce + fit.resid), "décomposition incohérente"

    attributions = []
    for window, ref_a, ref_n in WINDOWS:
        a, a_lo, a_hi = run.attributable(window)
        n_, n_lo, n_hi = run.natural(window)
        w, bl = range(window[0], window[1] + 1), base
        observed = None
        if all(y in temp for y in w) and all(y in temp for y in bl):
            observed = float(np.mean([temp[y] for y in w]) - np.mean([temp[y] for y in bl]))
        attributions.append(Attribution(window=Period(start=window[0], end=window[1]),
                                        baseline=Period(start=BASELINE[0], end=BASELINE[1]),
                                        anthropogenic=est(a, a_lo, a_hi), natural=est(n_, n_lo, n_hi), observed=observed,
                                        reference_anthropogenic=est(*ref_a), reference_natural=est(*ref_n),
                                        reference_source=REFERENCE_SOURCE))

    ba, ba_lo, ba_hi = fit.combination({"anthropique": 1.0})
    tcr = est(ba * F2X, ba_lo * F2X, ba_hi * F2X)

    yr = [y for y in years if y >= TREND_START]
    idx = [years.index(y) for y in yr]
    t_obs = annual_trend(yr, [float(run.T[i]) for i in idx], label=f"{TREND_START}-{yr[-1]}, observée")
    t_adj = annual_trend(yr, [float(adjusted[i]) for i in idx], label=f"{TREND_START}-{yr[-1]}, ajustée")
    resid_p = annual_trend(years, [float(x) for x in fit.resid], label="résidus").p_value
    slope_obs, slope_adj = sen_decade(yr, [run.T[i] for i in idx]), sen_decade(yr, [adjusted[i] for i in idx])

    # O8 — robustesse
    rob: list[RobustnessCase] = []

    def case(group: str, lab: str, r: Run, extra_ok: bool = True) -> RobustnessCase:
        a = r.attributable(CONTROL)[0]
        v, lo, hi = r.fit.combination({"anthropique": 1.0})
        return RobustnessCase(group=group, label=lab, period=Period(start=r.years[0], end=r.years[-1]),
                              beta_anthro=est(v, lo, hi), attributable=float(a), tcr=float(v * F2X),
                              rho=float(r.fit.rho), r2=float(r.fit.r2),
                              in_range=in_range(a, WINDOWS[1][1][1:]) and extra_ok)

    for le in ENSO_LAGS:
        for lv in VOLC_LAGS:
            rob.append(case("decalages", f"ENSO {le} mois, volcans {lv} mois", regress(temp, best, le, lv)))
    for level, inp in (("5 %", p05), ("95 %", p95)):
        rob.append(case("forcage", f"Forçage anthropique à {level}", regress(temp, inp)))
    sub = regress(temp, oni, start=SUB_START)
    _, s_lo, s_hi = sub.fit.combination({"anthropique": 1.0})
    overlap = s_lo <= ba_hi and ba_lo <= s_hi
    rob.append(case("sous-periode", f"{SUB_START}-{sub.years[-1]}, ENSO = ONI (ERSSTv5)"
                    + ("" if overlap else " — βₐ ne recoupe pas la période complète"), sub, overlap))

    ds = RegressionDataset(
        id=key, indicator_id=iid, label=label, period=Period(start=years[0], end=years[-1]), n=len(years),
        method=fit.method, rho=float(fit.rho), r2=float(fit.r2),
        residual_sd=float(np.std(fit.resid, ddof=len(fit.coef))),
        coefficients=coefficients(fit), coefficients_ols=coefficients(ols),
        vif={n: float(v) for n, v in zip(NAMES, R.vif(run.X))},
        tcr=tcr, attributions=attributions, trend_observed=t_obs, trend_adjusted=t_adj,
        slope_observed=slope_obs, slope_adjusted=slope_adj,
        residual_trend_p=resid_p, robustness=rob,
        series=RegressionSeries(years=years, observed=_r(run.T), fitted=_r(fit.fitted), adjusted=_r(adjusted),
                                anthropogenic=_r(ca), volcanic=_r(cv), solar=_r(cs), enso=_r(ce),
                                observed_rebased=_r(rebased)))
    p = dict(zip(fit.names, fit.p_values()))
    checks = {
        "O3": (b["anthropique"] > 0 and p["anthropique"] < ALPHA,
               f"βₐ = {_f(b['anthropique'], 3)} °C par W/m², p {_p(p['anthropique'])}"),
        "O4": (all(in_range(at.anthropogenic.value, (at.reference_anthropogenic.ci_low, at.reference_anthropogenic.ci_high))
                   for at in attributions),
               " ; ".join(f"{at.window.start}-{at.window.end} : {_f(at.anthropogenic.value, 2)} °C "
                          f"[{_f(at.anthropogenic.ci_low, 2)} ; {_f(at.anthropogenic.ci_high, 2)}], référence "
                          f"[{_f(at.reference_anthropogenic.ci_low, 1)} ; {_f(at.reference_anthropogenic.ci_high, 1)}]"
                          for at in attributions)),
        "O5": (all(in_range(at.natural.value, NATURAL_RANGE) for at in attributions),
               " ; ".join(f"{at.window.start}-{at.window.end} : {_f(at.natural.value, 3, True)} °C" for at in attributions)),
        "O6": (in_range(tcr.value, TCR_RANGE) and b["enso"] > 0 and p["enso"] < ALPHA and b["volcans"] > 0
               and p["volcans"] < ALPHA,
               f"réponse transitoire {_f(tcr.value, 2)} °C ; βₑ = {_f(b['enso'], 3)} (p {_p(p['enso'])}) ; "
               f"βᵥ = {_f(b['volcans'], 3)} (p {_p(p['volcans'])}) ; βₛ = {_f(b['soleil'], 3)} (p {_p(p['soleil'])}, "
               "sans exigence)"),
        "O7": (resid_p >= ALPHA, f"tendance des résidus : p {_p(resid_p)} (Hamed-Rao) ; ρ = {_f(fit.rho, 2)}"),
        "O8": (all(c.in_range for c in rob),
               f"réchauffement attribué {CONTROL[0]}-{CONTROL[1]} de {_f(min(c.attributable for c in rob), 2)} à "
               f"{_f(max(c.attributable for c in rob), 2)} °C sur {len(rob)} variantes"
               + ("" if all(c.in_range for c in rob) else " ; hors fourchette : "
                  + ", ".join(c.label for c in rob if not c.in_range))),
    }
    return ds, checks


def sen_decade(years: list[int], values) -> Estimate:
    """Pente de Sen et son intervalle à 95 % (scipy, comme etl/stats/trend.py), en °C/décennie, sans arrondi."""
    from scipy import stats
    slope, _, lo, hi = stats.theilslopes(np.asarray(values, float), np.asarray(years, float), alpha=1 - ALPHA)
    # round(…, 12) : retire le bruit flottant du ×10 (0,2025 et non 0,20249999…), sans arrondi d'affichage.
    return est(round(slope * 10, 12), round(lo * 10, 12), round(hi * 10, 12))


def _r(a) -> list[float]:
    return [round(float(x), 4) + 0.0 for x in a]


def _f(x: float, nd: int, sign: bool = False) -> str:
    """Arrondi au plus proche, moitié vers l'extérieur, sur l'écriture décimale la plus courte du nombre : la même
    règle que l'affichage du site (Intl.NumberFormat), pour qu'un chiffre cité dans le texte et dans un tableau soit
    identique."""
    from decimal import ROUND_HALF_UP, Decimal
    q = Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    if q == 0:
        q = abs(q)
    s = f"{q:+f}" if sign else f"{q:f}"
    return s.replace("-", "−").replace(".", ",")


def _p(p: float) -> str:
    return "< 0,001" if p < 0.001 else "= " + _f(p, 3)


# ---------------------------------------------------------------- assemblage


PLANNED = (
    ("modele-energetique", "p10.5", "Modèle énergétique et projections",
     "Un modèle simple, validé sur le passé, que prévoit-il selon les scénarios d'émissions ?"),
)


def build(out_dir: Path = PROCESSED_DIR, raw_dir: Path = RAW_DIR) -> Demonstration:
    ctx = make_context(raw_dir)
    erf = I.load_erf(raw_dir, "best")
    erf05, erf95 = I.load_erf(raw_dir, "p05"), I.load_erf(raw_dir, "p95")
    nino = I.load_nino(raw_dir)
    oni_m = I.load_oni_monthly(raw_dir)
    enso = enso_index(nino)

    # O2 — contrôles des entrées
    worst = max(abs(r["anthro"] + r["volcanic"] + r["solar"] - r["total"]) for r in erf.values())
    oni = oni_annual(out_dir)
    common = [y for y in sorted(oni) if y >= SUB_START and lagged_mean(enso, y, 0) is not None]
    r_oni = float(np.corrcoef([lagged_mean(enso, y, 0) for y in common], [oni[y] for y in common])[0, 1])

    anth = {y: r["anthro"] for y, r in erf.items()}
    best = Inputs(erf, anth, enso)
    p05 = Inputs(erf, {y: r["anthro"] for y, r in erf05.items()}, enso)
    p95 = Inputs(erf, {y: r["anthro"] for y, r in erf95.items()}, enso)
    oni_inp = Inputs(erf, anth, oni_m)

    temps = load_temperatures(out_dir)
    datasets, checks = [], []
    for key, iid, label in DATASETS:
        ds, ck = dataset_result(key, iid, label, temps[iid], best, p05, p95, oni_inp)
        datasets.append(ds)
        checks.append((label, ck))
        enso_gaps = [y for y in range(ds.period.start, ds.period.end + 1) if lagged_mean(enso, y, LAG_ENSO) is None]
        if enso_gaps:
            raise ValueError(f"{label} : mois ENSO manquants pour {enso_gaps}")

    o2_ok = worst <= 0.01 and r_oni >= ONI_MIN_R
    criteria = [
        Criterion(id="O1", label="Exhaustivité", satisfied=len(datasets) == len(DATASETS),
                  detail=f"{len(datasets)} jeux sur {len(DATASETS)} : " + ", ".join(
                      f"{d.label} {d.period.start}-{d.period.end}" for d in datasets)),
        Criterion(id="O2", label="Données d'entrée", satisfied=o2_ok,
                  detail=f"écart maximal anthropique + volcanique + solaire − total : {_f(worst, 4)} W/m² (seuil 0,01) ; "
                         f"aucun mois ENSO manquant sur les périodes ; corrélation indice ENSO / ONI "
                         f"{common[0]}-{common[-1]} : r = {_f(r_oni, 3)} (seuil {_f(ONI_MIN_R, 2)})"),
    ]
    titles = {"O3": "Détection", "O4": "Attribution", "O5": "Part naturelle", "O6": "Plausibilité physique",
              "O7": "Résidus", "O8": "Robustesse"}
    for cid, title in titles.items():
        ok = all(ck[cid][0] for _, ck in checks)
        criteria.append(Criterion(id=cid, label=title, satisfied=ok,
                                  detail=" | ".join(f"{lab} {'✓' if ck[cid][0] else '✗'} {ck[cid][1]}" for lab, ck in checks)))

    ok = {c.id: c.satisfied for c in criteria}
    if all(ok[f"O{i}"] for i in range(2, 9)):
        confidence, reason = "elevee", ("Critères O2 à O8 conformes pour les trois jeux (règle D-AG). L'accord avec "
                                        "l'IGCC vaut recoupement par une autre méthode, pas preuve indépendante : "
                                        "les forçages sont communs.")
    elif ok["O3"]:
        failed = [c for c in criteria if not c.satisfied]
        parts = []
        for c in failed:
            if c.id == "O8":
                out = [f"{d.label} « {r.label} » {_f(r.attributable, 2)} °C" for d in datasets for r in d.robustness
                       if not r.in_range]
                parts.append(f"O8 (robustesse) : réchauffement attribué hors de [{_f(WINDOWS[1][1][1], 1)} ; "
                             f"{_f(WINDOWS[1][1][2], 1)}] °C pour " + ", ".join(out))
            else:
                parts.append(f"{c.id} ({c.label.lower()})")
        confidence, reason = "moyenne", ("Détection établie (O3), mais critère non conforme, d'où la confiance « moyenne » "
                                         "(règle D-AG) : " + " ; ".join(parts) + ". Analyse de l'écart : "
                                         "docs/validation-p10.md.")
    else:
        confidence, reason = "non_etabli", "Le forçage anthropique n'est pas détecté (O3) sur les trois jeux."

    main = datasets[0]
    att = {a.window.start: a for a in main.attributions}
    a16 = att[2016]
    coef = {c.name: c for c in main.coefficients}
    so, sa = main.slope_observed, main.slope_adjusted
    narrower = (sa.ci_high - sa.ci_low) < (so.ci_high - so.ci_low)
    same = all(ck["O3"][0] and ck["O4"][0] for _, ck in checks)
    y0, y1 = main.trend_observed.period.start, main.trend_observed.period.end
    finding = (
        f"Sur {main.period.start}-{main.period.end} ({main.label}), le forçage anthropique est détecté "
        f"(p {_p(coef['anthropique'].p_value)}). Le modèle lui attribue un réchauffement de "
        f"{_f(a16.anthropogenic.value, 2)} °C [{_f(a16.anthropogenic.ci_low, 2)} ; {_f(a16.anthropogenic.ci_high, 2)}] "
        f"entre 1850-1900 et 2016-2025 (intervalle statistique seul, hors incertitude des forçages), pour "
        f"{_f(a16.reference_anthropogenic.value, 2)} °C [{_f(a16.reference_anthropogenic.ci_low, 1)} ; "
        f"{_f(a16.reference_anthropogenic.ci_high, 1)}] selon l'IGCC 2025 ; les volcans et le soleil comptent pour "
        f"{_f(a16.natural.value, 2, True)} °C. Une fois ENSO, volcans et soleil retirés, la pente {y0}-{y1} passe de "
        f"{_f(so.value, 3)} [{_f(so.ci_low, 3)} ; {_f(so.ci_high, 3)}] à {_f(sa.value, 3)} [{_f(sa.ci_low, 3)} ; "
        f"{_f(sa.ci_high, 3)}] °C par décennie"
        + (" : le réchauffement de fond est du même ordre, avec un intervalle plus étroit. " if narrower else ". ")
        + ("Les trois jeux de températures concluent de même (détection et attribution)." if same
           else "Les trois jeux de températures ne concluent pas de même : voir les critères.")
    )

    reg = Regression(
        question="Une fois retirés El Niño, les volcans et le soleil, que reste-t-il du réchauffement mondial, "
                 "et le forçage d'origine humaine l'explique-t-il ?",
        model="T = c + βₐ·A + βᵥ·V + βₛ·S + βₑ·E + ε, erreurs ε autorégressives d'ordre 1",
        finding=finding, confidence=confidence, confidence_reason=reason,
        method_note=(
            "Régression multiple annuelle, moindres carrés généralisés à erreurs AR(1) (Prais-Winsten itéré), "
            "intervalles à 95 % sur une loi de Student à n − k − 1 degrés de liberté (k = 5 coefficients, constante "
            "comprise ; un degré de plus pour ρ). A : forçage radiatif effectif "
            "anthropique total ; V : forçage volcanique décalé de 6 mois ; S : forçage solaire (IGCC 2025, W/m²). "
            "E : Niño 3.4 de HadISST1.1 moins sa climatologie mobile de 30 ans, mois par mois, moyenné d'octobre à "
            "septembre (décalage de 3 mois). Décalages repris de Foster et Rahmstorf (2011), fixés avant calcul. "
            "Réchauffement attribué = βₐ × écart du forçage anthropique moyen entre la fenêtre et 1850-1900 ; "
            "réponse transitoire implicite = βₐ × 3,93 W/m² (doublement du CO₂, GIEC AR6). Température ajustée : "
            "observée moins les contributions ENSO, volcanique et solaire, centrées sur la période. Les pentes de la "
            "température observée et ajustée sont des pentes de Sen, testées par Hamed-Rao comme partout sur le site ; "
            "leur intervalle (scipy) n'est pas corrigé de l'autocorrélation, et l'incertitude des contributions "
            "retirées n'est pas propagée à la température ajustée."),
        limitations=[
            "Régression statistique, pas modèle physique : l'inertie de l'océan est absorbée dans les coefficients. "
            "La réponse à un forçage bref (volcan) étant amortie, βᵥ est plus petit que βₐ ; c'est attendu.",
            "L'IGCC calcule son réchauffement attribué avec les mêmes forçages et des températures qui partagent nos "
            "stations : l'accord vaut recoupement par une autre méthode, pas preuve indépendante.",
            "Incertitude des forçages (surtout des aérosols) propagée seulement par les bornes à 5 et 95 % de l'IGCC, "
            "qui ne sont pas des trajectoires cohérentes. Les intervalles des coefficients ne la contiennent pas.",
            "Les erreurs AR(1) ne représentent pas toute la variabilité multidécennale (Atlantique, Pacifique) : sur "
            "données simulées au ρ estimé (environ 0,7), un intervalle nominal de 95 % couvre la vraie valeur dans "
            "environ 92 % des cas.",
            "Avant 1950, le Niño 3.4 de HadISST repose sur peu de mesures ; la climatologie mobile de 30 ans retire "
            "aussi la variabilité de l'ENSO plus lente que 30 ans.",
            "HadCRUT5, GISTEMP et Berkeley partagent l'essentiel de leurs stations : leur accord ne vaut pas trois "
            "preuves (règle S1).",
            f"Forçages figés sur l'édition IGCC 2025 ({I.TAG}) : en changer est une décision consignée, car les "
            "références changent avec elle.",
        ],
        inputs=[
            InputSource(name="Indicators of Global Climate Change 2025 — forçages radiatifs effectifs 1750-2025 "
                             "(meilleure estimation, bornes à 5 et 95 %)", url=I.PAGE,
                        license="CC BY 4.0", note=f"ClimateIndicator/data, étiquette {I.TAG}"),
            InputSource(name="NOAA PSL — Niño 3.4 calculé sur HadISST1.1, anomalies mensuelles depuis 1870",
                        url=I.NINO_PAGE, license=I.NINO.license,
                        note="anomalies 1981-2010 publiées, recentrées ici sur une climatologie mobile de 30 ans"),
            InputSource(name="NOAA CPC — ONI (contrôle O2, sous-période O8 c)",
                        url=G.SOURCES["oni"].page, license="Domaine public (NOAA)"),
            *[InputSource(name=f"{lab} — température mondiale annuelle, telle que publiée sur le site",
                          url=f"https://projet-evolution-climat.vercel.app/monde/{iid}", license="voir la page de l'indicateur")
              for _, iid, lab in DATASETS],
        ],
        enso_oni_correlation=float(r_oni), tcr_reference=est(1.8, *TCR_RANGE), datasets=datasets, criteria=criteria, script=SCRIPT,
        etl_version=ctx.etl_version, extracted_at=ctx.extracted_at,
    )
    analyses = [DemonstrationAnalysis(id="regression-multiple", phase="p10.1",
                                      title="Ce qui reste du réchauffement une fois les facteurs naturels retirés",
                                      question=reg.question, status="publie", regression=reg)]

    # P10.2 — valeurs extrêmes en Gironde (etl/demo_extremes.py)
    from etl import demo_extremes as E
    ext = E.build(E.load_station(E.MAIN, raw_dir), [E.load_station(s, raw_dir) for s in E.OTHERS],
                  E.published(out_dir, E.GISTEMP), E.published(out_dir, E.HADCRUT), ctx.etl_version, ctx.extracted_at)
    analyses.append(DemonstrationAnalysis(id="extremes-gironde", phase="p10.2",
                                          title="Les canicules de Bordeaux, hier et aujourd'hui",
                                          question=ext.question, status="publie", extremes=ext))

    # P10.3 — amplification régionale (etl/demo_amplification.py)
    from etl import demo_amplification as A
    amp = A.load_and_build(out_dir, raw_dir, ctx.etl_version, ctx.extracted_at)
    analyses.append(DemonstrationAnalysis(id="amplification-regionale", phase="p10.3",
                                          title="La France et la Gironde se réchauffent-elles plus vite que le monde ?",
                                          question=amp.question, status="publie", amplification=amp))

    # P10.4 — cohérence physique (etl/demo_coherence.py)
    from etl import demo_coherence as C
    coh = C.load_and_build(out_dir, raw_dir, ctx.etl_version, ctx.extracted_at)
    analyses.append(DemonstrationAnalysis(id="coherence-physique", phase="p10.4",
                                          title="Les mesures indépendantes racontent-elles la même physique ?",
                                          question=coh.question, status="publie", coherence=coh))
    analyses += [DemonstrationAnalysis(id=i, phase=ph, title=t, question=q, status="prevu") for i, ph, t, q in PLANNED]
    return Demonstration(generated_at=datetime.now(timezone.utc).replace(microsecond=0), analyses=analyses)


def main() -> int:
    demo = build()
    OUT.write_text(demo.model_dump_json(indent=1) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    for a in demo.analyses:
        res = a.regression or a.extremes or a.amplification or a.coherence
        if res is None:
            continue
        print(f"  {a.phase} : confiance {res.confidence}")
        for c in res.criteria:
            print(f"    {c.id} {'✓' if c.satisfied else '✗'} {c.label} : {c.detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
