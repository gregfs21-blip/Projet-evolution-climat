"""Indicateurs de température annuelle en Gironde (phase 1), à partir des séries LSH.

Chaîne pour chaque série :
    mensuel LSH → moyenne annuelle (12 mois exigés) → anomalie / 1961-1990
    → normales 1961-1990 et 1991-2020 → tendances (Sen + Hamed-Rao) → rupture (Pettitt)

Règles :
- une année n'est calculée que si ses 12 mois existent ; aucune valeur n'est complétée ;
- une année n'est « homogénéisée » que si ses 12 mois le sont (Q_HOM = 1) ;
- tendances, normales et ruptures ne portent que sur les années homogénéisées (critère C2) ;
- TM = (TN + TX) / 2, calculée au pas mensuel.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml
from scipy import stats

from etl.context import ROOT, BuildContext
from etl.schema import Breakpoint, Indicator, Normal, Period, Provenance, Series, Station, Trend
from etl import vocabulary as vocab
from etl.sources import meteofrance_lsh as lsh
from etl.stats.breaks import pettitt
from etl.stats.trend import annual_trend

DEPARTMENT = "33"
REFERENCE = Period(start=1961, end=1990)
NORMALS = [Period(start=1961, end=1990), Period(start=1991, end=2020)]
CLIMATHD_WINDOW = Period(start=1959, end=2009)   # référence R1
COMMON_WINDOW = Period(start=1962, end=2022)     # critère C5
COMPOSITE_SPAN = Period(start=1953, end=2022)    # réseau constant du composite
MIN_REFERENCE_YEARS = 25

VARIABLES = {
    "TN": ("température minimale", "minimales"),
    "TX": ("température maximale", "maximales"),
    "TM": ("température moyenne", "moyennes"),
}

# ---------------------------------------------------------------- données


@dataclass(frozen=True)
class AnnualSeries:
    """Série annuelle d'une station ou d'un composite : année → (valeur °C, homogénéisée ?)."""

    variable: str
    values: dict[int, float]
    homogenized: dict[int, bool]
    stations: tuple[Station, ...]

    def hom_years(self) -> list[int]:
        return sorted(y for y, h in self.homogenized.items() if h)


def _offline() -> bool:
    return os.environ.get("LSH_OFFLINE") == "1"


@lru_cache(maxsize=4)
def _department(variable: str, raw_dir: str) -> tuple[lsh.LshSeries, ...]:
    return tuple(lsh.load_department(variable, DEPARTMENT, Path(raw_dir), download=not _offline()))


def monthly(variable: str, station_id: str, raw_dir: Path) -> tuple[dict, dict, tuple[Station, ...]]:
    """Valeurs mensuelles (année, mois) → °C et statut homogénéisé, pour TN, TX ou TM."""
    def one(var: str) -> lsh.LshSeries:
        for s in _department(var, str(raw_dir)):
            if s.station.id == station_id:
                return s
        raise KeyError(f"pas de série LSH {var} pour le poste {station_id}")

    def named(st: Station) -> Station:
        cfg = station_config().get(st.id)
        return st.model_copy(update={"name": cfg["name"]}) if cfg else st

    if variable in ("TN", "TX"):
        s = one(variable)
        return s.values, s.homogenized, (named(s.station),)
    tn, tx = one("TN"), one("TX")
    keys = tn.values.keys() & tx.values.keys()
    values = {k: (tn.values[k] + tx.values[k]) / 2 for k in keys}
    hom = {k: tn.homogenized[k] and tx.homogenized[k] for k in keys}
    return values, hom, (named(tn.station), named(tx.station))


def to_annual(values: dict, hom: dict) -> tuple[dict[int, float], dict[int, bool]]:
    years = sorted({y for y, _ in values})
    out_v, out_h = {}, {}
    for y in years:
        months = [(y, m) for m in range(1, 13)]
        if all(k in values for k in months):
            out_v[y] = sum(values[k] for k in months) / 12
            out_h[y] = all(hom[k] for k in months)
    return out_v, out_h


def station_annual(variable: str, station_id: str, raw_dir: Path) -> AnnualSeries:
    values, hom, stations = monthly(variable, station_id, raw_dir)
    v, h = to_annual(values, hom)
    return AnnualSeries(variable, v, h, stations)


def stations_with(variable: str, raw_dir: Path) -> list[str]:
    """Postes disposant de la variable (TM : postes disposant à la fois de TN et TX)."""
    if variable == "TM":
        tn = {s.station.id for s in _department("TN", str(raw_dir))}
        tx = {s.station.id for s in _department("TX", str(raw_dir))}
        return sorted(tn & tx)
    return [s.station.id for s in _department(variable, str(raw_dir))]


def mean_over(series: AnnualSeries, period: Period) -> float | None:
    """Moyenne sur une période, seulement si toutes ses années existent et sont homogénéisées."""
    years = range(period.start, period.end + 1)
    if not all(series.homogenized.get(y) for y in years):
        return None
    return sum(series.values[y] for y in years) / len(years)


def composite_members(variable: str, raw_dir: Path) -> tuple[list[str], list[str]]:
    """Membres du composite : postes homogénéisés sur toute la période COMPOSITE_SPAN (réseau constant)."""
    members, excluded = [], []
    for sid in stations_with(variable, raw_dir):
        s = station_annual(variable, sid, raw_dir)
        ok = all(s.homogenized.get(y) for y in range(COMPOSITE_SPAN.start, COMPOSITE_SPAN.end + 1))
        (members if ok else excluded).append(sid)
    return members, excluded


def composite_anomaly(variable: str, raw_dir: Path) -> tuple[AnnualSeries, list[str], list[str]]:
    """Moyenne des anomalies des stations membres (chacune relative à sa propre normale 1961-1990)."""
    members, excluded = composite_members(variable, raw_dir)
    if len(members) < 3:
        raise ValueError(f"composite {variable} : seulement {len(members)} station(s) à réseau constant")
    per = [station_annual(variable, sid, raw_dir) for sid in members]
    refs = [mean_over(s, REFERENCE) for s in per]
    years = sorted(set.intersection(*(set(s.values) for s in per)))
    values = {y: sum(s.values[y] - r for s, r in zip(per, refs)) / len(per) for y in years}
    hom = {y: all(s.homogenized[y] for s in per) for y in years}
    stations = tuple(st for s in per for st in s.stations)
    return AnnualSeries(variable, values, hom, stations), members, excluded


# ---------------------------------------------------------------- statistiques


def trends(series: AnnualSeries, anomalies: dict[int, float]) -> tuple[Trend, list[Trend]]:
    hom = series.hom_years()
    main = annual_trend(hom, [anomalies[y] for y in hom], label=f"Période homogénéisée {hom[0]}-{hom[-1]}")
    alts = []
    for window, label in [(CLIMATHD_WINDOW, "comparaison ClimatHD (R1)"), (COMMON_WINDOW, "période commune des stations (C5)")]:
        ys = [y for y in hom if window.start <= y <= window.end]
        if ys and ys[0] == window.start and ys[-1] == window.end and len(ys) == window.end - window.start + 1:
            alts.append(annual_trend(ys, [anomalies[y] for y in ys], label=f"{window.start}-{window.end}, {label}"))
    return main, alts


def mf_regime_years(stations: tuple[Station, ...]) -> list[int]:
    """Première année du nouveau régime pour chaque rupture d'homogénéité corrigée par Météo-France."""
    out = []
    for st in stations:
        for b in st.homogenization_breaks:
            year, month = int(b[:4]), int(b[5:7])
            out.append(year + 1 if month == 12 else year)
    return out


def detect_break(series: AnnualSeries, anomalies: dict[int, float], composite: bool, unit: str = "°C") -> list[Breakpoint]:
    hom = series.hom_years()
    res = pettitt([anomalies[y] for y in hom])
    if res.p_value >= 0.05:
        return []
    new_regime = hom[res.index + 1]
    mf = mf_regime_years(series.stations)
    near = [y for y in mf if abs(y - new_regime) <= 1]
    if composite:
        # Une rupture d'une seule station pèse 1/n dans le composite : on ne marque l'artefact
        # que si la majorité des stations membres ont une rupture corrigée à ±1 an.
        n_members = len({st.id for st in series.stations})
        hits = len({st.id for st in series.stations if any(abs(y - new_regime) <= 1 for y in mf_regime_years((st,)))})
        artifact = hits > n_members / 2
    else:
        artifact = bool(near)
    # Le test de Pettitt réagit aussi à une tendance régulière : on le refait sur les résidus
    # après retrait de la droite de Sen. Si la rupture disparaît, elle n'est que la tendance.
    x = np.asarray(hom, dtype=float)
    y = np.asarray([anomalies[k] for k in hom])
    slope, intercept, *_ = stats.theilslopes(y, x)
    detr = pettitt(y - (intercept + slope * x))
    shift = res.mean_after - res.mean_before
    note = f"écart des moyennes {fr(shift)} {unit} avant/après {new_regime}"
    if detr.p_value >= 0.05:
        note += (f" ; après retrait de la tendance, plus aucune rupture significative (p = {fr(detr.p_value, 2, False)}) : "
                 "la rupture traduit la tendance elle-même, pas un saut brusque")
    else:
        note += f" ; rupture encore significative après retrait de la tendance (p = {fr(detr.p_value, 3, False)})"
    if artifact:
        note += " ; coïncide avec une rupture d'homogénéité corrigée par Météo-France : non interprétable comme climatique"
    return [Breakpoint(time=str(new_regime), method="Pettitt (1979)", p_value=round(res.p_value, 6),
                       possible_artifact=artifact, detrended_p_value=round(detr.p_value, 6), note=note)]


# ---------------------------------------------------------------- construction


@lru_cache(maxsize=1)
def station_config() -> dict[str, dict]:
    with (ROOT / "etl" / "config" / "stations.yaml").open(encoding="utf-8") as f:
        return {s["id"]: s for s in yaml.safe_load(f)["gironde"]}


def confidence(trend: Trend, raw_dir: Path) -> str:
    """Règle C7 : « élevée » exige Hamed-Rao significatif et la validation P1 (C3, C4) satisfaite."""
    from etl.validation import p1  # import tardif : évite le cycle

    if trend.significant:
        return "elevee" if p1.external_validation_passed(raw_dir) else "moyenne"
    if trend.p_value_classical is not None and trend.p_value_classical < trend.alpha:
        return "faible"  # significatif seulement sans correction de l'autocorrélation
    return "non_etabli"


def fr(x: float, digits: int = 2, signed: bool = True) -> str:
    s = f"{x:+.{digits}f}" if signed else f"{x:.{digits}f}"
    return s.replace(".", ",")


def _finding(where: str, variable: str, trend: Trend) -> str:
    label = VARIABLES[variable][0]
    total = trend.fitted_end - trend.fitted_start
    sig = (
        "tendance significative, corrigée de l'autocorrélation"
        if trend.significant
        else "tendance non significative une fois l'autocorrélation prise en compte"
    )
    return (
        f"{where}, la {label} annuelle a évolué de {fr(trend.slope_per_decade)} °C par décennie "
        f"entre {trend.period.start} et {trend.period.end}, soit {fr(total, 1)} °C sur la période ({sig})."
    )


def _validation_caveats(variable: str, raw_dir: Path) -> list[str]:
    from etl.validation import p1  # import tardif : évite le cycle

    caveat = p1.variable_caveat(variable, raw_dir)
    return [caveat] if caveat else []


def _limitations(series: AnnualSeries, extra: list[str]) -> list[str]:
    raw = sorted(y for y, h in series.homogenized.items() if not h)
    out = [
        "Séries homogénéisées par Météo-France (méthode HOMER) : des ruptures résiduelles d'amplitude "
        "inférieure à l'amplitude minimale détectable peuvent subsister.",
    ]
    if raw:
        out.append(
            f"Années {raw[0]}-{raw[-1]} : prolongation par des données brutes non homogénéisées, affichées "
            "pour information et exclues des tendances et des normales."
        )
    out.append("Moyennes annuelles calculées seulement pour les années aux 12 mois complets ; aucune valeur n'est complétée.")
    return out + extra


def _provenance(ctx: BuildContext) -> Provenance:
    return Provenance(
        source_name=lsh.SOURCE_NAME,
        source_url=lsh.DATASET_URL,
        license=lsh.LICENSE,
        extracted_at=ctx.extracted_at,
        script="etl/indicators/temperature.py",
        etl_version=ctx.etl_version,
        homogenized=True,
    )


def _assemble(ctx, *, ind_id, group, title, description, series, anomalies, where, composite, method_note, extra_limits,
              place, reference=REFERENCE):
    years = sorted(anomalies)
    normals = []
    if not composite:  # un composite d'anomalies n'a pas de normale absolue
        for p in NORMALS:
            m = mean_over(series, p)
            if m is not None:
                normals.append(Normal(period=p, value=round(m, 3)))
    main, alts = trends(series, anomalies)
    return Indicator(
        id=ind_id,
        scale="gironde",
        group=group,
        variable=vocab.variable(series.variable.lower()),
        place=place,
        title=title,
        unit="°C",
        description=description,
        frequency="annual",
        is_anomaly=True,
        reference_period=reference,
        series=Series(
            time=[str(y) for y in years],
            value=[round(anomalies[y], 3) for y in years],
            quality=["homogenized" if series.homogenized[y] else "raw" for y in years],
        ),
        normals=normals,
        trend=main,
        alt_trends=alts,
        breakpoints=detect_break(series, anomalies, composite),
        stations=list(series.stations),
        method_note=method_note,
        finding=_finding(where, series.variable, main),
        confidence=confidence(main, ctx.raw_dir),
        limitations=_limitations(series, extra_limits),
        provenance=_provenance(ctx),
    )


def build_station(ctx: BuildContext, variable: str, station: str) -> Indicator:
    cfg = next(c for c in station_config().values() if c["slug"] == station)
    series = station_annual(variable, cfg["id"], ctx.raw_dir)
    reference, extra = REFERENCE, []
    ref = mean_over(series, REFERENCE)
    if ref is None:
        # Série commençant après 1961 : référence réduite au début de la série, jamais complétée.
        first = series.hom_years()[0]
        reference = Period(start=first, end=REFERENCE.end)
        if reference.end - reference.start + 1 < MIN_REFERENCE_YEARS or (ref := mean_over(series, reference)) is None:
            raise ValueError(f"{cfg['name']} {variable} : période de référence trop courte")
        extra.append(
            f"La série commence en {first} : l'anomalie est calculée par rapport à {first}-{REFERENCE.end} "
            f"({reference.end - reference.start + 1} ans) au lieu de 1961-1990. Les tendances n'en dépendent pas."
        )
    anomalies = {y: v - ref for y, v in series.values.items()}
    label, plural = VARIABLES[variable]
    note = None
    if variable == "TM":
        note = "TM = (TN + TX) / 2, calculée mois par mois à partir des séries homogénéisées TN et TX."
    return _assemble(
        ctx,
        ind_id=f"{variable.lower()}-annuelle-{station}",
        group=f"Stations — températures {plural}",
        title=f"{label.capitalize()} annuelle à {cfg['name']}",
        description=(
            f"Moyenne annuelle des {plural} quotidiennes, en écart à la moyenne {reference.start}-{reference.end} "
            f"de la station ({fr(ref, 1, signed=False)} °C). {cfg['note']}"
        ),
        series=series,
        anomalies=anomalies,
        where=f"À {cfg['name']}",
        composite=False,
        method_note=note,
        extra_limits=extra + _validation_caveats(variable, ctx.raw_dir) + [f"Particularité du site : {cfg['note']}"],
        place=vocab.station(station, cfg["name"]),
        reference=reference,
    )


def build_composite(ctx: BuildContext, variable: str) -> Indicator:
    series, members, excluded = composite_anomaly(variable, ctx.raw_dir)
    names = station_config()
    member_names = ", ".join(names[s]["name"] for s in members)
    label, plural = VARIABLES[variable]
    note = (
        f"Moyenne des anomalies annuelles de {len(members)} stations ({member_names}), chacune rapportée à sa "
        f"propre normale 1961-1990. Réseau constant : seules les stations homogénéisées sur toute la période "
        f"{COMPOSITE_SPAN.start}-{COMPOSITE_SPAN.end} sont retenues"
    )
    if excluded:
        note += f" (exclues : {', '.join(names[s]['name'] for s in excluded)}, séries plus courtes)"
    note += "."
    if variable == "TM":
        note += " TM = (TN + TX) / 2, calculée mois par mois."
    return _assemble(
        ctx,
        ind_id=f"{variable.lower()}-annuelle-gironde",
        group="Synthèse Gironde",
        title=f"{label.capitalize()} annuelle en Gironde",
        description=(
            f"Anomalie annuelle des {plural} quotidiennes, moyenne de {len(members)} stations longues homogénéisées, "
            "en écart à la normale 1961-1990."
        ),
        series=series,
        anomalies=series.values,
        where="En Gironde",
        composite=True,
        method_note=note,
        extra_limits=_validation_caveats(variable, ctx.raw_dir) + [
            "Composite de stations, non pondéré par la surface : il ne représente pas une moyenne spatiale "
            "rigoureuse du département. Les stations littorales y pèsent autant que les stations intérieures."
        ],
        place=vocab.composite("gironde", "Gironde"),
    )
