import json
import tempfile
import unittest
from pathlib import Path

from etl.pipeline import run
from etl.validate import validate

REGISTRY = """
indicators:
  - id: demo-temperature-annuelle
    scale: gironde
    builder: etl.sources.demo:build
"""


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.out = self.root / "processed"
        self.out.mkdir()
        self.registry = self.root / "indicators.yaml"
        self.registry.write_text(REGISTRY, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_chaine_complete(self):
        self.assertEqual(run(out_dir=self.out, registry_path=self.registry), 0)
        self.assertEqual(validate(self.out), [])
        manifest = json.loads((self.out / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual([e["path"] for e in manifest["indicators"]], ["gironde/demo-temperature-annuelle.json"])

    def test_sortie_reproductible(self):
        run(out_dir=self.out, registry_path=self.registry)
        first = json.loads((self.out / "gironde/demo-temperature-annuelle.json").read_text())
        run(out_dir=self.out, registry_path=self.registry)
        second = json.loads((self.out / "gironde/demo-temperature-annuelle.json").read_text())
        for d in (first, second):
            d["provenance"].pop("extracted_at")
        self.assertEqual(first, second)

    def test_indicateur_retire_supprime(self):
        stale = self.out / "france" / "ancien.json"
        stale.parent.mkdir()
        stale.write_text("{}", encoding="utf-8")
        run(out_dir=self.out, registry_path=self.registry)
        self.assertFalse(stale.exists())

    def test_echec_signale(self):
        self.registry.write_text(REGISTRY.replace("gironde", "france"), encoding="utf-8")
        self.assertEqual(run(out_dir=self.out, registry_path=self.registry), 1)

    def test_validation_detecte_fichier_orphelin(self):
        run(out_dir=self.out, registry_path=self.registry)
        (self.out / "monde").mkdir()
        (self.out / "monde" / "orphelin.json").write_text("{}", encoding="utf-8")
        self.assertTrue(any("absent du manifeste" in e for e in validate(self.out)))


if __name__ == "__main__":
    unittest.main()
