# Validation P9 — résultats automatiques

Fichier généré par `python -m etl.validation.p9` à chaque exécution de l'ETL. Ne pas éditer à la main. Critères : `docs/phases.md` (P9).

**Tous les critères comptant pour la clôture sont satisfaits.**

| Critère | Résultat | Mesure |
|---|---|---|
| N1 exhaustivité | ✅ conforme | 6 séries sur 6 publiées ; câble du détroit de Floride déclaré « sans donnée » (D-AA); transport de chaleur publié en plus |
| N2 complétude | ✅ conforme | RAPID : 2004 (9 mois) écartées; EN4 : 2026 (9 mois) écartée(s) |
| N3 plausibilité | ✅ conforme | câble : sans objet (aucune donnée) ; amoc-debit : moyenne 2005-2024 = 17,03 Sv (attendu 15,5 à 18,5) ; amoc-profondeur : moyenne 2005-2024 = 1002 m (attendu 700,0 à 1300,0) |
| N4 correction géomagnétique | ✅ conforme | câble seul : sans objet tant qu'il est « sans donnée ». RAPID utilise depuis la version v2023.1 le débit du détroit de Floride corrigé de la dérive séculaire du champ géomagnétique (README RAPID ; Volkov et al., 2024) ; version lue : v2024-2 |
| N5 robustesse sans les années du relais du câble (information) | ℹ️ information | tendance avec et sans 2023-2024 (câble en panne depuis novembre 2023) : amoc-debit : 2005-2024 -0,717, 2005-2022 -0,976 Sv/déc. (même signe) ; amoc-profondeur : 2005-2024 +6,717, 2005-2022 +6,833 m/déc. (même signe) ; amoc-chaleur : 2005-2024 -0,009, 2005-2022 -0,031 PW/déc. (même signe) |
| N6 technique | ℹ️ information | Tests, contrat et construction des pages vérifiés par la CI (ci.yml), hors de ce module, comme pour les phases précédentes. |
| N7 couverture d'observations | ✅ conforme | salinite-0700-gulf-stream : début 1995 ; salinite-0700-gyre-subpolaire : début 1996 ; temperature-0700-gulf-stream : début 1953 ; temperature-0700-gyre-subpolaire : début 1961 |
