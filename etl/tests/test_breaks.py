import unittest

import numpy as np

from etl.stats.breaks import pettitt


class PettittTest(unittest.TestCase):
    def test_saut_detecte(self):
        rng = np.random.default_rng(3)
        x = np.r_[rng.normal(0, 0.5, 35), rng.normal(1.5, 0.5, 35)]
        r = pettitt(x)
        self.assertLess(r.p_value, 0.01)
        self.assertIn(r.index, range(32, 38))

    def test_bruit_blanc(self):
        r = pettitt(np.random.default_rng(4).normal(0, 1, 70))
        self.assertGreater(r.p_value, 0.05)

    def test_tendance_pure_detectee_puis_effacee(self):
        # Une tendance régulière suffit à rendre Pettitt significatif : d'où le test sur résidus.
        rng = np.random.default_rng(5)
        t = np.arange(70)
        x = 0.03 * t + rng.normal(0, 0.3, 70)
        self.assertLess(pettitt(x).p_value, 0.05)
        resid = x - np.polyval(np.polyfit(t, x, 1), t)
        self.assertGreater(pettitt(resid).p_value, 0.05)

    def test_lacune_refusee(self):
        with self.assertRaises(ValueError):
            pettitt([1.0] * 5 + [np.nan] + [2.0] * 10)


if __name__ == "__main__":
    unittest.main()
