# Validation P2b — résultats automatiques

Fichier généré par `python -m etl.validation.p2b` à chaque exécution de l'ETL. Ne pas éditer à la main. Critères et seuils : `docs/phases.md` (P2b).

**Au moins un critère comptant pour la clôture n'est pas satisfait.**

| Critère | Résultat | Mesure |
|---|---|---|
| F1 exhaustivité | ✅ conforme | 9 postes de pluie retenus, 6 au composite 1961-2017 (hors composite : Hourtin, Lacanau, St-Symphorien) ; 3 postes ETP/SPEI ; 52 indicateurs attendus, tous publiés |
| F2 complétude | ℹ️ information | Appliquée par le code : quotidien ETCCDI, correction B′ sur mois complets seulement, années de 12 mois, cumuls SPEI interrompus par tout mois manquant. |
| F3 brut ≠ homogénéisé | ✅ conforme | 52 indicateurs validés par le contrat : aucune tendance ni normale sur une année brute (règle C2). |
| F4 validation externe (R6, ETP) | ❌ non conforme | Attendu [+16 ; +30] mm/déc. sur 1962-2019 ; mesuré : Bordeaux-Paulin : 16.4036 mm/déc.; Cap-Ferret : 14.4787 mm/déc.; Cazaux : 16.6592 mm/déc.. Pluies intenses : pas de référence (R7 abandonnée), confiance au plus « moyenne ». |
| F5 cohérence du correctif | ✅ conforme | 6924 mois corrigés ; écart maximal au cumul LSH : 0.000 mm (tolérance 0.5 mm). |
| F6 cohérence inter-stations (r10mm) | ❌ non conforme | Belin-Beliet −, Bordeaux-Paulin +, Cap-Ferret −, Captieux −, Cazaux −, Hourtin +, Lacanau +, Sauternes −, St-Symphorien − |
| F6 cohérence inter-stations (etp) | ✅ conforme | Bordeaux-Paulin +, Cap-Ferret +, Cazaux + |
| F7 robustesse méthode (A et B′) | ✅ conforme | 40 concordants sur 40 évaluables ; non concordants : aucun ; non évaluables : aucun. |
| F8 période ancienne (P2b) | ✅ conforme | ruptures établies : aucune (tendance alors limitée à la période postérieure). |
| F8 diagnostic sur P2a (extrêmes de température) | ℹ️ information | ruptures établies : aucune. Diagnostic seulement : ne modifie pas P2a. |
| F9 indices rares | ℹ️ information | 1 indice(s) rare(s) : r20mm-cap-ferret. |
| F10 contrôle du SPEI | ✅ conforme | Bordeaux-Paulin SPEI-3 : moyenne +0.003, écart-type 0.985 ; Bordeaux-Paulin SPEI-12 : moyenne +0.005, écart-type 0.986 ; Cap-Ferret SPEI-3 : moyenne +0.002, écart-type 0.988 ; Cap-Ferret SPEI-12 : moyenne +0.001, écart-type 0.987 ; Cazaux SPEI-3 : moyenne +0.003, écart-type 0.987 ; Cazaux SPEI-12 : moyenne +0.002, écart-type 0.987 |
| F11 technique | ℹ️ information | Tests, CI et contrat vérifiés par les workflows. |

### F7 — contrôle A

| Indicateur | Période A | Pente A | Pente B′ | Concordant |
|---|---|---|---|---|
| r10mm-belin-beliet | 1985-2017 | -0.57 | -0.62 | oui |
| r10mm-bordeaux-paulin | 1953-2017 | +0.21 | +0.19 | oui |
| r10mm-cap-ferret | 1996-2017 | +0.00 | +0.00 | oui |
| r10mm-captieux | 1992-2017 | -3.64 | -3.64 | oui |
| r10mm-cazaux | 1969-2017 | +0.00 | +0.00 | oui |
| r10mm-gironde | 2006-2017 | +0.21 | +0.23 | oui |
| r10mm-hourtin | 1985-2017 | +0.83 | +0.83 | oui |
| r10mm-lacanau | 2003-2015 | +10.00 | +10.00 | oui |
| r10mm-sauternes | 2006-2017 | -5.50 | -5.50 | oui |
| r10mm-st-symphorien | 1985-2017 | -1.00 | -1.00 | oui |
| r20mm-belin-beliet | 1985-2017 | -0.80 | -0.83 | oui |
| r20mm-bordeaux-paulin | 1953-2017 | +0.00 | +0.00 | oui |
| r20mm-cap-ferret | 1996-2017 | +0.00 | +0.00 | oui |
| r20mm-captieux | 1992-2017 | -1.67 | -1.67 | oui |
| r20mm-cazaux | 1969-2017 | -0.32 | -0.32 | oui |
| r20mm-gironde | 2006-2017 | +0.49 | +0.49 | oui |
| r20mm-hourtin | 1985-2017 | +0.00 | +0.00 | oui |
| r20mm-lacanau | 2003-2015 | +0.00 | +0.00 | oui |
| r20mm-sauternes | 2006-2017 | +0.00 | +0.00 | oui |
| r20mm-st-symphorien | 1985-2017 | -0.38 | -0.38 | oui |
| rx1day-belin-beliet | 1985-2017 | -2.26 | -2.26 | oui |
| rx1day-bordeaux-paulin | 1953-2017 | +0.48 | +0.49 | oui |
| rx1day-cap-ferret | 1996-2017 | -2.53 | -2.53 | oui |
| rx1day-captieux | 1992-2017 | -3.33 | -3.33 | oui |
| rx1day-cazaux | 1969-2017 | -1.31 | -1.31 | oui |
| rx1day-gironde | 2006-2017 | +2.82 | +2.82 | oui |
| rx1day-hourtin | 1985-2017 | -0.43 | -0.43 | oui |
| rx1day-lacanau | 2003-2015 | -4.64 | -4.64 | oui |
| rx1day-sauternes | 2006-2017 | +11.44 | +11.44 | oui |
| rx1day-st-symphorien | 1985-2017 | -2.00 | -2.00 | oui |
| rx5day-belin-beliet | 1985-2017 | -0.60 | -0.60 | oui |
| rx5day-bordeaux-paulin | 1953-2017 | +0.12 | +0.12 | oui |
| rx5day-cap-ferret | 1996-2017 | +5.59 | +5.59 | oui |
| rx5day-captieux | 1992-2017 | -5.83 | -5.83 | oui |
| rx5day-cazaux | 1969-2017 | -0.21 | -0.21 | oui |
| rx5day-gironde | 2006-2017 | +14.26 | +14.26 | oui |
| rx5day-hourtin | 1985-2017 | +1.23 | +1.23 | oui |
| rx5day-lacanau | 2003-2015 | +11.02 | +11.02 | oui |
| rx5day-sauternes | 2006-2017 | +0.00 | +0.00 | oui |
| rx5day-st-symphorien | 1985-2017 | -2.38 | -2.38 | oui |

### F8 — période ancienne, pluies

| Poste | Indice | Résultat | Détail |
|---|---|---|---|
| Belin-Beliet | r10mm | non évaluable | 9 années comparables avant 1985 |
| Belin-Beliet | r20mm | non évaluable | 9 années comparables avant 1985 |
| Belin-Beliet | rx1day | non évaluable | 9 années comparables avant 1985 |
| Belin-Beliet | rx5day | non évaluable | 9 années comparables avant 1985 |
| Bordeaux-Paulin | r10mm | sans objet | aucune rupture LSH corrigée : la correction ne fait que caler les cumuls |
| Bordeaux-Paulin | r20mm | sans objet | aucune rupture LSH corrigée : la correction ne fait que caler les cumuls |
| Bordeaux-Paulin | rx1day | sans objet | aucune rupture LSH corrigée : la correction ne fait que caler les cumuls |
| Bordeaux-Paulin | rx5day | sans objet | aucune rupture LSH corrigée : la correction ne fait que caler les cumuls |
| Captieux | r10mm | non évaluable | 9 années comparables avant 1992 |
| Captieux | r20mm | non évaluable | 9 années comparables avant 1992 |
| Captieux | rx1day | non évaluable | 9 années comparables avant 1992 |
| Captieux | rx5day | non évaluable | 9 années comparables avant 1992 |
| Hourtin | r10mm | non évaluable | 0 années comparables avant 1964 |
| Hourtin | r20mm | non évaluable | 0 années comparables avant 1964 |
| Hourtin | rx1day | non évaluable | 0 années comparables avant 1964 |
| Hourtin | rx5day | non évaluable | 0 années comparables avant 1964 |
| Lacanau | r10mm | sans objet | aucune rupture LSH corrigée : la correction ne fait que caler les cumuls |
| Lacanau | r20mm | sans objet | aucune rupture LSH corrigée : la correction ne fait que caler les cumuls |
| Lacanau | rx1day | sans objet | aucune rupture LSH corrigée : la correction ne fait que caler les cumuls |
| Lacanau | rx5day | sans objet | aucune rupture LSH corrigée : la correction ne fait que caler les cumuls |
| Cap-Ferret | r10mm | non évaluable | 9 années comparables avant 1996 |
| Cap-Ferret | r20mm | non évaluable | 9 années comparables avant 1996 |
| Cap-Ferret | rx1day | non évaluable | 9 années comparables avant 1996 |
| Cap-Ferret | rx5day | non évaluable | 9 années comparables avant 1996 |
| St-Symphorien | r10mm | non évaluable | 9 années comparables avant 1985 |
| St-Symphorien | r20mm | non évaluable | 9 années comparables avant 1985 |
| St-Symphorien | rx1day | non évaluable | 9 années comparables avant 1985 |
| St-Symphorien | rx5day | non évaluable | 9 années comparables avant 1985 |
| Sauternes | r10mm | non évaluable | 9 années comparables avant 2006 |
| Sauternes | r20mm | non évaluable | 9 années comparables avant 2006 |
| Sauternes | rx1day | non évaluable | 9 années comparables avant 2006 |
| Sauternes | rx5day | non évaluable | 9 années comparables avant 2006 |
| Cazaux | r10mm | non évaluable | 5 années comparables avant 1969 |
| Cazaux | r20mm | non évaluable | 5 années comparables avant 1969 |
| Cazaux | rx1day | non évaluable | 5 années comparables avant 1969 |
| Cazaux | rx5day | non évaluable | 5 années comparables avant 1969 |

### F8 — diagnostic P2a

| Poste | Indice | Résultat | Détail |
|---|---|---|---|
| Bordeaux-Paulin | jours-tx25 | conforme | 1962-1994 : aucune rupture (p = 0.75) |
| Cap-Ferret | jours-tx25 | conforme | 1962-2001 : aucune rupture (p = 0.20) |
| Bordeaux-Mérignac | jours-tx25 | conforme | 1962-1999 : aucune rupture (p = 0.06) |
| Cazaux | jours-tx25 | conforme | 1962-1986 : rupture en 1973 qui disparaît après retrait de la tendance |
| Villenave-d'Ornon | jours-tx25 | conforme | 1962-1992 : aucune rupture (p = 1.00) |
| Bordeaux-Paulin | jours-tx30 | conforme | 1962-1994 : aucune rupture (p = 0.24) |
| Cap-Ferret | jours-tx30 | conforme | 1962-2001 : aucune rupture (p = 0.07) |
| Bordeaux-Mérignac | jours-tx30 | conforme | 1962-1999 : aucune rupture (p = 0.67) |
| Cazaux | jours-tx30 | conforme | 1962-1986 : aucune rupture (p = 1.00) |
| Villenave-d'Ornon | jours-tx30 | conforme | 1962-1992 : aucune rupture (p = 0.21) |
| Bordeaux-Paulin | jours-tx35 | conforme | 1962-1994 : aucune rupture (p = 0.60) |
| Cap-Ferret | jours-tx35 | conforme | 1962-2001 : aucune rupture (p = 0.35) |
| Bordeaux-Mérignac | jours-tx35 | conforme | 1962-1999 : aucune rupture (p = 0.11) |
| Cazaux | jours-tx35 | conforme | 1962-1986 : aucune rupture (p = 0.25) |
| Villenave-d'Ornon | jours-tx35 | conforme | 1962-1992 : aucune rupture (p = 0.09) |
| Bordeaux-Paulin | nuits-tn20 | conforme | 1967-1997 : aucune rupture (p = 0.26) |
| Lacanau | nuits-tn20 | conforme | 1967-1997 : rupture en 1987 qui disparaît après retrait de la tendance |
| Cap-Ferret | nuits-tn20 | conforme | 1967-1994 : aucune rupture (p = 0.07) |
| Bordeaux-Mérignac | nuits-tn20 | conforme | 1967-1987 : aucune rupture (p = 0.51) |
| Sauternes | nuits-tn20 | conforme | 1967-1990 : aucune rupture (p = 0.17) |
| Cazaux | nuits-tn20 | conforme | 1967-1997 : aucune rupture (p = 0.06) |
| Villenave-d'Ornon | nuits-tn20 | conforme | 1967-1997 : aucune rupture (p = 1.00) |
| Bordeaux-Paulin | jours-gel | conforme | 1967-1997 : aucune rupture (p = 0.14) |
| Lacanau | jours-gel | conforme | 1967-1997 : aucune rupture (p = 0.41) |
| Cap-Ferret | jours-gel | conforme | 1967-1994 : aucune rupture (p = 1.00) |
| Bordeaux-Mérignac | jours-gel | conforme | 1967-1987 : aucune rupture (p = 0.43) |
| Sauternes | jours-gel | conforme | 1967-1990 : aucune rupture (p = 0.52) |
| Cazaux | jours-gel | conforme | 1967-1997 : aucune rupture (p = 0.50) |
| Villenave-d'Ornon | jours-gel | conforme | 1967-1997 : aucune rupture (p = 0.24) |
