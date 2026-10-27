"""P2b : correction B′, indices de pluie, F8, ETP de Hargreaves, SPEI (données synthétiques)."""

import math
import unittest

import numpy as np

from etl.indicators import eau as E
from etl.indicators import pluie as P


def month_days(y, m, value=0.0):
    return {d: value for d in P.days_of(y, m)}


class TestCorrection(unittest.TestCase):
    def test_factor_restores_monthly_total(self):
        raw = {}
        for m in range(1, 13):
            raw.update(month_days(2000, m, 1.0))
        lsh_v = {(2000, m): 2.0 * len(P.days_of(2000, m)) for m in range(1, 13)}
        corr, status, f = P.correct(raw, lsh_v, {k: True for k in lsh_v})
        self.assertEqual(status, {2000: "homogenized"})
        for m in range(1, 13):                                            # F5 par construction
            self.assertAlmostEqual(sum(corr[d] for d in P.days_of(2000, m)), lsh_v[(2000, m)])
        self.assertEqual(set(f.values()), {2.0})

    def test_incomplete_or_inconsistent_month_not_corrected(self):
        raw = {}
        for m in range(1, 13):
            raw.update(month_days(2000, m, 1.0))
        del raw["2000-03-05"]                                             # ETCCDI ok, mais mois incomplet
        lsh_v = {(2000, m): 30.0 for m in range(1, 13)}
        _, status, f = P.correct(raw, lsh_v, {k: True for k in lsh_v})
        self.assertEqual(status, {2000: "raw"})
        self.assertNotIn((2000, 3), f)
        raw["2000-03-05"] = 1.0
        lsh_v[(2000, 4)] = 0.0                                            # pluie brute, LSH nul : non corrigeable
        _, status, _ = P.correct(raw, lsh_v, {k: True for k in lsh_v})
        self.assertEqual(status, {2000: "raw"})

    def test_indices(self):
        days = [0.0] * 365
        days[10], days[11], days[12], days[13], days[14] = 25.0, 12.0, 5.0, 3.0, 1.0
        days[100] = None
        self.assertEqual(P.INDICES["r10mm"].compute(days), 2.0)
        self.assertEqual(P.INDICES["r20mm"].compute(days), 1.0)
        self.assertEqual(P.INDICES["rx1day"].compute(days), 25.0)
        self.assertEqual(P.INDICES["rx5day"].compute(days), 46.0)


class TestF8(unittest.TestCase):
    def test_no_break_no_object(self):
        self.assertEqual(P.f8({}, [], None, "jours")["status"], "sans objet")

    def test_detects_offset_before_last_break(self):
        rng = np.random.default_rng(1)
        others = [{y: 20 + float(rng.normal(0, 1)) for y in range(1950, 2018)} for _ in range(3)]
        mine = {y: 20 + float(rng.normal(0, 1)) + (6 if y < 1975 else 0) for y in range(1950, 2018)}
        self.assertEqual(P.f8(mine, others, 1995, "jours")["status"], "rupture")
        clean = {y: 20 + float(rng.normal(0, 1)) for y in range(1950, 2018)}
        self.assertEqual(P.f8(clean, others, 1995, "jours")["status"], "conforme")


class TestWater(unittest.TestCase):
    def test_ra_fao56_example(self):
        self.assertAlmostEqual(E.ra_doy(-20.0, 246), 32.2, places=1)     # FAO-56, exemple 8

    def test_hargreaves_magnitude(self):
        self.assertTrue(130 < E.etp_month(16.0, 27.0, 44.8, 2000, 7) < 180)
        self.assertEqual(E.etp_month(10.0, 9.0, 44.8, 2000, 7), 0.0)        # amplitude négative : ETP nulle

    def test_spei_standardised_on_calibration(self):
        rng = np.random.default_rng(0)
        d = {(y, m): float(rng.normal(-20 if m in (6, 7, 8) else 40, 30)) for y in range(1962, 2018) for m in range(1, 13)}
        for k in (3, 12):
            s = E.spei(d, k)
            vals = [v for (y, m), v in s.items()]
            self.assertLess(abs(np.mean(vals)), 0.05)                    # F10
            self.assertLess(abs(np.std(vals) - 1), 0.1)

    def test_accumulate_breaks_on_missing_month(self):
        d = {(2000, m): 1.0 for m in range(1, 13)}
        del d[(2000, 6)]
        acc = E.accumulate(d, 3)
        self.assertNotIn((2000, 7), acc)
        self.assertEqual(acc[(2000, 12)], 3.0)


if __name__ == "__main__":
    unittest.main()
