"""Cache de lecture du quotidien Météo-France : même résultat, relecture si le fichier change."""

import gzip
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from etl.sources import meteofrance_quot as quot

HEADER = "NUM_POSTE;NOM_USUEL;LAT;LON;ALTI;AAAAMMJJ;RR;QRR;TX;QTX\n"


def write(raw: Path, rows: str) -> None:
    d = raw / "quot"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index-33.json").write_text(json.dumps([{"title": "QUOT_departement_33_periode_x_RR-T-Vent",
                                                  "url": "https://example.org/Q_33_x_RR-T-Vent.csv.gz"}]))
    (d / "Q_33_x_RR-T-Vent.csv.gz").write_bytes(gzip.compress((HEADER + rows).encode()))


class TestCache(unittest.TestCase):
    def test_cached_equals_parsed_and_invalidated(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"QUOT_OFFLINE": "1"}):
            raw = Path(tmp)
            write(raw, "33281001;M;0;0;0;20000101;1.5;1;12.0;1\n33281001;M;0;0;0;20000102;;;13.0;1\n")
            a = quot.load("33", {"33281001"}, ("RR", "TX"), raw)
            self.assertTrue(any((raw / "quot" / "parsed").iterdir()))
            b = quot.load("33", {"33281001"}, ("RR", "TX"), raw)
            self.assertEqual(a, b)
            self.assertEqual(a["33281001"]["RR"]["2000-01-01"].value, 1.5)
            self.assertNotIn("2000-01-02", a["33281001"]["RR"])
            write(raw, "33281001;M;0;0;0;20000101;9.0;1;12.0;1\n")          # fichier modifié : relu
            c = quot.load("33", {"33281001"}, ("RR",), raw)
            self.assertEqual(c["33281001"]["RR"]["2000-01-01"].value, 9.0)


if __name__ == "__main__":
    unittest.main()
