# Validation P7 — résultats automatiques

Fichier généré par `python -m etl.validation.p7` à chaque exécution de l'ETL. Ne pas éditer à la main. Critères : `docs/phases.md` (P7).

**Tous les critères comptant pour la clôture sont satisfaits.**

| Critère | Résultat | Mesure |
|---|---|---|
| L1 exhaustivité | ✅ conforme | 4 indicateurs sur 4 |
| L2 complétude | ℹ️ information | Saisons retenues si tous leurs jours (blocages) ou leurs 3 mois (CAPE) existent ; années complètes (Z500). |
| L3 plausibilité climatologique | ✅ conforme | jours bloqués 1981-2010 : hiver 33,9 %, été 17,6 % (attendu : hiver > été, chacun entre 5 et 40 %) |
| L4 robustesse au secteur (information) | ℹ️ information | hiver : 30° O-30° E -2,00, 20° O-40° E -2,11 jours/déc. (même signe) ; ete : 30° O-30° E -0,91, 20° O-40° E -0,62 jours/déc. (même signe) |
| L5 technique | ℹ️ information | Tests, CI et contrat vérifiés par les workflows. |
