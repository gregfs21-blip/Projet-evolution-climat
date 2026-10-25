"""Indicateurs « largeur d'abord », lot 2 (25/10/2026) : pression, humidité, vent, tempêtes, altitude.

Trois sources, trois statuts — fixés avant le premier calcul :
- ERA5 (réanalyse ECMWF, via Open-Meteo), maille de Bordeaux-Mérignac : produit publié, traité comme les séries
  NOAA ou NASA (tendance calculée), sans référence publiée locale → confiance au plus « moyenne ». Série de plus de
  80 ans : la tendance mise en avant porte sur les 50 dernières années (ère satellitaire, règle du 23/10/2026).
- Rafales quotidiennes Météo-France (FXI), Mérignac, Cazaux, Cap-Ferret : mesures BRUTES, jamais homogénéisées
  (anémomètres déplacés, changés, automatisés).
- Radiosondages IGRA de Bordeaux-Mérignac (12 UTC) : mesures BRUTES (changements de sondes).
Pour ces deux sources, tendance INDICATIVE (`indicative: true` au registre) : exception à la règle C2 décidée par
Grég le 25/10/2026, après avoir vu les séries brutes ; confiance au plus « faible », sans normale ni référence.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from functools import lru_cache
from pathlib import Path

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import serie as S
from etl.indicators import temperature as T
from etl.indicators.extremes import MAX_MISSING_DAYS, days_of
from etl.schema import Indicator, Provenance, Station
from etl.sources import igra
from etl.sources import meteofrance_quot as quot
from etl.sources import openmeteo_era5 as era5

LAST = datetime.now(timezone.utc).year - 1            # dernière année complète
DEPARTMENT = "33"

# ---------------------------------------------------------------- ERA5

ERA5_POINT = (44.831, -0.691)                        # Bordeaux-Mérignac ; la maille ERA5 la plus proche est retenue
ERA5_START = "1940-01-01"
ERA5_DAILY = ("pressure_msl_mean", "relative_humidity_2m_mean", "wind_gusts_10m_max")
VENT_FORT_KMH = 57.6                                  # 16 m/s : seuil « vent fort » des statistiques Météo-France

# variable → (colonne ERA5, agrégat annuel, unité, bornes plausibles de la valeur annuelle)
ERA5_VARS = {
    "pression": ("pressure_msl_mean", "mean", "hPa", (1005.0, 1025.0)),
    "humidite": ("relative_humidity_2m_mean", "mean", "%", (55.0, 95.0)),
    "jours-vent-fort": ("wind_gusts_10m_max", "count", "jours", (0.0, 250.0)),
    "rafale-max": ("wind_gusts_10m_max", "max", "km/h", (40.0, 220.0)),
}


@lru_cache(maxsize=2)
def _era5(raw_dir: str) -> tuple[dict, dict[str, dict[date, float]]]:
    return era5.fetch_daily_vars(*ERA5_POINT, ERA5_START, f"{LAST}-12-31", ERA5_DAILY, Path(raw_dir),
                                 download=not T._offline())


def era5_annual(variable: str, cols: dict[str, dict[date, float]]) -> dict[int, float]:
    """Agrégat annuel des années dont TOUS les jours sont présents (aucune valeur complétée)."""
    col, agg, _unit, _ = ERA5_VARS[variable]
    by_year: dict[int, list[float]] = {}
    for d, v in cols[col].items():
        by_year.setdefault(d.year, []).append(v)
    out = {}
    for y, vals in by_year.items():
        if len(vals) != (date(y + 1, 1, 1) - date(y, 1, 1)).days:
            continue
        if agg == "mean":
            out[y] = round(sum(vals) / len(vals), 3)
        elif agg == "max":
            out[y] = max(vals)
        else:
            out[y] = float(sum(v >= VENT_FORT_KMH for v in vals))
    return out


def _check(variable: str, series: dict[int, float], bounds: tuple[float, float]) -> None:
    lo, hi = bounds
    bad = {y: v for y, v in series.items() if not lo <= v <= hi}
    if bad:
        raise ValueError(f"{variable} : {len(bad)} valeur(s) annuelle(s) hors de [{lo} ; {hi}] (ex. {list(bad.items())[:3]}) — unité ?")
    if len(series) < 30:
        raise ValueError(f"{variable} : seulement {len(series)} années complètes")


ERA5_LIMITS = [
    "Réanalyse ERA5 : un modèle météorologique contraint par les observations disponibles, pas une mesure. Les "
    "changements du système d'observation (satellites depuis 1979) peuvent créer de fausses tendances ; aucune "
    "homogénéisation n'est appliquée.",
    "Valeur d'une maille de 0,25° (environ 28 km) : moyenne spatiale, plus lisse qu'une station.",
]


def build_era5(ctx: BuildContext, variable: str, title: str, description: str, label: str,
               limitations: list[str] | None = None, reference: dict | None = None) -> Indicator:
    meta, cols = _era5(str(ctx.raw_dir))
    _col, _agg, unit, bounds = ERA5_VARS[variable]
    series = era5_annual(variable, cols)
    _check(variable, series, bounds)
    lat, lon = meta["lat"], meta["lon"]
    name = f"Bordeaux (maille ERA5 {T.fr(lat, 2, signed=False)} N ; {T.fr(-lon, 2, signed=False)} O)"
    st = Station(id="era5-bordeaux", name=name, latitude=lat, longitude=lon, altitude=meta["elevation"])
    prov = Provenance(source_name=era5.SOURCE_NAME, source_url="https://open-meteo.com/en/docs/historical-weather-api",
                      license=era5.LICENSE, extracted_at=ctx.extracted_at, script="etl.indicators.atmosphere",
                      etl_version=ctx.etl_version, homogenized=False)
    v = vocab.variable(variable)
    return S.assemble(ctx, ind_id=f"{variable}-bordeaux-era5", scale="gironde", variable=variable,
                      place=vocab.station("bordeaux-era5", "Bordeaux (ERA5)"), title=title, description=description,
                      unit=unit, series=series, hom=set(series), provenance=prov,
                      limitations=ERA5_LIMITS + (limitations or []), stations=[st], method_note=None,
                      reference=reference, baseline=None, group=f"Réanalyse ERA5 — {v.theme_label}",
                      where="À Bordeaux (réanalyse ERA5)", label=label)


# ---------------------------------------------------------------- rafales Météo-France (brutes)

FXI_POSTES = ("33281001", "33529001", "33236002")    # Mérignac, Cazaux, Cap-Ferret : séries FXI ≥ 50 ans (sonde 25/10)


@lru_cache(maxsize=2)
def _fxi(raw_dir: str):
    data = quot.load(DEPARTMENT, set(FXI_POSTES), ("FXI",), Path(raw_dir))
    return {p: v["FXI"] for p, v in data.items()}, quot.meta(DEPARTMENT, set(FXI_POSTES), Path(raw_dir))


def fxi_counts(daily: dict[str, quot.Daily], threshold_ms: float) -> dict[int, float]:
    """Jours avec rafale ≥ seuil, années complètes au sens ETCCDI (au plus 3 jours absents par mois)."""
    years = sorted({int(d[:4]) for d in daily})
    out = {}
    for y in years:
        if y > LAST:
            continue
        if all(sum(d in daily for d in days_of(y, m)) >= len(days_of(y, m)) - MAX_MISSING_DAYS for m in range(1, 13)):
            out[y] = float(sum(1 for d, x in daily.items() if d.startswith(f"{y}-") and x.value >= threshold_ms))
    return out


def build_fxi(ctx: BuildContext, station: str, variable: str, threshold_ms: float, title: str, description: str,
              label: str, limitations: list[str] | None = None, indicative: bool = False) -> Indicator:
    daily, meta = _fxi(str(ctx.raw_dir))
    if station not in daily or not daily[station]:
        raise KeyError(f"pas de rafales FXI pour le poste {station}")
    over = [x.value for x in daily[station].values() if x.value > 75]
    if over:
        raise ValueError(f"FXI {station} : {len(over)} valeur(s) > 75 m/s — unité ?")
    series = fxi_counts(daily[station], threshold_ms)
    if len(series) < 20:
        raise ValueError(f"FXI {station} : seulement {len(series)} années complètes")
    cfg = T.station_config().get(station, {})
    nom, lat, lon, alt = meta[station]
    name = cfg.get("name") or nom.title()
    slug = cfg.get("slug") or S.slugify(name)
    st = Station(id=station, name=name, latitude=lat, longitude=lon, altitude=alt)
    prov = Provenance(source_name=quot.SOURCE_NAME, source_url=quot.DATASET_URL, license=quot.LICENSE, extracted_at=ctx.extracted_at,
                      script="etl.indicators.atmosphere", etl_version=ctx.etl_version, homogenized=False)
    lims = [
        "Rafale maximale instantanée du jour (FXI) telle que mesurée : l'environnement de l'anémomètre (arbres, "
        "bâtiments), son type et sa hauteur ont changé au fil des décennies, sans correction publiée.",
        "Une année n'est comptée que si chaque mois a au plus 3 jours sans mesure (règle ETCCDI) ; aucune valeur "
        "n'est complétée.",
    ] + (limitations or [])
    return S.assemble(ctx, ind_id=f"{variable}-{slug}", scale="gironde", variable=variable,
                      place=vocab.station(slug, name), title=title.format(name=name),
                      description=description.format(name=name), unit="jours", series=series, hom=set(), provenance=prov,
                      limitations=lims, stations=[st], method_note=None, reference=None, baseline=None,
                      group="Stations — rafales mesurées (brutes)", where=f"À {name}", label=label,
                      indicative=indicative,
                      raw_reason=None if indicative else
                      "série brute non homogénéisée, publiée sans tendance (règle C2) : les changements "
                      "d'anémomètre peuvent à eux seuls créer ou masquer une évolution.")


# ---------------------------------------------------------------- radiosondages IGRA (bruts)

IGRA_STATION = "FRM00007510"                          # Bordeaux-Mérignac
IGRA_HOUR = 12                                        # 12 UTC seulement : l'horaire le plus continu (fixé avant calcul)
IGRA_MIN_PER_MONTH = 15                               # sondages valides exigés pour une moyenne mensuelle
IGRA_LEVELS = (850, 500)
IGRA_VARS = {                                          # variable → (niveau hPa, grandeur, unité, bornes plausibles annuelles)
    "t850": (850, "temp", "°C", (-5.0, 15.0)),
    "t500": (500, "temp", "°C", (-35.0, -5.0)),
    "z500": (500, "gph", "m", (5400.0, 5900.0)),
}


@lru_cache(maxsize=2)
def _igra(raw_dir: str):
    return igra.load(IGRA_STATION, IGRA_LEVELS, IGRA_HOUR, Path(raw_dir))


def igra_annual(monthly: dict[tuple[int, int], list[float]]) -> dict[int, float]:
    """Moyenne des 12 moyennes mensuelles ; un mois exige IGRA_MIN_PER_MONTH sondages valides, une année ses 12 mois."""
    out = {}
    for y in sorted({y for y, _ in monthly}):
        months = [monthly.get((y, m), []) for m in range(1, 13)]
        if y <= LAST and all(len(v) >= IGRA_MIN_PER_MONTH for v in months):
            out[y] = round(sum(sum(v) / len(v) for v in months) / 12, 3)
    return out


def build_igra(ctx: BuildContext, variable: str, title: str, description: str, label: str,
               limitations: list[str] | None = None, indicative: bool = False) -> Indicator:
    level, what, unit, bounds = IGRA_VARS[variable]
    series = igra_annual(_igra(str(ctx.raw_dir))[level][what])
    _check(variable, series, bounds)
    st = Station(id=IGRA_STATION, name="Bordeaux-Mérignac (radiosondages)", latitude=44.8306, longitude=-0.6914, altitude=51.0)
    prov = Provenance(source_name=igra.SOURCE_NAME, source_url=igra.PAGE, license=igra.LICENSE,
                      extracted_at=ctx.extracted_at, script="etl.indicators.atmosphere", etl_version=ctx.etl_version,
                      homogenized=False)
    lims = [
        "Radiosondages bruts : les changements de modèle de sonde et de correction du rayonnement solaire créent des "
        "sauts connus dans les séries d'altitude ; aucune homogénéisation n'est appliquée ici.",
        f"Sondages de {IGRA_HOUR} UTC seulement ; un mois exige {IGRA_MIN_PER_MONTH} sondages valides, une année ses "
        "12 mois ; valeurs rejetées par le contrôle qualité d'IGRA exclues.",
    ] + (limitations or [])
    v = vocab.variable(variable)
    return S.assemble(ctx, ind_id=f"{variable}-bordeaux-merignac", scale="gironde", variable=variable,
                      place=vocab.station("bordeaux-merignac", "Bordeaux-Mérignac"), title=title,
                      description=description, unit=unit, series=series, hom=set(), provenance=prov, limitations=lims,
                      stations=[st], method_note=None, reference=None, baseline=None,
                      group=f"Radiosondages — {v.theme_label}", where="Au-dessus de Bordeaux-Mérignac", label=label,
                      indicative=indicative,
                      raw_reason=None if indicative else
                      "série brute non homogénéisée, publiée sans tendance (règle C2) : les changements de "
                      "sondes peuvent à eux seuls créer une évolution apparente.")
