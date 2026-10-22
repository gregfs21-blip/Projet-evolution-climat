import unittest

import numpy as np

from etl.stats.trend import annual_trend, ols_slope_per_decade


class TrendTest(unittest.TestCase):
    def test_pente_lineaire_exacte(self):
        years = list(range(1961, 2021))
        t = annual_trend(years, [0.02 * (y - 1961) for y in years])
        self.assertAlmostEqual(t.slope_per_decade, 0.2, places=6)
        self.assertTrue(t.significant)
        self.assertAlmostEqual(t.fitted_end - t.fitted_start, 0.02 * 59, places=6)

    def test_bruit_blanc_non_significatif(self):
        years = list(range(1961, 2021))
        t = annual_trend(years, np.random.default_rng(0).normal(0, 1, len(years)).tolist())
        self.assertFalse(t.significant)

    def test_autocorrelation_affaiblit_la_significativite(self):
        # Marche aléatoire (fortement autocorrélée, sans tendance) : Hamed-Rao doit être
        # nettement moins affirmatif que le test classique.
        rng = np.random.default_rng(11)
        years = list(range(1950, 2020))
        x = np.cumsum(rng.normal(0, 0.3, len(years))).tolist()
        t = annual_trend(years, x)
        self.assertGreater(t.p_value, t.p_value_classical)

    def test_lacune_refusee(self):
        years = list(range(2000, 2020))
        values = [float(i) for i in range(20)]
        values[5] = None
        with self.assertRaises(ValueError):
            annual_trend(years, values)

    def test_serie_trop_courte(self):
        with self.assertRaises(ValueError):
            annual_trend([2000, 2001, 2002], [1.0, 2.0, 3.0])

    def test_ols(self):
        years = list(range(1959, 2020))
        self.assertAlmostEqual(ols_slope_per_decade(years, [0.05 * y for y in years]), 0.5, places=9)


if __name__ == "__main__":
    unittest.main()
