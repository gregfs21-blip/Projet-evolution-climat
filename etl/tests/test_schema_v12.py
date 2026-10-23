"""Contrat v1.2 : variable et lieu, cohérences imposées par le schéma."""

import unittest

from pydantic import ValidationError

from etl import vocabulary as vocab
from etl.schema import Manifest, ManifestEntry, Place

ENTRY = dict(scale="gironde", title="t", unit="°C", confidence="elevee", is_demo=False, group=None)


def entry(i: str, var: str, place: Place) -> ManifestEntry:
    return ManifestEntry(id=i, path=f"gironde/{i}.json", variable=vocab.variable(var), place=place, **ENTRY)


class TestVocabulary(unittest.TestCase):
    def test_variables_p1(self):
        v = vocab.variable("tn")
        self.assertEqual((v.code, v.theme), ("TN", "temperature"))
        self.assertEqual([vocab.variable(x).order for x in ("tn", "tm", "tx")], [0, 1, 2])

    def test_variable_inconnue(self):
        with self.assertRaises(KeyError):
            vocab.variable("inconnue")


class TestManifest(unittest.TestCase):
    def manifest(self, entries):
        return Manifest(generated_at="2026-10-23T00:00:00Z", etl_version="t", indicators=entries)

    def test_doublon_variable_lieu_refuse(self):
        st = vocab.station("a", "A")
        with self.assertRaises(ValidationError):
            self.manifest([entry("tn-a", "tn", st), entry("tn-a-bis", "tn", st)])

    def test_variable_decrite_deux_fois_refusee(self):
        e1 = entry("tn-a", "tn", vocab.station("a", "A"))
        other = vocab.variable("tn").model_copy(update={"label": "autre libellé"})
        e2 = entry("tn-b", "tn", vocab.station("b", "B")).model_copy(update={"variable": other})
        with self.assertRaises(ValidationError):
            self.manifest([e1, e2])

    def test_famille_valide(self):
        m = self.manifest([entry("tn-a", "tn", vocab.station("a", "A")),
                           entry("tx-a", "tx", vocab.station("a", "A")),
                           entry("tn-gironde", "tn", vocab.composite("gironde", "Gironde"))])
        self.assertEqual(len(m.indicators), 3)


if __name__ == "__main__":
    unittest.main()
