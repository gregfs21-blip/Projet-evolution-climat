"""P10.1 : régression multiple à erreurs AR(1) (Prais-Winsten), Newey-West, indice ENSO, décalages (calculs purs)."""

import unittest

import numpy as np

from etl.stats import regression as R


def ar1(n: int, rho: float, sigma: float, rng: np.random.Generator) -> np.ndarray:
    e = np.empty(n)
    e[0] = rng.normal(0, sigma / np.sqrt(1 - rho ** 2))
    for t in range(1, n):
        e[t] = rho * e[t - 1] + rng.normal(0, sigma)
    return e


class TestPraisWinsten(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(10)
        n = 150
        self.x1 = np.linspace(0, 3, n) + rng.normal(0, 0.1, n)
        self.x2 = rng.normal(0, 1, n)
        self.X = np.column_stack([self.x1, self.x2])
        self.beta = np.array([-0.3, 0.45, 0.08])
        self.y = self.beta[0] + self.X @ self.beta[1:] + ar1(n, 0.5, 0.1, rng)

    def test_equals_exact_gls_at_estimated_rho(self):
        """À convergence, Prais-Winsten = MCG avec la matrice de covariance AR(1) de ρ estimé (formule fermée)."""
        fit = R.prais_winsten(self.y, self.X, ["a", "b"])
        n = len(self.y)
        idx = np.arange(n)
        V = fit.rho ** np.abs(idx[:, None] - idx[None, :]) / (1 - fit.rho ** 2)
        Vi = np.linalg.inv(V)
        Xc = np.column_stack([np.ones(n), self.X])
        b = np.linalg.solve(Xc.T @ Vi @ Xc, Xc.T @ Vi @ self.y)
        np.testing.assert_allclose(fit.coef, b, rtol=1e-8, atol=1e-10)
        # ρ est bien l'autocorrélation des résidus du β final (point fixe)
        self.assertAlmostEqual(fit.rho, R.lag1(self.y - Xc @ fit.coef), places=7)

    def test_recovers_coefficients(self):
        fit = R.prais_winsten(self.y, self.X, ["a", "b"])
        lo, hi = fit.ci()
        self.assertTrue(np.all((lo <= self.beta) & (self.beta <= hi)), (lo, hi))
        self.assertAlmostEqual(fit.rho, 0.5, delta=0.15)
        self.assertEqual(fit.dof, len(self.y) - 3 - 1)
        self.assertEqual(fit.names, ["constante", "a", "b"])

    def test_coverage_is_close_to_nominal(self):
        """Sur 300 tirages AR(1) (ρ = 0,6, n = 120), l'intervalle à 95 % contient la vraie pente dans 88 à 99 % des cas.

        Les MCG faisables sous-couvrent un peu en petit échantillon (ρ estimé biaisé vers 0) : sur 2 000 tirages,
        couverture mesurée de 92 % (ρ = 0,6) à 94 % (ρ = 0,3) pour n = 150. Limite publiée avec le résultat.
        """
        rng = np.random.default_rng(3)
        n, hits = 120, 0
        x = np.linspace(0, 2, n)
        for _ in range(300):
            y = 1 + 0.4 * x + ar1(n, 0.6, 0.1, rng)
            lo, hi = R.prais_winsten(y, x, ["x"]).ci()
            hits += lo[1] <= 0.4 <= hi[1]
        self.assertGreater(hits / 300, 0.88)
        self.assertLess(hits / 300, 0.99)

    def test_ols_understates_uncertainty_under_autocorrelation(self):
        fit = R.prais_winsten(self.y, self.X, ["a", "b"])
        nw0 = R.ols_newey_west(self.y, self.X, ["a", "b"], lag=0)
        self.assertGreater(fit.rho, 0.3)
        self.assertGreater(fit.se[1], nw0.se[1])

    def test_rejects_missing_values_and_collinearity(self):
        y = self.y.copy()
        y[5] = np.nan
        with self.assertRaises(ValueError):
            R.prais_winsten(y, self.X, ["a", "b"])
        with self.assertRaises(ValueError):
            R.prais_winsten(self.y, np.column_stack([self.x1, 2 * self.x1]), ["a", "b"])


class TestNeweyWest(unittest.TestCase):
    def test_lag_zero_is_white_hc1(self):
        rng = np.random.default_rng(1)
        n = 80
        x = rng.normal(size=n)
        y = 2 + 0.5 * x + rng.normal(size=n) * (1 + np.abs(x))
        fit = R.ols_newey_west(y, x, ["x"], lag=0)
        Xc = np.column_stack([np.ones(n), x])
        e = y - Xc @ np.linalg.lstsq(Xc, y, rcond=None)[0]
        bread = np.linalg.inv(Xc.T @ Xc)
        hc1 = bread @ (Xc.T * e ** 2) @ Xc @ bread * n / (n - 2)
        np.testing.assert_allclose(fit.se, np.sqrt(np.diag(hc1)), rtol=1e-10)

    def test_default_lag(self):
        self.assertEqual(R.newey_west_lag(100), 4)
        self.assertEqual(R.newey_west_lag(155), 4)

    def test_vif_orthogonal_is_one(self):
        X = np.column_stack([np.tile([1.0, -1.0], 10), np.repeat([1.0, -1.0], 10)])
        np.testing.assert_allclose(R.vif(X), [1.0, 1.0], atol=1e-12)


if __name__ == "__main__":
    unittest.main()
