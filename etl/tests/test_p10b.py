"""P10.2 : GEV non stationnaire, périodes de retour, rapports de probabilité, construction de la série (calculs purs)."""

import unittest

import numpy as np
from scipy import stats

from etl import demo_extremes as E
from etl.stats import gev


class TestGev(unittest.TestCase):
    def test_stationary_fit_equals_scipy(self):
        x = stats.genextreme.rvs(0.2, loc=35, scale=1.8, size=80, random_state=3)  # scipy c = 0,2 → ξ = −0,2
        f = gev.fit(x, np.zeros(80), stationary=True)
        c, loc, scale = stats.genextreme.fit(x)
        self.assertAlmostEqual(f.mu0, loc, places=3)
        self.assertAlmostEqual(f.sigma, scale, places=3)
        self.assertAlmostEqual(f.xi, -c, places=3)
        self.assertEqual(f.alpha, 0.0)

    def test_recovers_shift_and_detects_it(self):
        g = np.linspace(-0.2, 1.2, 73)
        x = stats.genextreme.rvs(0.25, loc=34 + 3.0 * g, scale=1.6, size=73, random_state=5)
        f = gev.fit(x, g)
        self.assertLess(abs(f.alpha - 3.0), 1.5)
        self.assertLess(f.xi, 0)
        self.assertLess(gev.likelihood_ratio_p(x, g), 0.01)
        # sans décalage, pas de détection à tort sur ce tirage
        x0 = stats.genextreme.rvs(0.25, loc=34, scale=1.6, size=73, random_state=6)
        self.assertGreater(gev.likelihood_ratio_p(x0, g), 0.05)

    def test_return_level_and_exceedance_are_inverse(self):
        f = gev.GevFit(mu0=34.0, alpha=3.0, sigma=1.7, xi=-0.3, loglik=0.0, stationary=False)
        for g in (0.0, 1.0):
            for T in (2, 20, 100):
                x = float(f.return_level(T, g))
                self.assertAlmostEqual(f.exceedance(x, g), 1 / T, places=10)
        # au-delà de la borne supérieure : probabilité nulle, période de retour infinie
        b = f.upper_bound(0.0)
        self.assertAlmostEqual(b, 34.0 + 1.7 / 0.3)
        self.assertEqual(f.exceedance(b + 0.1, 0.0), 0.0)
        self.assertEqual(E.rp(0.0), np.inf)

    def test_probability_ratio_conventions(self):
        self.assertEqual(E.pr(0.1, 0.01), 10)
        self.assertEqual(E.pr(0.1, 0.0), np.inf)
        self.assertTrue(np.isnan(E.pr(0.0, 0.0)))

    def test_interval_handles_infinity(self):
        s = np.array([10.0] * 50 + [np.inf] * 50)
        lo, hi = gev.interval(s)
        self.assertEqual(lo, 10.0)
        self.assertEqual(hi, np.inf)
        u = E.unbounded(np.inf, np.concatenate([s, [np.nan]]))
        self.assertIsNone(u.value)
        self.assertIsNone(u.ci_high)
        self.assertEqual(u.ci_low, 10.0)
        self.assertEqual(u.undefined_draws, 1)

    def test_bootstrap_is_reproducible(self):
        g = np.linspace(0, 1, 40)
        x = stats.genextreme.rvs(0.2, loc=30 + 2 * g, scale=1.5, size=40, random_state=9)
        a, fa = gev.bootstrap(x, g, 20, 7, lambda f: f.alpha)
        b, fb = gev.bootstrap(x, g, 20, 7, lambda f: f.alpha)
        np.testing.assert_array_equal(a, b)
        self.assertEqual(fa, fb)

    def test_rejects_short_or_missing(self):
        with self.assertRaises(ValueError):
            gev.fit([30.0] * 10, [0.0] * 10)
        with self.assertRaises(ValueError):
            gev.fit([30.0] * 30 + [np.nan], [0.0] * 31)


class TestSeries(unittest.TestCase):
    def setUp(self):
        Y = E.Year
        self.st = E.StationMaxima("x", "Test", 2000, {
            1950: Y(35.0, "1950-07-01", 33.0, "raw", 35.0),
            1953: Y(36.0, "1953-07-01", 34.0, "homogenized", 35.3),
            1954: Y(34.0, "1954-07-01", 32.0, "homogenized", 33.3),
            1955: Y(33.0, "1955-07-01", 31.0, "raw", 33.0),          # trou au milieu : non pris
            2001: Y(37.0, "2001-07-01", 35.0, "homogenized", 37.04),
            2022: Y(40.5, "2022-06-18", 38.5, "homogenized", 40.5),
            2023: Y(39.4, "2023-08-23", 38.5, "raw", 39.4),
            2025: Y(41.6, "2025-08-11", 39.3, "raw", 41.6),
        })

    def test_extension_after_last_homogenized_year_only(self):
        vals, raw = self.st.series()
        self.assertEqual(sorted(vals), [1953, 1954, 2001, 2022, 2023, 2025])
        self.assertEqual(raw, [2023, 2025])
        vals, raw = self.st.series(extend=False)
        self.assertEqual(sorted(vals), [1953, 1954, 2001, 2022])
        self.assertEqual(self.st.series(index="tx3x")[0][2025], 39.3)

    def test_extension_check_uses_years_after_break(self):
        self.assertAlmostEqual(self.st.ext_diff(), 0.04)  # 2001 et 2022 seulement (après la rupture de 2000)

    def test_smoothing_uses_no_future_year(self):
        g = {y: float(y - 2000) for y in range(2000, 2010)}
        s = E.smoothed(g)
        self.assertNotIn(2002, s)
        self.assertEqual(s[2003], 1.5)        # moyenne 2000-2003
        self.assertEqual(s[2009], 7.5)        # moyenne 2006-2009

    def test_tx3_requires_three_consecutive_days(self):
        days = {"2025-08-10": 39.0, "2025-08-11": 41.6, "2025-08-12": 39.4, "2025-08-20": 45.0}
        self.assertAlmostEqual(E.tx3(days, 2025), (39.0 + 41.6 + 39.4) / 3)


if __name__ == "__main__":
    unittest.main()
