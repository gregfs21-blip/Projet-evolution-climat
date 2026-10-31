"""P6 : lecteurs des sources mondiales, sur des extraits au format constaté par les sondes du 31/10/2026."""

import unittest

from etl.sources import globaux as G


class TestParsers(unittest.TestCase):
    def test_star_first_mission_and_complete_years(self):
        rows = ["#trend = 3.11 mm/year", "year,TOPEX/Poseidon,Jason-1"]
        rows += [f"2001.{int((m - 0.5) / 12 * 100000):05d},{10 + m},{99}" for m in range(1, 13)]   # 12 mois : TOPEX pris
        rows += ["2002.04,5,"]                                                                    # année incomplète
        out = G.parse_star_gmsl("\n".join(rows))
        self.assertEqual(out, {2001: round(sum(10 + m for m in range(1, 13)) / 12, 2)})

    def test_hot_ph_min_cruises(self):
        head = "cruise\tdays\tdate\ttemp\tpHcalc_insitu\tnotes"
        rows = [f"{i}\t0\t{d}-Jan-89\t25\t{8.10 + i / 1000}\t" for i, d in enumerate(range(1, 7), 1)]
        rows.append("7\t0\t2-Feb-90\t25\t8.05\t")
        rows.append("8\t0\t3-Mar-89\t25\t-999\t")
        out = G.parse_hot_ph("titre\n" + head + "\n" + "\n".join(rows))
        self.assertEqual(set(out), {1989})
        self.assertAlmostEqual(out[1989], 8.1035, places=4)

    def test_ozone(self):
        txt = "# NASA\n      O3 Hole Area Minimum Ozone\nYear     (mil km2)          (DU)\n----  ----\n1979           0.1         225.0\n2025          18.7         138.3\n"
        self.assertEqual(G.parse_ozone_hole(txt), {1979: 0.1, 2025: 18.7})

    def test_gcb_header_checked(self):
        txt = "# commentaire\nYear,GCB Ocean Sink,autre\n2023,3.27,3.06\n2024,3.39,3.17\n"
        self.assertEqual(G.parse_gcb(txt, ("ocean",)), {2023: 3.27, 2024: 3.39})
        with self.assertRaises(ValueError):
            G.parse_gcb(txt, ("fossil",))

    def test_uah_and_rss_annual(self):
        uah = " Year Mo Globe  Land\n" + "\n".join(f" 2000 {m:2d}  0.{m:02d} 0.0" for m in range(1, 13)) + "\n 2001  1  0.50 0.0\n"
        self.assertEqual(G.parse_uah(uah), {2000: round(sum(m / 100 for m in range(1, 13)) / 12, 3)})
        rss = "year  mon  TLT\n" + "\n".join(f"2000 {m:3d}   0.1000" for m in range(1, 13)) + "\n2001   1  -99.9000\n"
        self.assertEqual(G.parse_rss(rss), {2000: 0.1})


class TestGlobalMeans(unittest.TestCase):
    def test_cos_lat_weighting(self):
        import numpy as np
        from etl.sources import ads_aod as A
        arrays = {"valid_time": np.array([1577836800]), "latitude": np.array([0.0, 60.0]), "longitude": np.array([0.0, 1.0]),
                  "aod550": np.array([[[0.2, 0.2], [0.1, np.nan]]])}
        rows = A.global_means(arrays)
        self.assertEqual(rows[0]["month"], "2020-01")
        self.assertAlmostEqual(rows[0]["aod550"], round((0.2 * 2 + 0.1 * 0.5) / 2.5, 5))


if __name__ == "__main__":
    unittest.main()
