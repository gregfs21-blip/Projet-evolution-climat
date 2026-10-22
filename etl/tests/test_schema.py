import json
import unittest

from pydantic import ValidationError

from etl.context import make_context
from etl.schema import Indicator
from etl.sources.demo import build


def demo_dict() -> dict:
    return json.loads(build(make_context()).model_dump_json())


class SchemaTest(unittest.TestCase):
    def test_demo_valide(self):
        Indicator.model_validate(demo_dict())

    def test_anomalie_sans_reference_refusee(self):
        d = demo_dict()
        d["reference_period"] = None
        with self.assertRaises(ValidationError):
            Indicator.model_validate(d)

    def test_longueurs_differentes_refusees(self):
        d = demo_dict()
        d["series"]["value"] = d["series"]["value"][:-1]
        with self.assertRaises(ValidationError):
            Indicator.model_validate(d)

    def test_serie_non_triee_refusee(self):
        d = demo_dict()
        d["series"]["time"] = list(reversed(d["series"]["time"]))
        with self.assertRaises(ValidationError):
            Indicator.model_validate(d)

    def test_demo_doit_etre_signalee(self):
        d = demo_dict()
        d["title"] = "Anomalie de température"
        with self.assertRaises(ValidationError):
            Indicator.model_validate(d)

    def test_significativite_incoherente_refusee(self):
        d = demo_dict()
        d["trend"]["significant"] = not d["trend"]["significant"]
        with self.assertRaises(ValidationError):
            Indicator.model_validate(d)

    def test_champ_inconnu_refuse(self):
        d = demo_dict()
        d["champ_fantome"] = 1
        with self.assertRaises(ValidationError):
            Indicator.model_validate(d)

    def test_limitations_obligatoires(self):
        d = demo_dict()
        d["limitations"] = []
        with self.assertRaises(ValidationError):
            Indicator.model_validate(d)


if __name__ == "__main__":
    unittest.main()
