"""P2b — pluies intenses (critères F1-F11, validés par Grég le 26/10/2026 avant tout calcul ; R7 abandonnée).

Indices ETCCDI sur le quotidien Météo-France (non homogénéisé), corrigé par la méthode B′ :
- chaque jour d'un mois COMPLET (tous ses jours présents) est multiplié par LSH homogénéisé ÷ cumul brut du mois ;
  mois à cumul brut nul et LSH nul : facteur 1 ; un seul des deux nul : mois non corrigeable ;
- une année est « homogénéisée » si ses 12 mois sont corrigés ; « brute » si elle est complète au sens ETCCDI
  (au plus 3 jours absents par mois) sans être entièrement corrigeable : affichée, exclue des tendances (F3) ;
- contrôle A : valeurs brutes après la dernière rupture LSH RR du poste, comparées à B′ sur les mêmes années (F7) ;
- F8 : test de Pettitt sur l'écart du poste à la moyenne des autres postes, sur les années antérieures à sa dernière
  rupture (là où la correction agit) ; rupture établie → tendance limitée à la période postérieure ;
- indices de jours rares (médiane 1961-1990 < 5, F9) : écart entre normales, pente non mise en avant.
Aucune référence externe (R7 abandonnée) : confiance au plus « moyenne ».
"""

from __future__ import annotations

import calendar
import statistics
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import extremes as X
from etl.indicators import serie as S
from etl.indicators import temperature as T
from etl.schema import Indicator, Period, Provenance, Series, Station
from etl.sources import meteofrance_lsh as lsh
from etl.sources import meteofrance_quot as quot
from etl.stats.breaks import pettitt
from etl.stats.trend import annual_trend

DEPARTMENT = "33"
MIN_YEARS = 30                     # F1 : en dessous, poste exclu (justifié dans la validation)
COMPOSITE_SPAN = Period(start=1961, end=2017)
MIN_F8_YEARS = 15
MIN_TREND_YEARS = 30               # décision de Grég du 26/10/2026, APRÈS calcul (Lacanau : 13 années consécutives)


@dataclass(frozen=True)
class RainIndex:
    id: str
    title: str
    what: str
    unit: str

    def compute(self, days: list[float | None]) -> float:
        vals = [v for v in days if v is not None]
        if self.id == "r10mm":
            return float(sum(v >= 10.0 for v in vals))
        if self.id == "r20mm":
            return float(sum(v >= 20.0 for v in vals))
        if self.id == "rx1day":
            return round(max(vals), 1)
        # rx5day : fenêtres de 5 jours consécutifs, sans jour manquant
        best = 0.0
        for i in range(len(days) - 4):
            w = days[i:i + 5]
            if all(v is not None for v in w):
                best = max(best, sum(w))
        return round(best, 1)


INDICES = {
    "r10mm": RainIndex("r10mm", "Jours de pluie ≥ 10 mm", "jours de pluie d'au moins 10 mm", "jours"),
    "r20mm": RainIndex("r20mm", "Jours de pluie ≥ 20 mm", "jours de pluie d'au moins 20 mm", "jours"),
    "rx1day": RainIndex("rx1day", "Pluie maximale en un jour", "la pluie maximale tombée en un jour", "mm"),
    "rx5day": RainIndex("rx5day", "Pluie maximale en cinq jours", "la pluie maximale tombée en cinq jours consécutifs", "mm"),
}
COUNT_INDICES = ("r10mm", "r20mm")


def days_of(y: int, m: int) -> list[str]:
    return [f"{y}-{m:02d}-{d:02d}" for d in range(1, calendar.monthrange(y, m)[1] + 1)]


def year_days(y: int) -> list[str]:
    return [d for m in range(1, 13) for d in days_of(y, m)]


@dataclass
class RainDaily:
    station: Station
    raw: dict[str, float]
    corrected: dict[str, float]
    status: dict[int, str]                      # "homogenized" | "raw" ; années incomplètes absentes
    factors: dict[tuple[int, int], float] = field(default_factory=dict)
    lsh_month: dict[tuple[int, int], float] = field(default_factory=dict)
    last_break_regime: int | None = None

    def index(self, idx: RainIndex, raw: bool = False) -> dict[int, float]:
        out = {}
        for y, st in self.status.items():
            src = self.raw if raw or st == "raw" else self.corrected
            out[y] = idx.compute([src.get(d) for d in year_days(y)])
        return out

    def hom(self) -> set[int]:
        return {y for y, s in self.status.items() if s == "homogenized"}


def correct(raw: dict[str, float], lsh_values: dict, lsh_hom: dict) -> tuple[dict[str, float], dict[int, str], dict]:
    """Méthode B′. Renvoie les jours corrigés, le statut des années et les facteurs mensuels."""
    corrected, status, factors = {}, {}, {}
    for y in sorted({int(d[:4]) for d in raw}):
        etccdi = all(sum(d in raw for d in days_of(y, m)) >= len(days_of(y, m)) - X.MAX_MISSING_DAYS for m in range(1, 13))
        if not etccdi:
            continue
        all_ok = True
        for m in range(1, 13):
            ds = days_of(y, m)
            target = lsh_values.get((y, m))
            if not (lsh_hom.get((y, m)) and target is not None and all(d in raw for d in ds)):
                all_ok = False
                continue
            total = sum(raw[d] for d in ds)
            if total > 0 and target > 0:
                f = target / total
            elif total == 0 and target == 0:
                f = 1.0
            else:
                all_ok = False
                continue
            factors[(y, m)] = f
            for d in ds:
                corrected[d] = raw[d] * f
        status[y] = "homogenized" if all_ok else "raw"
    return corrected, status, factors


@lru_cache(maxsize=2)
def _lsh(raw_dir: str) -> dict[str, lsh.LshSeries]:
    return {s.station.id: s for s in lsh.load_department("RR", DEPARTMENT, Path(raw_dir), download=not T._offline())}


@lru_cache(maxsize=2)
def _daily(raw_dir: str) -> dict[str, dict[str, quot.Daily]]:
    postes = set(_lsh(raw_dir))
    return {p: v["RR"] for p, v in quot.load(DEPARTMENT, postes, ("RR",), Path(raw_dir)).items()}


def station_name(st: Station) -> tuple[str, str]:
    cfg = T.station_config().get(st.id, {})
    name = cfg.get("name") or st.name.title()
    return name, cfg.get("slug") or S.slugify(name)


@lru_cache(maxsize=16)
def rain_daily(poste: str, raw_dir: str) -> RainDaily:
    s = _lsh(raw_dir)[poste]
    raw = {d: x.value for d, x in _daily(raw_dir).get(poste, {}).items()}
    corrected, status, factors = correct(raw, s.values, s.homogenized)
    regimes = T.mf_regime_years((s.station,))
    name, _ = station_name(s.station)
    return RainDaily(s.station.model_copy(update={"name": name}), raw, corrected, status, factors,
                     {k: v for k, v in s.values.items() if s.homogenized.get(k)}, max(regimes) if regimes else None)


def eligible(raw_dir: str) -> tuple[list[str], dict[str, str]]:
    """F1 : postes LSH RR ayant au moins MIN_YEARS années corrigées ; les autres, avec leur motif."""
    ok, excluded = [], {}
    for poste in sorted(_lsh(raw_dir)):
        rd = rain_daily(poste, raw_dir)
        n = len(rd.hom())
        if not rd.raw:
            excluded[poste] = "aucune donnée quotidienne de pluie sous ce numéro de poste"
        elif n < MIN_YEARS:
            excluded[poste] = f"{n} années quotidiennes corrigeables seulement (minimum {MIN_YEARS})"
        else:
            ok.append(poste)
    return ok, excluded


# ---------------------------------------------------------------- contrôles


def f8(series: dict[int, float], others: list[dict[int, float]], before: int | None, unit: str) -> dict:
    """Écart du poste à la moyenne des autres postes, avant sa dernière rupture : rupture établie ou non."""
    if before is None:
        return {"status": "sans objet", "detail": "aucune rupture LSH corrigée : la correction ne fait que caler les cumuls"}
    years = sorted(y for y in series if y < before and all(y in o for o in others))
    run = X.longest_run(years)
    if len(run) < MIN_F8_YEARS or not others:
        return {"status": "non évaluable", "detail": f"{len(run)} années comparables avant {before}"}
    diff = [series[y] - sum(o[y] for o in others) / len(others) for y in run]
    res = pettitt(diff)
    if res.p_value >= 0.05:
        return {"status": "conforme", "detail": f"{run[0]}-{run[-1]} : aucune rupture (p = {res.p_value:.2f})"}
    import numpy as np
    from scipy import stats as st
    x = np.asarray(run, dtype=float)
    slope, intercept, *_ = st.theilslopes(diff, x)
    detr = pettitt(list(np.asarray(diff) - (intercept + slope * x)))
    when = run[res.index + 1]
    if detr.p_value >= 0.05:
        return {"status": "conforme", "detail": f"{run[0]}-{run[-1]} : rupture en {when} qui disparaît après retrait de la tendance"}
    return {"status": "rupture", "year": when,
            "detail": f"{run[0]}-{run[-1]} : rupture établie en {when} (écart {res.mean_after - res.mean_before:+.1f} {unit})"}


# ---------------------------------------------------------------- assemblage


def _prov(ctx: BuildContext) -> Provenance:
    return Provenance(source_name=f"{quot.SOURCE_NAME}, corrigées par les {lsh.SOURCE_NAME.split('— ')[-1]}",
                      source_url=quot.DATASET_URL, license=quot.LICENSE, extracted_at=ctx.extracted_at,
                      script="etl.indicators.pluie", etl_version=ctx.etl_version, homogenized=True)


LIMITS = [
    "Pluie quotidienne non homogénéisée, corrigée mois par mois par le rapport entre le cumul homogénéisé LSH et le "
    "cumul brut (méthode B′) : le cumul de chaque mois est rétabli, pas la forme de la distribution des pluies.",
    "Seuls les mois dont tous les jours sont présents sont corrigés ; une année n'est dans la tendance que si ses 12 "
    "mois le sont. Pluie homogénéisée jusqu'en 2017 : les années suivantes sont affichées brutes, hors tendance.",
    "Aucune référence publiée pour les pluies intenses en Gironde (ClimatHD ne publie que le cumul annuel) : confiance "
    "au plus « moyenne ».",
]


def _finding(where: str, idx: RainIndex, main, rare: bool, comp) -> str:
    if idx.id in COUNT_INDICES and rare:
        if comp is not None:
            v = "écart significatif" if comp.significant else "écart non significatif"
            return (f"{where}, les {idx.what} sont rares : {T.fr(comp.first_value, 1, False)} par an sur "
                    f"{comp.first.start}-{comp.first.end}, {T.fr(comp.second_value, 1, False)} sur "
                    f"{comp.second.start}-{comp.second.end} ({v}).")
        return (f"{where}, les {idx.what} sont rares (moins de 5 par an en médiane sur 1961-1990) et la normale "
                "1991-2020 est incomplète (pluie homogénéisée jusqu'en 2017) : aucune évolution n'est établie.")
    if main is None:
        return f"{where}, la série de {idx.what} est trop lacunaire pour une tendance."
    total = main.fitted_end - main.fitted_start
    verdict = ("tendance significative, corrigée de l'autocorrélation" if main.significant
               else "tendance non significative après correction de l'autocorrélation")
    what = f"le nombre annuel de {idx.what}" if idx.unit == "jours" else idx.what
    return (f"{where}, {what} a évolué de {T.fr(main.slope_per_decade)} {idx.unit} par décennie entre "
            f"{main.period.start} et {main.period.end}, soit {T.fr(total)} {idx.unit} sur la période ({verdict}).")


def assemble(ctx: BuildContext, *, ind_id: str, idx: RainIndex, members: list[RainDaily], series: dict[int, float],
             status: dict[int, str], f8_result: dict, place, where: str, title: str, description: str, group: str,
             note: str) -> Indicator:
    years = sorted(series)
    hom = {y for y, s in status.items() if s == "homogenized"}
    trend_years = sorted(hom)
    lims = list(LIMITS)
    if f8_result.get("status") == "rupture":
        trend_years = [y for y in trend_years if y >= f8_result["year"]]
        lims.append(f"Contrôle de la période ancienne (F8) : {f8_result['detail']} ; tendance limitée à la période "
                    "postérieure.")
    run = X.longest_run(trend_years)
    main = (annual_trend(run, [series[y] for y in run], label=f"Série corrigée {run[0]}-{run[-1]}")
            if len(run) >= MIN_TREND_YEARS else None)
    if main is None and run:
        lims.append(f"Plus longue suite d'années corrigées : {len(run)} ans ({run[0]}-{run[-1]}), moins de "
                    f"{MIN_TREND_YEARS} : pas de pente publiée (règle du 26/10/2026, fixée après calcul).")
    # Contrôle A : brut après la dernière rupture (de tous les membres), comparé à B′ sur les mêmes années.
    first = max((m.last_break_regime if m.last_break_regime is not None else min(m.status)) for m in members)
    end = max(hom) if hom else max(years)
    ya = X.longest_run([y for y in range(first, end + 1) if all(m.status.get(y) == "homogenized" for m in members)])
    alts, control_ok = [], False
    if len(ya) >= X.MIN_CONTROL_YEARS:
        raw_i = [m.index(idx, raw=True) for m in members]
        a = annual_trend(ya, [sum(r[y] for r in raw_i) / len(raw_i) for y in ya],
                         label=f"Contrôle A : brut après la dernière rupture, {ya[0]}-{ya[-1]}")
        b = annual_trend(ya, [series[y] for y in ya], label=f"Série corrigée sur la période du contrôle A, {ya[0]}-{ya[-1]}")
        alts, control_ok = [a, b], X.control_agrees(a, b)
    if not control_ok:
        lims.append("Contrôle A (brut après la dernière rupture) non concordant ou trop court (F7).")
    rare = idx.id in COUNT_INDICES and X.is_rare(series, hom)
    comp = X.compare_normals(series, hom) if idx.id in COUNT_INDICES else None
    if rare:
        lims.append("Indice rare (médiane 1961-1990 inférieure à 5 jours par an) : pente non mise en avant (F9).")
    headline = "normals" if rare and comp is not None else "trend"
    if rare:
        conf = "moyenne" if (comp is not None and comp.significant) else "non_etabli"
    elif main is None:
        conf = "non_etabli"
    elif main.significant:
        conf = "moyenne"                      # sans référence externe (R7 abandonnée) : au plus « moyenne »
    elif main.p_value_classical is not None and main.p_value_classical < main.alpha:
        conf = "faible"
    else:
        conf = "non_etabli"
    breaks = S.detect_break(run, series, [m.station for m in members], idx.unit) if main is not None else []
    return Indicator(
        id=ind_id, scale="gironde", group=group, variable=vocab.variable(idx.id), place=place, title=title, unit=idx.unit,
        description=description, frequency="annual", is_anomaly=False, reference_period=None,
        series=Series(time=[str(y) for y in years], value=[round(series[y], 2) for y in years],
                      quality=["homogenized" if status[y] == "homogenized" else "raw" for y in years]),
        normals=X.normals_of(series, hom), trend=main, alt_trends=alts, headline=headline, normals_comparison=comp,
        breakpoints=breaks, stations=[m.station for m in members], method_note=note,
        finding=_finding(where, idx, main, rare, comp), confidence=conf, limitations=lims, provenance=_prov(ctx),
    )


NOTE = ("Indice calculé sur les pluies quotidiennes corrigées : chaque jour d'un mois complet est multiplié par le "
        "rapport entre le cumul mensuel homogénéisé (LSH) et le cumul brut. Contrôle : même calcul sur les valeurs "
        "brutes, après la dernière rupture d'homogénéité connue.")


def _others(poste: str, idx: RainIndex, raw_dir: str) -> list[dict[int, float]]:
    ok, _ = eligible(raw_dir)
    out = []
    for p in ok:
        if p != poste:
            rd = rain_daily(p, raw_dir)
            ser = rd.index(idx)
            out.append({y: v for y, v in ser.items() if y in rd.hom()})
    return out


def build_station(ctx: BuildContext, index: str, poste: str) -> Indicator:
    raw = str(ctx.raw_dir)
    idx = INDICES[index]
    ok, excluded = eligible(raw)
    if poste not in ok:
        raise ValueError(f"poste {poste} exclu (F1) : {excluded.get(poste, 'pas de série LSH RR')}")
    rd = rain_daily(poste, raw)
    series = rd.index(idx)
    hom_series = {y: v for y, v in series.items() if y in rd.hom()}
    res = f8(hom_series, _others(poste, idx, raw), rd.last_break_regime, idx.unit)
    name, slug = station_name(rd.station)
    return assemble(ctx, ind_id=f"{index}-{slug}", idx=idx, members=[rd], series=series, status=rd.status, f8_result=res,
                    place=vocab.station(slug, name), where=f"À {name}", title=f"{idx.title} à {name}",
                    description=f"{idx.title} : {idx.what}, chaque année, à {name} (pluie quotidienne corrigée par la "
                                "série homogénéisée LSH).",
                    group=f"Stations — {idx.title.lower()}", note=NOTE)


def composite_members(raw_dir: str) -> tuple[list[RainDaily], list[str]]:
    ok, _ = eligible(raw_dir)
    members, excluded = [], []
    for p in ok:
        rd = rain_daily(p, raw_dir)
        full = all(rd.status.get(y) == "homogenized" for y in range(COMPOSITE_SPAN.start, COMPOSITE_SPAN.end + 1))
        (members if full else excluded).append(rd if full else rd.station.name)
    return members, excluded


def build_composite(ctx: BuildContext, index: str) -> Indicator:
    raw = str(ctx.raw_dir)
    idx = INDICES[index]
    members, excluded = composite_members(raw)
    if len(members) < 3:
        raise ValueError(f"composite {index} : {len(members)} poste(s) complet(s) sur {COMPOSITE_SPAN.start}-"
                         f"{COMPOSITE_SPAN.end} (exclus : {', '.join(excluded)})")
    per = [m.index(idx) for m in members]
    years = sorted(set.intersection(*(set(p) for p in per)))
    series = {y: sum(p[y] for p in per) / len(per) for y in years}
    status = {y: "homogenized" if all(m.status[y] == "homogenized" for m in members) else "raw" for y in years}
    names = ", ".join(m.station.name for m in members)
    note = (f"Moyenne, poste par poste, de l'indice de {len(members)} postes ({names}) complets et corrigés sur toute la "
            f"période {COMPOSITE_SPAN.start}-{COMPOSITE_SPAN.end} (réseau constant)"
            + (f" ; exclus : {', '.join(excluded)}" if excluded else "") + ". " + NOTE)
    return assemble(ctx, ind_id=f"{index}-gironde", idx=idx, members=members, series=series, status=status,
                    f8_result={"status": "sans objet", "detail": "composite : contrôle F8 porté par chaque poste"},
                    place=vocab.composite("gironde", "Gironde"), where="En Gironde", title=f"{idx.title} en Gironde",
                    description=f"{idx.title} : moyenne de {len(members)} postes longs, pluie quotidienne corrigée par "
                                "les séries homogénéisées LSH.",
                    group="Synthèse Gironde — pluies intenses", note=note)
