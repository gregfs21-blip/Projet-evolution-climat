"""Tendance monotone : test de Mann-Kendall et pente de Sen.

État P0 : implémentation provisoire avec scipy (Mann-Kendall classique, SANS
correction d'autocorrélation). Elle suffit à faire traverser la chaîne à
l'indicateur de démonstration.

À la phase 1, cette fonction passe sur pymannkendall (variante Hamed-Rao,
corrigée de l'autocorrélation) et ses résultats sont comparés à cette version
de référence. Le champ `method` du JSON indique toujours ce qui a été appliqué.
"""

from __future__ import annotations

import numpy as np
from scipy import stats

from etl.schema import Period, Trend

METHOD = "mann-kendall classique (sans correction d'autocorrélation) + pente de Sen"


def annual_trend(years: list[int], values: list[float | None], alpha: float = 0.05) -> Trend:
    """Tendance d'une série annuelle. Les valeurs manquantes sont ignorées."""
    x = np.asarray(years, dtype=float)
    y = np.asarray([np.nan if v is None else v for v in values], dtype=float)
    mask = ~np.isnan(y)
    x, y = x[mask], y[mask]
    if len(y) < 10:
        raise ValueError(f"série trop courte pour une tendance ({len(y)} valeurs, minimum 10)")

    tau = stats.kendalltau(x, y)
    slope, intercept, low, high = stats.theilslopes(y, x, alpha=1 - alpha)
    # Arrondi avant la décision, pour que `significant` reste cohérent avec la valeur publiée.
    p = round(float(tau.pvalue), 6)

    return Trend(
        method=METHOD,
        period=Period(start=int(x.min()), end=int(x.max())),
        slope_per_decade=round(float(slope) * 10, 4),
        slope_ci_low=round(float(low) * 10, 4),
        slope_ci_high=round(float(high) * 10, 4),
        fitted_start=round(float(intercept + slope * x.min()), 4),
        fitted_end=round(float(intercept + slope * x.max()), 4),
        p_value=p,
        significant=p < alpha,
        alpha=alpha,
    )
