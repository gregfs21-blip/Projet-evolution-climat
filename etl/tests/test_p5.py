"""P5 : pondération par département et réseau constant (calculs purs)."""

import unittest

from etl.indicators import france as F


class TestComposite(unittest.TestCase):
    def test_department_from_poste(self):
        self.assertEqual(F.department("1014002"), "01")
        self.assertEqual(F.department("33281001"), "33")
        self.assertEqual(F.department("20004002"), "20")

    def test_weighted_by_department(self):
        per = {"33000001": ({2000: 1.0, 2001: 1.0}, {2000, 2001}),
               "33000002": ({2000: 3.0, 2001: 3.0}, {2000, 2001}),
               "75000001": ({2000: 0.0, 2001: 0.0}, {2000})}
        s, hom = F.composite(per)
        self.assertEqual(s[2000], 1.0)                 # (moyenne 33 = 2 ; 75 = 0) / 2
        self.assertEqual(hom, {2000})                  # 2001 brute pour un poste
        s2, _ = F.composite(per, weighted=False)
        self.assertAlmostEqual(s2[2000], 4 / 3, places=4)

    def test_years_require_all_stations(self):
        per = {"33000001": ({2000: 1.0, 2001: 2.0}, {2000, 2001}), "75000001": ({2000: 0.0}, {2000})}
        s, _ = F.composite(per)
        self.assertEqual(set(s), {2000})


class TestCarte(unittest.TestCase):
    def test_shapes_metropole_and_corsica(self):
        from etl import carte as C
        sq = {"type": "Polygon", "coordinates": [[[0.12345, 45.0], [1.0, 45.0], [1.0, 46.0], [0.12345, 45.0]]]}
        geo = {"features": [{"properties": {"code": c, "nom": c}, "geometry": sq} for c in ("33", "2A", "2B", "971")]}
        out = C.shapes(geo)
        self.assertEqual([s.code for s in out], ["2A", "2B", "33"])
        self.assertEqual({s.value_code for s in out}, {"20", "33"})
        self.assertEqual(out[0].geometry["coordinates"][0][0], [0.123, 45.0])


if __name__ == "__main__":
    unittest.main()
