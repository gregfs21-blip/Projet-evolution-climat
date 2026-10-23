"""« Largeur d'abord » : lecteurs des sources (extraits au format constaté par la sonde) et constructeur générique."""

import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import numpy as np

from etl.context import make_context
from etl.indicators import serie as S
from etl.indicators import temperature as T
from etl.schema import Indicator
from etl.sources import globaux as G

GML = """# --------------------------------------------------------------------
# USE OF NOAA GML DATA
#
year,mean,unc
1979,336.85,0.11
1980,338.91,0.11
1981,340.11,0.11
"""
GISTEMP = """Land-Ocean: Global Means
Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D,D-N,DJF,MAM,JJA,SON
1880,-.19,-.25,-.09,-.16,-.10,-.21,-.19,-.10,-.15,-.23,-.22,-.18,-.17,***,***,-.12,-.17,-.20
2026,1.10,1.20,***,***,***,***,***,***,***,***,***,***,***,***,1.1,***,***,***
"""
HADCRUT = """Time,Anomaly (deg C),Lower confidence limit (2.5%),Upper confidence limit (97.5%)
1850,-0.4177114,-0.58925647,-0.2461663
1851,-0.2333498,-0.41186792,-0.054831687
"""
BERKELEY = """% This file contains a brief summary
%
% Year, Annual Anomaly, Annual Unc., Five-year Anomaly, Five-year Unc.
  1850    -0.432     0.170       NaN       NaN
  1851    -0.336     0.192       NaN       NaN
"""
ONI = """ SEAS  YR   TOTAL   ANOM
""" + "".join(f"  {s} 1950  25.01  {a:.2f}\n" for s, a in zip(["DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ"],
                                                            [-1.2] * 12)) + "  DJF 1951  25.67  -0.66\n"
NSIDC = """year, mo,source_dataset, region, extent,   area
1979,  9,    NSIDC-0051,      N,   7.05,   4.58
1980,  9,    NSIDC-0051,      N,   7.67,   4.87
1981,  9,    NSIDC-0051,      N,  -9999,  -9999
"""
OHC = """    YEAR      WO    WOse      NH    NHse      SH    SHse
1955.500  -3.201   1.700  -1.439   0.937  -1.762   0.771
1956.500  -2.608   0.719  -1.843   0.385  -0.765   0.533
"""
PSMSL = """1807;  6958;N;000
1808;-99999;N;000
1809;  6980;Y;001
1810;  6990;N;000
"""


class TestParsers(unittest.TestCase):
    def test_gml(self):
        self.assertEqual(G.parse_gml(GML), {1979: 336.85, 1980: 338.91, 1981: 340.11})

    def test_gistemp_ignore_annee_incomplete(self):
        self.assertEqual(G.parse_gistemp(GISTEMP), {1880: -0.17})

    def test_hadcrut_berkeley(self):
        self.assertAlmostEqual(G.parse_hadcrut5(HADCRUT)[1851], -0.2333498)
        self.assertEqual(G.parse_berkeley(BERKELEY), {1850: -0.432, 1851: -0.336})

    def test_oni_annees_completes(self):
        self.assertEqual(G.parse_oni(ONI), {1950: -1.2})

    def test_nsidc_manquant(self):
        self.assertEqual(G.parse_nsidc(NSIDC), {1979: 7.05, 1980: 7.67})

    def test_ohc_annee_milieu(self):
        self.assertEqual(G.parse_ohc(OHC), {1955: -3.201, 1956: -2.608})

    def test_psmsl_manquant_et_douteux(self):
        self.assertEqual(G.parse_psmsl(PSMSL), {1807: 6958.0, 1810: 6990.0})


def series(start, end, slope, base=0.0, noise=0.05, seed=1):
    rng = np.random.default_rng(seed)
    return {y: base + slope * (y - start) + rng.normal(0, noise) for y in range(start, end + 1)}


class TestReference(unittest.TestCase):
    def ref(self, **kw):
        return dict(statement="s", source="src", url="https://x.org", unit="u", fixed_on="2026-10-23", **kw)

    def test_rate(self):
        s = series(2000, 2025, 2.4)
        c = S.check_reference(self.ref(kind="rate", period=[2010, 2019], range=[2.14, 2.62]), s, set(s), "ppm")
        self.assertTrue(c.satisfied)
        self.assertAlmostEqual(c.measured, 2.4, delta=0.05)

    def test_rate_tolere_lacunes_jusqu_a_20_pourcent(self):
        s = series(1900, 1980, 0.13, noise=0.01)
        for y in (1944, 1945, 1946):
            s.pop(y)
        self.assertTrue(S.check_reference(self.ref(kind="rate", period=[1901, 1971], range=[0.1, 0.2]), s, set(s), "mm").satisfied)

    def test_difference(self):
        s = {y: (0.0 if y <= 1900 else 1.1) for y in range(1850, 2021)}
        c = S.check_reference(self.ref(kind="difference", base=[1850, 1900], period=[2011, 2020], range=[0.95, 1.2]), s, set(s), "°C")
        self.assertEqual((c.measured, c.satisfied), (1.1, True))

    def test_relative_slope(self):
        s = {y: 7.0 - 0.08 * (y - 1979) for y in range(1979, 2025)}
        c = S.check_reference(self.ref(kind="relative_slope", base=[1981, 2010], period=[1979, 2024], range=[-15, -10]), s, set(s), "")
        base = sum(s[y] for y in range(1981, 2011)) / 30
        self.assertAlmostEqual(c.measured, -0.8 / base * 100, places=2)
        self.assertTrue(c.satisfied)

    def test_not_significant(self):
        rng = np.random.default_rng(3)
        s = {y: 900 + rng.normal(0, 120) for y in range(1961, 2011)}
        c = S.check_reference(self.ref(kind="not_significant", period=[1961, 2010]), s, set(s), "mm")
        self.assertTrue(c.satisfied)

    def test_periode_incomplete_non_satisfaite(self):
        s = series(1990, 2025, 1.0)
        c = S.check_reference(self.ref(kind="slope", period=[1980, 2020], range=[0, 100]), s, set(s), "u")
        self.assertIsNone(c.measured)
        self.assertFalse(c.satisfied)


class TestBuild(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ctx = make_context(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def build(self, data, **kw):
        params = dict(source="co2-gl", scale="monde", variable="co2", place={"id": "monde", "name": "Monde"},
                      where="En moyenne mondiale", label="la concentration de CO₂", title="CO₂", description="d", limitations=[])
        params.update(kw)
        with mock.patch.object(G, "load", return_value=data):
            return S.build(self.ctx, **params)

    def test_confiance_elevee_avec_reference_satisfaite(self):
        ind = self.build(series(1979, 2025, 2.4, base=337),
                         reference=dict(kind="rate", period=[2010, 2019], range=[2.14, 2.62], unit="ppm/an", statement="s",
                                        source="NOAA", url="https://gml.noaa.gov", fixed_on="2026-10-23"))
        Indicator.model_validate(ind.model_dump())
        self.assertEqual((ind.id, ind.place.kind, ind.confidence), ("co2-monde", "composite", "elevee"))
        self.assertTrue(ind.reference_check.satisfied)
        self.assertIn("ppm par décennie", ind.finding)

    def test_sans_reference_au_plus_moyenne(self):
        ind = self.build(series(1979, 2025, 2.4, base=337))
        self.assertEqual(ind.confidence, "moyenne")
        self.assertTrue(any("Aucune référence" in lim for lim in ind.limitations))

    def test_reference_non_satisfaite_au_plus_moyenne(self):
        ind = self.build(series(1979, 2025, 2.4, base=337),
                         reference=dict(kind="rate", period=[2010, 2019], range=[5, 6], unit="ppm/an", statement="s",
                                        source="NOAA", url="https://gml.noaa.gov", fixed_on="2026-10-23"))
        self.assertEqual(ind.confidence, "moyenne")

    def test_ligne_de_base(self):
        ind = self.build(series(1950, 2020, 0.01), baseline=[1961, 1990], source="hadcrut5", variable="temperature-hadcrut5")
        self.assertTrue(ind.is_anomaly)
        vals = dict(zip(ind.series.time, ind.series.value))
        self.assertAlmostEqual(sum(vals[str(y)] for y in range(1961, 1991)) / 30, 0.0, places=3)

    def test_ligne_de_base_serie(self):
        ind = self.build({**series(1990, 2020, 3.0, base=7000)}, baseline="series", source="psmsl-1", variable="niveau-mer",
                         scale="france", place={"id": "brest", "name": "Brest", "kind": "station"},
                         station={"id": "PSMSL-1", "name": "Brest", "lat": 48.4, "lon": -4.5})
        self.assertEqual((ind.reference_period.start, ind.reference_period.end), (1990, 2020))
        self.assertEqual(ind.place.kind, "station")
        self.assertAlmostEqual(sum(ind.series.value) / len(ind.series.value), 0.0, places=6)


def lsh_rr_zip(raw: Path):
    """Archive LSH RR synthétique : 3 postes, cumuls mensuels ~ 75 mm, homogénéisés jusqu'en 2017."""
    rng = np.random.default_rng(5)
    with zipfile.ZipFile(raw / "lsh" / "SH_RR_metropole.zip", "w") as z:
        for i, poste in enumerate(["33000001", "33000002", "33000003"]):
            lines = ["# DONNEES MENSUELLES HOMOGENEISEES de RR : test", f"# NUM_POSTE= {poste}", f"# NOM_USUEL= POSTE {i}",
                     "# LATITUDE (°) = 44.8", "# LONGITUDE(°)= -0.6", "# ALTITUDE (m) = 20", f"# NUM_SERIE= MRR2{poste}",
                     "# Période homogénéisée : 195001 201712", "YYYYMM;VALEUR;Q_HOM"]
            for y in range(1950, 2025):
                for m in range(1, 13):
                    lines.append(f"{y}{m:02d};{max(0, 75 + rng.normal(0, 30)):.1f};{1 if y <= 2017 else 0}")
            z.writestr(f"SH_MRR2{poste}.csv", "\n".join(lines) + "\n")


class TestLshAnnual(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from etl.tests.fixtures import make_raw_dir
        cls.tmp = tempfile.TemporaryDirectory()
        cls.raw = make_raw_dir(Path(cls.tmp.name))
        lsh_rr_zip(cls.raw)
        cls.ctx = make_context(cls.raw)
        cls.p = mock.patch.object(T, "station_config", return_value={})
        cls.p.start()

    @classmethod
    def tearDownClass(cls):
        cls.p.stop()
        cls.tmp.cleanup()
        os.environ.pop("LSH_OFFLINE", None)

    def test_station(self):
        ind = S.build_lsh(self.ctx, lsh_var="RR", poste="33000001", variable="rr-cumul", title="Pluie à {name}",
                          description="d {name}", label="le cumul")
        self.assertEqual((ind.id, ind.unit, ind.place.id), ("rr-cumul-poste-0", "mm", "poste-0"))
        self.assertEqual(ind.series.quality[ind.series.time.index("2017")], "homogenized")
        self.assertEqual(ind.series.quality[ind.series.time.index("2018")], "raw")
        self.assertEqual(ind.trend.period.end, 2017)

    def test_composite_et_reference_sans_tendance(self):
        ind = S.build_lsh_composite(self.ctx, lsh_var="RR", variable="rr-cumul", span=[1961, 2017], title="Pluie",
                                    description="d", label="le cumul",
                                    reference=dict(kind="not_significant", period=[1961, 2010], unit="", statement="s",
                                                   source="src", url="https://x.org", fixed_on="2026-10-23"))
        self.assertEqual(len(ind.stations), 3)
        self.assertTrue(ind.reference_check.satisfied)      # bruit blanc : aucune tendance
        self.assertEqual(ind.confidence, "non_etabli")

    def test_unite_aberrante_refusee(self):
        with mock.patch.dict(S.PLAUSIBLE, {"rr-cumul": (10, 20)}):
            with self.assertRaises(ValueError):
                S.build_lsh(self.ctx, lsh_var="RR", poste="33000001", variable="rr-cumul", title="t {name}",
                            description="d {name}", label="l")


if __name__ == "__main__":
    unittest.main()
