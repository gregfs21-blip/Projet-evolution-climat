import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

import numpy as np

from etl.indicators import temperature as T
from etl.sources import openmeteo_era5 as era5
from etl.tests.fixtures import make_raw_dir
from etl.validation import p1


def payload(start: date, end: date, drift_per_year: float = 0.0, missing: date | None = None,
            suffix: str = "") -> dict:
    days, tmax, tmin = [], [], []
    d = start
    rng = np.random.default_rng(0)
    while d <= end:
        seasonal = 6 * np.sin((d.month - 4) / 12 * 2 * np.pi)
        base = 0.03 * (d.year - 1953) + seasonal - drift_per_year * (d.year - 1953) + rng.normal(0, 0.2)
        days.append(d.isoformat())
        tmax.append(None if d == missing else round(18.0 + base, 2))
        tmin.append(round(8.0 + base, 2))
        d += timedelta(days=1)
    return {"latitude": 44.75, "longitude": -0.5, "elevation": 30.0,
            "daily": {"time": days, f"temperature_2m_max{suffix}": tmax, f"temperature_2m_min{suffix}": tmin}}


class Era5ParseTest(unittest.TestCase):
    def test_mois_incomplet_ignore(self):
        data = era5.parse(payload(date(2000, 1, 1), date(2000, 2, 29), missing=date(2000, 2, 10)), (44.79, -0.577))
        m = era5.monthly_means(data)
        self.assertIn((2000, 1), m["TM"])
        self.assertNotIn((2000, 2), m["TM"])

    def test_cle_suffixee(self):
        data = era5.parse(payload(date(2000, 1, 1), date(2000, 1, 31), suffix="_era5"), (44.79, -0.577))
        self.assertEqual(len(data.tmax), 31)

    def test_maille(self):
        data = era5.parse(payload(date(2000, 1, 1), date(2000, 1, 31)), (44.79, -0.577))
        self.assertEqual((data.cell_lat, data.cell_lon), (44.75, -0.5))


class C4bisTest(unittest.TestCase):
    """La station synthétique « STATION-A » sert de Villenave ; ERA5 synthétique avec ou sans dérive."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raw = make_raw_dir(Path(self.tmp.name))
        T._department.cache_clear()
        p1.c4bis.cache_clear()
        p1.era5_villenave.cache_clear()
        self.patches = [mock.patch.object(p1, "VILLENAVE", "33000001")]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        T._department.cache_clear()
        p1.c4bis.cache_clear()
        p1.era5_villenave.cache_clear()
        self.tmp.cleanup()

    def _write(self, drift: float):
        path = era5.cache_path(self.raw, *p1.C4BIS_POINT, p1.ERA5_START, p1.ERA5_END)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload(date(1958, 12, 1), date(2022, 12, 31), drift_per_year=drift)))

    def test_accord_satisfait(self):
        self._write(drift=0.0)
        primary = p1.c4bis(str(self.raw))[0]
        self.assertTrue(primary.passed, primary.detail)
        self.assertEqual(primary.kind, "critère")

    def test_derive_detectee(self):
        self._write(drift=0.02)   # ERA5 se réchauffe 0,2 °C/déc. de moins que la station
        primary = p1.c4bis(str(self.raw))[0]
        self.assertFalse(primary.passed, primary.detail)

    def test_era5_absent_jamais_favorable(self):
        primary = p1.c4bis(str(self.raw))[0]
        self.assertFalse(primary.passed)
        self.assertIn("non évalué", primary.detail)

    def test_ecart_accepte_et_retire(self):
        accepted = p1.Check("C3 TX composite 1959-2009", False, "x")
        self.assertTrue(accepted.satisfied)
        self.assertFalse(p1.Check("C3 TN composite 1959-2009", False, "x").satisfied)
        self.assertIn("retiré", p1.Check("C4 Villenave TM été 1959-2019", False, "x", "retiré").status)


if __name__ == "__main__":
    unittest.main()
