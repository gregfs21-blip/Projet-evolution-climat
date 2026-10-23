# Validation P1 — résultats automatiques

Fichier généré par `python -m etl.validation.p1` à chaque exécution de l'ETL. Ne pas éditer à la main :
l'analyse des écarts est dans `docs/validation-p1.md`. Critères et seuils : `docs/phases.md`.

**Tous les critères comptant pour la clôture sont satisfaits (écarts acceptés compris).**

| Critère | Résultat | Mesure |
|---|---|---|
| C1 TN | ✅ conforme | 7/7 séries LSH traitées |
| C1 TX | ✅ conforme | 5/5 séries LSH traitées |
| C3 TN composite 1959-2009 | ✅ conforme | pente de Sen +0.294 °C/déc. (IC 95 % +0.183 à +0.395), attendu [0.15 ; 0.35], 6 stations |
| C3 TX composite 1959-2009 | ☑ écart accepté le 23/10/2026 | pente de Sen +0.354 °C/déc. (IC 95 % +0.237 à +0.457), attendu [0.25 ; 0.35], 4 stations |
| C4bis Villenave TM annuelle 1979-2022 | ✅ conforme | dérive LSH − ERA5 : pente +0.035 °C/déc. (IC 95 % -0.002 à +0.070), Hamed-Rao p = 0.187 ; seuil |pente| ≤ 0.1 et p ≥ 0,05 ; décalage moyen +0.14 °C ; maille ERA5 44.750 N ; -0.500 E, altitude 24 m (demandé 44.790 ; -0.577) |
| C4bis (info) Villenave TN annuelle 1979-2022 | ℹ information | dérive LSH − ERA5 : pente +0.099 °C/déc. (IC 95 % +0.057 à +0.139), Hamed-Rao p = 0.002 ; seuil |pente| ≤ 0.1 et p ≥ 0,05 ; décalage moyen +0.05 °C |
| C4bis (info) Villenave TX annuelle 1979-2022 | ℹ information | dérive LSH − ERA5 : pente -0.045 °C/déc. (IC 95 % -0.088 à -0.010), Hamed-Rao p = 0.078 ; seuil |pente| ≤ 0.1 et p ≥ 0,05 ; décalage moyen +0.24 °C |
| C4bis (info) Villenave TM annuelle 1959-2019 | ℹ information | dérive LSH − ERA5 : pente +0.029 °C/déc. (IC 95 % +0.004 à +0.046), Hamed-Rao p = 0.062 ; seuil |pente| ≤ 0.1 et p ≥ 0,05 ; décalage moyen +0.09 °C |
| C4bis (info) Villenave TM hiver 1979-2022 | ℹ information | dérive LSH − ERA5 : pente +0.037 °C/déc. (IC 95 % -0.016 à +0.086), Hamed-Rao p = 0.212 ; seuil |pente| ≤ 0.1 et p ≥ 0,05 ; décalage moyen +0.07 °C |
| C4bis (info) Villenave TM printemps 1979-2022 | ℹ information | dérive LSH − ERA5 : pente +0.045 °C/déc. (IC 95 % +0.011 à +0.075), Hamed-Rao p = 0.010 ; seuil |pente| ≤ 0.1 et p ≥ 0,05 ; décalage moyen +0.19 °C |
| C4bis (info) Villenave TM été 1979-2022 | ℹ information | dérive LSH − ERA5 : pente +0.024 °C/déc. (IC 95 % -0.047 à +0.102), Hamed-Rao p = 0.608 ; seuil |pente| ≤ 0.1 et p ≥ 0,05 ; décalage moyen +0.25 °C |
| C4bis (info) Villenave TM automne 1979-2022 | ℹ information | dérive LSH − ERA5 : pente +0.024 °C/déc. (IC 95 % -0.018 à +0.069), Hamed-Rao p = 0.288 ; seuil |pente| ≤ 0.1 et p ≥ 0,05 ; décalage moyen +0.05 °C |
| C4 Villenave TM hiver 1959-2019 | ↩ retiré, pour information | régression linéaire +0.215, Sen +0.192, publié +0.13 °C/déc., écart +0.085 (tolérance ±0.05) — référence jugée invalide |
| C4 Villenave TM printemps 1959-2019 | ↩ retiré, pour information | régression linéaire +0.364, Sen +0.370, publié +0.25 °C/déc., écart +0.114 (tolérance ±0.05) — référence jugée invalide |
| C4 Villenave TM été 1959-2019 | ↩ retiré, pour information | régression linéaire +0.381, Sen +0.387, publié +0.23 °C/déc., écart +0.151 (tolérance ±0.05) — référence jugée invalide |
| C4 Villenave TM automne 1959-2019 | ↩ retiré, pour information | régression linéaire +0.260, Sen +0.253, publié +0.12 °C/déc., écart +0.140 (tolérance ±0.05) — référence jugée invalide |
| C5 TN | ✅ conforme | médiane +0.343 ; 0 station(s) à plus de 0.1 de la médiane |
| C5 TX | ✅ conforme | médiane +0.429 ; 0 station(s) à plus de 0.1 de la médiane |
| C5 TM | ✅ conforme | médiane +0.384 ; 0 station(s) à plus de 0.1 de la médiane |
| C6 | ✅ conforme | 20 rupture(s) détectée(s), 4 marquée(s) artefact possible, 0 encore significative(s) après retrait de la tendance |
| C7 | ✅ conforme | 0 série(s) dont la conclusion change avec la correction |
| C8 | ✅ conforme | métadonnées Météo-France complètes |

### C5 — Pentes 1962-2022 par station (°C/déc.)

| Variable | Station | Pente | Écart à la médiane | À expliquer |
|---|---|---|---|---|
| TN | Bordeaux-Mérignac | +0.361 | +0.018 | non |
| TN | Cap-Ferret | +0.357 | +0.014 | non |
| TN | Lacanau | +0.351 | +0.008 | non |
| TN | Bordeaux-Paulin | +0.343 | +0.000 | non |
| TN | Villenave-d'Ornon | +0.341 | -0.002 | non |
| TN | Cazaux | +0.339 | -0.004 | non |
| TN | Sauternes | +0.337 | -0.006 | non |
| TX | Bordeaux-Mérignac | +0.440 | +0.011 | non |
| TX | Bordeaux-Paulin | +0.433 | +0.004 | non |
| TX | Cap-Ferret | +0.429 | +0.000 | non |
| TX | Cazaux | +0.427 | -0.002 | non |
| TX | Villenave-d'Ornon | +0.425 | -0.003 | non |
| TM | Bordeaux-Mérignac | +0.394 | +0.010 | non |
| TM | Cap-Ferret | +0.391 | +0.007 | non |
| TM | Cazaux | +0.384 | +0.000 | non |
| TM | Bordeaux-Paulin | +0.381 | -0.004 | non |
| TM | Villenave-d'Ornon | +0.378 | -0.006 | non |

### C6 — Ruptures de Pettitt (p < 0,05) sur séries homogénéisées

| Indicateur | Nouveau régime | p | p après retrait de tendance | Artefact possible | Détail |
|---|---|---|---|---|---|
| tn-annuelle-gironde | 1988 | 0.0000 | 0.474 | non | écart des moyennes +1,15 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,47) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tx-annuelle-gironde | 1988 | 0.0000 | 0.512 | non | écart des moyennes +1,43 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,51) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tm-annuelle-gironde | 1988 | 0.0000 | 0.522 | non | écart des moyennes +1,29 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,52) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tn-annuelle-bordeaux-paulin | 1988 | 0.0000 | 0.512 | non | écart des moyennes +1,14 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,51) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tn-annuelle-lacanau | 1990 | 0.0000 | 0.733 | non | écart des moyennes +1,17 °C avant/après 1990 ; après retrait de la tendance, plus aucune rupture significative (p = 0,73) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tn-annuelle-cap-ferret | 1988 | 0.0000 | 0.327 | non | écart des moyennes +1,17 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,33) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tn-annuelle-bordeaux-merignac | 1988 | 0.0000 | 0.574 | **oui** | écart des moyennes +1,18 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,57) : la rupture traduit la tendance elle-même, pas un saut brusque ; coïncide avec une rupture d'homogénéité corrigée par Météo-France : non interprétable comme climatique |
| tn-annuelle-sauternes | 1988 | 0.0000 | 0.446 | non | écart des moyennes +1,13 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,45) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tn-annuelle-cazaux | 1988 | 0.0000 | 0.640 | non | écart des moyennes +1,11 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,64) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tn-annuelle-villenave-d-ornon | 1988 | 0.0000 | 0.569 | non | écart des moyennes +1,17 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,57) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tx-annuelle-bordeaux-paulin | 1989 | 0.0000 | 1.000 | non | écart des moyennes +1,49 °C avant/après 1989 ; après retrait de la tendance, plus aucune rupture significative (p = 1,00) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tx-annuelle-cap-ferret | 1988 | 0.0000 | 0.299 | non | écart des moyennes +1,42 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,30) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tx-annuelle-bordeaux-merignac | 1989 | 0.0000 | 0.629 | non | écart des moyennes +1,46 °C avant/après 1989 ; après retrait de la tendance, plus aucune rupture significative (p = 0,63) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tx-annuelle-cazaux | 1988 | 0.0000 | 0.548 | **oui** | écart des moyennes +1,43 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,55) : la rupture traduit la tendance elle-même, pas un saut brusque ; coïncide avec une rupture d'homogénéité corrigée par Météo-France : non interprétable comme climatique |
| tx-annuelle-villenave-d-ornon | 1989 | 0.0000 | 0.553 | non | écart des moyennes +1,42 °C avant/après 1989 ; après retrait de la tendance, plus aucune rupture significative (p = 0,55) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tm-annuelle-bordeaux-paulin | 1988 | 0.0000 | 0.943 | non | écart des moyennes +1,33 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,94) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tm-annuelle-cap-ferret | 1988 | 0.0000 | 0.342 | non | écart des moyennes +1,30 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,34) : la rupture traduit la tendance elle-même, pas un saut brusque |
| tm-annuelle-bordeaux-merignac | 1988 | 0.0000 | 0.553 | **oui** | écart des moyennes +1,32 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,55) : la rupture traduit la tendance elle-même, pas un saut brusque ; coïncide avec une rupture d'homogénéité corrigée par Météo-France : non interprétable comme climatique |
| tm-annuelle-cazaux | 1988 | 0.0000 | 0.601 | **oui** | écart des moyennes +1,27 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,60) : la rupture traduit la tendance elle-même, pas un saut brusque ; coïncide avec une rupture d'homogénéité corrigée par Météo-France : non interprétable comme climatique |
| tm-annuelle-villenave-d-ornon | 1988 | 0.0000 | 0.569 | non | écart des moyennes +1,29 °C avant/après 1988 ; après retrait de la tendance, plus aucune rupture significative (p = 0,57) : la rupture traduit la tendance elle-même, pas un saut brusque |

### C7 — Significativité : Mann-Kendall classique vs Hamed-Rao (période homogénéisée)

| Indicateur | Pente | p classique | p Hamed-Rao | Conclusion modifiée | Confiance |
|---|---|---|---|---|---|
| tn-annuelle-gironde | +0.294 | 0.00e+00 | 0.00e+00 | non | elevee |
| tx-annuelle-gironde | +0.357 | 0.00e+00 | 0.00e+00 | non | elevee |
| tm-annuelle-gironde | +0.322 | 0.00e+00 | 0.00e+00 | non | elevee |
| tn-annuelle-bordeaux-paulin | +0.288 | 0.00e+00 | 0.00e+00 | non | elevee |
| tn-annuelle-lacanau | +0.293 | 0.00e+00 | 0.00e+00 | non | elevee |
| tn-annuelle-cap-ferret | +0.294 | 0.00e+00 | 0.00e+00 | non | elevee |
| tn-annuelle-bordeaux-merignac | +0.303 | 0.00e+00 | 0.00e+00 | non | elevee |
| tn-annuelle-sauternes | +0.283 | 0.00e+00 | 0.00e+00 | non | elevee |
| tn-annuelle-cazaux | +0.288 | 0.00e+00 | 0.00e+00 | non | elevee |
| tn-annuelle-villenave-d-ornon | +0.292 | 0.00e+00 | 0.00e+00 | non | elevee |
| tx-annuelle-bordeaux-paulin | +0.433 | 0.00e+00 | 0.00e+00 | non | elevee |
| tx-annuelle-cap-ferret | +0.351 | 0.00e+00 | 0.00e+00 | non | elevee |
| tx-annuelle-bordeaux-merignac | +0.372 | 0.00e+00 | 0.00e+00 | non | elevee |
| tx-annuelle-cazaux | +0.361 | 0.00e+00 | 0.00e+00 | non | elevee |
| tx-annuelle-villenave-d-ornon | +0.352 | 0.00e+00 | 0.00e+00 | non | elevee |
| tm-annuelle-bordeaux-paulin | +0.381 | 0.00e+00 | 0.00e+00 | non | elevee |
| tm-annuelle-cap-ferret | +0.324 | 0.00e+00 | 0.00e+00 | non | elevee |
| tm-annuelle-bordeaux-merignac | +0.335 | 0.00e+00 | 0.00e+00 | non | elevee |
| tm-annuelle-cazaux | +0.318 | 0.00e+00 | 0.00e+00 | non | elevee |
| tm-annuelle-villenave-d-ornon | +0.320 | 0.00e+00 | 0.00e+00 | non | elevee |
