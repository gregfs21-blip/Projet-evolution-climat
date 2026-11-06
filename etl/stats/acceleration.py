"""Test d'accélération d'une série annuelle (P8, règle S5 validée par Grég le 02/11/2026, avant tout calcul).

Régression quadratique par moindres carrés y = a + b·t + c·t², t centré sur la moyenne des années ;
accélération = 2c (unité de la série par an²). Erreur type de Newey-West (noyau de Bartlett, décalage
⌊0,75·n^(1/3)⌋), qui tient compte de l'autocorrélation des résidus ; p bilatéral sur une loi de Student à n − 3
degrés de liberté.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats

MIN_POINTS = 20


@dataclass(frozen=True)
class Acceleration:
    start: int
    end: int
    n: int
    lag: int
    value: float          # unité par an²
    se: float
    ci_low: float
    ci_high: float
    p_value: float
    significant: bool
    rate_start: float     # pente de l'ajustement au début et à la fin (unité par an)
    rate_end: float


def newey_west_lag(n: int) -> int:
    return int(np.floor(0.75 * n ** (1 / 3)))


def _hac_cov(X: np.ndarray, resid: np.ndarray, lag: int) -> np.ndarray:
    n = X.shape[0]
    xtx_inv = np.linalg.inv(X.T @ X)
    u = X * resid[:, None]
    s = u.T @ u
    for k in range(1, lag + 1):
        w = 1 - k / (lag + 1)
        g = u[k:].T @ u[:-k]
        s += w * (g + g.T)
    return xtx_inv @ s @ xtx_inv * n / (n - X.shape[1])


def quadratic_acceleration(years: list[int], values: list[float | None], alpha: float = 0.05) -> Acceleration:
    pairs = [(int(y), float(v)) for y, v in zip(years, values) if v is not None and np.isfinite(v)]
    if len(pairs) < MIN_POINTS:
        raise ValueError(f"série trop courte pour un test d'accélération ({len(pairs)} valeurs, minimum {MIN_POINTS})")
    x = np.array([p[0] for p in pairs], dtype=float)
    y = np.array([p[1] for p in pairs], dtype=float)
    if np.any(np.diff(x) != 1):
        raise ValueError("série annuelle lacunaire : le test exige des années consécutives")
    t = x - x.mean()
    X = np.column_stack([np.ones_like(t), t, t ** 2])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    n = len(y)
    lag = newey_west_lag(n)
    cov = _hac_cov(X, resid, lag)
    acc, se = 2 * beta[2], 2 * float(np.sqrt(cov[2, 2]))
    df = n - 3
    p = float(2 * stats.t.sf(abs(acc / se), df)) if se > 0 else 0.0
    q = float(stats.t.ppf(1 - alpha / 2, df))
    p = round(p, 6)
    return Acceleration(start=int(x[0]), end=int(x[-1]), n=n, lag=lag, value=float(acc), se=se,
                        ci_low=float(acc - q * se), ci_high=float(acc + q * se), p_value=p, significant=p < alpha,
                        rate_start=float(beta[1] + 2 * beta[2] * t[0]), rate_end=float(beta[1] + 2 * beta[2] * t[-1]))
