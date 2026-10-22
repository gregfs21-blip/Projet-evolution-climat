"""Indicateur de démonstration (phase 0).

Série SYNTHÉTIQUE, générée de façon déterministe. Elle ne représente aucune
mesure réelle. Son seul rôle est de vérifier que la chaîne complète fonctionne :
ETL → JSON validé → manifeste → page générée sur le site.

Elle sera retirée à la fin de la phase 1, quand le premier vrai indicateur
(températures LSH de Mérignac) l'aura remplacée.
"""

from __future__ import annotations

import numpy as np

from etl.context import BuildContext
from etl.schema import Indicator, Period, Provenance, Series
from etl.stats.trend import annual_trend

FIRST_YEAR, LAST_YEAR = 1961, 2025
REFERENCE = Period(start=1961, end=1990)


def _synthetic_series() -> tuple[list[int], list[float | None]]:
    rng = np.random.default_rng(seed=33)  # graine fixe : sortie reproductible
    years = np.arange(FIRST_YEAR, LAST_YEAR + 1)
    warming = np.where(years > 1980, (years - 1980) * 0.035, 0.0)
    raw = 13.2 + warming + rng.normal(0, 0.45, years.size)
    ref = raw[(years >= REFERENCE.start) & (years <= REFERENCE.end)].mean()
    values: list[float | None] = [round(float(v - ref), 3) for v in raw]
    values[years.tolist().index(1973)] = None  # trou volontaire : teste la gestion des lacunes
    return years.tolist(), values


def build(ctx: BuildContext) -> Indicator:
    years, values = _synthetic_series()
    trend = annual_trend(years, values)

    return Indicator(
        id="demo-temperature-annuelle",
        scale="gironde",
        title="DÉMO – Anomalie de température annuelle (données synthétiques)",
        unit="°C",
        description=(
            "Série fictive générée par l'ETL pour tester la chaîne de traitement. "
            "Elle ne doit pas être interprétée."
        ),
        frequency="annual",
        is_anomaly=True,
        reference_period=REFERENCE,
        series=Series(time=[str(y) for y in years], value=values),
        trend=trend,
        breakpoints=[],
        finding=(
            f"Démonstration : la série synthétique présente une pente de "
            f"{trend.slope_per_decade:+.2f} °C par décennie sur {trend.period.start}-{trend.period.end}."
            .replace(".", ",", 1)
        ),
        confidence="non_etabli",
        limitations=[
            "Données synthétiques : aucune valeur ne correspond à une mesure.",
            "Test de tendance provisoire, sans correction de l'autocorrélation (corrigé en phase 1).",
        ],
        provenance=Provenance(
            source_name="Générateur synthétique de l'ETL",
            source_url="https://github.com/gregfs21-blip/Projet-evolution-climat",
            license="CC0 (données synthétiques)",
            extracted_at=ctx.extracted_at,
            script="etl/sources/demo.py",
            etl_version=ctx.etl_version,
            homogenized=False,
        ),
        is_demo=True,
    )
