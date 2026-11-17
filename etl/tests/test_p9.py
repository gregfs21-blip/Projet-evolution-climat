"""P9 : zones de Caesar sur la grille EN4, couche 0-700 m, moyenne pondérée (calculs purs)."""

import unittest

import numpy as np

from etl.sources import en4 as E


class TestEN4(unittest.TestCase):
    lat = np.arange(-83.0, 89.1, 1.0)
    lon = np.arange(1.0, 360.1, 1.0)

    def test_grid_comments_ignored(self):
        self.assertEqual(E.read_grid("# grille\n65.50 -59.50\n\n65.50 -58.50\n"), [(65.5, -59.5), (65.5, -58.5)])

    def test_one_caesar_cell_covers_four_quarters(self):
        w = E.zone_weights([(40.5, -60.5)], self.lat, self.lon)
        i40, i41 = list(self.lat).index(40.0), list(self.lat).index(41.0)
        j299, j300 = list(self.lon).index(299.0), list(self.lon).index(300.0)
        self.assertEqual(np.count_nonzero(w), 4)
        self.assertAlmostEqual(w[i40, j299], 0.25 * np.cos(np.radians(40.0)))
        self.assertAlmostEqual(w[i41, j300], 0.25 * np.cos(np.radians(41.0)))

    def test_full_block_gives_full_inner_cell(self):
        cells = [(la + 0.5, lo + 0.5) for la in (39, 40) for lo in (-61, -60)]
        w = E.zone_weights(cells, self.lat, self.lon)
        self.assertAlmostEqual(w[list(self.lat).index(40.0), list(self.lon).index(300.0)], np.cos(np.radians(40.0)))

    def test_greenwich_wraps(self):
        w = E.zone_weights([(50.5, -0.5)], self.lat, self.lon)
        self.assertGreater(w[list(self.lat).index(50.0), list(self.lon).index(360.0)], 0)

    def test_layer_cut_at_700(self):
        b = np.array([[0, 10], [10, 600], [600, 750], [750, 900]], float)
        np.testing.assert_allclose(E.layer_thickness(b), [10, 590, 100, 0])

    def test_weighted_mean_skips_land(self):
        f = np.array([[[1.0, np.nan]], [[3.0, 5.0]]])           # (niveau, lat, lon)
        w2d = np.array([[1.0, 1.0]])
        self.assertAlmostEqual(E.weighted_mean(f, w2d, np.array([1.0, 3.0])), (1 + 9 + 15) / 7)


if __name__ == "__main__":
    unittest.main()


class TestRapidAndN7(unittest.TestCase):
    def test_depth_of_max(self):
        from etl.sources import rapid as R
        depth = np.array([0.0, 500.0, 1000.0, 1500.0, 3000.0])
        self.assertEqual(R.depth_of_max(np.array([0.0, 10.0, 17.0, 12.0, -5.0]), depth), 1000.0)
        self.assertTrue(np.isnan(R.depth_of_max(np.array([np.nan] * 5), depth)))

    def test_annual_needs_ten_months(self):
        from etl.sources import rapid as R
        months = {f"2004-{m:02d}": 15.0 for m in range(4, 13)} | {f"2005-{m:02d}": float(m) for m in range(1, 13)}
        series, counts = R.annual(months)
        self.assertEqual(counts, {2004: 9, 2005: 12})
        self.assertEqual(series, {2005: 6.5})

    def test_n7_start_requires_staying_above(self):
        w = {1950: 0.6, 1951: 0.4, 1952: 0.55, 1953: 0.7, 1954: 0.49, 1955: 0.8, 1956: 0.9}
        self.assertEqual(E.n7_start(w), 1955)
        self.assertIsNone(E.n7_start({2000: 0.2}))
