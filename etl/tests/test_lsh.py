import unittest

from etl.sources.meteofrance_lsh import parse_file
from etl.tests.fixtures import lsh_text


class LshParseTest(unittest.TestCase):
    def setUp(self):
        self.s = parse_file(lsh_text("TN", "33000001", "STATION-A", 1953, "196612 198712", seed=1), "TN")

    def test_metadonnees(self):
        st = self.s.station
        self.assertEqual(st.id, "33000001")
        self.assertEqual(st.series_id, "MTN233000001")
        self.assertEqual((st.homogenized_period.start, st.homogenized_period.end), (1953, 2022))
        self.assertEqual(st.homogenization_breaks, ["1966-12", "1987-12"])
        self.assertEqual(st.min_detectable_amplitude, 0.15)
        self.assertEqual(st.file_produced, "13/03/2025")

    def test_qualite(self):
        self.assertTrue(self.s.homogenized[(2022, 12)])
        self.assertFalse(self.s.homogenized[(2023, 1)])
        self.assertEqual(len(self.s.values), (2024 - 1953 + 1) * 12)

    def test_mois_duplique_refuse(self):
        txt = lsh_text("TN", "33000001", "A", 1953, "", seed=1) + "195301;1.0;1\n"
        with self.assertRaises(ValueError):
            parse_file(txt, "TN")

    def test_metadonnees_manquantes_refusees(self):
        txt = "\n".join(l for l in lsh_text("TN", "33000001", "A", 1953, "", 1).splitlines() if "NUM_SERIE" not in l)
        with self.assertRaises(ValueError):
            parse_file(txt, "TN")

    def test_mois_vide_non_complete(self):
        txt = lsh_text("TN", "33000001", "A", 1953, "", 1).replace("195306;", "195306;;", 1)
        txt = "\n".join(l if not l.startswith("195306") else "195306;;1" for l in txt.splitlines())
        s = parse_file(txt, "TN")
        self.assertNotIn((1953, 6), s.values)


if __name__ == "__main__":
    unittest.main()
