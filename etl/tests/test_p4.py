"""P4 : indices viticoles et canicule (calculs purs), lecture des dates de vendanges (format de la sonde du 28/10/2026)."""

import unittest

from etl.indicators import impacts as I
from etl.indicators import extremes as X
from etl.sources import globaux as G


def season(year, tn, tx):
    days = [d for m in range(1, 13) for d in X.days_of(year, m)]
    return {d: tn for d in days}, {d: tx for d in days}


class TestHuglin(unittest.TestCase):
    def test_constant_season(self):
        tn, tx = season(2001, 12.0, 26.0)       # TM 19 : ((9) + (16)) / 2 = 12,5 par jour, 183 jours
        self.assertAlmostEqual(I.huglin_year(tn, tx, 2001), round(12.5 * 183 * 1.04, 1))

    def test_cold_days_count_zero_and_missing_days_skipped(self):
        tn, tx = season(2001, 0.0, 8.0)          # négatif chaque jour → 0
        self.assertEqual(I.huglin_year(tn, tx, 2001), 0.0)
        tn, tx = season(2001, 12.0, 26.0)
        del tn["2001-07-14"]
        self.assertAlmostEqual(I.huglin_year(tn, tx, 2001), round(12.5 * 182 * 1.04, 1))


class TestCounts(unittest.TestCase):
    def test_late_frost_window(self):
        tn, _ = season(2001, 5.0, 20.0)
        for d in ("2001-03-31", "2001-04-01", "2001-05-15", "2001-05-16"):
            tn[d] = -1.0
        self.assertEqual(I.late_frost_days(tn, 2001), 2)

    def test_canicule_three_day_means(self):
        tn, tx = season(2003, 15.0, 28.0)
        for d, n, x in (("2003-08-04", 20.0, 34.0), ("2003-08-05", 22.0, 37.0), ("2003-08-06", 21.5, 35.0),
                        ("2003-08-07", 21.0, 36.0)):
            tn[d], tx[d] = n, x
        # Fenêtres 4-6 (TN 21,17 ; TX 35,33) et 5-7 (21,5 ; 36) : jours 4 à 7.
        self.assertEqual(I.canicule_days(tn, tx, 2003), 4)
        del tx["2003-08-05"]                     # un jour manquant rompt toutes les fenêtres qui le contiennent
        self.assertEqual(I.canicule_days(tn, tx, 2003), 0)

    def test_correlation(self):
        r, ys = I.correlation({1: 1.0, 2: 2.0, 3: 3.0, 4: 5.0}, {2: -2.0, 3: -3.0, 4: -5.0, 5: 0.0})
        self.assertAlmostEqual(r, -1.0)
        self.assertEqual(ys, [2, 3, 4])


GHD = """the number of days after 31 August.
                Alsace              Auvergne          Auxerre-Avalon    Beaujolais and Maconn      Bordeaux             Burgundy            Champagne 1          Champagne 2      Gaillac- South-West
Year              Als                  Auv                  Aux                  Bea                  Bor                  Bur                 Cha1                 Cha2                  Gai
1354                                                                                                                      15.3
1976             21.7                                                            6.0                 11.7                  8.8                                       1.0
2003              8.0                                                                                -4.3                 -10.1                                     -4.0
2006                                                                                                 16.1                 16.0                                      16.0

Year            Germany         High Loire Valley
1354              Ger                  HLV
"""


class TestGhd(unittest.TestCase):
    def test_right_aligned_columns(self):
        self.assertEqual(G.parse_ghd(GHD), {1976: 11.7, 2003: -4.3, 2006: 16.1})
        self.assertEqual(G.parse_ghd(GHD, "Bur"), {1354: 15.3, 1976: 8.8, 2003: -10.1, 2006: 16.0})


class TestFwiExtraction(unittest.TestCase):
    def test_west_column_dropped_and_weighted_mean(self):
        import numpy as np
        from etl.sources import ewds_fire as E
        lat = np.array([45.0, 44.5])
        lon = np.array([358.7, 359.0, 0.2])          # −1,3 (écartée), −1,0, +0,2
        f = np.array([[[99.0, 10.0, 20.0], [99.0, 30.0, np.nan]]])
        rows = E.extract_daily({"valid_time": np.array([1656633600]), "latitude": lat, "longitude": lon, "fwinx": f})
        w1, w2 = np.cos(np.radians(45.0)), np.cos(np.radians(44.5))
        expect = (10 * w1 + 20 * w1 + 30 * w2) / (2 * w1 + w2)
        self.assertEqual(rows[0]["day"], "2022-07-01")
        self.assertEqual(rows[0]["cells"], 3)
        self.assertAlmostEqual(rows[0]["fwi"], round(expect, 3))


if __name__ == "__main__":
    unittest.main()
