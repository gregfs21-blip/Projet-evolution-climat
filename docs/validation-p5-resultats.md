# Validation P5 — résultats automatiques

Fichier généré par `python -m etl.validation.p5` à chaque exécution de l'ETL. Ne pas éditer à la main. Critères : `docs/phases.md` (P5).

**Tous les critères comptant pour la clôture sont satisfaits.**

| Critère | Résultat | Mesure |
|---|---|---|
| J1 exhaustivité | ✅ conforme | 4 indicateurs sur 4 |
| J2 complétude | ℹ️ information | Appliquée par le code : années de 12 mois homogénéisés, réseau constant 1959-2021 (températures) et 1961-2020 (pluie). |
| J3 brut ≠ homogénéisé | ✅ conforme | Tendances, normales et R10 sur les seules années où toutes les stations sont homogénéisées. |
| J4 validation externe (R10, TM) | ✅ conforme | attendu [+0,2 ; +0,4] °C/déc. sur 1959-2021 ; mesuré : +0,344 |
| J5 cohérence spatiale (contrôle interne) | ✅ conforme | 220 pentes positives sur 220 (100,0 %) ; médiane +0,34 °C/déc. |
| J6 robustesse de la pondération | ✅ conforme | pondéré par département +0,344 ; moyenne simple +0,348 °C/déc. ; écart admis 0,05 |
| J7 plausibilité | ✅ conforme | Bornes contrôlées à la construction pour les 4 indicateurs publiés (un dépassement empêche la publication). |
| J8 technique | ℹ️ information | Tests, CI et contrat vérifiés par les workflows. |
