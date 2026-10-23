"""Indicateurs d'extrêmes de température en Gironde (phase 2a) : nombres annuels de jours au-delà d'un seuil.

Critères : docs/phases.md, section P2a (fixés le 23/10/2026, avant tout calcul).

Le quotidien Météo-France n'est pas homogénéisé. Deux séries sont construites (décision D-B, méthode C) :

- **B (résultat principal)** : chaque jour reçoit la correction de son mois, égale à l'écart entre la
  valeur mensuelle homogénéisée LSH et la moyenne mensuelle des valeurs quotidiennes brutes. La moyenne
  de chaque mois corrigé reproduit exactement la LSH (contrôle E5) ; la forme de la distribution n'est
  pas corrigée. Une année n'est « homogénéisée » que si ses 12 mois sont corrigés.
- **A (contrôle)** : valeurs brutes, seulement après la dernière rupture d'homogénéité corrigée par
  Météo-France pour cette série (aucune correction nécessaire si aucune rupture n'a eu lieu depuis).

Règles :
- complétude ETCCDI (E2) : un mois est manquant s'il lui manque plus de 3 jours, une année est manquante
  si un de ses mois l'est ; aucune valeur n'est complétée ;
- tendances et normales sur les seules années homogénéisées (E3, règle C2 du schéma) ;
- indice rare (E9) : médiane annuelle 1961-1990 inférieure à 5 jours → chiffre mis en avant = écart
  entre normales 1961-1990 et 1991-2020 (test de Mann-Whitney), confiance au plus « moyenne ».
"""

from __future__ import annotations

import calendar
import statistics
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from scipy import stats

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import temperature as T
from etl.schema import Indicator, Normal, NormalsComparison, Period, Provenance, Series, Station, Trend
from etl.sources import meteofrance_lsh as lsh
from etl.sources import meteofrance_quot as quot
from etl.stats.trend import annual_trend

DEPARTMENT = "33"
NORMALS = [Period(start=1961, end=1990), Period(start=1991, end=2020)]
COMMON_WINDOW = Period(start=1962, end=2022)       # matrice inter-stations, comme C5
CLIMATHD_WINDOW = Period(start=1961, end=2010)     # E4 (R3, R4), fixé le 23/10/2026
COMPOSITE_SPAN = Period(start=1961, end=2022)      # réseau constant du composite
MAX_MISSING_DAYS = 3                               # E2, règle ETCCDI
RARE_MEDIAN = 5                                    # E9 : médiane annuelle 1961-1990, en jours
MIN_CONTROL_YEARS = 10                             # contrôle A : longueur minimale pour une tendance


@dataclass(frozen=True)
class IndexDef:
    id: str
    variable: str          # "TN" ou "TX"
    op: str                # ">=" ou "<="
    threshold: float
    title: str             # « Journées estivales »
    what: str              # « journées estivales (TX ≥ 25 °C) »

    def hit(self, v: float) -> bool:
        if self.op == ">=":
            return v >= self.threshold
        if self.op == ">":
            return v > self.threshold
        if self.op == "<=":
            return v <= self.threshold
        if self.op == "<":
            return v < self.threshold
        raise ValueError(f"opérateur inconnu {self.op}")


INDICES = {
    "jours-tx25": IndexDef("jours-tx25", "TX", ">=", 25.0, "Journées estivales", "journées estivales (TX ≥ 25 °C)"),
    "jours-tx30": IndexDef("jours-tx30", "TX", ">=", 30.0, "Journées chaudes", "journées chaudes (TX ≥ 30 °C)"),
    "jours-tx35": IndexDef("jours-tx35", "TX", ">=", 35.0, "Journées très chaudes", "journées très chaudes (TX ≥ 35 °C)"),
    "nuits-tn20": IndexDef("nuits-tn20", "TN", ">=", 20.0, "Nuits tropicales", "nuits tropicales (TN ≥ 20 °C)"),
    "jours-gel": IndexDef("jours-gel", "TN", "<=", 0.0, "Jours de gel", "jours de gel (TN ≤ 0 °C)"),
}


# ---------------------------------------------------------------- données


@lru_cache(maxsize=4)
def _daily(variable: str, raw_dir: str) -> dict[str, dict[str, quot.Daily]]:
    postes = set(T.station_config())
    data = quot.load(DEPARTMENT, postes, (variable,), Path(raw_dir))
    return {p: v[variable] for p, v in data.items()}


def days_of(year: int, month: int) -> list[str]:
    return [f"{year}-{month:02d}-{d:02d}" for d in range(1, calendar.monthrange(year, month)[1] + 1)]


@dataclass
class StationDaily:
    """Série quotidienne d'une station pour une variable, brute et corrigée (méthode B)."""

    variable: str
    station: Station
    raw: dict[str, float]
    corrected: dict[str, float]
    year_status: dict[int, str]                     # "homogenized" | "raw" ; années incomplètes absentes
    deltas: dict[tuple[int, int], float] = field(default_factory=dict)
    lsh_month: dict[tuple[int, int], float] = field(default_factory=dict)
    last_break_regime: int | None = None            # première année du régime après la dernière rupture MF

    def values(self, year: int) -> list[float]:
        src = self.corrected if self.year_status.get(year) == "homogenized" else self.raw
        return [src[d] for m in range(1, 13) for d in days_of(year, m) if d in src]

    def hom_years(self) -> list[int]:
        return sorted(y for y, s in self.year_status.items() if s == "homogenized")


def station_daily(variable: str, station_id: str, raw_dir: Path, drop_q9: bool = False) -> StationDaily:
    """Construit les séries brute et corrigée. `drop_q9` : valeurs de code qualité 9 traitées comme absentes (E8)."""
    daily = _daily(variable, str(raw_dir)).get(station_id, {})
    raw = {d: x.value for d, x in daily.items() if not (drop_q9 and x.quality == "9")}
    values, hom, stations = T.monthly(variable, station_id, raw_dir)
    station = stations[0]
    years = sorted({int(d[:4]) for d in raw})
    corrected: dict[str, float] = {}
    deltas: dict[tuple[int, int], float] = {}
    status: dict[int, str] = {}
    for y in years:
        months_ok = all(sum(d in raw for d in days_of(y, m)) >= len(days_of(y, m)) - MAX_MISSING_DAYS for m in range(1, 13))
        if not months_ok:
            continue  # E2 : année manquante
        all_corrected = True
        for m in range(1, 13):
            present = [d for d in days_of(y, m) if d in raw]
            if hom.get((y, m)) and (y, m) in values:
                delta = values[(y, m)] - sum(raw[d] for d in present) / len(present)
                deltas[(y, m)] = delta
                for d in present:
                    corrected[d] = raw[d] + delta
            else:
                all_corrected = False
        status[y] = "homogenized" if all_corrected else "raw"
    regimes = T.mf_regime_years((station,))
    return StationDaily(variable, station, raw, corrected, status, deltas,
                        {k: v for k, v in values.items() if hom.get(k)}, max(regimes) if regimes else None)


def counts(sd: StationDaily, idx: IndexDef, use_raw: bool = False) -> dict[int, int]:
    """Nombre annuel de jours remplissant la condition, pour chaque année complète."""
    out = {}
    for y in sd.year_status:
        vals = [sd.raw[d] for m in range(1, 13) for d in days_of(y, m) if d in sd.raw] if use_raw else sd.values(y)
        out[y] = sum(idx.hit(v) for v in vals)
    return out


def stations_for(variable: str, raw_dir: Path) -> list[str]:
    """Postes de Gironde disposant d'une série LSH pour la variable (correction B et dates de ruptures)."""
    return T.stations_with(variable, raw_dir)


# ---------------------------------------------------------------- statistiques


def longest_run(years: list[int]) -> list[int]:
    best: list[int] = []
    cur: list[int] = []
    for y in sorted(years):
        cur = cur + [y] if cur and y == cur[-1] + 1 else [y]
        if len(cur) > len(best):
            best = cur
    return best


def window_trend(years: list[int], series: dict[int, int], window: Period, label: str) -> Trend | None:
    ys = [y for y in years if window.start <= y <= window.end]
    if len(ys) != window.end - window.start + 1:
        return None
    return annual_trend(ys, [series[y] for y in ys], label=label)


def control_a(sd_list: list[StationDaily], idx: IndexDef, end: int, composite: bool) -> tuple[Trend | None, Trend | None]:
    """Contrôle A : tendance brute après la dernière rupture MF, et tendance B sur la même période.

    Pour un composite, la période commence après la dernière rupture de tous les membres.
    """
    if not sd_list or any(not sd.year_status for sd in sd_list):
        return None, None
    # Début : après la dernière rupture MF de chaque série (ou son début s'il n'y en a pas), le plus tardif.
    first = max(sd.last_break_regime if sd.last_break_regime is not None else min(sd.year_status) for sd in sd_list)
    years = [y for y in range(first, end + 1) if all(sd.year_status.get(y) == "homogenized" for sd in sd_list)]
    run = longest_run(years)
    if len(run) < MIN_CONTROL_YEARS:
        return None, None
    raw_counts = [counts(sd, idx, use_raw=True) for sd in sd_list]
    b_counts = [counts(sd, idx) for sd in sd_list]
    a = {y: sum(c[y] for c in raw_counts) / len(raw_counts) for y in run}
    b = {y: sum(c[y] for c in b_counts) / len(b_counts) for y in run}
    lbl = f"{run[0]}-{run[-1]}"
    return (annual_trend(run, [a[y] for y in run], label=f"Contrôle A : brut après la dernière rupture, {lbl}"),
            annual_trend(run, [b[y] for y in run], label=f"Série corrigée sur la période du contrôle A, {lbl}"))


def control_agrees(a: Trend | None, b: Trend | None) -> bool:
    """E7 : même signe et intervalles de confiance qui se recouvrent."""
    if a is None or b is None or None in (a.slope_ci_low, a.slope_ci_high, b.slope_ci_low, b.slope_ci_high):
        return False
    same_sign = (a.slope_per_decade > 0) == (b.slope_per_decade > 0) or (a.slope_per_decade == 0 == b.slope_per_decade)
    overlap = a.slope_ci_low <= b.slope_ci_high and b.slope_ci_low <= a.slope_ci_high
    return same_sign and overlap


def normals_of(series: dict[int, float], hom: set[int]) -> list[Normal]:
    out = []
    for p in NORMALS:
        ys = range(p.start, p.end + 1)
        if all(y in hom for y in ys):
            out.append(Normal(period=p, value=round(sum(series[y] for y in ys) / len(ys), 2)))
    return out


def compare_normals(series: dict[int, float], hom: set[int]) -> NormalsComparison | None:
    a_p, b_p = NORMALS
    a = [series[y] for y in range(a_p.start, a_p.end + 1) if y in hom]
    b = [series[y] for y in range(b_p.start, b_p.end + 1) if y in hom]
    if len(a) != a_p.end - a_p.start + 1 or len(b) != b_p.end - b_p.start + 1:
        return None
    if len(set(a + b)) == 1:
        p = 1.0  # séries constantes (ex. toujours 0) : aucun écart
    else:
        p = round(float(stats.mannwhitneyu(a, b, alternative="two-sided").pvalue), 6)
    ma, mb = round(sum(a) / len(a), 2), round(sum(b) / len(b), 2)
    return NormalsComparison(first=a_p, second=b_p, first_value=ma, second_value=mb, difference=round(mb - ma, 2),
                             p_value=p, significant=p < 0.05, alpha=0.05,
                             method="test de Mann-Whitney bilatéral entre les années des deux normales")


def is_rare(series: dict[int, float], hom: set[int]) -> bool:
    ref = [series[y] for y in range(NORMALS[0].start, NORMALS[0].end + 1) if y in hom]
    return bool(ref) and statistics.median(ref) < RARE_MEDIAN


def confidence(main: Trend | None, rare: bool, comparison: NormalsComparison | None, control_ok: bool, raw_dir: Path) -> str:
    """Règle de confiance P2a : « élevée » si Hamed-Rao significatif, E4 et E7 satisfaits, indice non rare."""
    from etl.validation import p2a  # import tardif : évite le cycle

    if rare:
        if comparison is not None and comparison.significant:
            return "moyenne" if control_ok else "faible"
        return "non_etabli"
    if main is None:
        return "non_etabli"
    if main.significant:
        return "elevee" if (control_ok and p2a.external_validation_passed(raw_dir)) else "moyenne"
    if main.p_value_classical is not None and main.p_value_classical < main.alpha:
        return "faible"
    return "non_etabli"


# ---------------------------------------------------------------- construction


def fr(x: float, digits: int = 1, signed: bool = True) -> str:
    return T.fr(x, digits, signed)


def jours(x: float, digits: int = 1, signed: bool = True) -> str:
    """« +4,5 jours », « 0,1 jour » : singulier en dessous de 2, comme le veut l'usage."""
    return f"{fr(x, digits, signed)} {'jour' if abs(round(x, digits)) < 2 else 'jours'}"


def _finding(where: str, idx: IndexDef, main: Trend | None, rare: bool, comp: NormalsComparison | None) -> str:
    if rare and comp is not None:
        verdict = "écart significatif" if comp.significant else "écart non significatif"
        return (f"{where}, le nombre de {idx.what} est passé de {jours(comp.first_value, 1, False)} par an en moyenne "
                f"sur {comp.first.start}-{comp.first.end} à {jours(comp.second_value, 1, False)} sur "
                f"{comp.second.start}-{comp.second.end} ({verdict}, test de Mann-Whitney). Indice rare : la pente "
                "annuelle n'est pas mise en avant.")
    if main is None:
        return f"{where}, la série de {idx.what} est trop lacunaire pour une tendance."
    if rare:
        # Indice rare sans normales complètes : pas d'écart entre normales publiable, pente non mise en avant.
        return (f"{where}, les {idx.what} sont rares (moins de {RARE_MEDIAN} par an en médiane sur 1961-1990) et une "
                "normale est incomplète : aucune évolution n'est établie.")
    total = main.fitted_end - main.fitted_start
    verdict = ("tendance significative, corrigée de l'autocorrélation" if main.significant
               else "tendance non significative après correction de l'autocorrélation")
    return (f"{where}, le nombre annuel de {idx.what} a évolué de {jours(main.slope_per_decade)} par décennie entre "
            f"{main.period.start} et {main.period.end}, soit {jours(total)} sur la période ({verdict}).")


def _limitations(rare: bool, control_ok: bool, extra: list[str]) -> list[str]:
    from etl.validation import p2a

    out = [
        "Données quotidiennes non homogénéisées, corrigées mois par mois par l'écart entre la série homogénéisée "
        "LSH et la moyenne mensuelle brute (méthode B) : la moyenne de chaque mois est rétablie, pas la forme de la "
        "distribution. Les comptages de jours extrêmes peuvent garder un biais résiduel.",
        "Une année n'est comptée que si aucun de ses mois ne manque plus de 3 jours (règle ETCCDI) ; aucune valeur "
        "n'est complétée. Années non corrigeables (hors période homogénéisée LSH, dont 2023 et après) : affichées "
        "pour information, exclues des tendances et des normales.",
        "Valeurs de code qualité 9 incluses ; l'effet de leur exclusion est contrôlé (critère E8).",
    ]
    if not control_ok:
        out.append("Contrôle A (série brute après la dernière rupture) non concordant ou trop court : confiance au plus "
                   "« moyenne » (critère E7).")
    if not p2a.external_validation_passed():
        out.append("Validation externe (ClimatHD, critère E4) pas encore établie : confiance au plus « moyenne ».")
    if rare:
        out.append(f"Indice rare (médiane 1961-1990 inférieure à {RARE_MEDIAN} jours par an) : la pente annuelle est "
                   "peu informative ; le chiffre mis en avant est l'écart entre normales (critère E9).")
    return out + extra


def _provenance(ctx: BuildContext) -> Provenance:
    return Provenance(
        source_name=f"{quot.SOURCE_NAME}, corrigées par les {lsh.SOURCE_NAME.split('— ')[-1]}",
        source_url=quot.DATASET_URL,
        license=quot.LICENSE,
        extracted_at=ctx.extracted_at,
        script="etl.indicators.extremes",
        etl_version=ctx.etl_version,
        homogenized=True,
    )


def _assemble(ctx: BuildContext, *, ind_id: str, idx: IndexDef, sd_list: list[StationDaily], series: dict[int, float],
              status: dict[int, str], where: str, title: str, description: str, group: str, place, composite: bool,
              method_note: str, extra_limits: list[str]) -> Indicator:
    years = sorted(series)
    hom = {y for y, s in status.items() if s == "homogenized"}
    run = longest_run(sorted(hom))
    main = annual_trend(run, [series[y] for y in run], label=f"Série corrigée {run[0]}-{run[-1]}") if len(run) >= 10 else None
    alts = [t for t in (
        window_trend(run, series, COMMON_WINDOW, f"{COMMON_WINDOW.start}-{COMMON_WINDOW.end}, période commune des stations"),
        window_trend(run, series, CLIMATHD_WINDOW, f"{CLIMATHD_WINDOW.start}-{CLIMATHD_WINDOW.end}, comparaison ClimatHD (E4)"),
    ) if t is not None]
    end = max(run) if run else max(years)
    a_trend, b_on_a = control_a(sd_list, idx, end, composite)
    alts += [t for t in (a_trend, b_on_a) if t is not None]
    control_ok = control_agrees(a_trend, b_on_a)
    rare = is_rare(series, hom)
    comp = compare_normals(series, hom)
    headline = "normals" if rare and comp is not None else "trend"
    annual = T.AnnualSeries(idx.variable, {y: float(series[y]) for y in run}, {y: True for y in run},
                            tuple(sd.station for sd in sd_list))
    breaks = T.detect_break(annual, annual.values, composite, unit="jours") if main is not None else []
    return Indicator(
        id=ind_id,
        scale="gironde",
        group=group,
        variable=vocab.variable(idx.id),
        place=place,
        title=title,
        unit="jours",
        description=description,
        frequency="annual",
        is_anomaly=False,
        reference_period=None,
        series=Series(
            time=[str(y) for y in years],
            value=[round(series[y], 2) for y in years],
            quality=["homogenized" if status[y] == "homogenized" else "raw" for y in years],
        ),
        normals=normals_of(series, hom),
        trend=main,
        alt_trends=alts,
        headline=headline,
        normals_comparison=comp,
        breakpoints=breaks,
        stations=[sd.station for sd in sd_list],
        method_note=method_note,
        finding=_finding(where, idx, main, rare, comp),
        confidence=confidence(main, rare, comp, control_ok, ctx.raw_dir),
        limitations=_limitations(rare, control_ok, extra_limits),
        provenance=_provenance(ctx),
    )


METHOD_NOTE = (
    "Nombre de jours de l'année remplissant la condition, sur les valeurs quotidiennes corrigées : chaque jour "
    "reçoit la correction de son mois (valeur LSH homogénéisée − moyenne mensuelle des valeurs brutes). "
    "Contrôle : même calcul sur les valeurs brutes, après la dernière rupture d'homogénéité connue."
)


def build_station(ctx: BuildContext, index: str, station: str) -> Indicator:
    idx = INDICES[index]
    cfg = next(c for c in T.station_config().values() if c["slug"] == station)
    if cfg["id"] not in stations_for(idx.variable, ctx.raw_dir):
        raise ValueError(f"{cfg['name']} : pas de série LSH {idx.variable}, correction impossible (exclusion E1)")
    sd = station_daily(idx.variable, cfg["id"], ctx.raw_dir)
    c = counts(sd, idx)
    sd.station = sd.station.model_copy(update={"name": cfg["name"]})
    return _assemble(
        ctx, ind_id=f"{index}-{station}", idx=idx, sd_list=[sd], series={y: float(v) for y, v in c.items()},
        status=sd.year_status, where=f"À {cfg['name']}", title=f"{idx.title} à {cfg['name']}",
        description=f"Nombre annuel de {idx.what}, valeurs quotidiennes corrigées par la série homogénéisée LSH. {cfg['note']}",
        group=f"Stations — {idx.title.lower()}", place=vocab.station(station, cfg["name"]), composite=False,
        method_note=METHOD_NOTE, extra_limits=[f"Particularité du site : {cfg['note']}"],
    )


def composite_members(variable: str, raw_dir: Path) -> tuple[list[StationDaily], list[str]]:
    """Réseau constant : stations dont toutes les années de COMPOSITE_SPAN sont complètes et corrigées."""
    members, excluded = [], []
    for sid in stations_for(variable, raw_dir):
        sd = station_daily(variable, sid, raw_dir)
        ok = all(sd.year_status.get(y) == "homogenized" for y in range(COMPOSITE_SPAN.start, COMPOSITE_SPAN.end + 1))
        (members if ok else excluded).append(sd if ok else sid)
    return members, excluded


def build_composite(ctx: BuildContext, index: str) -> Indicator:
    idx = INDICES[index]
    members, excluded = composite_members(idx.variable, ctx.raw_dir)
    if len(members) < 3:
        raise ValueError(f"composite {index} : seulement {len(members)} station(s) à réseau constant {COMPOSITE_SPAN.start}-"
                         f"{COMPOSITE_SPAN.end}")
    names = T.station_config()
    per = [counts(sd, idx) for sd in members]
    years = sorted(set.intersection(*(set(c) for c in per)))
    series = {y: sum(c[y] for c in per) / len(per) for y in years}
    status = {y: "homogenized" if all(sd.year_status[y] == "homogenized" for sd in members) else "raw" for y in years}
    for sd in members:
        sd.station = sd.station.model_copy(update={"name": names[sd.station.id]["name"]})
    member_names = ", ".join(names[sd.station.id]["name"] for sd in members)
    note = (f"Moyenne, station par station, du nombre annuel de jours de {len(members)} stations ({member_names}). "
            f"Réseau constant : seules les stations complètes et corrigées sur toute la période {COMPOSITE_SPAN.start}-"
            f"{COMPOSITE_SPAN.end} sont retenues")
    if excluded:
        note += f" (exclues : {', '.join(names[s]['name'] for s in excluded)})"
    note += ". " + METHOD_NOTE
    return _assemble(
        ctx, ind_id=f"{index}-gironde", idx=idx, sd_list=members, series=series, status=status, where="En Gironde",
        title=f"{idx.title} en Gironde", group="Synthèse Gironde — extrêmes",
        description=f"Nombre annuel moyen de {idx.what} sur {len(members)} stations longues, valeurs quotidiennes "
                    "corrigées par les séries homogénéisées LSH.",
        place=vocab.composite("gironde", "Gironde"), composite=True, method_note=note,
        extra_limits=["Composite non pondéré par la surface : les stations littorales y pèsent autant que les stations "
                      "intérieures, alors que leurs nombres de jours diffèrent beaucoup."],
    )
