# Validation P4 — analyse des écarts (rédigée à la main)

Résultats automatiques : `docs/validation-p4-resultats.md`. Critères : `docs/phases.md` (P4).

## I4 — référence R9 (indice de Huglin) non retrouvée

Mesuré, écart des moyennes 2000-2019 et 1980-1999 : composite de Gironde (Cap-Ferret, Bordeaux-Mérignac, Cazaux)
+158 °C·j ; Bordeaux-Mérignac +165 ; Bordeaux-Paulin +162 ; Cap-Ferret +161 ; Cazaux +148. Villenave-d'Ornon n'est
pas mesurable : sa série homogénéisée s'arrête en 2001. Attendu : +127 (Ollat et al., 2021), fourchette [+102 ; +152]
fixée avant calcul.

Le réchauffement mesuré aux stations dépasse la référence de 4 à 30 %, dans le même sens partout, littoral compris.
La pente sur 1953-2022 est d'environ +70 °C·j par décennie à toutes les stations (I6 conforme). Cause la plus
probable, non démontrée : la référence est une grille interpolée (SAFRAN, 8 km), moyennée sur les points de grille du
vignoble, qui lisse les valeurs ; nos valeurs sont celles de stations, corrigées mois par mois par les séries
homogénéisées. Aucune erreur de calcul n'a été trouvée : la formule est celle de Huglin (1978) avec K = 1,04, et la
correction quotidienne conserve exactement les moyennes mensuelles LSH.

**Écart accepté par Grég le 28/10/2026, après calcul.** Le Huglin reste en confiance « moyenne », sauf à Cazaux, où
la référence est réellement retrouvée (« élevée »).

## I5 — vendanges et Huglin : conforme

r = −0,84 sur 54 ans (1953-2006). Les vendanges avancent de 3,3 jours par décennie sur 1957-2006 (−16 jours). La
série s'arrête en 2006 : elle ne dit rien des 20 dernières années, que l'ONERC décrit à Saint-Émilion (début vers le
15 septembre depuis les années 2010, contre le 26 septembre au XXe siècle). Les pratiques (maturité plus poussée)
retardent la récolte : la tendance sous-estime l'effet du climat.

## Remarques sans écart

- **Fraîcheur des nuits de septembre** : +0,08 à +0,14 °C par décennie, non significatif à toutes les stations
  (p de 0,08 à 0,27). Les nuits de septembre se réchauffent moins vite que la saison de végétation dans son ensemble.
- **Gelées tardives** : indice rare ; baisse significative entre normales à Bordeaux-Mérignac (0,8 → 0,1 jour par an)
  et à Cazaux (1,6 → 0,6) ; non significative ailleurs.
- **Canicule à Mérignac** : aucun épisode avant 2003 ; moyenne 0 → 0,9 jour par an entre 1961-1990 et 1991-2020
  (p = 0,04). Indice rare, confiance au plus « moyenne ».

## Danger météo d'incendie (FWI, calcul du 29/10/2026) : sans écart, à lire avec prudence

Moyenne de juin à septembre : 9,4 sur 1961-1990, 11,6 sur 1991-2020 ; tendance +0,93 par décennie sur 1976-2025
(p = 0,008). Jours de danger très élevé (FWI ≥ 21,3) : 12,2 puis 19,2 par saison ; +3,3 jours par décennie sur
1976-2025 (p = 0,009). Aucune référence publiée : confiance « moyenne ».

Réserve importante : sur toute la série (1940-2025), la tendance n'est pas significative (+0,14 par décennie), car les
années 1940 sont aussi dangereuses que les plus récentes (1942 et 1949 en tête, devant 2022 et 2016). 1949 est l'année
du grand incendie des Landes, ce qui rend ces valeurs plausibles ; mais ERA5 est beaucoup moins contraint par les
observations avant 1950. La hausse des cinquante dernières années est nette ; dire que le danger n'a jamais été aussi
élevé ne l'est pas.
