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
