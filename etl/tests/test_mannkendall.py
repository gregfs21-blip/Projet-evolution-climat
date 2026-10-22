"""Recoupement des fonctions embarquées avec pymannkendall (installé pour les tests)."""
import unittest

import numpy as np

from etl.stats.mannkendall import hamed_rao_test, original_test

try:
    import pymannkendall as pmk
except ImportError:  # pragma: no cover
    pmk = None


def ar1(phi: float, n: int, seed: int, trend: float = 0.0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + rng.normal()
    return x + trend * np.arange(n)


@unittest.skipIf(pmk is None, "pymannkendall non installé")
class RecoupementTest(unittest.TestCase):
    def test_classique_identique(self):
        for seed in range(10):
            x = ar1(0.3, 70, seed, trend=0.02)
            self.assertAlmostEqual(original_test(x).p, pmk.original_test(x).p, places=12)

    def test_hamed_rao_identique_ou_plus_prudent(self):
        # Le correctif amont (abs) ne change le résultat que si la somme des autocorrélations
        # significatives est négative ; il rend alors le test plus exigeant, jamais plus permissif.
        identical = 0
        for seed in range(20):
            x = ar1(0.6, 70, seed, trend=0.02)
            ours, ref = hamed_rao_test(x), pmk.hamed_rao_modification_test(x)
            if not np.isfinite(ref.p):
                continue  # défaut de la 1.4.3 (variance négative)
            if abs(ours.p - ref.p) < 1e-12:
                identical += 1
            else:
                self.assertGreater(ours.p, ref.p)
        self.assertGreaterEqual(identical, 12)

    def test_jamais_nan(self):
        for seed in range(30):
            self.assertTrue(np.isfinite(hamed_rao_test(ar1(-0.6, 40, seed)).p))

    def test_correction_conservatrice(self):
        for seed in range(30):
            x = ar1(-0.5, 60, seed, trend=0.03)
            self.assertGreaterEqual(hamed_rao_test(x).p, original_test(x).p - 1e-12)


if __name__ == "__main__":
    unittest.main()
