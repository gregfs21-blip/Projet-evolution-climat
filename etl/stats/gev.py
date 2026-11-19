"""Loi généralisée des valeurs extrêmes (GEV) non stationnaire, « décalage » de la position (P10.2).

Modèle (protocole du World Weather Attribution, Philip et al., 2020) : pour l'année a de covariable G(a),
    X(a) ~ GEV(μ(a) = μ₀ + α·G(a), σ, ξ),
avec la convention des climatologues : ξ > 0 queue lourde, ξ < 0 loi bornée à droite par μ − σ/ξ (scipy utilise
c = −ξ). Estimation par maximum de vraisemblance, plusieurs points de départ ; incertitude par rééchantillonnage des
années (bootstrap non paramétrique). Aucune dépendance au-delà de numpy et scipy ; recoupé par etl/tests/test_p10b.py
(comparaison à scipy.stats.genextreme dans le cas stationnaire).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import optimize, stats

XI_EPS = 1e-6


def nll(params: np.ndarray, x: np.ndarray, g: np.ndarray) -> float:
    """Opposé de la log-vraisemblance. params = (μ₀, α, log σ, ξ)."""
    mu0, alpha, logs, xi = params
    s = np.exp(logs)
    z = (x - mu0 - alpha * g) / s
    if abs(xi) < XI_EPS:
        return float(np.sum(logs + z + np.exp(-z)))
    t = 1 + xi * z
    if np.any(t <= 0):
        return np.inf
    return float(np.sum(logs + (1 + 1 / xi) * np.log(t) + t ** (-1 / xi)))


@dataclass(frozen=True)
class GevFit:
    mu0: float
    alpha: float
    sigma: float
    xi: float
    loglik: float
    stationary: bool
    converged: bool = True   # l'optimiseur retenu a déclaré sa convergence

    def mu(self, g: float | np.ndarray) -> float | np.ndarray:
        return self.mu0 + self.alpha * np.asarray(g)

    def cdf(self, x: float | np.ndarray, g: float | np.ndarray) -> np.ndarray:
        return stats.genextreme.cdf(x, -self.xi, loc=self.mu(g), scale=self.sigma)

    def exceedance(self, x: float, g: float) -> float:
        """Probabilité annuelle de dépasser x ; 0 au-delà de la borne supérieure (ξ < 0)."""
        return float(stats.genextreme.sf(x, -self.xi, loc=self.mu(g), scale=self.sigma))

    def return_level(self, period: float | np.ndarray, g: float) -> np.ndarray:
        """Niveau dépassé en moyenne une fois tous les `period` ans dans le climat g."""
        return stats.genextreme.isf(1 / np.asarray(period, float), -self.xi, loc=self.mu(g), scale=self.sigma)

    def upper_bound(self, g: float) -> float:
        return float(self.mu(g) - self.sigma / self.xi) if self.xi < 0 else np.inf


def fit(x, g, stationary: bool = False) -> GevFit:
    """Maximum de vraisemblance. `stationary` : α fixé à 0. Lève ValueError si aucune optimisation ne converge."""
    x = np.asarray(x, float)
    g = np.asarray(g, float)
    if len(x) != len(g) or len(x) < 20 or not (np.all(np.isfinite(x)) and np.all(np.isfinite(g))):
        raise ValueError("GEV : séries de longueurs différentes, trop courtes ou incomplètes")
    if stationary:
        a0, b0 = float(np.mean(x)), 0.0
    else:
        b0, a0 = np.polyfit(g, x, 1)
    resid = x - a0 - b0 * g
    s0 = max(float(np.std(resid)) * np.sqrt(6) / np.pi, 0.1)
    m0 = a0 - 0.5772 * s0
    best = None
    for xi0 in (-0.3, -0.1, 0.05):
        start = np.array([m0, b0, np.log(s0), xi0])
        f = (lambda p: nll(np.array([p[0], 0.0, p[1], p[2]]), x, g)) if stationary else (lambda p: nll(p, x, g))
        p0 = start[[0, 2, 3]] if stationary else start
        r = optimize.minimize(f, p0, method="Nelder-Mead",
                              options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 20000, "maxfev": 40000})
        r = optimize.minimize(f, r.x, method="Nelder-Mead",
                              options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000, "maxfev": 40000})
        if np.isfinite(r.fun) and (best is None or r.fun < best.fun):
            best = r
    if best is None:
        raise ValueError("GEV : l'ajustement ne converge pas")
    p = best.x
    if stationary:
        return GevFit(float(p[0]), 0.0, float(np.exp(p[1])), float(p[2]), -float(best.fun), True, bool(best.success))
    return GevFit(float(p[0]), float(p[1]), float(np.exp(p[2])), float(p[3]), -float(best.fun), False,
                  bool(best.success))


def likelihood_ratio_p(x, g) -> float:
    """Test du rapport de vraisemblance, H0 : α = 0 (χ² à 1 degré de liberté)."""
    full, null = fit(x, g), fit(x, g, stationary=True)
    if not (full.converged and null.converged):
        raise ValueError("GEV : rapport de vraisemblance sur un ajustement sans convergence déclarée")
    stat = max(0.0, 2 * (full.loglik - null.loglik))
    return float(stats.chi2.sf(stat, 1))


def ks_p(f: GevFit, x, g) -> float:
    """Adéquation : probabilités transformées F(x(a); μ(a)) comparées à une loi uniforme (Kolmogorov-Smirnov).

    Paramètres estimés sur les mêmes données : le p est approché (test plutôt indulgent)."""
    u = f.cdf(np.asarray(x, float), np.asarray(g, float))
    return float(stats.kstest(u, "uniform").pvalue)


def bootstrap(x, g, n: int, seed: int, stat) -> tuple[np.ndarray, int]:
    """Rééchantillonne les années avec remise, réajuste, applique `stat(fit)` (scalaire ou tableau).

    Renvoie (tableau des statistiques, nombre de tirages écartés : ajustement en échec ou optimiseur sans
    convergence déclarée)."""
    x = np.asarray(x, float)
    g = np.asarray(g, float)
    rng = np.random.default_rng(seed)
    out, failed = [], 0
    for _ in range(n):
        i = rng.integers(0, len(x), len(x))
        try:
            ff = fit(x[i], g[i])
        except ValueError:
            failed += 1
            continue
        if not ff.converged:
            failed += 1
            continue
        out.append(np.asarray(stat(ff), float))
    return np.array(out), failed


def interval(samples: np.ndarray, alpha: float = 0.05) -> tuple[float, float]:
    """Percentiles sans interpolation : supporte les valeurs infinies (période de retour infinie)."""
    lo = np.quantile(samples, alpha / 2, method="inverted_cdf")
    hi = np.quantile(samples, 1 - alpha / 2, method="inverted_cdf")
    return float(lo), float(hi)
