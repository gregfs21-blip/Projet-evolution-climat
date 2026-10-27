"""P3 — température de la mer (ERA5, Copernicus Climate Data Store), critères validés par Grég le 27/10/2026.

SST mensuelle ERA5 (single levels), moyenne pondérée par cos(latitude) des mailles de mer de chaque boîte ;
moyenne annuelle des 12 mois. Deux boîtes fixées avant calcul :
- au large de la Gironde (44-46° N, 3-1° O) : l'indicateur local, sans référence ;
- golfe de Gascogne entier (43,5-48° N, 10-1° O) : porte la référence R8 (Costoya, + 0,26 °C/déc. depuis 1982,
  fourchette ± 20 % : [+0,21 ; +0,31], évaluée sur 1982-2014).
Série de plus de 80 ans : tendance mise en avant sur les 50 dernières années (règle du 23/10/2026).
"""

from __future__ import annotations

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import altitude as A
from etl.indicators import serie as S
from etl.schema import Indicator, Station
from etl.sources import cds_era5 as cds

R8 = {
    "kind": "slope", "period": [1982, 2014], "range": [0.21, 0.31], "unit": "°C/déc.", "fixed_on": "2026-10-27",
    "statement": ("Golfe de Gascogne : + 0,26 °C par décennie depuis 1982 (bassin entier, 1982-2014), fourchette ± 20 % "
                  "fixée par Grég faute d'incertitude publiée"),
    "source": "X. Costoya, thèse, université de Vigo, 2016 ; Costoya et al., Journal of Marine Systems, 2015",
    "url": "https://cim.uvigo.gal/en/2016/07/the-temperature-of-the-bay-of-biscay-has-increased-by-0-26-degrees-per-decade/",
}

BOXES = {
    "sst-large-gironde": {"variable": "sst-gascogne", "place": ("large-gironde", "Large de la Gironde"),
                          "where": "Au large de la Gironde", "reference": None},
    "sst-golfe-gascogne": {"variable": "sst-golfe", "place": ("gascogne", "Golfe de Gascogne"),
                           "where": "Dans le golfe de Gascogne", "reference": R8},
}

LIMITS = [
    "Température de surface ERA5 : avant 1979, elle provient d'analyses fondées sur les navires (HadISST), "
    "plus rares et moins précises ; depuis 1982, d'analyses satellitaires (OSTIA). Le changement de source peut "
    "peser sur les tendances longues.",
    "Moyenne d'une boîte en mer : la température près de la côte, dans le bassin d'Arcachon ou l'estuaire peut "
    "évoluer différemment (refroidissement hivernal sous le panache de la Gironde signalé par Costoya).",
]


def build(ctx: BuildContext, box: str, title: str, description: str, label: str,
          limitations: list[str] | None = None) -> Indicator:
    spec = BOXES[box]
    series = A.annual(cds.load_sst(box))
    bad = {y: v for y, v in series.items() if not 10.0 <= v <= 20.0}        # H7
    if bad or len(series) < 30:
        raise ValueError(f"{box} : valeurs hors [10 ; 20] °C ou série trop courte : {list(bad.items())[:3]}, {len(series)} ans")
    n, w, s_, e = cds.SST_BOXES[box]
    slug, name = spec["place"]
    st = Station(id=f"era5-{box}", name=f"{name} (ERA5, {s_:g}-{n:g}° N, {-w:g}-{-e:g}° O)".replace(".", ","),
                 latitude=(n + s_) / 2, longitude=(w + e) / 2, altitude=0.0)
    return S.assemble(ctx, ind_id=f"{spec['variable']}-{slug}", scale="gironde", variable=spec["variable"],
                      place=vocab.station(slug, name), title=title, description=description, unit="°C", series=series,
                      hom=set(series), provenance=A._provenance(ctx).model_copy(update={
                          "source_name": "ECMWF / Copernicus — ERA5, moyennes mensuelles (single levels, Climate Data Store)",
                          "source_url": "https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means",
                          "script": "etl.indicators.mer"}),
                      limitations=LIMITS + (limitations or []), stations=[st],
                      method_note="Moyenne pondérée par le cosinus de la latitude des mailles de mer de la boîte, puis "
                                  "moyenne des 12 mois de l'année.",
                      reference=spec["reference"], baseline=None, group=f"Réanalyse ERA5 — {vocab.variable(spec['variable']).theme_label}",
                      where=spec["where"], label=label)


# ---------------------------------------------------------------- niveau marin par altimétrie (P3, décision du 27/10/2026)

ALTI_LIMITS = [
    "Altimétrie satellite (produit C3S/DUACS, version DT2024) : niveau géocentrique, insensible à l'enfoncement du sol "
    "contrairement aux marégraphes ; mais la précision se dégrade près des côtes, et la série ne commence qu'en 1993.",
    "Anomalie par rapport à la référence du produit (1993-2012) ; aucune correction de l'ajustement isostatique "
    "glaciaire (de l'ordre de 0,3 mm/an en moyenne mondiale, plus faible ici).",
    "Aucune référence publiée chiffrée pour cette zone : confiance au plus « moyenne ».",
]


def build_alti(ctx: BuildContext, title: str, description: str, label: str) -> Indicator:
    series = A.annual(cds.load_alti())
    bad = {y: v for y, v in series.items() if not -250.0 <= v <= 250.0}
    if bad or len(series) < 25:
        raise ValueError(f"altimétrie : valeurs hors [−250 ; 250] mm ou série trop courte : {list(bad.items())[:3]}, {len(series)} ans")
    n, w, s_, e = cds.ALTI_BOX
    st = Station(id="alti-large-gironde", name=f"Large de la Gironde (altimétrie, {s_:g}-{n:g}° N, {-w:g}-{-e:g}° O)".replace(".", ","),
                 latitude=(n + s_) / 2, longitude=(w + e) / 2, altitude=0.0)
    prov = A._provenance(ctx).model_copy(update={
        "source_name": "Copernicus (C3S) — niveau de la mer par altimétrie satellite, moyennes mensuelles (DT2024)",
        "source_url": "https://cds.climate.copernicus.eu/datasets/satellite-sea-level-global",
        "license": "CC BY 4.0 (Copernicus)", "script": "etl.indicators.mer"})
    return S.assemble(ctx, ind_id="niveau-mer-large-gironde", scale="gironde", variable="niveau-mer",
                      place=vocab.station("large-gironde", "Large de la Gironde (satellite)"), title=title,
                      description=description, unit="mm", series=series, hom=set(series), provenance=prov,
                      limitations=ALTI_LIMITS, stations=[st],
                      method_note="Anomalie mensuelle du niveau de la mer (sla) moyennée sur la zone, pondérée par le "
                                  "cosinus de la latitude, puis moyenne des 12 mois.",
                      reference=None, baseline=None, group="Satellite — niveau de la mer", where="Au large de la Gironde",
                      label=label)
