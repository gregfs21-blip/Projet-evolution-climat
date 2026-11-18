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


# ---------------------------------------------------------------- lecteurs (formats de la sonde du 17/11/2026)

from etl import demonstration as D  # noqa: E402
from etl.sources import igcc as I  # noqa: E402

ERF_TXT = """﻿time,timebound_lower,timebound_upper,CO2,solar,volcanic,anthro,total,minor
1750.5,1750,1751,0,0.02159121,0.234943996,0,0.256535206,0
1751.5,1751,1752,0.001417292,0.000780029,0.243453584,0.005577837,0.249811451,-0.000441816
"""

PSL_TXT = """            1870        2026
   1870    -1.00   -1.20   -0.83   -0.81   -1.27   -1.08   -1.04   -0.88   -0.53   -0.92   -0.79   -0.79
   2026    -0.54   -0.25   -0.12    0.38    0.80    1.37    1.90    2.37    2.63  -99.99  -99.99  -99.99
    -99.99
    NINA34
"""

ONI_TXT = """SEAS  YR   TOTAL   ANOM
  DJF 1950   24.72  -1.53
  NDJ 1950   25.20  -0.85
  DJF 1951   25.24  -0.82
"""


class TestReaders(unittest.TestCase):
    def test_erf(self):
        erf = I.parse_erf(ERF_TXT)
        self.assertEqual(sorted(erf), [1750, 1751])
        self.assertAlmostEqual(erf[1751]["anthro"], 0.005577837)
        self.assertAlmostEqual(erf[1750]["volcanic"], 0.234943996)
        with self.assertRaises(ValueError):
            I.parse_erf(ERF_TXT.replace("anthro", "anthropogenic"))

    def test_psl_missing_values_dropped(self):
        n = I.parse_psl_monthly(PSL_TXT)
        self.assertEqual(n[(1870, 1)], -1.0)
        self.assertEqual(n[(2026, 9)], 2.63)
        self.assertNotIn((2026, 10), n)
        self.assertEqual(len(n), 21)

    def test_oni_centre_month(self):
        o = I.parse_oni_monthly(ONI_TXT)
        self.assertEqual(o[(1950, 1)], -1.53)
        self.assertEqual(o[(1950, 12)], -0.85)
        self.assertEqual(o[(1951, 1)], -0.82)


class TestEnsoAndLags(unittest.TestCase):
    def test_moving_climatology_removes_trend_and_constant(self):
        # Anomalie = tendance lente + constante + oscillation de période 4 ans : l'indice garde l'oscillation.
        anom = {}
        for y in range(1870, 2026):
            for m in range(1, 13):
                t = y + (m - 1) / 12
                anom[(y, m)] = 0.01 * (y - 1870) + 3.0 + np.sin(2 * np.pi * t / 4)
        idx = D.enso_index(anom)
        mid = [idx[(y, m)] - np.sin(2 * np.pi * (y + (m - 1) / 12) / 4) for y in range(1900, 1990) for m in range(1, 13)]
        self.assertLess(max(abs(x) for x in mid), 0.06)
        # bords : fenêtre décalée de 30 ans, jamais tronquée (1870 → base 1870-1899 ; 2025 → base 1996-2025)
        self.assertAlmostEqual(idx[(1870, 1)], anom[(1870, 1)] - np.mean([anom[(y, 1)] for y in range(1870, 1900)]), places=10)
        self.assertAlmostEqual(idx[(2025, 7)], anom[(2025, 7)] - np.mean([anom[(y, 7)] for y in range(1996, 2026)]), places=10)
        # milieu : base a − 15 à a + 14
        self.assertAlmostEqual(idx[(1950, 3)], anom[(1950, 3)] - np.mean([anom[(y, 3)] for y in range(1935, 1965)]), places=10)

    def test_lagged_mean_window(self):
        monthly = {(y, m): 100 * y + m for y in (2000, 2001) for m in range(1, 13)}
        # décalage 3 : octobre 2000 à septembre 2001
        self.assertAlmostEqual(D.lagged_mean(monthly, 2001, 3), np.mean([200010, 200011, 200012] + [200100 + m for m in range(1, 10)]))
        self.assertAlmostEqual(D.lagged_mean(monthly, 2001, 0), np.mean([200100 + m for m in range(1, 13)]))
        self.assertIsNone(D.lagged_mean(monthly, 2000, 3))

    def test_volcanic_lag(self):
        v = {2000: -1.0, 2001: 0.0}
        self.assertEqual(D.volcanic_lagged(v, 2001, 0), 0.0)
        self.assertEqual(D.volcanic_lagged(v, 2001, 6), -0.5)
        self.assertEqual(D.volcanic_lagged(v, 2001, 12), -1.0)
        self.assertIsNone(D.volcanic_lagged(v, 2000, 6))


class TestRegressionRun(unittest.TestCase):
    """Données synthétiques : la régression retrouve les coefficients et le réchauffement attribué attendu."""

    def setUp(self):
        rng = np.random.default_rng(42)
        years = range(1750, 2026)
        self.erf = {}
        for y in years:
            a = 0.0 if y < 1850 else 3.0 * ((y - 1850) / 175) ** 2
            v = -2.0 if y in (1883, 1902, 1963, 1982, 1991) else 0.2
            s = 0.1 * np.sin(2 * np.pi * y / 11)
            self.erf[y] = {"anthro": a, "volcanic": v, "solar": s, "total": a + v + s}
        self.enso = {(y, m): float(rng.normal(0, 1)) for y in range(1869, 2026) for m in range(1, 13)}
        inp = D.Inputs(self.erf, {y: r["anthro"] for y, r in self.erf.items()}, self.enso)
        self.inp = inp
        noise = ar1(len(range(1871, 2026)), 0.4, 0.05, rng)
        self.temp = {}
        for i, y in enumerate(range(1871, 2026)):
            self.temp[y] = (-0.3 + 0.45 * inp.anthro[y] + 0.15 * D.volcanic_lagged({k: r["volcanic"] for k, r in self.erf.items()}, y, 6)
                            + 0.1 * self.erf[y]["solar"] + 0.08 * D.lagged_mean(self.enso, y, 3) + noise[i])

    def test_recovers_and_attributes(self):
        run = D.regress(self.temp, self.inp)
        self.assertEqual(run.years[0], 1871)
        b, se = run.fit.get("anthropique")
        self.assertLess(abs(b - 0.45), 3 * se)
        a, lo, hi = run.attributable((2016, 2025))
        dA = np.mean([self.erf[y]["anthro"] for y in range(2016, 2026)]) - np.mean([self.erf[y]["anthro"] for y in range(1850, 1901)])
        self.assertAlmostEqual(a, b * dA, places=10)
        self.assertLess(abs(a - 0.45 * dA), 3 * se * dA)
        self.assertLess(lo, a)
        self.assertGreater(hi, a)

    def test_gap_in_middle_is_refused(self):
        temp = dict(self.temp)
        del temp[1950]
        with self.assertRaises(ValueError):
            D.regress(temp, self.inp)


class TestFormat(unittest.TestCase):
    def test_half_up_like_the_site(self):
        self.assertEqual(D._f(0.1795, 3), "0,180")
        self.assertEqual(D._f(1.115, 2), "1,12")
        self.assertEqual(D._f(-0.32, 3), "−0,320")
        self.assertEqual(D._f(-0.0004, 3, True), "+0,000")
        self.assertEqual(D._f(0.0333, 2, True), "+0,03")
