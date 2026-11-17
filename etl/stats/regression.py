"""Régression linéaire multiple sur séries annuelles, avec erreurs autocorrélées (P10.1).

- Estimation principale : moindres carrés généralisés faisables à erreurs AR(1), méthode de Prais et Winsten (1954),
  itérée jusqu'à convergence de ρ. Contrairement à Cochrane-Orcutt, la première année est conservée (pondérée par
  √(1 − ρ²)). Intervalles et p sur une loi de Student à n − k − 1 degrés de liberté (k coefficients, constante
  comprise, et un degré de plus pour ρ estimé).
- Contrôle publié pour information : moindres carrés ordinaires, erreurs types de Newey et West (1987), noyau de
  Bartlett, décalage ⌊4·(n/100)^(2/9)⌋.

Aucune dépendance au-delà de numpy et scipy : le calcul reste lisible et recoupé par les tests (etl/tests/test_p10.py).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats

MAX_ITER = 100
TOL = 1e-8


@dataclass(frozen=True)
class Fit:
    method: str
    names: list[str]          # constante en premier
    coef: np.ndarray
    cov: np.ndarray           # matrice de covariance des coefficients
    se: np.ndarray
    dof: int
    rho: float                # autocorrélation d'ordre 1 des résidus (AR(1) estimé, ou résidus MCO)
    resid: np.ndarray         # résidus dans l'espace d'origine (y − Xβ)
    fitted: np.ndarray        # Xβ
    r2: float                 # part de la variance de y expliquée par Xβ (espace d'origine)
    iterations: int

    def ci(self, alpha: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
        q = stats.t.ppf(1 - alpha / 2, self.dof)
        return self.coef - q * self.se, self.coef + q * self.se

    def p_values(self) -> np.ndarray:
        t = self.coef / self.se
        return 2 * stats.t.sf(np.abs(t), self.dof)

    def get(self, name: str) -> tuple[float, float]:
        i = self.names.index(name)
        return float(self.coef[i]), float(self.se[i])

    def combination(self, weights: dict[str, float], alpha: float = 0.05) -> tuple[float, float, float]:
        """Combinaison linéaire Σ wᵢ·βᵢ : (valeur, borne basse, borne haute), covariance des coefficients comprise."""
        g = np.zeros(len(self.coef))
        for name, w in weights.items():
            g[self.names.index(name)] = w
        value = float(g @ self.coef)
        half = float(stats.t.ppf(1 - alpha / 2, self.dof) * np.sqrt(g @ self.cov @ g))
        return value, value - half, value + half


def _design(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X[:, None]
    return np.column_stack([np.ones(len(X)), X])


def _check(y: np.ndarray, X: np.ndarray) -> None:
    if not (np.all(np.isfinite(y)) and np.all(np.isfinite(X))):
        raise ValueError("régression : valeur manquante ou non finie (aucune valeur n'est complétée)")
    n, k = X.shape
    if n < k + 10:
        raise ValueError(f"régression : {n} années pour {k} coefficients, série trop courte")
    if np.linalg.matrix_rank(X) < k:
        raise ValueError("régression : variables explicatives colinéaires (matrice de rang incomplet)")


def _r2(y: np.ndarray, fitted: np.ndarray) -> float:
    return float(1 - np.sum((y - fitted) ** 2) / np.sum((y - y.mean()) ** 2))


def lag1(e: np.ndarray) -> float:
    """Autocorrélation d'ordre 1 (estimateur de Prais-Winsten : Σ e_t e_{t−1} / Σ e_{t−1}²)."""
    return float(np.sum(e[1:] * e[:-1]) / np.sum(e[:-1] ** 2))


def prais_winsten(y, X, names: list[str]) -> Fit:
    """MCG faisables AR(1), Prais-Winsten itéré. `X` sans constante ; `names` nomme ses colonnes."""
    y = np.asarray(y, dtype=float)
    Xc = _design(X)
    _check(y, Xc)
    n, k = Xc.shape
    beta = np.linalg.lstsq(Xc, y, rcond=None)[0]
    rho = 0.0
    it = 0
    for it in range(1, MAX_ITER + 1):
        e = y - Xc @ beta
        new = lag1(e)
        if not -1 < new < 1:
            raise ValueError(f"Prais-Winsten : ρ = {new:.3f} hors de ]−1 ; 1[ (résidus non stationnaires)")
        ys, Xs = _transform(y, Xc, new)
        beta = np.linalg.lstsq(Xs, ys, rcond=None)[0]
        converged = abs(new - rho) < TOL
        rho = new
        if converged:
            break
    else:
        raise ValueError("Prais-Winsten : ρ ne converge pas")
    ys, Xs = _transform(y, Xc, rho)
    us = ys - Xs @ beta
    dof = n - k - 1
    sigma2 = float(us @ us) / dof
    cov = sigma2 * np.linalg.inv(Xs.T @ Xs)
    fitted = Xc @ beta
    return Fit("Prais-Winsten AR(1) itéré", ["constante", *names], beta, cov, np.sqrt(np.diag(cov)), dof, rho,
               y - fitted, fitted, _r2(y, fitted), it)


def _transform(y: np.ndarray, X: np.ndarray, rho: float) -> tuple[np.ndarray, np.ndarray]:
    w = np.sqrt(1 - rho ** 2)
    ys = np.concatenate([[w * y[0]], y[1:] - rho * y[:-1]])
    Xs = np.vstack([w * X[0], X[1:] - rho * X[:-1]])
    return ys, Xs


def newey_west_lag(n: int) -> int:
    return int(np.floor(4 * (n / 100) ** (2 / 9)))


def ols_newey_west(y, X, names: list[str], lag: int | None = None) -> Fit:
    """MCO, erreurs types de Newey-West (Bartlett). Loi de Student à n − k degrés de liberté."""
    y = np.asarray(y, dtype=float)
    Xc = _design(X)
    _check(y, Xc)
    n, k = Xc.shape
    L = newey_west_lag(n) if lag is None else lag
    beta = np.linalg.lstsq(Xc, y, rcond=None)[0]
    e = y - Xc @ beta
    xe = Xc * e[:, None]
    S = xe.T @ xe
    for j in range(1, L + 1):
        w = 1 - j / (L + 1)
        G = xe[j:].T @ xe[:-j]
        S += w * (G + G.T)
    bread = np.linalg.inv(Xc.T @ Xc)
    cov = bread @ S @ bread * n / (n - k)
    fitted = Xc @ beta
    return Fit(f"MCO, erreurs de Newey-West (décalage {L})", ["constante", *names], beta, cov, np.sqrt(np.diag(cov)),
               n - k, lag1(e), e, fitted, _r2(y, fitted), 0)


def vif(X) -> np.ndarray:
    """Facteurs d'inflation de la variance de chaque colonne de X (sans constante)."""
    X = np.asarray(X, dtype=float)
    out = []
    for j in range(X.shape[1]):
        others = _design(np.delete(X, j, axis=1))
        b = np.linalg.lstsq(others, X[:, j], rcond=None)[0]
        r2 = _r2(X[:, j], others @ b)
        out.append(np.inf if r2 >= 1 else 1 / (1 - r2))
    return np.array(out)
