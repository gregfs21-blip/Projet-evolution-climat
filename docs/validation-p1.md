# Validation P1 — analyse des écarts

Première analyse le 22/10/2026 (ETL `0.1.0+0587963`), complétée le 23/10/2026 après les décisions de
Grég et l'évaluation de C4bis (ETL `0.1.0+b0c758e`). Mesures brutes : `docs/validation-p1-resultats.md`,
régénéré à chaque ETL. Critères, seuils et décisions : `docs/phases.md`, chacun commité avant le calcul
qu'il encadre.

## Bilan — P1 close le 23/10/2026

| Critère | Statut |
|---|---|
| C1 Exhaustivité | conforme (12/12 séries) |
| C2 Homogénéisé ≠ brut | conforme, garanti par le schéma (pydantic et zod) et testé |
| C3 TN | conforme : +0,294 dans [0,15 ; 0,35] |
| C3 TX | **écart accepté** par Grég le 23/10/2026 (+0,354 pour une borne de 0,35) |
| C4 | **retiré** le 23/10/2026 : référence invalide. Toujours calculé, pour information |
| C4bis Recoupement ERA5 | **conforme** : dérive LSH − ERA5 de +0,035 °C/déc., p = 0,19 |
| C5 Cohérence | conforme, avec la réserve exposée plus bas |
| C6 Ruptures | conforme : 20 ruptures détectées, aucune établie |
| C7 Autocorrélation | conforme. Avec C3 et C4bis satisfaits, les 20 indicateurs passent en confiance « élevée » |
| C8 Traçabilité | conforme |
| C9 Technique | conforme |

## C4bis — recoupement avec ERA5 : conforme, avec deux réserves

Villenave-d'Ornon, TM annuelle 1979-2022. La différence station − réanalyse dérive de **+0,035 °C par
décennie** (IC 95 % −0,002 à +0,070), non significative (Hamed-Rao, p = 0,19). Le critère fixé d'avance
est satisfait : la station et ERA5 décrivent le même réchauffement à environ 10 % près. Le décalage moyen
de +0,14 °C est un écart constant, attendu entre un point de mesure et une maille de 25 km : il ne pèse pas
sur les tendances. Maille ERA5 retenue par l'API : 44,750 N ; 0,500 O, à 7 km de la station.

Les résultats informatifs, publiés sans effet sur la clôture, appellent deux réserves.

**1. L'accord sur la moyenne recouvre en partie une compensation.** Sur les minimales, la station se
réchauffe plus vite qu'ERA5, de +0,099 °C/déc., écart **significatif** (p = 0,002). Sur les maximales,
elle se réchauffe moins vite, de −0,045 °C/déc. (p = 0,08). Les deux écarts se compensent en partie dans
TM = (TN + TX) / 2. Les deux sources s'accordent sur le sens (les maximales montent plus vite que les
minimales), pas sur l'ampleur de la différence. Impossible de départager : ERA5 représente mal les nuits
stables sous inversion, et la série homogénéisée peut garder un résidu sur les minimales, plus sensibles à
l'environnement du capteur. **Conséquence pratique** : la tendance de la température moyenne est la grandeur
la mieux établie. Celle des minimales est confirmée en ordre de grandeur, pas à 0,1 °C/déc. près. Une mise
en garde automatique est désormais affichée sur les indicateurs TN.

**2. Petit écart systématique de même signe.** Sur les quatre saisons, la station se réchauffe un peu plus
vite qu'ERA5 (+0,02 à +0,05 °C/déc.). L'écart n'est significatif qu'au printemps (p = 0,01), et reste partout
bien sous le seuil. Sur 1959-2019, la dérive est du même ordre (+0,029, p = 0,06). Un léger biais de l'une
des deux sources est possible ; il ne change aucune conclusion.

Rappel des limites fixées d'avance : ERA5 assimile les mesures synoptiques (vraisemblablement
Bordeaux-Mérignac, à 9 km). L'accord est un recoupement, pas une preuve indépendante.

## C3 TX — écart marginal, attribuable à l'arrondi de la référence

La pente 1959-2009 du composite TX vaut +0,354 °C/déc. ClimatHD publie « +0,3 °C par décennie » pour
la Nouvelle-Aquitaine. La fourchette [0,25 ; 0,35] retenue correspond à l'arrondi au dixième. L'écart
au-delà de la borne est de **0,004 °C/déc.**, alors que l'intervalle de confiance à 95 % de notre pente
(+0,237 à +0,457) recouvre entièrement la fourchette publiée.

S'y ajoutent deux différences de périmètre connues dès le départ :
- R1 est **régional**, notre composite est **départemental** (4 stations, dont 2 sous influence
  littorale). Un écart réel de quelques centièmes entre Gironde et région n'aurait rien d'anormal.
- R1 a été calculé sur une version antérieure de l'homogénéisation (les fichiers actuels datent de 2025).

**Décision (23/10/2026)** : écart accepté. Le résultat TN, lui, tombe au milieu de sa fourchette.

## C4 — la référence est incohérente, pas le calcul (critère retiré le 23/10/2026)

Notre TM saisonnière à Villenave-d'Ornon (1959-2019, régression linéaire) dépasse les valeurs ORACLE
de +0,09 (hiver) à +0,15 (été) °C/déc. L'écart est systématique, toujours de même signe, sur les quatre
saisons. J'ai vérifié la référence à la source (ORACLE Nouvelle-Aquitaine 2020, p. 26 : « Analyse de la
tendance linéaire par décennie en °C sur la période 1959 – 2019 »). Les valeurs sont bien celles
retenues, mais le tableau est **incohérent avec le reste du document** :

1. **Contradiction interne.** La tendance annuelle est, par linéarité, la moyenne des quatre tendances
   saisonnières. Celles d'ORACLE pour Villenave donnent (0,13 + 0,25 + 0,23 + 0,12) / 4 = **+0,18
   °C/déc.** Or le même document indique, pour les sites présentés, une tendance annuelle « légèrement
   supérieure à +0,33 °C par décennie » (p. 14) et « +0,3 °C par décennie » sur 1953-2017 (p. 16).
2. **Uniformité invraisemblable.** Les 16 stations du tableau, du littoral basque (Ciboure) à la
   montagne limousine (La Courtine), ont des valeurs presque identiques : 0,10 à 0,16 en hiver, 0,22 à
   0,27 au printemps et en été. Ce n'est pas compatible avec la diversité des sites.
3. **Nos chiffres sont cohérents entre eux.** Moyenne de nos quatre tendances saisonnières : +0,305 ;
   tendance annuelle calculée directement : +0,309. Ils sont aussi cohérents avec R1 (régional, même
   ordre de grandeur) et avec la tendance annuelle d'ORACLE lui-même (p. 14).

La cause exacte de l'erreur dans ORACLE n'est pas identifiable de l'extérieur. Le rapport entre leurs
valeurs et les nôtres (0,46 à 0,69) n'est pas constant, ce qui exclut une simple erreur d'unité.

**Décision (23/10/2026)** : option (b). R2 est écartée et remplacée par C4bis, recoupement avec ERA5
(voir plus haut), protocole commité avant tout calcul.

## C5 — conforme, mais ce n'est pas une confirmation indépendante

Toutes les stations sont à moins de 0,02 °C/déc. de la médiane, très loin du seuil de 0,10. Cette
homogénéité doit être lue avec prudence. La méthode HOMER corrige chaque série **par comparaison avec ses
voisines** : les séries homogénéisées tendent mécaniquement vers le signal régional commun. Sept stations
concordantes ne sont donc pas sept preuves indépendantes.

Cas particulier de **Bordeaux-Paulin** (centre urbain) : elle ne se réchauffe pas plus vite que les
stations rurales (TN +0,343 contre une médiane de +0,343 sur 1962-2022). Deux explications possibles,
non départageables avec ces données : l'îlot de chaleur urbain était déjà installé en 1962 et n'a plus
évolué, ou sa dérive a été traitée comme une inhomogénéité lors de l'homogénéisation. Les données brutes
quotidiennes (P2) permettront de comparer brut et homogénéisé sur cette station.

## C6 — la « rupture de 1988 » n'est pas établie

Le test de Pettitt détecte une rupture dans les 20 séries, presque toujours en 1988-1989, avec un écart
apparent de +1,1 à +1,5 °C entre avant et après. **Ce chiffre ne doit pas être cité** : il mélange la
tendance et un éventuel saut. Une fois la tendance de Sen retirée, aucune rupture ne reste significative
(p entre 0,30 et 1,0). Un modèle « droite + saut en 1988 » n'améliore que faiblement l'ajustement, et cette
amélioration est surestimée puisque la date a été choisie sur les mêmes données.

**Conclusion** : nos séries ne permettent pas de distinguer un réchauffement régulier d'un saut à la fin
des années 1980. Un tel changement de régime est décrit dans la littérature à l'échelle européenne, mais
il n'est **pas établi** ici. 4 ruptures coïncident en outre avec une correction d'homogénéité (Mérignac
TN et TM, Cazaux TX et TM) et sont marquées « artefact possible ».

## C7 — correction sans effet ici, ce qui était attendu

Avec 70 ans de données et des pentes de +0,3 °C/déc., les tendances sont si nettes (p de l'ordre de
1e-10) que la correction de Hamed-Rao ne change aucune conclusion. Elle deviendra déterminante en P2 et
P3, sur des indicateurs plus bruités : précipitations, vent, extrêmes.

Avec C3 et C4bis satisfaits, la règle C7 place les 20 indicateurs en confiance « élevée ». Pour les
minimales, cette confiance porte sur le **sens et l'ordre de grandeur** de la tendance (voir C4bis, réserve 1).

## Incident technique traité pendant la phase

La version 1.4.3 de pymannkendall (PyPI) peut produire une variance corrigée négative, donc p = NaN. Le
schéma l'a bloquée en CI avant toute publication. Le correctif amont (commit `ec2e3ab`, mars 2025) n'est
pas publié sur PyPI et ne s'installe pas depuis GitHub sous Python 3.12. Les fonctions concernées sont
donc reprises dans `etl/stats/mannkendall.py` (licence MIT, attribution) et recoupées contre la 1.4.3 dans
les tests. Le correctif borne le facteur de correction à 1 au minimum : le test ne peut que devenir plus
exigeant, jamais plus permissif. Résultats publiés inchangés à la décimale près.

## Résultats principaux (pour mémoire)

| Indicateur | Pente 1953-2022 | Pente 1962-2022 | Normale 1991-2020 − 1961-1990 |
|---|---|---|---|
| TN Gironde | +0,29 °C/déc. | +0,35 | +1,0 à +1,1 °C selon la station |
| TX Gironde | +0,36 °C/déc. | +0,43 | +1,2 °C |
| TM Gironde | +0,32 °C/déc. | +0,39 | +1,1 °C |

Le réchauffement est plus marqué sur les maximales que sur les minimales. La pente 1962-2022 dépasse
d'environ 20 % celle de 1953-2022 : c'est compatible avec une accélération, mais **ce n'est pas un test
d'accélération**. Une pente dépend de son point de départ, et 1953-1962 comporte des années chaudes
(1959, 1961) qui la tirent vers le bas. Une accélération se teste explicitement (tendances glissantes ou
modèle quadratique) : à prévoir en P8 pour la synthèse, pas à affirmer ici.
