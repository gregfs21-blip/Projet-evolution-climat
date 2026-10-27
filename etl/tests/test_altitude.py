"""ERA5 niveaux de pression (Copernicus CDS) : extraction au format constaté par la sonde du 26/10/2026, indices."""

import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

import numpy as np

from etl.context import make_context
from etl.indicators import altitude as A
from etl.schema import Indicator
from etl.sources import cds_era5 as cds


def epoch(y: int, m: int) -> int:
    return int(datetime(y, m, 1, tzinfo=timezone.utc).timestamp())


class TestExtraction(unittest.TestCase):
    def test_point_nearest_cell_and_units(self):
        lat, lon, lvl = np.array([45.0, 44.75, 44.5]), np.array([-1.0, -0.75, -0.5]), np.array([850.0, 500.0, 250.0])
        t = np.full((1, 3, 3, 3), 270.0)
        t[0, 0, 1, 1] = 277.15                         # 850 hPa, maille (44,75 ; −0,75)
        z = np.full((1, 3, 3, 3), 14710.0)
        u = np.zeros((1, 3, 3, 3))
        rows = cds.extract_point({"valid_time": np.array([1704067200]), "pressure_level": lvl, "latitude": lat,
                                  "longitude": lon, "t": t, "z": z, "u": u}, 44.83, -0.69)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], {"month": "2024-01", "level": 850, "t_c": 4.0, "z_m": 1500.0, "u_ms": 0.0})

    def test_zonal_mean(self):
        u = np.array([[[[10.0, 20.0, 30.0], [1.0, 1.0, 1.0]]]])     # (temps, niveau, lat, lon)
        rows = cds.extract_zonal({"valid_time": np.array([epoch(2000, 1)]), "latitude": np.array([50.0, 49.0]),
                                  "longitude": np.array([-2.0, -1.0, 0.0]), "u": u})
        self.assertEqual(rows, [{"month": "2000-01", "lat": 50.0, "u_ms": 20.0}, {"month": "2000-01", "lat": 49.0, "u_ms": 1.0}])

    def test_same_request(self):
        r = cds.requests()["bordeaux"]
        self.assertTrue(cds._same({**r, "year": [int(y) for y in r["year"]]}, r))
        self.assertFalse(cds._same({**r, "year": r["year"][:-1]}, r))


class TestIndices(unittest.TestCase):
    def test_annual_requires_twelve_months(self):
        monthly = {f"2000-{m:02d}": float(m) for m in range(1, 13)} | {f"2001-{m:02d}": 1.0 for m in range(1, 12)}
        self.assertEqual(A.annual(monthly), {2000: 6.5})

    def test_jet_djf_parabola(self):
        lats = [40.0, 45.0, 50.0, 55.0]
        prof = {40.0: 20.0, 45.0: 40.0, 50.0: 40.0, 55.0: 10.0}     # maximum entre 45 et 50 : parabole vers 47,1
        zonal = {m: dict(prof) for m in ("1999-12", "2000-01", "2000-02", "2000-12", "2001-01")}
        out = A.jet_indices(zonal)
        self.assertEqual(set(out), {2000})                           # 2001 sans février : écarté
        speed, lat = out[2000]
        self.assertEqual(speed, 40.0)
        self.assertTrue(45.0 < lat < 50.0)
        self.assertTrue(all(la in lats for la in prof))


class TestBuilders(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ctx = make_context(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_point_and_jet_valid_indicators(self):
        point = {850: {"t_c": {}, "z_m": {}, "u_ms": {}}, 500: {"t_c": {}, "z_m": {}, "u_ms": {}}}
        zonal = {}
        for y in range(1940, 2026):
            for m in range(1, 13):
                k = f"{y}-{m:02d}"
                point[850]["t_c"][k] = 4.0 + 0.02 * (y - 1940) + (0.3 if y % 2 else -0.3)
                point[500]["t_c"][k] = -20.0
                point[500]["z_m"][k] = 5650.0
                zonal[k] = {float(la): 15.0 - 0.3 * abs(la - 45.0) for la in range(15, 76)}
        with mock.patch.object(A.cds, "load_point", return_value=point), mock.patch.object(A.cds, "load_zonal", return_value=zonal):
            ind = A.build_point(self.ctx, "t850", "t", "d", "x")
            self.assertEqual(ind.trend.period.start, 1976)              # plus de 80 ans : 50 dernières années
            self.assertLessEqual(["non_etabli", "faible", "moyenne", "elevee"].index(ind.confidence), 2)
            Indicator.model_validate(ind.model_dump())
            jet = A.build_jet(self.ctx, "jet-latitude", "t", "d", "x")
            self.assertEqual(jet.series.value[0], 45.0)
            self.assertEqual(jet.series.time[0], "1941")                # premier hiver complet : décembre 1940
            Indicator.model_validate(jet.model_dump())

    def test_csv_round_trip(self):
        d = Path(self.tmp.name)
        cds._write_csv(d / "bordeaux.csv", [{"month": "2000-01", "level": 850, "t_c": 4.0, "z_m": 1500.0, "u_ms": 2.0}])
        cds._write_csv(d / "atlantique-u850.csv", [{"month": "2000-01", "lat": 45.0, "u_ms": 30.0}])
        self.assertEqual(cds.load_point(d)[850]["z_m"]["2000-01"], 1500.0)
        self.assertEqual(cds.load_zonal(d)["2000-01"][45.0], 30.0)


if __name__ == "__main__":
    unittest.main()
