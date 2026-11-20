"""P10.4 : contrôles de cohérence physique (calculs purs, sur des séries synthétiques)."""

import math
import unittest
from unittest import mock
from datetime import datetime, timezone

import numpy as np

from etl import demo_coherence as C
from etl.schema import Coherence
from etl.sources import grace as GR
from etl.sources import rss_vapor as RV


def world(seed: int = 1, cc: float = 0.07, resid: float = 0.0, strat: float = -0.03, gap: bool = True,
          ocean_trend: float = 0.5):
    """Un monde synthétique cohérent : chaque contrôle doit passer (sauf paramètre modifié)."""
    rng = np.random.default_rng(seed)
    yrs = range(1850, 2026)
    sst = {y: 0.012 * max(0, y - 1950) + 0.08 * math.sin(y / 1.7) + rng.normal(0, 0.03) for y in yrs}
    sst_alt = {y: v + rng.normal(0, 0.01) for y, v in sst.items()}
    tpw_monthly = {}
    for y in range(1988, 2026):
        for m in range(1, 13):
            tpw_monthly[f"{y}-{m:02d}"] = 28.0 * math.exp(cc * sst[y] + rng.normal(0, 0.002)) + 0.3 * math.sin(m)
    tlt = {n: {y: 0.018 * (y - 1979) + rng.normal(0, 0.08) for y in range(1979, 2026)} for n in ("rss", "uah")}
    tls = {n: {y: strat * (y - 1979) + rng.normal(0, 0.08) for y in range(1979, 2026)} for n in ("rss", "uah")}
    thermo = {y: 1.3 * (y - 2005) + rng.normal(0, 1.5) for y in range(2005, 2026)}
    mass_rate = 2.0
    gmsl = {y: (1.3 + mass_rate + resid - C.GIA) * (y - 2005) + rng.normal(0, 2) for y in range(1993, 2025)}
    rows = []
    t = 2002.29
    while t < 2026.7:
        if not (gap and 2017.5 <= t < 2018.45):
            rows.append({"time": round(t, 2), "mass_mm": 0.0, "sigma_mm": 0.5,
                         "deseasoned_mm": mass_rate * (t - 2005) + rng.normal(0, 1.0)})
        t += 1 / 12
    ohc = {}
    for y in range(2005, 2026):
        # flux (W/m²) = 0,6 + ocean_trend/10 par an ; contenu = intégrale
        ohc[y] = (sum((0.6 + ocean_trend / 10 * (a - 2005)) for a in range(2005, y)) * C.YEAR_S * C.EARTH_AREA / 1e22
                  + rng.normal(0, 0.15))
    eei = {y: 0.65 + 0.05 * (y - 2005) + rng.normal(0, 0.1) for y in range(2001, 2026)}
    return dict(tpw_monthly=tpw_monthly, tpw_meta={"mask_area_fraction": 0.62, "file": "synthétique"}, sst=sst,
                sst_alt=sst_alt, tlt=tlt, tls=tls, gmsl=gmsl, thermo=thermo, grace_rows=rows, ohc=ohc, eei=eei)


def build(**kw) -> Coherence:
    return C.build(**world(**kw), ctx_version="test", extracted_at=datetime(2026, 11, 20, tzinfo=timezone.utc))


class TestChecks(unittest.TestCase):
    def test_consistent_world_is_high_confidence(self):
        r = build()
        ok = {c.id: c.satisfied for c in r.criteria}
        self.assertTrue(all(ok.values()), [c.detail for c in r.criteria if not c.satisfied])
        self.assertEqual(r.confidence, "elevee")
        self.assertEqual([c.letter for c in r.checks], ["V", "S", "N", "E"])

    def test_cc_rate_is_recovered(self):
        v = build().checks[0].values[0].estimate
        self.assertAlmostEqual(v.value, 7.0, delta=0.6)
        bad = build(cc=0.02)
        self.assertFalse({c.id: c.satisfied for c in bad.criteria}["C2"])

    def test_budget_residual(self):
        r = build(resid=1.5)
        ok = {c.id: c.satisfied for c in r.criteria}
        self.assertFalse(ok["C4"])
        self.assertEqual(r.confidence, "moyenne")
        self.assertAlmostEqual(r.checks[2].values[0].estimate.value, 1.5, delta=0.4)

    def test_warming_stratosphere_fails(self):
        self.assertFalse({c.id: c.satisfied for c in build(strat=0.02).criteria}["C3"])

    def test_two_failures_not_established(self):
        r = build(resid=1.5, strat=0.02)
        self.assertEqual(r.confidence, "non_etabli")

    def test_ocean_flux_and_area(self):
        self.assertAlmostEqual(C.EARTH_AREA, 5.10e14, delta=0.01e14)
        f = C.ocean_flux({2005: 0.0, 2006: 1.0, 2007: 2.0}, [2006])
        self.assertAlmostEqual(f[2006], 1e22 / (C.YEAR_S * C.EARTH_AREA), places=6)    # ≈ 0,62 W/m²
        self.assertEqual(sorted(C.smooth3({1: 1.0, 2: 2.0, 3: 3.0, 4: 7.0})), [2, 3])

    def test_grace_gap_counted(self):
        w = world()
        mass = C.mass_months(w["grace_rows"], C.N_SPAN)
        self.assertLess(C.month_count(mass), 240)
        self.assertGreater(C.month_count(mass), 0.8 * 240)

    def test_c1_fails_on_small_mask(self):
        w = world()
        w["tpw_meta"]["mask_area_fraction"] = 0.3
        r = C.build(**w, ctx_version="t", extracted_at=datetime(2026, 11, 20, tzinfo=timezone.utc))
        self.assertFalse({c.id: c.satisfied for c in r.criteria}["C1"])
        self.assertNotEqual(r.confidence, "elevee")

    def test_robustness_fit_failure_is_reported_not_raised(self):
        real = C.fit_cc
        calls = []

        def flaky(tpw, sst, years):
            calls.append(1)
            if len(calls) == 2:
                raise ValueError("Prais-Winsten : ρ ne converge pas")
            return real(tpw, sst, years)

        with mock.patch.object(C, "fit_cc", flaky):
            r = build()
        c6 = next(c for c in r.criteria if c.id == "C6")
        self.assertFalse(c6.satisfied)
        self.assertIn("ne converge pas", c6.detail)
        self.assertEqual(r.confidence, "moyenne")

    def test_confidence_rule_is_enforced(self):
        r = build()
        with self.assertRaises(ValueError):
            Coherence.model_validate({**r.model_dump(), "confidence": "moyenne"})


class TestSources(unittest.TestCase):
    def test_rss_months(self):
        self.assertEqual(RV.month_of(1988.0416666666667), "1988-01")
        self.assertEqual(RV.month_of(2025.958333333299), "2025-12")

    def test_grace_parse(self):
        text = "HDR x\nHDR Header_End-----\n" + "\n".join(f"{2002.29 + i / 12:.2f} 1.0 0.5 0.2" for i in range(120))
        rows = GR.parse(text)
        self.assertEqual(len(rows), 120)
        self.assertEqual(rows[0]["deseasoned_mm"], 0.2)
        with self.assertRaises(ValueError):
            GR.parse("HDR Header_End\n2002.29 1 2\n")


if __name__ == "__main__":
    unittest.main()


try:
    import netCDF4  # noqa: F401
    HAS_NC = True
except ImportError:      # bac à sable sans netCDF4 ; la CI l'installe (etl/requirements.txt)
    HAS_NC = False


@unittest.skipUnless(HAS_NC, "netCDF4 absent")
class TestCommonDomain(unittest.TestCase):
    def test_extract_common_matches_known_fields(self):
        import datetime as dt
        import tempfile
        from pathlib import Path

        import netCDF4
        with tempfile.TemporaryDirectory() as tmp:
            rp, ep = Path(tmp) / "r.nc", Path(tmp) / "e.nc"
            n = 24
            with netCDF4.Dataset(rp, "w") as ds:
                ds.createDimension("latitude", 180)
                ds.createDimension("longitude", 360)
                ds.createDimension("time", n)
                ds.createVariable("latitude", "f4", ("latitude",))[:] = np.arange(-89.5, 90, 1.0)
                ds.createVariable("longitude", "f4", ("longitude",))[:] = np.arange(-179.5, 180, 1.0)
                ds.createVariable("time", "f8", ("time",))[:] = [1988 + (k + 0.5) / 12 for k in range(n)]
                v = ds.createVariable("merged_vapor", "f4", ("latitude", "longitude", "time"), fill_value=-999.0)
                data = np.full((180, 360, n), 30.0) + np.arange(n)[None, None, :] * 0.1
                data[:, :10, :] = -999.0                      # « continent » toujours absent
                v[:] = data
            with netCDF4.Dataset(ep, "w") as ds:
                ds.createDimension("lat", 89)
                ds.createDimension("lon", 180)
                ds.createDimension("time", 600)
                ds.createVariable("lat", "f4", ("lat",))[:] = np.arange(88, -89, -2.0)
                ds.createVariable("lon", "f4", ("lon",))[:] = np.arange(0, 360, 2.0)
                t = ds.createVariable("time", "f8", ("time",))
                t.units = "days since 1800-1-1 00:00:00"
                t[:] = netCDF4.date2num([dt.datetime(1960 + k // 12, k % 12 + 1, 1) for k in range(600)], t.units)
                s = ds.createVariable("sst", "f4", ("time", "lat", "lon"), fill_value=-9.96921e36)
                sst = np.full((600, 89, 180), 20.0) + np.arange(600)[:, None, None] * 0.01
                sst[:, :, 0] = -9.96921e36                     # longitude 0° absente : mailles RSS voisines exclues
                s[:] = sst
            rows, meta = RV.extract_common(rp, ep)
        self.assertEqual(rows[0]["month"], "1988-01")
        self.assertEqual(len(rows), n)
        self.assertAlmostEqual(rows[0]["tpw_kgm2"], 30.0, places=3)
        self.assertAlmostEqual(rows[1]["tpw_kgm2"] - rows[0]["tpw_kgm2"], 0.1, places=3)
        self.assertAlmostEqual(rows[0]["sst_c"], 20.0 + 0.01 * (1988 - 1960) * 12, places=3)
        self.assertGreater(meta["rss_cells_dropped"], 0)
        self.assertLess(meta["common_area_fraction"], 1.0)
