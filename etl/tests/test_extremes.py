"""P2a : comptages de jours sur données quotidiennes synthétiques (aucun accès réseau)."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from etl.context import make_context
from etl.indicators import extremes as X
from etl.indicators import temperature as T
from etl.pipeline import run
from etl.schema import Indicator
from etl.tests.fixtures import DAILY_BIAS, DAILY_GAP, DAILY_Q9, STATIONS, make_daily_dir, make_raw_dir
from etl.validate import validate
from etl.validation import p2a

CONFIG = {p: {"id": p, "slug": n.lower(), "name": n.title(), "note": "test"} for p, n, *_ in STATIONS}
A, B, C, D = (s[0] for s in STATIONS)


class ExtremesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.raw = make_raw_dir(Path(cls.tmp.name))
        T._department.cache_clear()
        make_daily_dir(cls.raw)
        X._daily.cache_clear()
        cls.ctx = make_context(cls.raw)
        cls.patches = [mock.patch.object(T, "station_config", return_value=CONFIG),
                       mock.patch("etl.validation.p1.external_validation_passed", return_value=True),
                       # Par défaut, E4 « en attente » : les références réelles portent sur des postes absents des fixtures.
                       mock.patch.object(p2a, "REFERENCES", {})]
        for p in cls.patches:
            p.start()

    def setUp(self):
        p2a._e4_cached.cache_clear()

    @classmethod
    def tearDownClass(cls):
        for p in cls.patches:
            p.stop()
        p2a._e4_cached.cache_clear()
        T._department.cache_clear()
        X._daily.cache_clear()
        cls.tmp.cleanup()

    def test_regle_etccdi(self):
        poste, year, month, n = DAILY_GAP
        sd = X.station_daily("TX", poste, self.raw)
        self.assertNotIn(year, sd.year_status, "4 jours manquants dans un mois : l'année doit être écartée")
        self.assertIn(year + 1, sd.year_status)

    def test_correction_retrouve_la_lsh(self):
        sd = X.station_daily("TX", A, self.raw)
        for y in (1960, 1987, 1988, 2010):
            for m in (1, 7):
                days = [d for d in X.days_of(y, m) if d in sd.corrected]
                self.assertAlmostEqual(sum(sd.corrected[d] for d in days) / len(days), sd.lsh_month[(y, m)], places=6)

    def test_correction_efface_le_biais_brut(self):
        # Station A : brut trop chaud de 0,8 °C avant 1988 ; après correction, l'écart moyen au brut vaut −0,8.
        sd = X.station_daily("TX", A, self.raw)
        year, bias = DAILY_BIAS[A]
        before = [sd.corrected[d] - sd.raw[d] for d in X.days_of(year - 5, 7)]
        after = [sd.corrected[d] - sd.raw[d] for d in X.days_of(year + 5, 7)]
        self.assertAlmostEqual(sum(before) / len(before), -bias, delta=0.06)  # arrondi à 0,1 du brut
        self.assertAlmostEqual(sum(after) / len(after), 0.0, delta=0.06)

    def test_annees_non_corrigeables_marquees_brutes(self):
        sd = X.station_daily("TX", B, self.raw)
        self.assertEqual(sd.year_status[2022], "homogenized")
        self.assertEqual(sd.year_status[2023], "raw")

    def test_derniere_rupture(self):
        self.assertEqual(X.station_daily("TX", A, self.raw).last_break_regime, 1988)
        self.assertIsNone(X.station_daily("TX", C, self.raw).last_break_regime)

    def test_code_9_ignore_sur_demande(self):
        poste, year = DAILY_Q9
        self.assertIn(year, X.station_daily("TN", poste, self.raw).year_status)
        self.assertNotIn(year, X.station_daily("TN", poste, self.raw, drop_q9=True).year_status)

    def test_indicateur_station(self):
        ind = X.build_station(self.ctx, "jours-tx25", "station-a")
        Indicator.model_validate(ind.model_dump())
        self.assertEqual(ind.unit, "jours")
        self.assertEqual((ind.variable.id, ind.place.kind), ("jours-tx25", "station"))
        self.assertGreater(ind.trend.slope_per_decade, 0)  # tendance imposée de +0,3 °C/déc. dans la fixture
        labels = [t.label for t in ind.alt_trends]
        self.assertTrue(any(lbl.startswith("Contrôle A") for lbl in labels))
        self.assertTrue(any("période commune" in lbl for lbl in labels))
        # E4 en attente : jamais de confiance « élevée ».
        self.assertNotEqual(ind.confidence, "elevee")
        self.assertTrue(any("E4" in lim for lim in ind.limitations))

    def test_e4_references_par_groupe_de_stations(self):
        refs = {
            "R3 test": {"variable": "TX", "op": ">", "threshold": 25.0, "definition": "journées chaudes (TX > 25 °C)",
                        "stations": [A, B], "range": (0.0, 20.0)},
            "R4 test": {"variable": "TN", "op": "<=", "threshold": 0.0, "definition": "gel", "stations": None,
                        "range": (-0.1, 0.0)},
            "R3 incomplet": {"variable": "TX", "op": ">", "threshold": 25.0, "definition": "x", "stations": [C],
                             "range": (0.0, 20.0)},
        }
        with mock.patch.object(p2a, "REFERENCES", refs), mock.patch.object(X, "COMPOSITE_SPAN", X.Period(start=1963, end=2022)):
            by = {c.name.split(" :")[0]: c for c in p2a.e4(self.raw)}
        self.assertTrue(by["E4 R3 test"].passed)
        self.assertFalse(by["E4 R4 test"].passed)          # le gel baisse : pente < −0,1 dans la fixture
        self.assertIn("non évaluable", by["E4 R3 incomplet"].detail)  # C : année 1970 manquante

    def test_operateur_strict(self):
        strict = X.IndexDef("t", "TX", ">", 25.0, "t", "t")
        self.assertFalse(strict.hit(25.0))
        self.assertTrue(X.INDICES["jours-tx25"].hit(25.0))

    def test_indice_rare_met_en_avant_les_normales(self):
        ind = X.build_station(self.ctx, "jours-tx35", "station-a")
        self.assertEqual(ind.headline, "normals")
        self.assertIsNotNone(ind.normals_comparison)
        self.assertIn("Indice rare", ind.finding)
        self.assertIn(ind.confidence, ("moyenne", "faible", "non_etabli"))

    def test_indice_rare_sans_normale_complete(self):
        # Station C : année 1970 manquante, donc pas de normale 1961-1990 : rien n'est établi.
        ind = X.build_station(self.ctx, "jours-tx35", "station-c")
        self.assertIsNone(ind.normals_comparison)
        self.assertEqual(ind.headline, "trend")
        self.assertEqual(ind.confidence, "non_etabli")
        self.assertIn("aucune évolution n'est établie", ind.finding)

    def test_composite_reseau_constant(self):
        # Fenêtre 1963-2022 : D (début 1962) entre, C (année 1970 manquante) reste exclu.
        with mock.patch.object(X, "COMPOSITE_SPAN", X.Period(start=1963, end=2022)):
            ind = X.build_composite(self.ctx, "jours-gel")
        self.assertEqual(ind.place.kind, "composite")
        self.assertEqual({s.id for s in ind.stations}, {A, B, D})
        self.assertIn("exclues : Station-C", ind.method_note)

    def test_composite_trop_petit_refuse(self):
        with mock.patch.object(X, "stations_for", return_value=[A]):
            with self.assertRaises(ValueError):
                X.build_composite(self.ctx, "jours-gel")

    def test_pipeline_et_validation(self):
        out = Path(self.tmp.name) / "processed"
        out.mkdir(exist_ok=True)
        reg = Path(self.tmp.name) / "p2a.yaml"
        entries = [("jours-tx25-station-a", "build_station", "{index: jours-tx25, station: station-a}"),
                   ("jours-tx25-station-b", "build_station", "{index: jours-tx25, station: station-b}"),
                   ("jours-gel-station-a", "build_station", "{index: jours-gel, station: station-a}"),
                   ("jours-gel-station-b", "build_station", "{index: jours-gel, station: station-b}")]
        reg.write_text("indicators:\n" + "".join(
            f"  - id: {i}\n    scale: gironde\n    builder: etl.indicators.extremes:{b}\n    params: {p}\n" for i, b, p in entries))
        self.assertEqual(run(out_dir=out, registry_path=reg, raw_dir=self.raw), 0)
        self.assertEqual(validate(out), [])
        inds = p2a.load_indicators(out)
        self.assertEqual(len(inds), 4)
        cs, _ = p2a.checks(inds, self.raw)
        by = {c.name: c for c in cs}
        self.assertTrue(by["E4 validation externe (ClimatHD)"].pending)
        self.assertTrue(by["E5 cohérence du correctif"].passed)
        report = p2a.build_report(cs, "v", [i.id for i in inds])
        self.assertFalse(report.closure_ok, "E4 en attente : la phase ne peut pas être close")
        manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual({e["variable"]["theme"] for e in manifest["indicators"]}, {"extremes-temperature"})


if __name__ == "__main__":
    unittest.main()
