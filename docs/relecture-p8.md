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

Affirmations relues (passes 1 et 2, 02/11/2026) : gironde-tm#05526d0868, gironde-tx-tn#7f1aa217dd, gironde-chaleur#a6eaacd9b2, gironde-tres-chaud#1ab39e8d90, gironde-gel#ecb0536083, gironde-canicule#40a38a35a3, gironde-sst#0e976c4d16, gironde-sst-large#54f3bd0144, gironde-altitude#4ab994f62d, gironde-z500#f079cc5717, gironde-pluie#9b6e974054, gironde-pluies-intenses#dd0d71c597, gironde-etp#f691243f8d, gironde-bilan-hydrique#cb2ee3e233, gironde-mois-secs#96aa9e02b9, gironde-mois-secs-bordeaux#823bd2023e, gironde-huglin#d9b0163d5a, gironde-vendanges#e32012bf85, gironde-gelees-tardives#e4bd5f2c1c, gironde-gelees-autres#1d8e18a785, gironde-fwi#ec031e7d4e, gironde-fwi-1940#0e65421d35, gironde-atmosphere#3c4ecc9944, gironde-niveau-mer#faca9d9d41, gironde-arcachon#0b04f322b9, gironde-catnat#08e6a77791, france-tm#4d9b131490, france-tx-tn#bf766e0eb7, france-pluie#d0f6fa972e, france-brest#efc5e4c9e0, france-catnat-secheresse#7cf0808802, france-catnat#d05b22496b, monde-temperature#a15fbd7045, monde-sst#02fb93fdff, monde-tlt#c8ff88498f, monde-co2-ch4#fa55cac245, monde-n2o#8341ef83d8, monde-aerosols#78f22f3e24, monde-eei#85088d3c8f, monde-ohc#326bb52156, monde-niveau-mer#3f982ecc3e, monde-ph#81fbe6aade, monde-banquise-arctique#9eda345ef3, monde-banquise-antarctique#d493550980, monde-puits#027aac619a, monde-part-puits#0b16533a07, monde-ace#1e7359068c, monde-ouragans#4e755c34d2, monde-jet#22bac8d699, monde-enso#3754e594ab, monde-ozone#d38d4252a4, monde-ozone-creusement#14a8c8cbfa, cmp-gironde-monde#8a448c63da, cmp-france-monde#efc7f678b9, cmp-gironde-france#795657e38a, cmp-terres-oceans#89b84a8e57, cmp-sst-golfe-monde#ad7de87b9c, cmp-mer-gironde-monde#f9817963c1, acc-niveau-mer#fb4d14e44b, acc-niveau-mer-nerem#0e5f55bf8b, acc-temperature-monde#d55fdc074e, acc-temperature-contexte#114bb5b7da, acc-co2#136c877d0d, acc-ch4#35ee3adbd2, acc-tm-france#1e99c1c409, acc-tm-gironde#71bf33d41d, lacune-foudre-gironde#9dc9a0fa6f, lacune-foudre-monde#71885d7ab7, lacune-geopotentiel-monde#5761fbbbe1, lacune-localite-chaude-monde#87931078e0, lacune-localite-froide-monde#0f2a69944e, limite-europe#465d5bcf43, limite-glaciers#72fef4d3cd, limite-projections#31ccce92d2, limite-attribution#37ae4501a4, contexte-attribution#f33867f934, limite-pluie#5e6ceedf12, limite-non-detecte#0d67f2b759, limite-reanalyse#37c171f492


## Ajouts de la P7 (06-07/11/2026)

Les ajouts de la P7 ont été relus par un agent séparé, qui n'avait pas rédigé ces textes. Aucun chiffre n'était faux.

| | Signalement | Traitement |
|---|---|---|
| A1 | `limite-europe` devenue fausse : le Z500 Atlantique-Europe touche aussi l'Europe | Corrigé |
| A2 | M6 affichait « conforme » alors que les ajouts n'étaient pas relus : la marque de clôture suffisait | M6 exige une liste d'affirmations relues, avec une empreinte du texte rédigé (contre-relecture, N3-N4) |
| A3 | La validation P8 avait tourné avant la dernière génération de la synthèse | Relancée dans l'ordre |
| A4 | L2 et L5 affichés « information » sans trace | L2 mesuré et conforme ; L5 rattaché à la CI ; tracé |
| A5 | La ligne P7 du tableau donnait tout P7 en « signal non établi » | Corrigée (Z500 en « moyenne », D-V) |
| B1 | `exp-cape` affirmait une hausse dans une « absence » ; faille du contrôle M2 | Passée en « information » ; M2 refuse désormais une absence fondée sur un indicateur significatif, même plafonné |
| B2 | « Changer le secteur ne change pas le signe » généralisait un seul test | « Décaler le secteur de 10° vers l'est… un seul décalage a été testé » |
| B3 | `exp-blocages-hiver` : « établie » au lieu de « détectée » ; artefact suggéré sans test | Reformulé ; l'intervalle est cité |
| B4 | `monde-z500-europe` : réchauffement de la colonne non mesuré sur la zone | Reformulé |
| B5 | `limite-foudre` trop absolue | Supprimée ; la case foudre de la Gironde reste « sans donnée », avec une note de couverture corrigée |
| B6 | L'intro laissait croire que toute la P7 était plafonnée | Corrigée |
| B7 | `validation-p7.md` : mêmes généralisations | Corrigé |
| C1 | Limites de la CAPE : ERA5, dérive d'humidité, année de départ | Ajoutées |
| C2 | `limite-reanalyse` incomplète | Complétée |
| C3 | Case foudre affichée « publiée » par la seule CAPE | Remise en « sans donnée » |
| C4 | Changements non tracés | Tracés au journal P8 et dans `validation-p7.md` |
| C5 | Doublon dans les limites du Z500 ; décalage de ± 5° et taux de 33,9 % | Doublon retiré ; le reste demeure dans les limites des indicateurs (accepté) |

Contre-relecture du 07/11/2026 :

| | Signalement | Traitement |
|---|---|---|
| N1 | Deux phrases dépendaient de calculs de contrôle non automatisés (hiver : décalage du secteur ; CAPE : départ en 1981) | Retirées de la synthèse ; dans les limites de la CAPE, remplacées par un constat daté renvoyant à `validation-p7.md`, où restent les calculs de relecture |
| N2 | `validation-p7.md` : une cause non testée était donnée pour la faible pente du Z500 sur toute la série | Reformulé |
| N3 | M6 contrôlait les identifiants, pas les textes | Empreinte du gabarit rédigé. `limite-europe`, `limite-reanalyse` et `lacune-foudre-gironde` restent dans la liste des passes 1 et 2 avec leur empreinte du 02/11, devenue caduque ; elles sont relues dans la liste P7. Limite : l'empreinte ne couvre que le texte ; un changement de type, d'indicateurs, de paramètres, ou des intros et conclusions de section, n'est pas détecté par M6 |
| N4 | Les lacunes tirées de la couverture échappaient à M6 | Incluses (empreinte du texte généré) |
| — | « restitue mal » exagérait le contrôle H5 ; « +0,0 » ; style du Z500 | Corrigés |

Vérification finale du 07/11/2026 : `exp-blocages-hiver` et `exp-cape` conformes ; intro de la section exploratoire relue. Point mineur non corrigé : la première limite de la CAPE (« aucune série ouverte d'impacts de foudre n'existe ») est plus absolue que la note de couverture. **Relecture des ajouts P7 close** le 07/11/2026.

Affirmations relues (contre-relecture P7, 07/11/2026) : monde-z500-europe#76d2d64b2d, exp-blocages-ete#913b8ce646, exp-blocages-methode#f9f5489b20, limite-europe#e49a347af5, limite-reanalyse#c9837a9c32, lacune-foudre-gironde#f2649a15b7
Affirmations relues (vérification finale P7, 07/11/2026) : exp-blocages-hiver#6b7c01cb8e, exp-cape#cad95b7c94
