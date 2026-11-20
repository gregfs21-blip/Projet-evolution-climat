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

## Reformulation de `limite-attribution` à la publication de P10.1 (17-18/11/2026, décision D-AH)

La publication de l'onglet Démonstration (régression multiple, P10.1) rendait fausse l'affirmation « L'étude ne fait
aucune attribution ». Sa reformulation, ainsi que les textes de P10.1 (constat, méthode, limites, page, analyse
`docs/validation-p10.md`), ont été relus par un agent séparé, qui ne les avait pas rédigés, en recalculant les chiffres
à partir des entrées brutes. 21 signalements en première passe, tous traités :

| | Signalement | Traitement |
|---|---|---|
| 1 | « Seule la température mondiale » ambigu (SST et troposphère publiées mais non attribuées ; c'est un réchauffement moyen par rapport à 1850-1900 qui est attribué) | Formulation du relecteur reprise mot pour mot |
| 2 | Aucun garde-fou : P10.2, P10.3 et P10.5 rendront `limite-attribution` et `limite-projections` inexactes | Contrôle « D-AH cohérence de la synthèse » dans `etl/validation/p10.py` : échoue dès qu'une autre analyse est publiée |
| 3-5 | Double arrondi (JSON à 3-4 décimales puis affichage) : plusieurs chiffres décalés d'une unité ; fichiers de validation non régénérés ; tableau de `validation-p10.md` faux | Valeurs en pleine précision dans le JSON, pentes de Sen recalculées sans arrondi, arrondi unique à l'affichage ; fichiers régénérés ; tableau corrigé |
| 6-10 | `validation-p10.md` : « ± 0,09 » sans sens ; 0,56 au lieu de 0,55 ; Newey-West présenté comme « sans correction » ; « rejet par les observations » trop fort ; non-significativité confondue avec valeur faible | Corrigés |
| 11-14 | Constat : intervalle statistique comparé à la fourchette IGCC sans préciser qu'il exclut l'incertitude des forçages ; raison de confiance opaque ; limite d'indépendance cachée dans un bloc replié ; intervalles de Sen non corrigés de l'autocorrélation | Corrigés (constat, raison de confiance détaillée, texte visible de la page, note de méthode) |
| 15-21 | Formulations trop fortes ou imprécises ; chiffres de référence écrits à la main sur la page ; « gaz à effet de serre moins aérosols » ; licence HadISST incohérente ; k non défini | Corrigés ; références lues dans le JSON (`tcr_reference`, références d'attribution) |

Contre-relecture : les 21 points sont confirmés corrigés. Trois remarques de style traitées (bruit flottant sur une
pente, fourchette du coefficient solaire, verbe « explique » sur la page) ; une remarque facultative non appliquée
(« la température de la mer prise seule »), qui imposerait une nouvelle relecture sans changer le sens.

Affirmations relues (P10, 18/11/2026) : limite-attribution#254699f490

## Intégration de la P9 dans la synthèse (18/11/2026, demande de Grég)

La validation P8 était non conforme depuis la P9 : M3 (case `amoc / monde` sans affirmation) et M6
(`lacune-gulf-stream-monde` jamais relue). Ajouts : groupe « Gulf Stream et gyre subpolaire (P9) » de la section Monde
(`monde-gulf-stream`, `monde-gyre-subpolaire`, `contexte-empreinte-amoc`, `contexte-amoc-giec`), affirmation `exp-amoc`
de la section exploratoire (titre « Exploratoire (P7, P9) », intro complétée), conclusion Monde complétée. Relus par un
agent séparé, qui ne les avait pas rédigés.

| | Signalement | Traitement |
|---|---|---|
| 1 | Contexte GIEC : le constat sur le XXe siècle n'est pas dans le résumé pour décideurs cité | Source corrigée (chapitres 2 et 9 ; SPM C.3.4) ; « pour tous les scénarios d'émissions » ajouté |
| 2-3 | Empreinte de Caesar et al. mal paraphrasée (refroidissement de surface au sud du Groenland, réchauffement du Gulf Stream), sans dire qu'elle porte sur la surface et non sur 0-700 m ; juxtaposée aux deux pentes, elle invitait à une comparaison hors S3 | Formulation du relecteur reprise |
| 4 | « Sans donnée ouverte » faux pour le câble (série ouverte mais inaccessible) | Libellé du statut : « sans donnée ouverte exploitable » (définition élargie dans `couverture.yaml`, D-AA inchangée) ; note de la case reformulée, puis corrigée en contre-relecture : le blocage constaté est propre à GitHub Actions (le serveur de l'AOML répond à d'autres clients) |
| 5 | `exp-amoc` : « variabilité d'une année à l'autre » trop étroit | « variabilité naturelle, notamment d'une décennie à l'autre » |
| 6 | Conclusion Monde non mise à jour (gyre, AMOC) | Complétée ; « toutes » retiré en contre-relecture (contradiction avec l'exception) |
| 7-8 | Titre du groupe ; p de la salinité du gyre absent | Corrigés |

Les lacunes de la foudre changent avec le libellé du statut : relues, conformes.

Affirmations relues (P9, 18/11/2026) : monde-gulf-stream#4cc9c1a2e8, monde-gyre-subpolaire#f33a7c4e60, contexte-empreinte-amoc#908be91cea, contexte-amoc-giec#fb1e0d13bd, exp-amoc#385eaf8402, lacune-gulf-stream-monde#ea82572732, lacune-foudre-gironde#b00cb7101a, lacune-foudre-monde#b1ce13a9d1

## Lacunes « localité la plus chaude / froide » mises à jour par la P11 (18/11/2026)

La note de couverture des deux cases change (source METAR, page Instantané) ; les lacunes générées ont été relues par un
agent séparé : exactes, sans sur-interprétation. La même relecture a porté sur le code et la page de la P11
(`docs/validation-p11.md`).

Affirmations relues (P11, 18/11/2026) : lacune-localite-chaude-monde#6fba07708d, lacune-localite-froide-monde#aa2c4baefa

## P10.2 — valeurs extrêmes en Gironde (19/11/2026, garde-fou D-AH)

Publier P10.2 rendait `limite-attribution` incomplète. Relecture par un agent séparé, qui n'avait rien rédigé, de
l'affirmation reformulée, du constat et des textes générés (`data/processed/demonstration.json`), de la page
(`web/app/demonstration/page.tsx`, `ExtremesView.tsx`, `ReturnLevelChart.tsx`), de `docs/validation-p10.md` et des
points du code qui pèsent sur les chiffres. Le relecteur a réajusté la loi et refait le bootstrap (graine 1002) :
chiffres reproduits.

| | Signalement | Traitement |
|---|---|---|
| 1 | Page : « si la chaleur ne dépendait pas du réchauffement mondial, α serait nul » confond évolution commune et dépendance ; le renvoi à P10.1 invitait à conclure à une chaleur bordelaise d'origine humaine | Formulation du relecteur reprise : évolution commune, facteurs concomitants (urbanisation, aérosols, circulation), la régression mondiale ne se transpose pas |
| 2 | Constat : « au moins 538 ans », « au moins 27 » présentent des percentiles à 2,5 % comme des minimums ; indicatif pour un contrefactuel | Conditionnel ; nombre de tirages au-delà de la borne publié (779 sur 1 000 au calcul relu, 780 au calcul officiel) ; « bornes basses des intervalles à 95 % » |
| 3 | `limite-attribution` : « ce réchauffement » ambigu ; effets régionaux omis ; indice imprécis | Proposition du relecteur reprise |
| 4 | « Valeur la plus probable (position μ) » faux : μ n'est pas le mode | « Position μ de la loi (dépassée près de 2 années sur 3) » |
| 5 | « La variante sans 2025 mesure ce biais » sans rien publier | Période de retour du record aujourd'hui publiée pour chaque variante ; limitation chiffrée (11,5 → 14,7 ans) |
| 6 | Validation : part des tirages infinis non donnée ; G 1880-1900 présenté comme lissé | Corrigés |
| 7 | « Sans convergence » mesuré nulle part | Convergence déclarée de l'optimiseur contrôlée (ajustement central, ajustement stationnaire du test X3, tirages) ; libellé exact |
| 8 | Valeurs écrites en dur (1880-1900, 20 ans, 95 %, axe, 73, « quatre ») | Champs `preindustrial_period`, `past_return_period`, `ci_level` ; axe et textes tirés des données |
| 9 | Arrondis différents entre constat et tableau | Règle unique (une décimale sous 100, entier au-delà, après arrondi), partagée par l'ETL et la page |
| 10 | Sens de « ∞ » en borne d'intervalle et tirage indéfini non expliqués ; ∞ et 0/0 confondus | Note réécrite ; nombre de tirages infinis affiché ; erreur levée si une valeur centrale ou tous les tirages sont indéfinis |
| 11 | « Corrigé et brut coïncident » inexact ; prolongation brute des autres postes non contrôlée ; Villenave à 72 ans | « à 0,05 °C près » ; même seuil appliqué dans le code aux quatre postes ; années, manquantes et brutes dans X6 |
| 12 | Écart d'intensité identique à toute rareté par hypothèse ; intervalle de 1,2 an absent | Dit dans le constat ; intervalle et probabilité annuelle (≈ 80 %) ajoutés |
| 13 | En-tête « modèle explicite des causes » faux pour P10.2 | « modèle explicite » |
| 14 | `limite-projections` | Inchangée : P10.2 compare deux climats observés, sans projection |

Contre-relecture : corrections confirmées ; un défaut introduit (« au moins 3 % » pour 2,5 %, arrondi entier) et des
défauts latents (99,96 affiché « 100,0 », phrase agrammaticale si la période de retour devenait infinie, robustesse
affirmée sans condition, milliers, convergence de l'ajustement stationnaire et tirages écartés des autres postes non
suivis) : tous corrigés. Singulier « 1,2 an » retenu partout. `limite-attribution` et `limite-projections` déclarées
relues dans leur rédaction actuelle.

Affirmations relues (P10.2, 19/11/2026) : limite-attribution#c24c5413be, limite-projections#31ccce92d2

## P10.3 — amplification régionale (19/11/2026, garde-fou D-AH)

Publier P10.3 rendait `limite-attribution` incomplète et `cmp-terres-oceans` fausse (elle disait que l'étude ne compare
pas la région aux seules terres). Relecture par un agent séparé, qui n'avait rien rédigé, des deux affirmations, du
constat et des textes générés, de la page, de `docs/validation-p10.md`, du journal et du code. Le relecteur a réajusté
k à partir des séries publiées : chiffres reproduits.

| | Signalement | Traitement |
|---|---|---|
| 1 | JSON périmé : « le facteur est plus fort en été qu'en hiver » alors que les intervalles se recoupent | Code déjà corrigé ; JSON régénéré par l'ETL |
| 2 | Limitation : « trois postes proches du littoral » (faux : deux) ; contrôle A6 peu indépendant | Corrigés ; indépendance discutée dans la limitation et la validation |
| 3 | Constat lisible comme un réchauffement total de 2,16 °C | « par °C mondial (ajustement sur …) » ; unités des saisons |
| 4 | `cmp-terres-oceans` sans période ni statut | Datée ; « résultat de l'étude, à titre d'information, sans critère » ; contrôle D-AH étendu aux périodes ; Newey-West publié contre les terres |
| 5 | « La variante homogénéisée mesure l'effet des années brutes » : elle mêle trois effets | Reformulé ; libellé de la variante France précisé |
| 6 | Autocorrélations calculées avec un autre estimateur que celui du test | Valeurs du test données (−0,37, −0,32, −0,38) |
| 7 | Ljung-Box de la Gironde contre les terres non signalé ; note de méthode incomplète sur le lissage de CRUTEM5 | Corrigés |
| 8 | Effet des aérosols affirmé sans test ; chiffres de Ribes et al. à vérifier | « probablement, selon la littérature » ; Ribes et al. vérifiés sur le résumé |
| 9 | Journal P10.2 « 5,13 » ; « 1,2 an / ans » | 5,13 juste (calcul officiel) ; harmonisé |
| 10 | Valeurs écrites en dur sur la page ; pentes à 2 décimales ; périodes des saisons | Champs ajoutés au JSON ; 3 décimales ; périodes affichées |
| 11 | « Principe » : G moyen sur 4 ans non dit ; « ne se transpose pas à la France » | Corrigés (« ni à la France ni à la Gironde ») |
| 12 | Double arrondi des pentes ; formatage du contrôle ; nombre de postes en dur | Pleine précision ; règle d'arrondi commune ; nombre lu dans la série |

Contre-relecture : corrections confirmées ; un défaut nouveau (libellé « même k » pour le contrôle de Newey-West, qui
est une autre estimation) corrigé, et des points mineurs traités (paires d'années citées, place d'une remarque,
contrôle de Newey-West contre les terres affiché). `limite-attribution`, `cmp-terres-oceans` et `limite-projections`
déclarées relues dans leur rédaction actuelle.

Affirmations relues (P10.3, 19/11/2026) : limite-attribution#466794c70d, cmp-terres-oceans#9e20716866, limite-projections#31ccce92d2

## P10.4 et P10.4b — cohérence physique (20/11/2026, garde-fou D-AH)

Publier P10.4 et P10.4b rendait `limite-attribution` incomplète (rien sur les contrôles de cohérence) ; `limite-glaciers`
complétée (la masse GRACE est utilisée sans en séparer l'origine). Relecture par un agent séparé, qui n'avait rien
rédigé, des affirmations, des textes générés (constats, résultats, références, limites, notes des graphiques), de la
page, du code de calcul et de relevé, de la validation et du journal. Le relecteur a vérifié les chiffres des textes
contre le JSON et les références en ligne.

| | Signalement | Traitement |
|---|---|---|
| 1 | `limite-attribution` : « vérifient que les mesures s'accordent » se lit comme une confirmation ; « indépendantes » trop fort | « mesures de natures différentes », « testent si … (elles ne s'accordent pas toutes) » |
| 2 | Écart B2 : l'explication de remplacement (fourchette inadaptée à la mer) affirmée sans test ; effet de l'estimateur omis | Dite « non testée » ; O'Gorman et Muller rapportés à l'air ; rapports de tendances qualifiés ; MCO 9,9 contre Prais-Winsten 10,9 |
| 3 | Constat de P10.4b : « se ferme sur 2005-2015 » alors que l'incertitude dépasse la tolérance ; 2016-2024 tu | « dans la tolérance … mais son incertitude dépasse la tolérance » ; 2016-2024 cité |
| 4 | Résultat E : « les deux hausses sont compatibles » alors que la hausse du flux océanique n'est pas établie | Intervalles affichés ; « ne se contredisent pas, mais le contrôle est peu exigeant » |
| 5 | Critères recadrés de P10.4 comptés comme traités dès la publication de P10.4b | Chacun suit son correspondant (C2 → B2, C4 → B3, C6 → B4) |
| 6 | Références : Fu et al. paru en 2025 et rapport de tendances ; TMR sans auteur ; période de fermeture du WCRP et de Chen et al. ; intervalle à 90 % de Loeb et al. ; R-B1 plus fort que le cadrage | Corrigées dans le code, l'onglet et la validation ; cadrage laissé d'origine, dit au journal |
| 7 | P10.4 sans renvoi à la réfutation de l'hypothèse du domaine | Renvoi dans la note du graphique V, la limitation et la validation |
| 8 | Limitation E : part de l'excédent hors de l'océan 0-2000 m sous-estimée (10 %) | Terres 5 %, glaces 3 %, atmosphère 1 % (GIEC AR6, vérifié) plus l'océan profond |
| 9 | Bilan marin : correction isostatique de GRACE omise ; intervalles probablement trop étroits | Limites ajoutées ; validation nuancée |
| 10 | `confidence_reason` de P10.4b confuse | Réécrite |
| 11 | Page : année en dur ; « critères fixés avant le calcul » trompeur pour P10.4b ; pointillés absents de N′ | Corrigés |
| 12 | Arrondi à 4 décimales ; « 2,0 » contre « 2,05 » ; centrage de la masse ; espace des milliers ; R² gonflé par la tendance | Pleine précision ; deux décimales ; note précisée ; corrigés |

Contre-relecture : corrections confirmées. Défauts nouveaux corrigés : deux branches du constat de P10.4b qui
auraient produit un texte faux (« nettement » réservé au cas où l'intervalle sort de la tolérance ; « y revient »
au lieu de « y reste ») ; ponctuation et cas « B2 et B3 conformes » de la raison de confiance ; commentaire et libellé
de la validation ; « β n'est pas une pente interannuelle » précisé ; incertitude de la correction isostatique de GRACE
dite non évaluée faute de source. `limite-attribution`, `limite-glaciers` et `limite-projections` déclarées relues
dans leur rédaction actuelle.

Affirmations relues (P10.4, 20/11/2026) : limite-attribution#518167d701, limite-glaciers#7c38ea8242, limite-projections#31ccce92d2
