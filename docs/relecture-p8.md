# Relecture indépendante de la synthèse P8 (critère M6)

Le 02/11/2026, un agent séparé qui n'avait pas vu la rédaction a relu la synthèse. Il a confronté chaque affirmation
de `data/processed/synthese.json` aux indicateurs publiés et recalculé les comparaisons et les accélérations. Il n'a
modifié aucun fichier.

La relecture s'est faite en deux passes :
1. Un rapport complet.
2. Une contre-relecture des corrections.

Ce fichier trace chaque signalement et ce qui en a été fait.

## Première passe

Résultats de la première passe :
- **57 affirmations qualifiées relues.**
- **Chiffres** : tous exacts sauf un, car ils sont lus dans les JSON.
- **Recalculs** : les 8 comparaisons et les 8 accélérations recalculées coïncident.
- **Défauts** : presque tous dans le texte écrit à la main hors des champs à trous.

### A. Erreurs factuelles (toutes corrigées)

| | Signalement | Traitement |
|---|---|---|
| A1 | `gironde-etp` : période de Cazaux fausse (1962-2022 au lieu de 1953-2022) | Corrigé : chaque station porte sa période |
| A2 | `gironde-gelees-autres` : « plus abrités », contredit par les métadonnées (Sauternes exposé aux inversions, Paulin urbain) | Supprimé |
| A3 | `gironde-pluies-intenses` : R10 et R20 cités sans être rattachés aux indicateurs, donc hors contrôles S1 et M2 | `r10mm-gironde` et `r20mm-gironde` ajoutés |
| A4 | `france-tm` : « pondérée par département », alors que les départements pèsent autant | « à poids égal » |

### B. Sur-interprétations (toutes corrigées)

| | Signalement | Traitement |
|---|---|---|
| B1 | `cmp-terres-oceans` : « ne disent rien de propre à la région ». Avec les chiffres du GIEC, l'effet terres/océan explique un rapport d'environ 1,5, alors que l'étude trouve environ 1,9 | Reformulé : une partie seulement de l'écart est attendue, et faute d'une moyenne des seules terres l'étude ne peut pas trancher. **Règle S3 corrigée dans `phases.md` et tracée comme correction après calcul** |
| B2 | `monde-enso` : l'absence de dérive vient de la construction de l'ONI ; « module les températures » est une causalité | Reformulé : l'indice ne permet pas de dire si El Niño évolue |
| B3 | `monde-eei` : le niveau du produit CERES EBAF est calé sur Argo | Seule la variation est attribuée au satellite, et le calage du niveau est dit |
| B4 | Conclusion Gironde : le +2,2 °C semblait valoir partout ; « ses effets » est une attribution ; confusion entre ETP et évaporation ; « pas encore » | Réécrite |
| B5 | `gironde-mois-secs-bordeaux` : comparaison implicite sans test ; Cazaux n'est pas littoral | Reformulé |
| B6 | `monde-part-puits` : « les puits suivent les émissions » affirme une stabilité | Supprimé |
| B7 | `monde-ph` : « la plus longue série ouverte », non vérifiable et probablement faux (BATS) ; causalité | Retiré |
| B8 | `monde-ace` : la lecture de la rupture contredisait la note de l'indicateur ; « moyens d'observation » sans source | Réécrit ; ajout de la limite sur la variabilité multidécennale de l'Atlantique |
| B9 | `gironde-z500` : explication non testée | « cohérent avec le réchauffement mesuré à 850 et 500 hPa » |
| B10 | `acc-tm-gironde` : « période plate » et « années 1970 » non établis | « concentré sur la seconde partie de la période (rupture vers 1988, Pettitt) » |
| B11 | `acc-temperature-contexte` : « d'autres travaux » sans source ; lien vers un communiqué | Phrase retirée ; la source cite l'article (revue, volume), lien vers sa notice NSF PAR. **DOI non vérifié, donc non donné** |
| B12 | Conclusion Monde : « profondeurs », « pas encore » | « jusqu'à 2000 m », « pas significative au seuil de 5 % » |
| B13 | Points mineurs : liste des variables ERA5 et seuil 1950/1979 ; « encore » ; ozone typé absence alors qu'il contient un signal ; méthane ; aérosols ; période de `france-tx-tn` | Corrigés ; ozone scindé (`monde-ozone-creusement` en information) |

### C. Omissions (corrigées, sauf une exception tracée)

| | Signalement | Traitement |
|---|---|---|
| C1 | Accélération du niveau marin 1993-2017 : intervalle large, valeur sous les deux références | Intervalle et position par rapport aux références ajoutés |
| C2 | Pas de correction isostatique, hausse sous-estimée | Ajouté |
| C3 | ETP de Hargreaves fonction des seules températures ; SPEI et mois secs en dépendent ; rupture de Cap-Ferret en 1975 marquée artefact possible | ETP : ajouté. **Exception tracée** : la dépendance du SPEI et la rupture de 1975 ne figurent pas dans le texte des mois secs. Elles sont dans les limites des indicateurs, et la synthèse les qualifie d'un intervalle qui touche zéro |
| C4 | Banquise antarctique : rupture de 2016 omise | Citée |
| C5 | Chaleur de l'océan 0-700 m : rupture de 1991 encore significative après retrait de la tendance ; mesures rares avant Argo | Ajouté |
| C6 | Séries longues ERA5 : vent fort et vitesse du jet significatifs depuis 1940 | Ajouté, avec la réserve sur l'avant-1979 |
| C7 | Comparaisons entre produits différents ; changement de source de la température de mer ERA5 en 1979-1982 | Ajouté (intro des comparaisons, `gironde-sst`) |
| C8 | Gelées tardives à Cazaux : saut en 1983 plutôt qu'une pente | Ajouté |
| C9 | Jours de gel : non significatif sur 1961-2010 ; validation externe non établie | Ajouté |
| C10 | pH : la tendance s'arrête en 2021 (2022 manque) | Ajouté |
| C11 | Composite de la Gironde à poids égal | Ajouté |
| C12 | Brest : niveau relatif au sol | Ajouté |

## Contre-relecture

Les points A, B et C sont confirmés corrigés, à l'exception de B11 et C3, partiels et tracés ci-dessus. Aucune autre
erreur n'a été trouvée dans les ruptures citées (1983, 1988, 1991, 1995, 2016), les `alt_trends`, les intervalles ou
les périodes. Deux problèmes introduits par les corrections ont été signalés :

| | Signalement | Traitement |
|---|---|---|
| N1 | `monde-niveau-mer` : « rebond postglaciaire du fond des océans ». C'est faux : en moyenne, le fond s'affaisse | Corrigé : « ajustement isostatique glaciaire (l'affaissement moyen du fond des océans) » |
| N2 | `gironde-mois-secs` : « tout juste », alors que p = 0,005 à Cazaux ; la borne à zéro vient des comptages entiers | Corrigé |
| — | Conclusion Monde : « les mesures vont toutes dans le même sens » | Gardé ; le relecteur l'a jugé acceptable, car la phrase énumère ensuite les mesures concernées |

Verdict de la contre-relecture : M6 peut être clos une fois N1 corrigé et les exceptions B11 et C3 tracées. C'est
fait.

**Relecture close** le 02/11/2026.

Affirmations relues (passes 1 et 2, 02/11/2026) : gironde-tm, gironde-tx-tn, gironde-chaleur, gironde-tres-chaud, gironde-gel, gironde-canicule, gironde-sst, gironde-sst-large, gironde-altitude, gironde-z500, gironde-pluie, gironde-pluies-intenses, gironde-etp, gironde-bilan-hydrique, gironde-mois-secs, gironde-mois-secs-bordeaux, gironde-huglin, gironde-vendanges, gironde-gelees-tardives, gironde-gelees-autres, gironde-fwi, gironde-fwi-1940, gironde-atmosphere, gironde-niveau-mer, gironde-arcachon, gironde-catnat, france-tm, france-tx-tn, france-pluie, france-brest, france-catnat-secheresse, france-catnat, monde-temperature, monde-sst, monde-tlt, monde-co2-ch4, monde-n2o, monde-aerosols, monde-eei, monde-ohc, monde-niveau-mer, monde-ph, monde-banquise-arctique, monde-banquise-antarctique, monde-puits, monde-part-puits, monde-ace, monde-ouragans, monde-jet, monde-enso, monde-ozone, monde-ozone-creusement, cmp-gironde-monde, cmp-france-monde, cmp-gironde-france, cmp-terres-oceans, cmp-sst-golfe-monde, cmp-mer-gironde-monde, acc-niveau-mer, acc-niveau-mer-nerem, acc-temperature-monde, acc-temperature-contexte, acc-co2, acc-ch4, acc-tm-france, acc-tm-gironde, limite-europe, limite-glaciers, limite-projections, limite-attribution, contexte-attribution, limite-pluie, limite-non-detecte, limite-reanalyse

