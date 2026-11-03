"""Alerte de fraîcheur : quand la fenêtre peut avancer, téléchargements en échec, pas de doublon d'issue."""
import json
import unittest
from unittest import mock

from etl import fraicheur as X


def report(**kw):
    base = dict(current_end=2021, gironde_end=2024, monde_end=2025, stations={2021: 220, 2022: 230, 2023: 225}, possible_end=2023)
    return X.Report(**{**base, **kw})


class FinPossible(unittest.TestCase):
    def test_avance_jusqua_la_derniere_annee_permise(self):
        self.assertEqual(X.possible_end(2021, 2024, 2025, {2021: 300, 2022: 250, 2023: 240, 2024: 230}), 2024)

    def test_limitee_par_la_gironde(self):
        self.assertIsNone(X.possible_end(2021, 2021, 2025, {2022: 300}))
        self.assertEqual(X.possible_end(2021, 2022, 2025, {2022: 300, 2023: 300}), 2022)

    def test_limitee_par_le_globe(self):
        self.assertEqual(X.possible_end(2021, 2030, 2023, {2023: 300, 2024: 300}), 2023)

    def test_seuil_de_stations_france(self):
        self.assertIsNone(X.possible_end(2021, 2024, 2025, {2022: 219, 2023: 80}))
        self.assertEqual(X.possible_end(2021, 2024, 2025, {2022: 220, 2023: 80}), 2022)

    def test_fin_actuelle_ne_declenche_rien(self):
        self.assertIsNone(X.possible_end(2021, 2021, 2021, {2021: 300}))


class Telechargements(unittest.TestCase):
    def test_repere_les_echecs_sans_doublon(self):
        text = "OK tm-france\nLSH TN : téléchargement impossible (HTTP 503), cache réutilisé\nLSH TN : téléchargement impossible (HTTP 503), cache réutilisé\nOK x\n"
        self.assertEqual(X.stale_downloads(text), ["LSH TN : téléchargement impossible (HTTP 503), cache réutilisé"])

    def test_journal_propre(self):
        self.assertEqual(X.stale_downloads("OK tm-france\n"), [])


class Issues(unittest.TestCase):
    def test_rien_a_signaler(self):
        self.assertEqual(X.issues_for(report(possible_end=None)), [])

    def test_extension_decrit_la_decision(self):
        (title, body), = X.issues_for(report())
        self.assertIn("2023", title)
        self.assertIn("T_SPAN", body)
        self.assertIn("| 2022 | 230 |", body)

    def test_echec_de_telechargement(self):
        titles = [t for t, _ in X.issues_for(report(possible_end=None, stale=["LSH TN : ... cache réutilisé"]))]
        self.assertEqual(len(titles), 1)
        self.assertIn("téléchargements", titles[0])

    def test_pas_de_doublon(self):
        calls = []

        def fake(*args):
            calls.append(args)
            return json.dumps([{"title": "déjà ouverte"}]) if args[1] == "list" else ""

        with mock.patch.object(X, "gh", fake):
            created = X.open_issues([("déjà ouverte", "b"), ("nouvelle", "b")])
        self.assertEqual(created, ["nouvelle"])
        self.assertEqual(sum(c[1] == "create" for c in calls), 1)

    def test_aucun_appel_sans_alerte(self):
        with mock.patch.object(X, "gh", side_effect=AssertionError):
            self.assertEqual(X.open_issues([]), [])


if __name__ == "__main__":
    unittest.main()
