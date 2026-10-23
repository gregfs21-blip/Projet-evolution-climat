import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pydantic import ValidationError

from etl.context import make_context
from etl.indicators import temperature as T
from etl.pipeline import run
from etl.schema import Indicator
from etl.tests.fixtures import STATIONS, make_raw_dir
from etl.validate import validate

CONFIG = {p: {"id": p, "slug": n.lower(), "name": n.title(), "note": "test"} for p, n, *_ in STATIONS}


class TemperatureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.raw = make_raw_dir(Path(cls.tmp.name))
        cls.ctx = make_context(cls.raw)
        T._department.cache_clear()
        cls.patches = [
            mock.patch.object(T, "station_config", return_value=CONFIG),
            mock.patch("etl.validation.p1.external_validation_passed", return_value=True),
        ]
        for p in cls.patches:
            p.start()

    @classmethod
    def tearDownClass(cls):
        for p in cls.patches:
            p.stop()
        T._department.cache_clear()
        cls.tmp.cleanup()

    def test_departement_filtre(self):
        self.assertEqual(T.stations_with("TN", self.raw), [p for p, *_ in STATIONS])

    def test_annee_incomplete_ignoree(self):
        v, h = T.to_annual({(2000, m): 1.0 for m in range(1, 12)}, {(2000, m): True for m in range(1, 12)})
        self.assertEqual(v, {})

    def test_annee_mixte_non_homogeneisee(self):
        vals = {(2000, m): 1.0 for m in range(1, 13)}
        hom = {(2000, m): m < 12 for m in range(1, 13)}
        self.assertFalse(T.to_annual(vals, hom)[1][2000])

    def test_station_anomalie_et_tendance(self):
        ind = T.build_station(self.ctx, "TN", "station-a")
        Indicator.model_validate(json.loads(ind.model_dump_json()))
        self.assertAlmostEqual(ind.trend.slope_per_decade, 0.30, delta=0.03)
        self.assertEqual(ind.trend.period.end, 2022)             # C2 : 2023-2024 exclues
        self.assertEqual(ind.series.quality[-1], "raw")
        ref = [v for t, v in zip(ind.series.time, ind.series.value) if 1961 <= int(t) <= 1990]
        self.assertAlmostEqual(sum(ref) / len(ref), 0.0, places=2)
        self.assertEqual([n.period.start for n in ind.normals], [1961, 1991])
        self.assertEqual(ind.confidence, "elevee")
        labels = [a.label for a in ind.alt_trends]
        self.assertTrue(any(l.startswith("1959-2009") for l in labels))
        self.assertTrue(any(l.startswith("1962-2022") for l in labels))

    def test_rupture_de_tendance_signalee_comme_telle(self):
        ind = T.build_station(self.ctx, "TN", "station-a")
        for b in ind.breakpoints:
            self.assertGreater(b.detrended_p_value, 0.05)    # tendance pure : pas de saut réel
            self.assertIn("traduit la tendance", b.note)

    def test_artefact_possible(self):
        ind = T.build_station(self.ctx, "TN", "station-a")   # rupture MF 1987-12 → régime 1988
        bp = [b for b in ind.breakpoints if abs(int(b.time) - 1988) <= 1]
        for b in bp:
            self.assertTrue(b.possible_artifact)

    def test_reference_reduite_serie_courte(self):
        ind = T.build_station(self.ctx, "TX", "station-d")
        self.assertEqual((ind.reference_period.start, ind.reference_period.end), (1962, 1990))
        self.assertTrue(any("1962-1990" in l for l in ind.limitations))

    def test_composite_reseau_constant(self):
        ind = T.build_composite(self.ctx, "TM")
        ids = {s.id for s in ind.stations}
        self.assertNotIn("33000004", ids)                    # commence en 1962 : exclue
        self.assertIn("exclues", ind.method_note)
        self.assertEqual(ind.normals, [])

    def test_schema_refuse_tendance_sur_brut(self):
        d = json.loads(T.build_station(self.ctx, "TN", "station-a").model_dump_json())
        d["trend"]["period"]["end"] = 2024
        with self.assertRaises(ValidationError):
            Indicator.model_validate(d)

    def test_schema_refuse_normale_sur_brut(self):
        d = json.loads(T.build_station(self.ctx, "TN", "station-a").model_dump_json())
        d["normals"][1]["period"] = {"start": 1995, "end": 2024}
        with self.assertRaises(ValidationError):
            Indicator.model_validate(d)

    def test_pipeline_complet(self):
        out = Path(self.tmp.name) / "processed"
        out.mkdir(exist_ok=True)
        registry = Path(self.tmp.name) / "indicators.yaml"
        registry.write_text(
            "indicators:\n"
            "  - id: tn-annuelle-gironde\n    scale: gironde\n    builder: etl.indicators.temperature:build_composite\n"
            "    params: {variable: TN}\n"
            "  - id: tx-annuelle-station-b\n    scale: gironde\n    builder: etl.indicators.temperature:build_station\n"
            "    params: {variable: TX, station: station-b}\n"
            "  - id: tm-annuelle-station-b\n    scale: gironde\n    builder: etl.indicators.temperature:build_station\n"
            "    params: {variable: TM, station: station-b}\n",
            encoding="utf-8",
        )
        (out / "france").mkdir(exist_ok=True)
        (out / "france" / "ancien.json").write_text("{}", encoding="utf-8")
        self.assertEqual(run(out_dir=out, registry_path=registry, raw_dir=self.raw), 0)
        self.assertEqual(validate(out), [])
        self.assertFalse((out / "france" / "ancien.json").exists())
        manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual({e["group"] for e in manifest["indicators"]},
                         {"Synthèse Gironde", "Stations — températures maximales", "Stations — températures moyennes"})
        # Contrat v1.2 : variable et lieu explicites, recopiés dans le manifeste.
        got = {e["id"]: (e["variable"]["id"], e["place"]["id"], e["place"]["kind"]) for e in manifest["indicators"]}
        self.assertEqual(got, {"tn-annuelle-gironde": ("tn", "gironde", "composite"),
                               "tx-annuelle-station-b": ("tx", "station-b", "station"),
                               "tm-annuelle-station-b": ("tm", "station-b", "station")})


if __name__ == "__main__":
    unittest.main()
