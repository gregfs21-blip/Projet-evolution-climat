# Validation P2a — résultats automatiques

Fichier généré par `python -m etl.validation.p2a` à chaque exécution de l'ETL. Ne pas éditer à la main. Critères et seuils : `docs/phases.md` (P2a).

**Au moins un critère comptant pour la clôture n'est pas satisfait.**

| Critère | Résultat | Mesure |
|---|---|---|
| E1 exhaustivité | ✅ conforme | 29/29 couples indice × poste traités ; exclus faute de série LSH (ni correction B ni dates de ruptures) : TX Lacanau, TX Sauternes |
| E2 complétude ETCCDI | ✅ conforme | règle appliquée à la construction (mois manquant au-delà de 3 jours absents, année manquante si un mois l'est) ; détail par poste ci-dessous |
| E3 brut exclu des tendances | ✅ conforme | aucune tendance de série corrigée ne contient d'année brute |
| E4 R3 littoral : journées chaudes (TX > 25 °C), littoral 1961-2010 | ❌ écart | pente de Sen +5.83 j/déc. (IC 95 % +3.46 à +8.70), attendu [4 ; 5] ; Cap-Ferret, Cazaux |
| E4 R3 intérieur : journées chaudes (TX > 25 °C), intérieur 1961-2010 | ❌ écart | non évaluable : années manquantes ou non corrigées pour ["Villenave-d'Ornon"] |
| E4 R4 : jours de gel (TN ≤ 0 °C), composite 1961-2010 | ✅ conforme | pente de Sen -1.43 j/déc. (IC 95 % -3.56 à +0.75), attendu [-2 ; -1] ; Bordeaux-Paulin, Cap-Ferret, Bordeaux-Mérignac, Sauternes, Cazaux |
| E5 cohérence du correctif | ✅ conforme | écart annuel maximal corrigé − LSH : 0.0000 °C (TN Cap-Ferret 2015), tolérance 0.05 °C |
| E6 même signe jours-tx25 | ✅ conforme | 5 hausse(s), 0 baisse(s), 0 nulle(s) |
| E6 même signe jours-gel | ✅ conforme | 0 hausse(s), 7 baisse(s), 0 nulle(s) |
| E7 concordance des méthodes | ❌ écart | 23/34 concordants ; 0 discordant(s) ; 11 non évaluable(s) |
| E8 robustesse au code qualité 9 | ❌ écart | 3 conclusion(s) modifiée(s) sur 29 |
| E9 indices rares | ✅ conforme | 10 indicateur(s) rare(s), aucun en confiance « élevée » |

### E2 — Années complètes (règle ETCCDI) et corrigées, par poste

| Variable | Poste | Années complètes | dont corrigées | Première | Dernière corrigée |
|---|---|---|---|---|---|
| TN | Bordeaux-Paulin | 73 | 70 | 1953 | 2022 |
| TN | Lacanau | 52 | 49 | 1967 | 2022 |
| TN | Cap-Ferret | 94 | 70 | 1921 | 2022 |
| TN | Bordeaux-Mérignac | 93 | 70 | 1927 | 2022 |
| TN | Sauternes | 129 | 70 | 1897 | 2022 |
| TN | Cazaux | 93 | 70 | 1922 | 2022 |
| TN | Villenave-d'Ornon | 99 | 69 | 1924 | 2022 |
| TX | Bordeaux-Paulin | 73 | 61 | 1953 | 2022 |
| TX | Cap-Ferret | 93 | 70 | 1921 | 2022 |
| TX | Bordeaux-Mérignac | 98 | 70 | 1921 | 2022 |
| TX | Cazaux | 91 | 70 | 1922 | 2022 |
| TX | Villenave-d'Ornon | 99 | 69 | 1924 | 2022 |

### E7 — Contrôle A (brut après dernière rupture) contre B (corrigé), même période

| Indicateur | Période | Pente A | IC A | Pente B | IC B | Concordance |
|---|---|---|---|---|---|---|
| jours-gel-bordeaux-merignac | 1988-2022 | -2.00 | -5.24 à +0.48 | -2.00 | -5.22 à +0.37 | oui |
| jours-gel-bordeaux-paulin | — | — | — | — | — | non évaluable (période trop courte) |
| jours-gel-cap-ferret | 1995-2022 | -2.12 | -5.00 à +0.62 | -1.75 | -4.44 à +0.62 | oui |
| jours-gel-cazaux | 2008-2022 | -10.00 | -26.00 à +5.00 | -10.00 | -26.00 à +6.00 | oui |
| jours-gel-gironde | — | — | — | — | — | non évaluable (période trop courte) |
| jours-gel-lacanau | — | — | — | — | — | non évaluable (période trop courte) |
| jours-gel-sauternes | 1991-2022 | -3.68 | -8.42 à +0.83 | -3.54 | -7.78 à +1.00 | oui |
| jours-gel-villenave-d-ornon | — | — | — | — | — | non évaluable (période trop courte) |
| jours-tx25-bordeaux-merignac | 2000-2022 | +8.67 | -0.95 à +20.00 | +10.00 | -1.67 à +21.67 | oui |
| jours-tx25-bordeaux-paulin | 1995-2022 | +4.68 | -2.22 à +11.25 | +6.92 | -0.00 à +13.16 | oui |
| jours-tx25-cap-ferret | 2005-2022 | +20.00 | +5.00 à +38.00 | +21.43 | +5.00 à +38.75 | oui |
| jours-tx25-cazaux | 1987-2022 | +5.00 | -0.00 à +10.53 | +5.45 | -0.00 à +10.77 | oui |
| jours-tx25-gironde | 2005-2022 | +13.33 | -2.50 à +27.58 | +13.70 | -1.67 à +28.21 | oui |
| jours-tx25-villenave-d-ornon | — | — | — | — | — | non évaluable (période trop courte) |
| jours-tx30-bordeaux-merignac | 2000-2022 | +6.67 | -1.33 à +15.00 | +6.67 | -1.18 à +14.00 | oui |
| jours-tx30-bordeaux-paulin | 1995-2022 | +5.56 | +1.11 à +10.00 | +4.76 | -1.05 à +10.00 | oui |
| jours-tx30-cap-ferret | 2005-2022 | +3.33 | -1.43 à +11.67 | +3.33 | -1.43 à +10.00 | oui |
| jours-tx30-cazaux | 1987-2022 | +1.67 | -0.59 à +4.21 | +1.54 | -0.67 à +4.12 | oui |
| jours-tx30-gironde | 2005-2022 | +10.00 | +0.71 à +15.15 | +10.00 | -0.00 à +15.00 | oui |
| jours-tx30-villenave-d-ornon | — | — | — | — | — | non évaluable (période trop courte) |
| jours-tx35-bordeaux-merignac | 2000-2022 | +2.22 | -0.00 à +4.29 | +2.50 | -0.00 à +4.00 | oui |
| jours-tx35-bordeaux-paulin | 1995-2022 | +2.50 | -0.00 à +5.00 | +2.31 | -0.00 à +4.29 | oui |
| jours-tx35-cap-ferret | 2005-2022 | +0.00 | -0.77 à +4.00 | -0.00 | -0.71 à +3.33 | oui |
| jours-tx35-cazaux | 1987-2022 | +1.00 | -0.00 à +2.00 | +1.00 | -0.00 à +1.90 | oui |
| jours-tx35-gironde | 2005-2022 | +2.50 | -0.33 à +4.76 | +2.08 | -0.56 à +4.44 | oui |
| jours-tx35-villenave-d-ornon | — | — | — | — | — | non évaluable (période trop courte) |
| nuits-tn20-bordeaux-merignac | 1988-2022 | +1.07 | -0.00 à +2.38 | +1.15 | -0.00 à +2.50 | oui |
| nuits-tn20-bordeaux-paulin | — | — | — | — | — | non évaluable (période trop courte) |
| nuits-tn20-cap-ferret | 1995-2022 | +2.16 | -1.67 à +5.91 | +1.90 | -1.54 à +5.56 | oui |
| nuits-tn20-cazaux | 2008-2022 | +4.00 | +2.00 à +6.00 | +4.00 | +1.67 à +6.25 | oui |
| nuits-tn20-gironde | — | — | — | — | — | non évaluable (période trop courte) |
| nuits-tn20-lacanau | — | — | — | — | — | non évaluable (période trop courte) |
| nuits-tn20-sauternes | 1991-2022 | +0.61 | -0.00 à +1.43 | +0.48 | -0.00 à +1.25 | oui |
| nuits-tn20-villenave-d-ornon | — | — | — | — | — | non évaluable (période trop courte) |

### E8 — Sans les valeurs de code qualité 9

| Indicateur | Pente | Significative | Pente sans code 9 | Significative | Conclusion modifiée |
|---|---|---|---|---|---|
| jours-gel-bordeaux-merignac | -2.42 | oui | -2.18 | oui | non |
| jours-gel-bordeaux-paulin | -1.61 | oui | -1.50 | oui | non |
| jours-gel-cap-ferret | -1.25 | oui | -1.25 | oui | non |
| jours-gel-cazaux | -2.41 | oui | -2.41 | oui | non |
| jours-gel-lacanau | -3.16 | non | -3.16 | non | non |
| jours-gel-sauternes | -2.37 | oui | -2.37 | oui | non |
| jours-gel-villenave-d-ornon | -2.22 | oui | -1.92 | non | **oui** |
| jours-tx25-bordeaux-merignac | +6.73 | oui | +7.00 | oui | non |
| jours-tx25-bordeaux-paulin | +6.92 | oui | +6.92 | non | **oui** |
| jours-tx25-cap-ferret | +6.97 | oui | +6.97 | oui | non |
| jours-tx25-cazaux | +6.00 | oui | +6.00 | oui | non |
| jours-tx25-villenave-d-ornon | +5.71 | oui | +6.07 | oui | non |
| jours-tx30-bordeaux-merignac | +3.17 | oui | +3.30 | oui | non |
| jours-tx30-bordeaux-paulin | +4.00 | oui | +6.32 | non | **oui** |
| jours-tx30-cap-ferret | +1.52 | oui | +1.52 | oui | non |
| jours-tx30-cazaux | +2.22 | oui | +2.22 | oui | non |
| jours-tx30-villenave-d-ornon | +2.95 | oui | +3.33 | oui | non |
| jours-tx35-bordeaux-merignac | +0.48 | oui | +0.50 | oui | non |
| jours-tx35-bordeaux-paulin | +0.90 | oui | +2.50 | oui | non |
| jours-tx35-cap-ferret | -0.00 | oui | -0.00 | oui | non |
| jours-tx35-cazaux | +0.47 | oui | +0.47 | oui | non |
| jours-tx35-villenave-d-ornon | -0.00 | non | -0.00 | non | non |
| nuits-tn20-bordeaux-merignac | +0.78 | oui | +0.80 | oui | non |
| nuits-tn20-bordeaux-paulin | +1.25 | oui | +1.54 | oui | non |
| nuits-tn20-cap-ferret | +1.61 | oui | +1.61 | oui | non |
| nuits-tn20-cazaux | +0.51 | oui | +0.51 | oui | non |
| nuits-tn20-lacanau | +0.83 | oui | +0.83 | oui | non |
| nuits-tn20-sauternes | +0.26 | oui | +0.26 | oui | non |
| nuits-tn20-villenave-d-ornon | +0.61 | oui | +0.71 | oui | non |
