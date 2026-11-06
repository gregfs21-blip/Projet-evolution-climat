"""Tests P8 : test d'accélération, formatage, règles S1-S3 et contrôles M1-M2 de la synthèse."""

import unittest

import numpy as np

from etl import synthese as S
from etl.stats.acceleration import newey_west_lag, quadratic_acceleration


def ind(i, conf="elevee", sig=True, slope=0.3, years=range(1950, 2021), values=None, headline="trend"):
    years = list(years)
    vals = values if values is not None else [0.03 * (y - years[0]) for y in years]
    return {"id": i, "scale": "gironde", "title": i.upper(), "confidence": conf, "headline": headline,
            "series": {"time": [str(y) for y in years], "value": vals},
            "trend": {"slope_per_decade": slope, "slope_ci_low": slope - 0.1, "slope_ci_high": slope + 0.1,
                      "period": {"start": years[0], "end": years[-1]}, "p_value": 0.001 if sig else 0.4,
                      "significant": sig, "fitted_start": 0.0, "fitted_end": 2.1},
            "normals_comparison": None}


class TestAcceleration(unittest.TestCase):
    def test_recovers_known_acceleration(self):
        rng = np.random.default_rng(1)
        t = np.arange(40)
        r = quadratic_acceleration(list(range(1980, 2020)), list(2 * t + 0.04 * t ** 2 + rng.normal(0, 1, 40)))
        self.assertAlmostEqual(r.value, 0.08, delta=0.01)
        self.assertTrue(r.significant)
        self.assertLess(r.rate_start, r.rate_end)

    def test_linear_series_not_significant(self):
        rng = np.random.default_rng(2)
        r = quadratic_acceleration(list(range(1980, 2020)), list(np.arange(40) * 0.5 + rng.normal(0, 1, 40)))
        self.assertFalse(r.significant)

    def test_lag_and_guards(self):
        self.assertEqual(newey_west_lag(32), 2)
        self.assertEqual(newey_west_lag(70), 3)
        with self.assertRaises(ValueError):
            quadratic_acceleration(list(range(2000, 2010)), list(range(10)))
        with self.assertRaises(ValueError):
            quadratic_acceleration([y for y in range(1980, 2010) if y != 1995], list(range(29)))


class TestFormat(unittest.TestCase):
    def test_french_numbers(self):
        self.assertEqual(S.fmt(0.3218, "+.2"), "+0,32")
        self.assertEqual(S.fmt(-2.04, ".1"), "−2,0")
        self.assertEqual(S.fmt(-0.001, ".1"), "0,0")
        self.assertEqual(S.fmt(12345.6, "d"), "12 346")
        self.assertEqual(S.fmt(0.0004, "p"), "< 0,001")
        self.assertEqual(S.fmt(0.0655, "p"), "= 0,07")

    def test_literal_numbers(self):
        t = "TX ≥ 25 °C, {a|slope|+.2} °C par décennie entre 1953 et 2022, soit 2,2 °C"
        self.assertEqual(S.literal_numbers(t, [25]), ["2,2"])
        self.assertEqual(S.literal_numbers("CO₂ et 10²² J", [10]), [])


class TestClaims(unittest.TestCase):
    def setUp(self):
        self.inds = {"a": ind("a"), "b": ind("b", conf="moyenne"), "n": ind("n", conf="non_etabli", sig=False),
                     "s": ind("s", conf="faible", sig=True)}
        self.r = S.Renderer(self.inds, {}, {})

    def test_confidence_is_weakest(self):
        c, m1 = S.claim_from({"id": "x", "kind": "signal", "text": "{a|slope|+.2} et {b|slope|+.2}"}, self.r, "gironde")
        self.assertEqual(c.confidence, "moyenne")
        self.assertEqual(c.text, "+0,30 et +0,30")
        self.assertIsNone(c.problem)
        self.assertEqual(m1, [])

    def test_signal_on_weak_indicator_is_flagged(self):
        c, _ = S.claim_from({"id": "x", "kind": "signal", "text": "{n|slope|.1}"}, self.r, "gironde")
        self.assertIn("M2", c.problem)
        c, _ = S.claim_from({"id": "y", "kind": "signal", "text": "{s|slope|.1}"}, self.r, "gironde")
        self.assertIn("M2", c.problem)

    def test_absence_on_significant_indicator_is_flagged(self):
        c, _ = S.claim_from({"id": "x", "kind": "absence", "text": "rien : {a|start}"}, self.r, "gironde")
        self.assertIn("M2", c.problem)
        c, _ = S.claim_from({"id": "y", "kind": "absence", "text": "rien : {n|start}"}, self.r, "gironde")
        self.assertIsNone(c.problem)
        self.assertEqual(c.confidence, "non_etabli")

    def test_comparison_words_reserved(self):
        c, _ = S.claim_from({"id": "x", "kind": "signal", "text": "{a|slope|.1}, plus rapide qu'ailleurs"}, self.r, "gironde")
        self.assertIn("S3", c.problem)

    def test_hardcoded_number_reported(self):
        _, m1 = S.claim_from({"id": "x", "kind": "information", "text": "environ 2,2 °C"}, self.r, None)
        self.assertEqual(len(m1), 1)


class TestComparison(unittest.TestCase):
    def test_verdict_needs_disjoint_intervals(self):
        class T:
            def __init__(self, s, lo, hi):
                self.slope_per_decade, self.slope_ci_low, self.slope_ci_high = s, lo, hi
        c = S.Comparison("c", "a", "b", 1959, 2021, T(0.33, 0.26, 0.41), T(0.18, 0.16, 0.19))
        self.assertEqual(c.verdict, "plus rapide que")
        c = S.Comparison("c", "a", "b", 1959, 2021, T(0.33, 0.26, 0.41), T(0.34, 0.26, 0.42))
        self.assertEqual(c.verdict, "du même ordre que")
        c = S.Comparison("c", "a", "b", 1959, 2021, T(0.1, 0.05, 0.15), T(0.3, 0.2, 0.4))
        self.assertEqual(c.verdict, "plus lent que")


if __name__ == "__main__":
    unittest.main()
