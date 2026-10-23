"""Rapport de validation publié pour le site : même contenu que le tableau Markdown, contrôlé par etl.validate."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError

from etl.context import PROCESSED_DIR
from etl.schema import ValidationReport
from etl.validate import validate
from etl.validation.p1 import Check, build_report


CHECKS = [
    Check("C1 TN", True, "7/7 séries LSH traitées"),
    Check("C3 TX composite 1959-2009", False, "pente +0.354"),          # écart accepté (ACCEPTED)
    Check("C4 Villenave TM hiver 1959-2019", False, "écart +0.085", kind="retiré"),
    Check("C4bis (info) Villenave TN annuelle 1979-2022", False, "dérive +0.099", kind="info"),
]


class TestBuildReport(unittest.TestCase):
    def test_contenu_fidele(self):
        r = build_report(CHECKS, "verdict", ["tn-a"])
        self.assertEqual([c.name for c in r.checks], [c.name for c in CHECKS])
        self.assertEqual([c.status for c in r.checks], [c.status for c in CHECKS])
        self.assertEqual([c.satisfied for c in r.checks], [True, True, False, False])
        # Seuls les critères comptent : un « info » ou un « retiré » en échec ne bloque pas la clôture.
        self.assertTrue(r.closure_ok)

    def test_critere_en_echec_bloque(self):
        r = build_report(CHECKS + [Check("C8", False, "incomplètes")], "verdict", ["tn-a"])
        self.assertFalse(r.closure_ok)

    def test_closure_incoherente_refusee(self):
        data = json.loads(build_report(CHECKS + [Check("C8", False, "x")], "v", ["tn-a"]).model_dump_json())
        data["closure_ok"] = True
        with self.assertRaises(ValidationError):
            ValidationReport.model_validate(data)


class TestValidateDir(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(PROCESSED_DIR, self.tmp, dirs_exist_ok=True)
        for p in self.tmp.glob("validation-*.json"):
            p.unlink()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_rapport_valide_accepte(self):
        (self.tmp / "validation-p1.json").write_text(build_report(CHECKS, "v", ["tn-a"]).model_dump_json())
        self.assertEqual(validate(self.tmp), [])

    def test_rapport_invalide_signale(self):
        (self.tmp / "validation-p1.json").write_text('{"schema_version": "1.0"}')
        errors = validate(self.tmp)
        self.assertEqual(len(errors), 1)
        self.assertIn("validation-p1.json invalide", errors[0])


if __name__ == "__main__":
    unittest.main()
