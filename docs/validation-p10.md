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

Tous les critères X1 à X6 sont conformes ; confiance « élevée » (règle D-AO). (Relecture P10.3 : « [2,39 ; 5,13] »
suit le calcul officiel, 5,132, et non le calcul local, 5,135.)

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
L'échec tient à une seule autocorrélation des résidus blanchis (estimateur du test), au décalage de 10 ans : −0,37
(−0,32 pour la France) ; les autres décalages de 1 à 12 ans restent entre −0,18 et +0,17 (France : entre −0,22 et
+0,13). Le même test passe à 5 ans (p = 0,62), 15 ans (p = 0,08) et 20 ans (p = 0,09). Ce motif est dans la série
régionale elle-même : sans aucune covariable, les résidus d'une tendance quadratique ont la même autocorrélation à
10 ans (−0,38). Il vient de paires d'années à 10 ans d'intervalle et d'écarts opposés (pour la Gironde, d'abord
1956 et 1966, 2011 et 2021, 1997 et 2007, 1980 et 1990) : variabilité propre de la région ou hasard d'échantillonnage sur 72 ans, que le modèle
AR(1) ne représente pas.

Effet sur la conclusion : un contrôle par moindres carrés ordinaires avec erreurs de Newey-West, qui ne suppose aucune
forme d'autocorrélation, donne pour la Gironde k = 2,14 avec des intervalles [1,82 ; 2,45] (troncature 4 ans),
[1,85 ; 2,43] (10 ans) et [1,87 ; 2,40] (15 ans) : la borne basse reste nettement au-dessus de 1, A3 tient. Le
contrôle à 10 ans est désormais publié pour chaque facteur. L'écart ne change pas le constat ; il signale que
l'intervalle de Prais-Winsten repose sur une hypothèse (AR(1)) que les résidus ne respectent pas tout à fait. Critère
non modifié. **Écart accepté par Grég le 19/11/2026 (D-AR)** ; confiance « moyenne » inchangée.

### Constats sans effet sur les critères

- France et Gironde ont des facteurs presque identiques (2,16 et 2,13) : sur 1959-2024, leurs anomalies annuelles sont
  corrélées à 0,98. Pour trois variantes, les deux facteurs coïncident même à deux décimales (HadCRUT5 : 2,107 et
  2,109 ; Berkeley : 2,062 et 2,058 ; G annuel : 1,973 et 1,970) : coïncidence d'arrondi, vérifiée en pleine
  précision.
- k France dépasse la borne haute de la fourchette de contrôle (2,0) ; seul son intervalle la recoupe (A4). La TRACC
  (rapport ≈ 1,33) compare des réchauffements cumulés jusqu'en 2030-2100 (France depuis 1900-1930, monde depuis
  1850-1900) ; k mesure le rythme observé depuis 1959, probablement accru, selon la littérature, par la baisse des
  aérosols en Europe depuis les années 1980 (non testé ici) : la variante 1979-2024 donne 2,40 pour la France. Ce
  rythme récent n'est pas une projection.
- Contre les seules terres émergées, les deux facteurs restent au-dessus de 1 (borne basse 1,28 et 1,27) : le contraste
  terres-océans explique une partie de l'amplification (terres ≈ 1,43 fois le monde), pas toute.
- Le facteur d'été est plus élevé que celui d'hiver, mais leurs intervalles se recoupent : l'hiver, très variable,
  laisse un intervalle d'environ ± 1 (période 1960-2024 pour la France et 1954-2024 pour la Gironde : l'hiver de 1959
  et de 1953 demanderait le mois de décembre précédent). Ribes et al. (2022, Earth System Dynamics 13, 1397, résumé)
  attendent pour l'avenir un réchauffement d'hiver environ 15 % sous la moyenne annuelle et d'été environ 30 %
  au-dessus : même sens, non testé ici.
- Information « terres contre monde » : le premier calcul lissait les deux séries (autocorrélation des résidus 0,92,
  intervalle trop étroit) ; corrigé après le calcul en prenant CRUTEM5 annuel, comme les séries régionales (incohérence
  de mise en œuvre sur une information sans critère ; 1,38 → 1,43). Son test de Ljung-Box échoue aussi (p = 0,01),
  comme celui de la Gironde contre les terres (p = 0,03) ; la France contre les terres passe (p = 0,10). Les intervalles
  de Newey-West publiés pour chaque facteur servent de contrôle.
- La Gironde suit la France : les cinq postes donnent 2,10 à 2,19, littoraux compris (Cap-Ferret 2,14). Le contrôle A6
  est peu indépendant : quatre de ces postes forment le composite ; seul Bordeaux-Paulin (2,17) est extérieur.
- La variante « années homogénéisées seules » change trois choses à la fois : elle retire les années brutes, raccourcit
  la période (sans 2022-2024, très chaudes) et, pour la France, prend la série publiée à 220 postes ; l'écart
  2,16 → 2,01 mêle ces trois effets.

## P10.4 — cohérence physique

Cadrage, décisions D-AS à D-AU et critères C1-C7 : `docs/phases.md`, section P10.4. Résultats automatiques :
`docs/validation-p10-resultats.md`. Calcul officiel : ETL du 20/11/2026 sur la branche `p10-4`.

### Résultats

Confiance « non établie » (règle D-AT) : deux contrôles physiques sur quatre sont conformes.

| Contrôle | Résultat | Critère |
|---|---|---|
| V, vapeur d'eau | β = 9,4 % par °C [8,6 ; 10,2], 1988-2025, contre [6 ; 8] attendu | C2 non conforme |
| S, stratosphère | TLT +0,229 (RSS) et +0,148 (UAH) °C/décennie, TLS −0,140 et −0,196, tous nets, 1979-2025 | C3 conforme |
| N, niveau marin | 3,94 mm/an observés (0,3 d'ajustement isostatique compris) contre 1,27 de dilatation + 2,05 de masse ; résidu +0,62 mm/an, 2005-2024 | C4 non conforme |
| E, énergie | déséquilibre +0,50 W/m²/décennie [+0,25 ; +0,74], flux océanique +0,15 [−0,19 ; +0,49], 2006-2024 | C5 conforme |

C1 conforme (masque de vapeur d'eau : 65,1 % de la bande ; GRACE : 206 mois sur 240). C6 non conforme : la variante
NOAA de C2 ne converge pas (Prais-Winsten) et donnerait de toute façon 9,9 % par °C en moindres carrés ; le résidu de
C4 avec les pentes de Sen est +0,63 ; seule la variante de C5 (flux lissé) est conforme.

Essai avant le calcul officiel : le contrôle V a été essayé sur les données relevées (β = 9,4, et la non-convergence
de la variante NOAA) avant l'exécution officielle. Aucun critère, seuil ni choix n'a été modifié après ; la seule
modification du code après l'essai traite la non-convergence comme un échec de la variante au lieu d'arrêter l'ETL.

### Écart C2 : la vapeur d'eau croît plus vite que 7 % par °C de la température moyenne de la mer

Le résultat n'indique pas une physique violée ; il indique, probablement, un contrôle mal construit. Le taux de
Clausius-Clapeyron porte sur la vapeur et la température **d'une même masse d'air**. Le cadrage a rapporté la vapeur
mesurée entre 60° S et 60° N à la température moyenne de la mer du globe entier. Les variations d'une année à l'autre
de ces deux grandeurs sont dominées par El Niño, qui fait varier fortement la mer tropicale (où se trouve l'essentiel
de la vapeur) et beaucoup moins la moyenne du globe : le dénominateur est trop faible, la pente trop forte. La
littérature va dans ce sens : dans les modèles, la vapeur d'eau totale croît de 7,3 % par °C de la température moyenne,
mais de 6 à 12 % par °C selon la latitude (O'Gorman et Muller, 2010) ; des mesures micro-ondes indépendantes donnent
environ 11 % par °C contre la température de mer moyennée par bandes de latitude (radiomètre TMR de Topex, 1992-2005, étude publiée en 2009).
La relation elle-même est très serrée (96 % de la variance expliquée) : la vapeur suit bien la température, avec un
facteur que ce contrôle ne permet pas de comparer à 7 %. Cette explication n'est pas vérifiée ici : il faudrait la
température de la mer sur le même domaine, que l'étude ne publie pas.

### Écart C4 : le bilan du niveau marin laisse +0,62 mm/an non expliqués

La non-fermeture du bilan après 2016 est documentée : le bilan était fermé sur 1993-2016, il ne l'est plus depuis avec
Jason-3, Argo et GRACE-FO (Chen et al., 2020). Barnoud et al. (2021, GRL 48) l'attribuent pour environ 40 % à des
dérives de salinité des flotteurs Argo — sans effet ici, puisque le cadrage n'utilise que la dilatation thermique —
et ne trouvent pas d'erreur suffisante dans l'altimétrie ; la composante thermique et la masse GRACE restent les
suspects pour le reste. S'y ajoutent l'océan sous 2000 m (environ 0,1 mm/an) et l'incertitude de la correction
isostatique (0,3 mm/an retenu). Le résidu (+0,62, information [+0,34 ; +0,90]) est du même ordre que les écarts publiés ;
il ne remet pas en cause la conclusion qualitative (la hausse vient de la dilatation et de l'eau ajoutée, la masse en
représentant environ la moitié et la dilatation un tiers), mais le bilan **n'est pas fermé à 0,5 mm/an près** sur
2005-2024 avec ces trois produits.

### Constats sans effet sur les critères

- C5 est conforme, mais faiblement : le flux de chaleur entrant dans l'océan 0-2000 m, obtenu par différence du contenu
  thermique annuel, a une tendance positive (+0,15 W/m² par décennie) mais non significative ; c'est surtout la largeur
  de son intervalle qui le fait recouper celui de CERES. Le critère (deux tendances positives, intervalles qui se
  recoupent) était peu exigeant ; il est tenu, sans plus.
- C3 est conforme et attendu d'avance. Information : la stratosphère se refroidit encore sur 1998-2025 (−0,055 °C par
  décennie pour RSS, −0,096 pour UAH, intervalles sous zéro), plus lentement que sur 1979-1997 (−0,41 et −0,49) ; le
  « stable depuis le milieu des années 1990 » du GIEC (R-B2) n'est donc pas retrouvé tel quel avec ces versions.
- La légende du graphique de vapeur d'eau affirmait que les deux courbes se superposent si la physique est respectée ;
  corrigée après le calcul (les deux courbes ne portent pas sur la même région).

## P10.4b — recadrage de V et N (après le calcul de P10.4)

Cadrage, décisions D-AV à D-AX et critères B1-B5 : `docs/phases.md`, section P10.4b. Sous-phase cadrée **en
connaissant** le résultat de P10.4 ; seuils non élargis (D-AW). Calcul officiel : ETL du 20/11/2026 sur la branche
`p10-4`. Aucun essai local avant ce calcul. Les chiffres de P10.4 sont inchangés par ce second calcul.

### Résultats

Confiance « moyenne » (règle D-AX) : un contrôle recadré sur deux est conforme.

| Contrôle | Résultat | Critère |
|---|---|---|
| V′, vapeur d'eau et mer du même domaine | β = 10,9 % par °C [9,6 ; 12,2], 1988-2025 (masque commun : 65,0 % de la bande, 27 582 mailles) | B2 non conforme |
| N′, bilan marin 2005-2015 | 3,47 mm/an observés contre 1,18 de dilatation + 2,22 de masse ; résidu +0,07 mm/an (information [−0,64 ; +0,78]) | B3 conforme |
| Information, 2016-2024 | résidu +1,30 mm/an [+0,90 ; +1,70] : la masse ralentit (1,42 mm/an) quand l'altimétrie accélère (4,12) | — |

B1 conforme (GRACE : 116 mois sur 132). B4 non conforme : la variante en moindres carrés de B2 donne 9,9 % par °C
[8,9 ; 10,9], également hors de [6 ; 8] ; la variante de Sen de B3 donne +0,13, conforme.

### Écart B2 : la vapeur d'eau croît d'environ 10 % par °C de la mer, même sur le même domaine

Corriger le domaine n'a pas ramené la pente vers 7 % : elle passe de 9,4 à 10,9 % par °C. L'hypothèse avancée pour
l'écart C2 (domaines différents) n'explique donc pas l'écart ; elle est réfutée par ce calcul. Ce que les deux calculs
montrent ensemble, c'est que **la fourchette de 6 à 8 % par °C n'est pas la bonne référence quand la température est
celle de la mer** : le taux de Clausius-Clapeyron porte sur la température de l'air, et la troposphère tropicale, où
se trouve l'essentiel de la vapeur, varie plus que la mer. Les valeurs publiées contre la température de la mer sont
du même ordre que celles trouvées ici : environ 9,9 % par K dans les tropiques pour un enregistrement satellite (Fu et
al., préprint ESSD 2024) et environ 11 % par K pour le radiomètre TMR (1992-2005). Le cadrage
(R-B1) aurait dû le prévoir ; la fourchette a été maintenue après coup pour ne pas ajuster un seuil à un résultat
(D-AW). L'autocorrélation des résidus est forte (ρ = 0,62) : la pente est moins précise qu'elle n'en a l'air.

### Constats sans effet sur les critères

- B3 est conforme, mais faiblement : onze ans seulement, et un intervalle d'information de ± 0,7 mm/an, plus large que
  la tolérance ; le découpage en 2016 a été choisi après le premier calcul, en s'appuyant sur la littérature. Ce que
  le recadrage établit nettement, c'est la **localisation** de l'écart de P10.4 : le bilan se ferme avant 2016
  (+0,07) et pas après (+1,30), comme l'ont décrit Chen et al. (2020) et Barnoud et al. (2021).
