"""« Largeur d'abord », lot 2 : lecteurs (extraits au format constaté par la sonde du 25/10/2026) et constructeurs."""

import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from etl.context import make_context
from etl.indicators import atmosphere as A
from etl.indicators import serie as S
from etl.schema import Indicator, Provenance
from etl.sources import globaux as G
from etl.sources import igra
from etl.sources.meteofrance_quot import Daily
from etl import vocabulary as vocab

CAG = """# Title: "Global Ocean January - December Average Temperature Departures"
# Units: Degrees Celsius
# Base Period: 1901-2000
Year,Departure from Average
1850,0
1851,0.06
1852,-0.07
"""
HADSST = """year,anomaly,total_uncertainty,uncorrelated_uncertainty
1850,-0.334,0.169,0.06
1851,-0.271,0.152,0.06
2026,0.9,0.1,0.01
"""


def oisst(year_days: dict[int, int]) -> str:
    rows = ["time,zlev,latitude,longitude,sst", "UTC,m,degrees_north,degrees_east,degree_C"]
    for y, n in year_days.items():
        d = date(y, 1, 1)
        for i in range(n):
            rows.append(f"{(d + timedelta(days=i)).isoformat()}T12:00:00Z,0.0,45.125,-1.875,{14 + (i % 2):.2f}")
    return "\n".join(rows) + "\n"


IBT_HEADER = "SID,SEASON,NUMBER,BASIN,SUBBASIN,NAME,ISO_TIME,NATURE,LAT,LON,WMO_WIND,WMO_PRES,WMO_AGENCY,TRACK_TYPE,DIST2LAND,LANDFALL,IFLAG,USA_AGENCY,USA_ATCF_ID,USA_LAT,USA_LON,USA_RECORD,USA_STATUS,USA_WIND,USA_PRES,USA_SSHS"
IBT_UNITS = "  ,Year, , , , ,  , ,degrees_north,degrees_east,kts,mb, , ,km,km, , , ,degrees_north,degrees_east, , ,kts,mb,1"


def ibt(sid, season, time, nature, track, wind, sshs):
    return f"{sid},{season},1,NA,NA,X,{time},{nature},20,-60,,,,{track},100,100,,,,20,-60,,,{wind},,{sshs}"


IBTRACS = "\n".join([
    IBT_HEADER, IBT_UNITS,
    ibt("A", 2000, "2000-08-01 00:00:00", "TS", "main", 30, -1),        # dépression : pas d'ACE
    ibt("A", 2000, "2000-08-01 06:00:00", "TS", "main", 50, 0),         # 0,25
    ibt("A", 2000, "2000-08-01 09:00:00", "TS", "main", 70, 1),         # heure non synoptique : compte pour la catégorie, pas l'ACE
    ibt("A", 2000, "2000-08-01 12:00:00", "TS", "main", 100, 3),        # 1,00
    ibt("A", 2000, "2000-08-02 00:00:00", "ET", "main", 60, -4),        # post-tropical : pas d'ACE
    ibt("B", 2000, "2000-09-01 00:00:00", "TS", "main", 40, 0),         # 0,16, tempête seulement
    ibt("C", 2000, "2000-09-03 00:00:00", "TS", "spur-other", 90, 2),   # trajectoire secondaire : ignorée
    ibt("D", 2001, "2001-09-01 00:00:00", "TS", "PROVISIONAL", 80, 1),  # 0,64, ouragan
    ibt("E", 1950, "1950-09-01 00:00:00", "TS", "main", 80, 1),         # avant 1966 : hors série
]) + "\n"


def igra_line(press_pa: int, gph: int, temp_tenths: int, tflag: str = " ") -> str:
    return f"21 -9999 {press_pa:6d} {gph:5d} {temp_tenths:5d}{tflag}-9999 -9999 -9999 -9999"


class TestParsers(unittest.TestCase):
    def test_cag(self):
        self.assertEqual(G.parse_cag(CAG), {1850: 0.0, 1851: 0.06, 1852: -0.07})

    def test_hadsst(self):
        self.assertEqual(G.parse_hadsst(HADSST), {1850: -0.334, 1851: -0.271, 2026: 0.9})

    def test_oisst_years_complete_only(self):
        out = G.parse_oisst_point(oisst({1982: 365, 1983: 100, 1984: 366}))
        self.assertEqual(set(out), {1982, 1984})
        self.assertAlmostEqual(out[1984], 14.5, places=2)

    def test_ibtracs_hurricanes(self):
        self.assertEqual(G.parse_ibtracs_hurricanes(IBTRACS), {2000: 1.0, 2001: 1.0})

    def test_ibtracs_ace(self):
        self.assertEqual(G.parse_ibtracs_ace(IBTRACS), {2000: 1.41, 2001: 0.64})

    def test_igra_levels_hour_and_flags(self):
        lines = [
            "#FRM00007510 1990 01 02 12 1115   10 ncdc6310          448306    -6914",
            igra_line(85000, 1500, -12),
            igra_line(50000, 5560, -255),
            igra_line(70000, 3000, -80),                    # niveau non demandé
            "#FRM00007510 1990 01 02 00 2315    3 ncdc6310          448306    -6914",
            igra_line(85000, 1490, 50),                     # 00 UTC : ignoré
            "#FRM00007510 1990 01 03 12 1115    3 ncdc6310          448306    -6914",
            igra_line(85000, -9999, -20),                   # géopotentiel manquant
            igra_line(50000, 5570, -250, tflag="X"),         # température rejetée par le drapeau
        ]
        out = igra.parse(lines, (850, 500), 12)
        self.assertEqual(out[850]["temp"][(1990, 1)], [-1.2, -2.0])
        self.assertEqual(out[850]["gph"][(1990, 1)], [1500.0])
        self.assertEqual(out[500]["temp"][(1990, 1)], [-25.5])
        self.assertEqual(out[500]["gph"][(1990, 1)], [5560.0, 5570.0])


CATNAT = """id_gaspar;code_commune;libelle_commune;num_risque_jo;lib_risque_jo;date_debut;date_fin;date_signature_arrete;date_publication_jo;date_modification
A;33436;Saint-Magne;CMV;Chocs Mécaniques;1999-12-25 12:00:00;1999-12-29 12:00:00;x;x;x
A;33436;Saint-Magne;CMV;Chocs Mécaniques;1999-12-25 12:00:00;1999-12-29 12:00:00;x;x;x
A;33436;Saint-Magne;ICB;Inondations;1999-12-25 12:00:00;1999-12-29 12:00:00;x;x;x
B;37100;Ã‰peignÃ©;SEC;SÃ©cheresse;2003-07-01 02:00:00;2003-09-30 02:00:00;x;x;x
C;33063;Bordeaux;SEC;Sécheresse;1981-07-01 02:00:00;x;x;x;x
"""


class TestCatnat(unittest.TestCase):
    def test_department_duplicates_and_zero_years(self):
        out = G.parse_catnat(CATNAT, department="33")
        self.assertEqual(out[1999], 2.0)                         # doublon retiré, deux périls
        self.assertEqual(out[2003], 0.0)                         # année sans reconnaissance : zéro, pas absente
        self.assertNotIn(1981, out)                              # avant le régime (1982)
        self.assertEqual(max(out), date.today().year - 1 - G.CATNAT_LAG)

    def test_peril_matches_badly_encoded_label(self):
        out = G.parse_catnat(CATNAT, peril="cheresse")
        self.assertEqual(sum(out.values()), 1.0)
        self.assertEqual(out[2003], 1.0)


class TestAggregates(unittest.TestCase):
    def test_igra_annual_requires_every_month(self):
        monthly = {(2000, m): [1.0] * 15 for m in range(1, 13)}
        monthly.update({(2001, m): [2.0] * 20 for m in range(1, 13)})
        monthly[(2001, 7)] = [2.0] * 14
        self.assertEqual(A.igra_annual(monthly), {2000: 1.0})

    def test_fxi_counts_etccdi(self):
        daily = {}
        d = date(2000, 1, 1)
        while d.year == 2000:
            daily[d.isoformat()] = Daily(30.0 if d.day == 1 else 10.0, "1")
            d += timedelta(days=1)
        for k in ["2000-02-02", "2000-02-03", "2000-02-04"]:      # 3 jours absents : année gardée
            del daily[k]
        self.assertEqual(A.fxi_counts(daily, 27.8), {2000: 12.0})
        del daily["2000-02-05"]                                     # 4 jours absents en février : année écartée
        self.assertEqual(A.fxi_counts(daily, 27.8), {})

    def test_era5_annual(self):
        days = [date(2001, 1, 1) + timedelta(days=i) for i in range(365)]
        gust = {d: (60.0 if i < 10 else 30.0) for i, d in enumerate(days)}
        gust[days[50]] = 120.0
        cols = {"wind_gusts_10m_max": gust, "pressure_msl_mean": {d: 1015.0 for d in days[:-1]}}
        self.assertEqual(A.era5_annual("jours-vent-fort", cols), {2001: 11.0})
        self.assertEqual(A.era5_annual("rafale-max", cols), {2001: 120.0})
        self.assertEqual(A.era5_annual("pression", cols), {})     # un jour manque : année écartée


class TestRules(unittest.TestCase):
    REF = {"kind": "mean", "period": [1991, 2020], "range": [6.5, 7.5], "unit": "ouragans", "fixed_on": "2026-10-25",
           "statement": "s", "source": "src", "url": "https://example.org"}

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ctx = make_context(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def _assemble(self, series, raw_reason=None, reference=None):
        prov = Provenance(source_name="x", source_url="https://example.org", license="l", extracted_at=self.ctx.extracted_at,
                          script="t", etl_version="0", homogenized=False)
        return S.assemble(self.ctx, ind_id="ouragans-monde", scale="monde", variable="ouragans",
                          place=vocab.composite("monde", "Atlantique Nord"), title="t", description="d", unit="ouragans",
                          series=series, hom=set(series), provenance=prov, limitations=["l"], stations=[], method_note=None,
                          reference=reference, baseline=None, group="g", where="Ici", label="x", raw_reason=raw_reason)

    def test_mean_reference_never_gives_high_confidence(self):
        series = {y: 5.0 + (y - 1966) * 0.05 + (0.3 if y % 2 else -0.3) for y in range(1966, 2026)}
        ind = self._assemble(series, reference=self.REF)
        self.assertTrue(ind.trend.significant)
        self.assertTrue(ind.reference_check.satisfied)
        self.assertEqual(ind.confidence, "moyenne")
        self.assertTrue(any("niveau moyen" in x for x in ind.limitations))
        Indicator.model_validate(ind.model_dump())

    def test_mean_reference_measured(self):
        series = {y: 7.0 for y in range(1966, 2026)}
        ind = self._assemble(series, reference=self.REF)
        self.assertEqual(ind.reference_check.measured, 7.0)
        self.assertTrue(ind.reference_check.satisfied)

    def test_raw_series_published_without_trend(self):
        series = {y: float(y % 5) for y in range(1950, 2026)}
        ind = self._assemble(series, raw_reason="série brute.")
        self.assertIsNone(ind.trend)
        self.assertEqual(ind.alt_trends, [])
        self.assertEqual(ind.normals, [])
        self.assertEqual(set(ind.series.quality), {"raw"})
        self.assertEqual(ind.confidence, "non_etabli")
        self.assertIn("série brute.", ind.finding)
        Indicator.model_validate(ind.model_dump())


if __name__ == "__main__":
    unittest.main()
