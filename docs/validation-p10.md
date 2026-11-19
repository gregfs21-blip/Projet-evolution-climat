# Validation P10 — analyse des résultats et des écarts

## P10.1 — régression multiple

Critères O1-O9 et références R-O1 à R-O4 validés par Grég le 17/11/2026, avant tout calcul (`docs/phases.md`, P10).
Mesures automatiques : `docs/validation-p10-resultats.md` (régénéré à chaque ETL). Ce document explique les écarts ; il
ne modifie aucun critère. Chiffres arrondis une seule fois, à partir des valeurs en pleine précision de
`data/processed/demonstration.json` (relecture du 18/11/2026, signalement n° 3).

### Premier calcul (17-18/11/2026)

Entrées : ERF IGCC 2025 (`v2026.06.02`, 1750-2025), Niño 3.4 HadISST1.1 (anomalies complètes jusqu'en 2025),
HadCRUT5 1871-2025, GISTEMP v4 1880-2025, Berkeley Earth 1871-2024, telles que publiées sur le site.

| Jeu | βₐ (°C par W/m²) | ρ | R² | Humain 2010-2019 | Humain 2016-2025 | Naturel 2016-2025 | Réponse transitoire |
|---|---|---|---|---|---|---|---|
| HadCRUT5 | 0,466 [0,417 ; 0,516] | 0,71 | 0,93 | 1,06 °C | 1,25 °C [1,12 ; 1,38] | +0,03 °C | 1,83 °C |
| GISTEMP v4 | 0,447 [0,401 ; 0,492] | 0,70 | 0,93 | 1,02 °C | 1,20 °C [1,07 ; 1,32] | +0,03 °C | 1,76 °C |
| Berkeley Earth | 0,485 [0,433 ; 0,538] | 0,70 | 0,92 | 1,11 °C | 1,30 °C [1,16 ; 1,44] | +0,03 °C | 1,91 °C |
| Référence | — | — | — | 1,07 [0,9 ; 1,3] (IGCC 2025 ; AR6 1,07) | 1,24 [1,0 ; 1,5] (IGCC 2025) | [−0,1 ; 0,2] | 1,8, très probable 1,2-2,4 (AR6) |

Les intervalles du réchauffement attribué sont statistiques seulement : ils ne contiennent ni l'incertitude des forçages
ni celle de la structure du modèle, contrairement à la fourchette de l'IGCC. Ils ne sont donc pas « plus précis » que
l'IGCC.

O1 à O7 conformes pour les trois jeux. ENSO (βₑ = 0,110 à 0,119 °C par °C) et volcans (βᵥ = 0,133 à 0,138 °C par W/m²)
très significatifs ; soleil non significatif (p = 0,43 à 0,66). Corrélation de l'indice ENSO avec l'ONI : r = 0,991.
Facteurs d'inflation de la variance de 1,01 à 1,04 : les quatre termes ne se confondent pas.

### Écart O8 (b) : forçage anthropique à 5 %

**Constat.** Avec la borne basse (5 %) du forçage anthropique de l'IGCC, le réchauffement attribué 2016-2025 tombe à
0,22 °C (HadCRUT5), 0,09 °C (GISTEMP) et 0,09 °C (Berkeley), hors de [1,0 ; 1,5]. Les 9 combinaisons de décalages, la
borne haute (95 % : 1,22 à 1,30 °C) et la sous-période 1951-fin avec l'ONI (1,08 à 1,12 °C, βₐ recoupant la période
complète) sont conformes. O8 échoue donc sur la seule variante (b) à 5 %, pour les trois jeux.

**Analyse.**

- La borne à 5 % suppose un refroidissement par les aérosols si fort que le forçage anthropique net baisse de 1950 à
  1970 (minimum −0,46 W/m² en 1970) et n'augmente que de 0,11 W/m² entre 1901-1910 et 1936-1945, période où HadCRUT5
  se réchauffe de 0,47 °C. La meilleure estimation n'explique pas non plus ce réchauffement du début du siècle
  (+0,21 W/m², soit environ 0,10 °C avec βₐ) : c'est une limite commune, plus marquée avec la borne basse.
- Avec cette borne, l'estimateur AR(1) dégénère : l'autocorrélation estimée des résidus monte à ρ = 0,985-0,990, et la
  part de variance expliquée tombe à 0,18 (HadCRUT5), 0,00 (Berkeley) et −0,16 (GISTEMP), contre 0,92-0,93 avec la
  meilleure estimation. La transformation de Prais-Winsten revient alors presque à travailler sur les variations d'une
  année à l'autre ; estimé presque uniquement sur ces variations, βₐ tombe à 0,10 [−0,07 ; 0,27] °C par W/m²
  (HadCRUT5), d'où le réchauffement attribué très faible.
- Par moindres carrés ordinaires, la même variante ajuste encore la température (R² de 0,81 à 0,84) avec βₐ = 0,51 à
  0,56 et un réchauffement attribué de 1,10 à 1,19 °C, dans la fourchette ; mais l'autocorrélation des résidus (0,84)
  montre un modèle nettement moins bien spécifié qu'avec la meilleure estimation.

**Lecture.** Avec la borne à 5 %, le modèle ajuste nettement moins bien et l'estimateur AR(1) rend βₐ non identifiable.
Cela va dans le sens des contraintes observationnelles sur le forçage des aérosols (un refroidissement aussi fort cadre
mal avec les températures observées), sans le démontrer avec ce modèle à réponse instantanée. Le critère O8 (b)
supposait que chaque borne publiée resterait ajustable ; ce n'est pas le cas pour la borne basse, qui n'est d'ailleurs
pas une trajectoire cohérente (limite écrite d'avance).

**Statut.** Critère non modifié. Écart expliqué et **accepté par Grég le 18/11/2026 (décision D-AI)**. Selon la règle
D-AG et la pratique du projet (P2b : un écart accepté clôt la phase mais ne relève pas la confiance), P10.1 est close
et la confiance publiée reste « moyenne » tant qu'O8 n'est pas conforme au calcul.

### Constats sans effet sur les critères

- Température ajustée : pente de Sen 1979-2025 de 0,196 [0,179 ; 0,214] °C/décennie (HadCRUT5) contre 0,205
  [0,179 ; 0,234] observée ; l'intervalle se resserre de plus d'un tiers (37 %). Ces intervalles de Sen ne sont pas
  corrigés de l'autocorrélation, et l'incertitude des contributions retirées n'est pas propagée.
- Les années 2023, 2024 et 2025 ajustées sont 0,18, 0,13 et 0,26 °C au-dessus de la droite 1979-2025, alors que les
  résidus de la régression n'y valent que +0,08, −0,01 et +0,09 °C (écart type des résidus 0,11 °C) : le forçage
  anthropique, qui croît plus vite que linéairement, rend compte de ces années. C'est compatible avec le rythme de
  0,27 °C/décennie de réchauffement d'origine humaine sur 2016-2025 publié par l'IGCC 2025 ; aucune accélération n'est
  testée ici.
- Sous-période 1951-fin avec l'ONI : βₐ plus faible (0,410 contre 0,466 pour HadCRUT5) et ρ bien plus faible (0,13) ;
  les intervalles se recoupent. Le même calcul avec l'indice HadISST donne ρ = 0,16 : la baisse tient à la période, pas
  à l'indice. Elle suggère qu'une part de l'autocorrélation de la période complète vient de la variabilité
  multidécennale de la première moitié du XXe siècle, que le modèle ne représente pas ; des erreurs de forçage ou des
  biais de mesure de cette époque (températures de la mer des années 1940) peuvent aussi y contribuer.
- Contrôle MCO + Newey-West : coefficients voisins, sauf pour le soleil. Par MCO, même avec les erreurs de Newey-West
  (troncature à 4 ans, courte pour ρ ≈ 0,7), le soleil ressort significatif pour HadCRUT5 (0,55, p = 0,03) et GISTEMP
  (0,46, p = 0,048) ; l'estimation AR(1), qui modélise l'autocorrélation, donne 0,17 et 0,19 pour ces deux jeux (0,12 pour Berkeley ; p ≥ 0,43).

## P10.2 — valeurs extrêmes en Gironde

Données, méthode, références et critères X1-X7 validés par Grég le 19/11/2026, avant tout ajustement (D-AM à D-AO,
`docs/phases.md`). Calcul officiel du 19/11/2026 (ETL en GitHub Actions, version `0.1.0+1fb8608`) : `etl/demo_extremes.py`, 1 000
tirages bootstrap, graine 1002, aucun tirage écarté (échec ou optimiseur sans convergence déclarée). Chiffres arrondis une seule fois à partir de
`data/processed/demonstration.json` ; périodes de retour et rapports de probabilité avec une décimale sous 100, comme
sur la page.

### Résultats

| Grandeur | Valeur [intervalle à 95 %] |
|---|---|
| α, °C de TXx par °C de réchauffement mondial | 3,94 [2,39 ; 5,13] |
| σ ; ξ | 1,76 [1,25 ; 2,12] ; −0,31 [−0,47 ; −0,04] |
| Rapport de vraisemblance (contre la loi stationnaire) ; Kolmogorov-Smirnov | p < 0,001 ; p = 0,73 |
| G, GISTEMP lissé sur 4 ans : 1960 ; 2025 | −0,07 ; 1,03 °C |
| G de référence 1880-1900 (moyenne simple des 21 années) | −0,32 °C |
| Chaleur de retour 20 ans en 1960 | 37,7 [37,0 ; 38,4] °C ; revient tous les 1,2 [1,0 ; 2,4] ans en 2025 ; probabilité × 16,0 [8,4 ; 19,5] |
| Écart d'intensité à rareté égale, 2025 − 1960 | +4,3 [2,6 ; 5,6] °C (identique pour toutes les raretés : décalage pur) |
| Record du 11/08/2025, 41,6 °C, climat de 2025 | période de retour 11,5 [4,6 ; 75,8] ans |
| Le même, climat de 1960 | au-delà de la borne supérieure de la loi ajustée (40,0 °C) dans l'estimation centrale et dans 780 tirages sur 1 000 ; bornes basses des intervalles : période de retour 542 ans, rapport de probabilité 26,9 |

Tous les critères X1 à X6 sont conformes ; confiance « élevée » (règle D-AO).

### Constats sans effet sur les critères

- α central (3,94) est au-dessus du centre de la référence régionale (3,3) et du chiffre ERA5 de Vautard et al. (3,4),
  mais son intervalle recoupe [2,5 ; 4,2] (X4). Une station seule est plus bruitée qu'une moyenne régionale ; les
  quatre autres postes donnent 3,6 à 3,9. La valeur élevée n'est pas propre à Mérignac.
- Le record de 2025 est choisi après coup et figure dans l'ajustement. Sans 2025, α vaut 3,73, la période de retour du
  record aujourd'hui passe de 11,5 à 14,7 ans, et le record reste au-delà de la borne supérieure de la loi de 1960 : la
  conclusion qualitative ne dépend pas de cette année.
- « Pratiquement impossible » dans le climat de 1960 est une affirmation du modèle : elle dépend de la borne supérieure
  de la GEV, elle-même mal connue (ξ entre −0,47 et −0,04). 220 tirages sur 1 000 donnent une période de retour finie ;
  les bornes basses publiées (542 ans, × 26,9) sont des percentiles à 2,5 %, pas des minimums certains. Un tirage donne
  0/0 pour le rapport de probabilité (record au-delà de la borne dans les deux climats) et est écarté de son intervalle.
- Villenave-d'Ornon : 72 années (2002 manquante) et ξ = −0,41, proche de la borne de X2 ; X2 ne porte que sur
  Mérignac, et α de ce poste (3,63 [1,98 ; 4,60]) est cohérent. Les quatre postes sont prolongés en brut de 2023 à 2025
  selon la règle de X1 (écart corrigé − brut après la dernière rupture au plus 0,1 °C), désormais vérifiée dans le code.
- Le décalage pur (σ et ξ constants) fait que l'écart d'intensité est le même pour toutes les périodes de retour ; une
  variante où σ suit aussi G n'a pas été testée (hors cadrage).
- Calcul local préalable (mêmes code et graine, à partir des maxima de la sonde arrondis au centième) : mêmes
  conclusions, écarts d'une unité sur le dernier chiffre de quelques valeurs (borne haute de α 5,14 ; borne basse de la
  période de retour du record en 1960, 538 ans ; 779 tirages au-delà de la borne). Les chiffres publiés sont ceux du
  calcul officiel, sur les valeurs en pleine précision.

## P10.3 — amplification régionale

Données, méthode, références et critères A1-A7 validés par Grég le 19/11/2026, avant tout calcul (D-AP, D-AQ,
`docs/phases.md`). Calcul officiel : ETL en GitHub Actions sur la branche `p10-3` (données LSH et CRUTEM5).
Chiffres arrondis une seule fois à partir de `data/processed/demonstration.json`.

### Résultats

| Grandeur | France (1959-2024, 217 postes) | Gironde (1953-2024, 4 postes) |
|---|---|---|
| k contre le monde (GISTEMP lissé sur 4 ans) | 2,16 [1,77 ; 2,56] | 2,13 [1,75 ; 2,52] |
| ρ ; Ljung-Box à 10 ans | 0,02 ; p = 0,09 | 0,07 ; p = 0,03 |
| k contre les terres émergées (CRUTEM5 lissé), information | 1,56 [1,28 ; 1,85] | 1,55 [1,27 ; 1,84] |
| k d'été (juin-août), information | 2,76 [2,21 ; 3,31] | 2,62 [2,12 ; 3,12] |
| k d'hiver (décembre-février), information | 1,91 [0,84 ; 2,98] | 1,58 [0,68 ; 2,48] |
| Pentes de Sen, région / monde (information) | 0,377 / 0,175 °C par décennie, rapport 2,15 | 0,339 / 0,163, rapport 2,08 |

Terres émergées (CRUTEM5 annuel) contre le monde, 1953-2024 : 1,43 [1,33 ; 1,54] (GIEC AR6 : 1,59 / 1,09 ≈ 1,46 sur
2011-2020 contre 1850-1900).

Critères : A1, A3, A4, A5, A6 conformes ; **A2 non conforme** (Ljung-Box de la Gironde, p = 0,03). Confiance
« moyenne » (règle D-AQ).

### Écart A2 : autocorrélation restante à 10 ans en Gironde

Le test de Ljung-Box à 10 ans échoue pour la Gironde (p = 0,027 ; seuil 0,05) ; il passe pour la France (p = 0,09).
L'échec tient à une seule autocorrélation des résidus blanchis, au décalage de 10 ans : −0,44 (−0,39 pour la France) ;
les autres décalages de 1 à 12 ans restent entre −0,19 et +0,19. Le même test passe à 5 ans (p = 0,62), 15 ans
(p = 0,08) et 20 ans (p = 0,09). Ce motif est dans la série régionale elle-même : sans aucune covariable, les résidus
d'une tendance quadratique ont la même autocorrélation à 10 ans (−0,45). Il vient de paires d'années à 10 ans
d'intervalle et d'écarts opposés (2000 et 2010, 1956 et 1966, 1980 et 1990, 2010 et 2020) : variabilité propre de la
région ou hasard d'échantillonnage sur 72 ans, que le modèle AR(1) ne représente pas.

Effet sur la conclusion : un contrôle par moindres carrés ordinaires avec erreurs de Newey-West, qui ne suppose aucune
forme d'autocorrélation, donne pour la Gironde k = 2,14 avec des intervalles [1,82 ; 2,45] (troncature 4 ans),
[1,85 ; 2,43] (10 ans) et [1,87 ; 2,40] (15 ans) : la borne basse reste nettement au-dessus de 1, A3 tient. L'écart
ne change pas le constat ; il signale que l'intervalle de Prais-Winsten repose sur une hypothèse (AR(1)) que les
résidus ne respectent pas tout à fait. Critère non modifié ; décision d'accepter ou non l'écart laissée à Grég.

### Constats sans effet sur les critères

- France et Gironde ont des facteurs presque identiques (2,16 et 2,13) : sur 1959-2024, leurs anomalies annuelles sont
  corrélées à 0,98. Pour trois variantes, les deux facteurs coïncident même à deux décimales (HadCRUT5 : 2,107 et
  2,109 ; Berkeley : 2,062 et 2,058 ; G annuel : 1,973 et 1,970) : coïncidence d'arrondi, vérifiée en pleine
  précision.
- k France dépasse la borne haute de la fourchette de contrôle (2,0) ; seul son intervalle la recoupe (A4). La TRACC
  (rapport ≈ 1,33) compare des réchauffements cumulés jusqu'en 2030-2100 (France depuis 1900-1930, monde depuis
  1850-1900) ; k mesure le rythme observé depuis
  1959, gonflé en Europe par la baisse des aérosols depuis les années 1980 : la variante 1979-2024 donne 2,40 pour la
  France. Ce rythme récent n'est pas une projection.
- Contre les seules terres émergées, les deux facteurs restent au-dessus de 1 (borne basse 1,28 et 1,27) : le contraste
  terres-océans explique une partie de l'amplification (terres ≈ 1,43 fois le monde), pas toute.
- Le facteur d'été est plus élevé que celui d'hiver, mais leurs intervalles se recoupent : l'hiver, très variable,
  laisse un intervalle d'environ ± 1. Ribes et al. (2022) attendent pour l'avenir un réchauffement d'été environ 30 %
  au-dessus de la moyenne annuelle et d'hiver 15 % en dessous : même sens, non testé ici.
- Information « terres contre monde » : le premier calcul lissait les deux séries (autocorrélation des résidus 0,92,
  intervalle trop étroit) ; corrigé après le calcul en prenant CRUTEM5 annuel, comme les séries régionales (incohérence
  de mise en œuvre sur une information sans critère ; 1,38 → 1,43). Son test de Ljung-Box échoue aussi (p = 0,01).
- La Gironde suit la France : les cinq postes donnent 2,10 à 2,19, littoraux compris (Cap-Ferret 2,14).
