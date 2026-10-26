"""Tendance monotone : pente de Sen et test de Mann-Kendall corrigé de Hamed et Rao.

- Pente : estimateur de Sen (scipy.stats.theilslopes) sur les années réelles, avec
  son intervalle de confiance. Robuste aux valeurs extrêmes, gère les lacunes.
- Significativité : test de Mann-Kendall modifié de Hamed et Rao (1998), repris de
  pymannkendall. Il corrige la variance de la statistique S de l'autocorrélation
  de la série ; sans cette correction, une série autocorrélée paraît
  significative à tort.
- Le p de Mann-Kendall classique est publié à côté, pour mesurer l'effet de la
  correction (critère C7).

Implémentation des tests : etl/stats/mannkendall.py, repris de pymannkendall
(commit ec2e3ab, correctif de l'issue 29). Voir ce module pour les raisons et
l'écart conservateur au calcul original.
"""

from __future__ import annotations

import numpy as np
from scipy import stats

from etl.schema import Period, Trend
from etl.stats.mannkendall import hamed_rao_test, original_test

METHOD = "pente de Sen ; significativité Mann-Kendall corrigé de Hamed-Rao (1998)"
MIN_POINTS = 10


def _clean(years, values):
    x = np.asarray(years, dtype=float)
    y = np.asarray([np.nan if v is None else v for v in values], dtype=float)
    mask = ~np.isnan(y)
    return x[mask], y[mask]


def annual_trend(years: list[int], values: list[float | None], label: str = "", alpha: float = 0.05) -> Trend:
    """Tendance d'une série annuelle. Les valeurs manquantes sont ignorées."""
    x, y = _clean(years, values)
    if len(y) < MIN_POINTS:
        raise ValueError(f"série trop courte pour une tendance ({len(y)} valeurs, minimum {MIN_POINTS})")
    if np.any(np.diff(x) != 1):
        # Hamed-Rao estime l'autocorrélation par décalage d'indice : une lacune le fausserait.
        raise ValueError("série annuelle lacunaire : le test de Hamed-Rao exige des années consécutives")

    slope, intercept, low, high = stats.theilslopes(y, x, alpha=1 - alpha)
    hr = hamed_rao_test(y, alpha=alpha)
    classical = original_test(y)
    if not np.isfinite(hr.p) or not np.isfinite(classical.p):
        raise ValueError("test de Mann-Kendall non calculable (p non fini) : vérifier etl/stats/mannkendall.py")
    # Arrondi avant la décision, pour que `significant` reste cohérent avec la valeur publiée.
    p = round(float(hr.p), 6)

    return Trend(
        label=label,
        method=METHOD,
        period=Period(start=int(x.min()), end=int(x.max())),
        slope_per_decade=round(float(slope) * 10, 4) + 0.0,  # + 0.0 : pas de « −0 » affiché
        slope_ci_low=round(float(low) * 10, 4) + 0.0,
        slope_ci_high=round(float(high) * 10, 4) + 0.0,
        fitted_start=round(float(intercept + slope * x.min()), 4),
        fitted_end=round(float(intercept + slope * x.max()), 4),
        p_value=p,
        significant=p < alpha,
        alpha=alpha,
        p_value_classical=round(float(classical.p), 6),
    )


def ols_slope_per_decade(years: list[int], values: list[float | None]) -> float:
    """Pente par moindres carrés, pour comparaison avec des références qui l'utilisent (critère C4)."""
    x, y = _clean(years, values)
    return float(np.polyfit(x, y, 1)[0] * 10)
