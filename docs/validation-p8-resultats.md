# Validation P8 — résultats automatiques

Fichier généré par `python -m etl.validation.p8` à chaque exécution de l'ETL. Ne pas éditer à la main. Critères : `docs/phases.md` (P8).

**Au moins un critère comptant pour la clôture n'est pas satisfait.**

| Critère | Résultat | Mesure |
|---|---|---|
| M1 chiffres produits par l'ETL | ✅ conforme | aucun nombre écrit en dur hors années et seuils déclarés |
| M2 confiance et type d'affirmation | ✅ conforme | 57 affirmations qualifiées selon S1, aucune règle S2 enfreinte |
| M3 couverture | ✅ conforme | chaque case publiée de la couverture a au moins une affirmation à son échelle |
| M4 comparaisons sur période commune (S3) | ✅ conforme | 8 affirmations de comparaison ; tm-gironde-monde 1959-2021 : plus rapide; tm-france-monde 1959-2021 : plus rapide; tm-gironde-france 1959-2021 : du même ordre; sst-golfe-monde 1976-2025 : plus rapide; mer-gironde-monde 1993-2024 : du même ordre; tlt-rss-uah 1979-2025 : plus rapide; tx-tn-gironde 1953-2022 : du même ordre; tx-tn-france 1959-2021 : du même ordre |
| M5 accélération du niveau marin 1993-2017 | ✅ conforme | 0.067 mm/an² (IC 0.006 à 0.128, p = 0.032089) ; fourchette [0.059 ; 0.109] (Nerem et al., 2018) |
| M6 relecture indépendante | ❌ non conforme | relecture indépendante non close (docs/relecture-p8.md) |
| M7 section exploratoire (P7) | ✅ conforme | en attente du relevé P7, mention affichée |
| Accélération gmsl | ℹ️ information | niveau-mer-monde 1993-2024 : 0.07642 par an² (IC 0.04505 à 0.1078), p = 2.7e-05, Newey-West décalage 2 |
| Accélération gmsl-nerem | ℹ️ information | niveau-mer-monde 1993-2017 : 0.06723 par an² (IC 0.006301 à 0.1282), p = 0.032089, Newey-West décalage 2 |
| Accélération co2 | ℹ️ information | co2-monde 1979-2025 : 0.03219 par an² (IC 0.02969 à 0.03469), p = 0.0, Newey-West décalage 2 |
| Accélération ch4 | ℹ️ information | ch4-monde 1984-2025 : 0.08231 par an² (IC -0.05999 à 0.2246), p = 0.249118, Newey-West décalage 2 |
| Accélération hadcrut | ℹ️ information | temperature-hadcrut5-monde 1970-2025 : 0.0002607 par an² (IC -1.729e-05 à 0.0005387), p = 0.065466, Newey-West décalage 2 |
| Accélération berkeley | ℹ️ information | temperature-berkeley-monde 1970-2024 : 0.0002186 par an² (IC -3.566e-05 à 0.0004728), p = 0.09043, Newey-West décalage 2 |
| Accélération tm-france | ℹ️ information | tm-france 1959-2021 : 0.000903 par an² (IC -0.0001771 à 0.001983), p = 0.099663, Newey-West décalage 2 |
| Accélération tm-gironde | ℹ️ information | tm-annuelle-gironde 1953-2022 : 0.0007811 par an² (IC 0.0001234 à 0.001439), p = 0.020645, Newey-West décalage 3 |
| Répartition des affirmations | ℹ️ information | absence 16, acceleration 2, comparaison 8, contexte 4, information 5, lacune 12, signal 31 |
