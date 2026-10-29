# Validation P4 — résultats automatiques

Fichier généré par `python -m etl.validation.p4` à chaque exécution de l'ETL. Ne pas éditer à la main. Critères : `docs/phases.md` (P4).

**Tous les critères comptant pour la clôture sont satisfaits.**

| Critère | Résultat | Mesure |
|---|---|---|
| I1 exhaustivité | ✅ conforme | 27 indicateurs sur 27 |
| I2 complétude | ℹ️ information | Appliquée par le code : mois à 3 jours absents au plus, TN et TX complets (stations) ; saisons complètes (ERA5). |
| I3 brut ≠ homogénéisé | ✅ conforme | Tendances et normales sur les seules années dont TN et TX sont corrigés sur 12 mois. |
| I4 validation externe (R9, Huglin) | ☑ écart accepté le 28/10/2026 (stations contre grille SAFRAN du vignoble) | attendu [+102 ; +152] °C·j entre 1980-1999 et 2000-2019 ; mesuré : gironde : +158,0 ; bordeaux-paulin : +162,0 ; cap-ferret : +160,9 ; bordeaux-merignac : +165,1 ; cazaux : +148,1 ; villenave-d-ornon : — |
| I5 cohérence physique (vendanges ~ Huglin) | ✅ conforme | r = -0,84 sur 54 années (1953-2006) ; seuil r ≤ −0,6 |
| I6 cohérence entre stations (Huglin) | ✅ conforme | bordeaux-paulin +83,6 °C·j/déc. ; cap-ferret +72,8 °C·j/déc. ; bordeaux-merignac +71,6 °C·j/déc. ; cazaux +69,9 °C·j/déc. ; villenave-d-ornon +55,1 °C·j/déc. |
| I7 plausibilité | ✅ conforme | Bornes contrôlées à la construction pour les 27 indicateurs publiés (un dépassement empêche la publication). |
| I8 CatNat par péril sans tendance | ✅ conforme | aucune tendance ni normale |
| I9 technique | ℹ️ information | Tests, CI et contrat vérifiés par les workflows. |
