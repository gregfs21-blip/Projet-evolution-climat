# Validation P2a — analyse des écarts

Résultats automatiques : `docs/validation-p2a-resultats.md` (régénéré à chaque ETL). Critères : `docs/phases.md`.
Ce document est rédigé à la main. Il explique chaque écart et propose une décision, que seul Grég prend.

État au 23/10/2026, premier calcul sur données réelles : **8 critères satisfaits sur 12**. La phase n'est pas close.

## Ce qui est solide

- **Signe partout le même (E6).** Les journées estivales (TX ≥ 25 °C) augmentent aux 5 stations, de +5,7 à +7,0
  j/déc. (séries corrigées, de 1953 ou 1962 à 2022 ; Villenave jusqu'en 2001). Les jours de gel baissent aux 7
  stations, de −1,25 (Cap-Ferret) à −3,16 j/déc. (Lacanau, série 1967-1997, non significative).
- **Correctif exact (E5).** Après correction, la moyenne annuelle reproduit la série homogénéisée LSH à moins de
  0,0001 °C (tolérance 0,05 °C).
- **Référence gel (E4, R4).** Composite 1961-2010 : −1,43 j/déc., dans la fourchette publiée [−2 ; −1]. L'intervalle
  de confiance (−3,56 à +0,75) contient toutefois zéro : sur cette période seule, la baisse n'est pas significative.

## Écarts

### E4 R3 littoral — journées chaudes 1961-2010 : +5,83 j/déc. pour une fourchette [+4 ; +5]

Moyenne de Cap-Ferret et Cazaux, TX > 25 °C. L'écart est de 0,83 j/déc. au-dessus de la borne. L'intervalle de
confiance (+3,46 à +8,70) contient toute la fourchette publiée.

Éléments, sans conclusion définitive :
- la référence est de seconde main, arrondie au jour, et porte sur 1960-2010, pour un « littoral » non défini ;
- **la correction B relève la tendance de Cap-Ferret** : +4,63 j/déc. en brut, +6,97 corrigée (1953-2022, TX ≥ 25 °C).
  C'est le plus grand effet de la correction sur les 29 séries. Ce peut être une vraie rupture corrigée par
  Météo-France, ou un effet de la méthode, qui ne corrige que la moyenne mensuelle. Rien ne permet de trancher ici.

Différence avec C3 en P1 : l'écart était de 0,004 °C/déc. pour une référence arrondie au dixième. Ici, il est de 0,83
pour une fourchette d'un jour de large. Ce n'est pas un arrondi.

### E4 R3 intérieur — non évaluable

Villenave-d'Ornon a une année incomplète (2002) dans 1961-2010 : la moyenne Mérignac + Villenave n'existe pas.
**C'est une erreur de ma part au moment de fixer la référence.** L'inventaire des années complètes était connu sans
aucun résultat, je ne l'ai pas consulté. Le remplacer maintenant par Mérignac seul serait un choix fait **après**
publication des pentes de Mérignac (sa tendance 1961-2010 pour TX ≥ 25 °C figure déjà dans ses détails
statistiques). Si ce choix est fait, il doit être tracé comme tel.

### E7 — contrôle A : 23 concordants, 0 discordant, 11 non évaluables

Non évaluables : la dernière rupture corrigée par Météo-France est trop récente (moins de 10 ans après), ou des
années manquent (Villenave, Lacanau, composites TN). Leur confiance est déjà limitée à « moyenne ».

**Limite du critère, à dire clairement.** Le contrôle A ne porte que sur la période **après** la dernière rupture.
Sur cette période, la correction B est presque nulle par construction : A et B sont donc proches d'office. E7
vérifie que la correction ne déforme pas la période récente. Il ne valide **pas** la période ancienne, où la
correction agit vraiment. Le tableau d'information « effet de la correction B » le montre : écart médian brut −
corrigé de 0,19 j/déc., mais jusqu'à 2,34 j/déc. (Cap-Ferret, TX ≥ 25 °C).

### E8 — sans code qualité 9 : 3 conclusions modifiées sur 29

Villenave gel, Paulin TX ≥ 25 °C et TX ≥ 30 °C. Dans les trois cas, la pente reste du même signe et d'ampleur
voisine ou plus forte. Seule la significativité est perdue : retirer les valeurs de code 9 rend des années
incomplètes et raccourcit la série. C'est une perte de puissance statistique, pas un renversement.

## Conséquence actuelle

E4 n'étant pas satisfait, **aucun indicateur P2a n'est en confiance « élevée »** : ils sont « moyenne » au mieux.
C'est la règle fixée, appliquée.

## Décisions de Grég (23/10/2026, après le premier calcul)

- E4 R3 littoral : écart **maintenu**, non accepté.
- E4 R3 intérieur : évalué sur **Bordeaux-Mérignac seul**, choix fait après publication de ses résultats.
- E7 et E8 : écarts **acceptés**, explications ci-dessus.
- Publication en production avec les écarts affichés.
