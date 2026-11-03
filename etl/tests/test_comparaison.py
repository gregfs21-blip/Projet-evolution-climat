"""Pente de comparaison entre échelles : même fenêtre, années homogénéisées seulement, rien d'autre ne change."""
import unittest
from datetime import datetime, timezone

from etl.indicators import comparaison as C
from etl.schema import Indicator, Provenance, Series


def make(ind_id="tm-france", start=1950, end=2024, raw_from=None, gap=None):
    years = [y for y in range(start, end + 1) if y != gap]
    return Indicator(
        id=ind_id, scale="france", title="Test", unit="°C", description="d", frequency="annual", is_anomaly=False, reference_period=None, trend=None,
        series=Series(time=[str(y) for y in years], value=[0.03 * (y - start) for y in years],
                      quality=["raw" if raw_from and y >= raw_from else "homogenized" for y in years]),
        finding="f", confidence="moyenne", limitations=["l"],
        provenance=Provenance(source_name="s", source_url="https://x.org", license="l", extracted_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                              script="t", etl_version="0", homogenized=True),
    )


class Comparaison(unittest.TestCase):
    def test_ajoute_la_fenetre_commune(self):
        out = C.with_comparison(make())
        t = out.alt_trends[-1]
        self.assertEqual((t.period.start, t.period.end), (1959, 2021))
        self.assertEqual(t.label, C.LABEL)
        self.assertAlmostEqual(t.slope_per_decade, 0.3, places=3)

    def test_ne_touche_pas_au_reste(self):
        ind = make()
        out = C.with_comparison(ind)
        self.assertEqual(out.trend, ind.trend)
        self.assertEqual(out.confidence, ind.confidence)
        self.assertEqual(out.finding, ind.finding)

    def test_autre_indicateur_inchange(self):
        ind = make(ind_id="tx-france")
        self.assertEqual(C.with_comparison(ind).alt_trends, [])

    def test_annees_brutes_exclues_sans_chevauchement(self):
        out = C.with_comparison(make(raw_from=2023))
        self.assertEqual(out.alt_trends[-1].period.end, 2021)

    def test_fenetre_incomplete_echoue(self):
        for kw in ({"start": 1960}, {"end": 2020}, {"gap": 1990}, {"raw_from": 2015}):
            with self.assertRaises(ValueError):
                C.with_comparison(make(**kw))

    def test_libelle_distinct_de_la_periode_commune_des_stations(self):
        # Le site repère la période commune des stations par ce texte : les deux ne doivent pas se confondre.
        self.assertNotIn("période commune", C.LABEL)


if __name__ == "__main__":
    unittest.main()
