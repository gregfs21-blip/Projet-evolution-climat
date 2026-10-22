import unittest

import numpy as np

from etl.stats.trend import annual_trend


class TrendTest(unittest.TestCase):
    def test_pente_lineaire_exacte(self):
        years = list(range(1961, 2021))
        values = [0.02 * (y - 1961) for y in years]
        t = annual_trend(years, values)
        self.assertAlmostEqual(t.slope_per_decade, 0.2, places=6)
        self.assertTrue(t.significant)
        self.assertAlmostEqual(t.fitted_start, 0.0, places=6)
        self.assertAlmostEqual(t.fitted_end, 0.02 * 59, places=6)

    def test_bruit_blanc_non_significatif(self):
        rng = np.random.default_rng(0)
        years = list(range(1961, 2021))
        t = annual_trend(years, rng.normal(0, 1, len(years)).tolist())
        self.assertFalse(t.significant)

    def test_lacunes_ignorees(self):
        years = list(range(2000, 2020))
        values = [float(i) for i in range(20)]
        values[5] = None
        t = annual_trend(years, values)
        self.assertAlmostEqual(t.slope_per_decade, 10.0, places=6)

    def test_serie_trop_courte(self):
        with self.assertRaises(ValueError):
            annual_trend([2000, 2001, 2002], [1.0, 2.0, 3.0])


if __name__ == "__main__":
    unittest.main()
