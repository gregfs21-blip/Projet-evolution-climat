# Validation P7 : analyse

Résultats automatiques : `docs/validation-p7-resultats.md`. Critères L1-L5 validés par Grég le 31/10/2026, avant tout
calcul. Les décisions sont dans `docs/phases.md`, section P7.

## Bilan

L1 et L3 sont conformes ; L2, L4 et L5 sont informatifs. Les quatre indicateurs sont publiés le 06/11/2026, après le
relevé complet du Z500 quotidien ERA5 de 1940 à 2025. Ce relevé correspond à 43 requêtes de 2 ans, en moyenne
quotidienne de 0, 6, 12 et 18 UTC, et a duré du 01/11 au 06/11.

| Indicateur | 1976-2025 | Toute la série | Confiance |
|---|---|---|---|
| Jours de blocage, hiver | −2,0 jours par décennie, p = 0,08 | −1,05, 1941-2025, p = 0,04 | signal non établi (plafond) |
| Jours de blocage, été | −0,9, p = 0,44 | −0,26, p = 0,57 | signal non établi (plafond) |
| Z500 Atlantique-Europe | +6,7 m par décennie, p < 0,001 | +2,9, p = 0,009 | moyenne (règle ERA5) |
| CAPE de l'été, Gironde | +15,3 J/kg par décennie, p = 0,01 | +10,8, p < 0,001 | signal non établi (plafond) |

## Lecture

**Blocages.** Aucune tendance n'est établie sur 1976-2025. En hiver, la série complète baisse significativement, mais
elle commence dans les années 1940, quand ERA5 manque d'observations en altitude. La littérature ne retient pas de
tendance robuste observée. Le plafond est justifié, et L4 montre que le signe ne dépend pas du secteur choisi.

**Z500.** Il monte nettement. C'est cohérent avec le réchauffement de la colonne d'air, mais l'indicateur reste
« moyenne » : c'est ERA5, sans référence. Une rupture vers 2002 disparaît une fois la tendance retirée.

**CAPE.** La pente est significative, mais la CAPE est un indicateur indirect : elle mesure l'énergie disponible pour
la convection, pas la foudre ni les orages, et c'est une moyenne mensuelle. Elle reste plafonnée.

**L3.** Sur 1981-2010, les jours bloqués représentent 33,9 % de l'hiver et 17,6 % de l'été. L'ordre attendu (hiver >
été) est respecté et les valeurs sont dans la fourchette fixée, mais la fourchette [5 ; 40 %] est large : ce contrôle
écarte une erreur grossière, il ne valide pas une fréquence.

## Couverture

- Géopotentiel monde : passe de « prévu » à « publié » (Z500 Atlantique-Europe et blocages).
- Foudre Gironde : passe à « publié » par la seule CAPE, indicateur indirect. La note de la case le dit ; ce n'est
  pas la foudre.
