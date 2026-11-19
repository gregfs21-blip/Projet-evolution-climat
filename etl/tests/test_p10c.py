"""P10.3 : facteur d'amplification, saisons, contrôles (calculs purs, sans données Météo-France)."""

import unittest

import numpy as np

from etl import demo_amplification as A


def ar1(n: int, rho: float, sd: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    e = np.zeros(n)
    for t in range(n):
        e[t] = (rho * e[t - 1] if t else 0.0) + rng.normal(0, sd)
    return e


class TestFit(unittest.TestCase):
    def test_recovers_k(self):
        years = list(range(1953, 2025))
        g = {y: 0.015 * (y - 1953) + 0.05 * np.sin(y) for y in years}
        noise = ar1(len(years), 0.3, 0.35, 4)
        reg = {y: 0.2 + 1.7 * g[y] + noise[i] for i, y in enumerate(years)}
        f = A.fit_k(reg, g)
        self.assertLess(f.lo, 1.7)
        self.assertGreater(f.hi, 1.7)
        self.assertAlmostEqual(f.k, 1.7, delta=0.4)
        self.assertEqual(len(f.fitted), len(years))
        self.assertEqual(f.years[0], 1953)

    def test_coverage_is_reasonable(self):
        years = list(range(1959, 2025))
        g = {y: 0.017 * (y - 1959) for y in years}
        hits = 0
        for seed in range(200):
            noise = ar1(len(years), 0.3, 0.4, seed)
            f = A.fit_k({y: 1.5 * g[y] + noise[i] for i, y in enumerate(years)}, g)
            hits += f.lo <= 1.5 <= f.hi
        self.assertGreater(hits / 200, 0.88)

    def test_rejects_gaps_and_missing_covariate(self):
        g = {y: 0.01 * y for y in range(1950, 2025)}
        reg = {y: 0.02 * y + (y % 3) * 0.1 for y in range(1960, 2025) if y != 1990}
        with self.assertRaises(ValueError):
            A.fit_k(reg, g)
        with self.assertRaises(ValueError):
            A.fit_k({y: 1.0 + (y % 2) for y in range(1940, 2000)}, g)


class TestLjungBox(unittest.TestCase):
    def test_white_noise_passes_and_ar1_fails(self):
        self.assertGreater(A.ljung_box_p(np.random.default_rng(1).normal(size=72)), 0.05)
        self.assertLess(A.ljung_box_p(ar1(72, 0.7, 1.0, 2)), 0.01)


class TestSeasons(unittest.TestCase):
    def test_winter_uses_previous_december(self):
        mon = {(2000, 12): 5.0, (2001, 1): 3.0, (2001, 2): 4.0, (2001, 6): 20.0, (2001, 7): 22.0, (2001, 8): 21.0,
               (2002, 1): 2.0, (2002, 2): 3.0}
        hom = {k: True for k in mon}
        hom[(2001, 7)] = False
        w, wh = A.season_values(mon, hom, "hiver")
        self.assertEqual(w, {2001: 4.0})           # 2002 incomplet (pas de décembre 2001)
        self.assertEqual(wh, {2001})
        s, sh = A.season_values(mon, hom, "ete")
        self.assertEqual(s, {2001: 21.0})
        self.assertEqual(sh, set())                 # juillet non homogénéisé

    def test_anomaly_requires_full_base(self):
        full = {y: float(y - 1950) for y in range(1955, 2000)}
        a = A.anomaly(full)
        self.assertAlmostEqual(a[1961] + a[1990], 0.0)
        with self.assertRaises(ValueError):
            A.anomaly({y: 1.0 for y in range(1965, 2000)})


class TestHelpers(unittest.TestCase):
    def test_raw_tail_and_overlap(self):
        years = list(range(2018, 2025))
        self.assertTrue(A.contiguous_raw_tail(years, {2018, 2019, 2020, 2021, 2022}))
        self.assertFalse(A.contiguous_raw_tail(years, {2018, 2020, 2021, 2022}))
        self.assertTrue(A.contiguous_raw_tail(years, set(years)))
        self.assertTrue(A.overlap((1.0, 2.0), (1.9, 3.0)))
        self.assertFalse(A.overlap((1.0, 1.2), (1.3, 2.0)))


if __name__ == "__main__":
    unittest.main()
