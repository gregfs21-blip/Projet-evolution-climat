# Validation P7 : analyse

Résultats automatiques : `docs/validation-p7-resultats.md`. Critères L1-L5 validés par Grég le 31/10/2026, avant tout
calcul. Les décisions sont dans `docs/phases.md`, section P7.

## Bilan

L1, L2 et L3 sont conformes ; L4 est informatif, comme décidé, et L5 est vérifié par la CI, hors du module de validation. Les quatre indicateurs sont publiés le 06/11/2026, après le
relevé complet du Z500 quotidien ERA5 de 1940 à 2025. Ce relevé correspond à 43 requêtes de 2 ans, en moyenne
quotidienne de 0, 6, 12 et 18 UTC, et a duré du 01/11 au 06/11.

| Indicateur | 1976-2025 | Toute la série | Confiance |
|---|---|---|---|
| Jours de blocage, hiver | −2,0 jours par décennie, p = 0,08 | −1,05, 1941-2025, p = 0,04 | signal non établi (plafond) |
| Jours de blocage, été | −0,9, p = 0,44 | −0,26, p = 0,57 | signal non établi (plafond) |
| Z500 Atlantique-Europe | +6,7 m par décennie, p < 0,001 | +2,9, p = 0,009 | moyenne (règle ERA5) |
| CAPE de l'été, Gironde | +15,3 J/kg par décennie, p = 0,01 | +10,8, p < 0,001 | signal non établi (plafond) |

## Lecture

**Blocages.** Aucune tendance n'est détectée sur 1976-2025. En hiver, la série complète baisse au test (p = 0,04),
mais son intervalle touche zéro, elle commence quand ERA5 manque d'observations en altitude, et la relecture trouve
p = 0,056 avec le secteur décalé. La littérature ne retient pas de tendance robuste observée. Le plafond est justifié.
L4 montre que décaler le secteur de 10° vers l'est ne change pas le signe des pentes 1976-2025 ; un seul décalage a
été testé.

**Z500.** Il monte nettement, ce qu'on attend d'une colonne d'air qui se réchauffe ; l'étude ne mesure pas la
température de la colonne sur cette zone, et la circulation peut aussi jouer. L'indicateur reste « moyenne » : c'est
ERA5, sans référence. Une rupture vers 2002 disparaît une fois la tendance retirée. Sur toute la série, la pente est
plus faible (+2,9 m par décennie, p = 0,009) parce que la série baisse avant 1979, période où ERA5 est moins
contraint ; la part réelle et la part d'artefact ne sont pas séparées.

**CAPE.** La pente est significative, mais fragile et indirecte. Elle dépend de l'année de départ : selon la
relecture, +13,8 J/kg par décennie (p = 0,04) en partant de 1979, +9,1 (p = 0,12) en partant de 1981. Elle dépend aussi
de l'humidité des basses couches, que ERA5 restitue avec une dérive à Bordeaux (contrôle H5 de la P3). Enfin, la CAPE
mesure l'énergie disponible pour la convection, pas la foudre ni les orages, et c'est une moyenne mensuelle. Elle reste
plafonnée.

**L3.** Sur 1981-2010, les jours bloqués représentent 33,9 % de l'hiver et 17,6 % de l'été. L'ordre attendu (hiver >
été) est respecté et les valeurs sont dans la fourchette fixée, mais la fourchette [5 ; 40 %] est large : ce contrôle
écarte une erreur grossière, il ne valide pas une fréquence.

## Couverture

- Géopotentiel monde : passe de « prévu » à « publié » (Z500 Atlantique-Europe et blocages).
- Foudre Gironde : reste « sans donnée ». La CAPE est publiée en exploratoire, mais ce n'est pas la foudre ; la
  rattacher à la case l'aurait affichée « publiée » (corrigé sur relecture, le 06/11/2026).

## Corrections tracées après calcul (relecture indépendante des 06 et 07/11/2026)

- L2 était affiché « information » alors que c'est un critère avec seuil : il est désormais mesuré (aucune saison ni
  année écartée en cours de série) et conforme. L5 reste vérifié par la CI, comme aux phases précédentes.
- Limites de la CAPE complétées (ERA5, dérive d'humidité, sensibilité à l'année de départ) ; doublon retiré des limites
  du Z500.
- Les chiffres « selon la relecture » ci-dessus viennent de calculs de contrôle du relecteur ; ils ne sont pas publiés
  dans les indicateurs.
- Les deux phrases qui dépendaient de ces calculs de contrôle (hiver : « ne résiste pas au décalage du secteur » ;
  CAPE : « plus significative si l'on part de 1981 ») sont retirées de la synthèse : un texte qui dépend d'un résultat
  doit être choisi par le code, et ces calculs ne sont pas automatisés. Ils restent ici, comme constats de relecture.
