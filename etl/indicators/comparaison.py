"""Pente de comparaison entre échelles (décision de Grég du 02/11/2026, fenêtre fixée avant calcul).

Les tendances mises en avant de la Gironde, de la France et du globe ne couvrent pas la même période : elles ne
se comparent pas. Cette tendance, publiée à côté dans `alt_trends`, porte sur la même fenêtre pour les trois séries,
avec la même méthode. Elle ne change ni la tendance mise en avant, ni le constat, ni le niveau de confiance.

La fenêtre est l'intersection des périodes homogénéisées des trois séries. Elle est fixe : si une série ne la couvre
plus entièrement, la construction échoue plutôt que de comparer des périodes différentes.
"""

from __future__ import annotations

from etl.schema import Indicator, Period
from etl.stats.trend import annual_trend

WINDOW = Period(start=1959, end=2021)
LABEL = f"{WINDOW.start}-{WINDOW.end}, comparaison entre échelles"
SERIES = {"tm-annuelle-gironde", "tm-france", "temperature-hadcrut5-monde"}


def with_comparison(ind: Indicator) -> Indicator:
    """Ajoute la tendance de comparaison aux séries concernées ; tout autre indicateur est rendu tel quel."""
    if ind.id not in SERIES:
        return ind
    quality = ind.series.quality or ["homogenized"] * len(ind.series.time)
    usable = {int(t[:4]): v for t, v, q in zip(ind.series.time, ind.series.value, quality) if v is not None and q != "raw"}
    years = list(range(WINDOW.start, WINDOW.end + 1))
    missing = [y for y in years if y not in usable]
    if missing:
        raise ValueError(f"{ind.id} : fenêtre de comparaison {WINDOW.start}-{WINDOW.end} incomplète, années manquantes {missing[:5]}")
    trend = annual_trend(years, [usable[y] for y in years], label=LABEL)
    return ind.model_copy(update={"alt_trends": [*ind.alt_trends, trend]})
