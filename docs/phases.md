# Phases du projet

Chaque phase suit la même boucle : ETL → JSON → page → validation contre des valeurs publiées.
Une phase n'est close que lorsque les écarts avec les références sont expliqués.

| Phase | Contenu | Validation | État |
|---|---|---|---|
| P0 | Socle : arborescence, schéma, ETL, site, CI, workflow mensuel | Un indicateur factice traverse la chaîne jusqu'au site déployé | **close le 22/10/2026** |
| P1 | Températures Gironde : LSH TX/TN Mérignac + stations longues, anomalies 1961-1990 et 1991-2020, tendances Hamed-Rao, ruptures | Critères C1-C9 ci-dessous (C4 → C4bis) | **close le 23/10/2026** |
| P2 | Extrêmes et eau Gironde : jours > 30/35 °C, nuits tropicales, gelées, précipitations, insolation, SPEI | | à faire |
| P3 | Atmosphère et littoral Gironde : vent, humidité, pression (ERA5), SST golfe de Gascogne, marégraphe (PSMSL) | | à faire |
| P4 | Impacts Gironde : vendanges, danger météo incendie, CatNat (avec avertissement exposition/déclarations) | | à faire |
| P5 | France : indicateur thermique national (LSH), cartes de tendances, extension P2-P4 | | à faire |
| P6 | Monde : GES, températures croisées, océans, niveau marin, cryosphère, ozone, ENSO, EEI (CERES), puits de carbone | | à faire |
| P7 | Exploratoire : jet stream, Z500, blocages (CDS), proxy foudre — statut « signal non établi » | | à faire |
| P8 | Synthèse par échelle, avec niveau de confiance par affirmation | | à faire |

## Journal P0

- Contrat de données v1.0 (`etl/schema.py`, miroir `web/lib/schema.ts`).
- Tendance provisoire : Mann-Kendall classique + Sen (scipy). **Sans correction d'autocorrélation**,
  remplacée par Hamed-Rao (pymannkendall) en P1, avec comparaison des deux.
- Indicateur `demo-temperature-annuelle` : série synthétique, graine fixe, une lacune volontaire (1973).
  À retirer à la clôture de P1.
- Reporté : carte MapLibre (P1, quand il y aura plusieurs stations), détection de ruptures (P1).
- CI et ETL : actions passées en versions Node 24 (checkout v7, setup-python v7, setup-node v7, cache v6),
  runner épinglé sur ubuntu-24.04 pour qu'un changement d'OS ne modifie pas les résultats sans trace.
- Vercel : protection limitée aux préviews, la production est publique.
- Clôture P0 (22/10/2026) : chaîne vérifiée de bout en bout. Workflow ETL déclenché → commit
  `data: ETL du 2026-10-22` par etl-bot → déploiement Vercel de production automatique (READY).

## P1 — Critères de clôture (fixés le 22/10/2026, avant tout calcul)

Ces critères sont commités **avant** les premiers résultats, pour qu'ils ne puissent pas être ajustés
après coup. Ils ne seront modifiés que par un commit explicite, motivé, et signalé dans ce journal.

### Données (constat de la sonde du 22/10/2026)

Jeu LSH Météo-France (Licence Ouverte 2.0), méthode HOMER. En Gironde : 7 séries TN (Bordeaux-Paulin,
Lacanau, Cap-Ferret, Bordeaux-Mérignac, Sauternes, Cazaux, Villenave-d'Ornon) et 5 séries TX (les mêmes
sans Lacanau ni Sauternes). Homogénéisé de 1953 (1955 Lacanau TN, 1962 Paulin TX) à **2022**.
2023-2024 : prolongation **non homogénéisée** (`Q_HOM=0`).

### Références externes

- **R1** — ClimatHD Nouvelle-Aquitaine (Météo-France), repris par ORACLE Nouvelle-Aquitaine 2020 (p. 4),
  période 1959-2009 : TN annuelle **+0,2 à +0,3 °C/décennie**, TX annuelle **+0,3 °C/décennie**.
- **R2** — ORACLE Nouvelle-Aquitaine 2020 (p. 26), Villenave-d'Ornon, séries homogénéisées, 1959-2019,
  température moyenne saisonnière : hiver **+0,13**, printemps **+0,25**, été **+0,23**, automne **+0,12**
  °C/décennie.

### Critères

| # | Critère | Seuil |
|---|---|---|
| C1 | Exhaustivité | Les 12 séries de Gironde sont traitées ; aucune écartée sans justification écrite |
| C2 | Homogénéisé ≠ brut | 2023-2024 affichées distinctement, exclues de toute tendance et de toute normale (test automatique) |
| C3 | Validation régionale (R1) | Pente de Sen 1959-2009 du composite Gironde : TN dans [0,15 ; 0,35], TX dans [0,25 ; 0,35] °C/déc. (fourchettes publiées, arrondies au dixième) |
| C4 | Validation stationnelle (R2) | Villenave TM saisonnière 1959-2019, régression linéaire : écart ≤ 0,05 °C/déc. sur chacune des 4 saisons (Sen publié en complément) |
| C5 | Cohérence inter-stations | Période commune 1962-2022 : toute station à plus de 0,10 °C/déc. de la médiane des stations (même variable) est expliquée |
| C6 | Ruptures | Test de Pettitt (p < 0,05) sur séries annuelles homogénéisées. Toute rupture à ±1 an d'une rupture d'homogénéité corrigée par Météo-France est marquée « artefact possible » et n'est pas interprétée comme climatique |
| C7 | Autocorrélation | Significativité Hamed-Rao publiée ; écart avec le test classique documenté pour chaque série. Confiance « élevée » seulement si Hamed-Rao significatif **et** C3/C4 satisfaits (C4 remplacé par C4bis le 23/10/2026, voir ci-dessous) |
| C8 | Traçabilité | Chaque JSON porte : n° de série MF, amplitude minimale détectable, ruptures MF, période homogénéisée, date de production du fichier MF |
| C9 | Technique | Tests et CI verts, pages déployées, indicateur démo retiré, `package-lock.json` commité |

**Règle de clôture :** P1 est close quand C1-C9 sont satisfaits, ou quand chaque échec est expliqué dans
`docs/validation-p1.md` **et** accepté par Grég. Un écart inexpliqué bloque la clôture.

### Décisions du 23/10/2026 (Grég), avant tout calcul ERA5

**C3 TX — écart accepté.** Pente composite 1959-2009 de +0,354 °C/déc. pour une borne de 0,35 : écart de
0,004, inférieur à la précision de la référence (« +0,3 », arrondie au dixième), référence régionale
contre composite départemental, intervalle de confiance qui contient toute la fourchette publiée.
C3 est réputé satisfait pour l'application de C7.

**C4 — retiré, remplacé par C4bis.** La référence R2 (ORACLE 2020, p. 26) est incohérente avec le reste
du document (moyenne saisonnière +0,18 contre plus de +0,33 en annuel) : elle ne peut valider ni
invalider nos calculs. C4 reste calculé et publié pour information, sans effet sur la clôture. C4bis est
un **nouveau critère**, pas un assouplissement de C4 : il change de référence, de période et de test.

| # | Critère | Seuil |
|---|---|---|
| C4bis | Recoupement stationnel par une réanalyse | Villenave-d'Ornon, TM annuelle 1979-2022. Série des différences D = TM(LSH) − TM(ERA5). Satisfait si **\|pente de Sen de D\| ≤ 0,10 °C/déc.** **et** tendance de D **non significative** (Hamed-Rao, p ≥ 0,05) |

Protocole, fixé avant calcul :
- **ERA5** (ECMWF / Copernicus, maille 0,25°), via l'API archive d'Open-Meteo avec `models=era5` (pas de
  mélange de modèles), point 44,790 N ; 0,577 W. Maille effectivement retenue par l'API consignée dans le rapport.
- Variables quotidiennes `temperature_2m_max` et `temperature_2m_min`, jour local. TM = (TN + TX) / 2 au pas
  mensuel, puis moyenne annuelle sur 12 mois complets : même construction que pour LSH.
- **1979-2022** : début de l'ère satellitaire, où ERA5 est la plus robuste ; fin de l'homogénéisation LSH.
- Le test porte sur la série des différences, et non sur l'écart entre deux pentes : la variabilité
  interannuelle commune s'annule, et le test devient bien plus sensible à une dérive relative.
- Seuil de 0,10 °C/déc. choisi a priori : environ le quart de la tendance attendue sur 1979-2022. Au-delà,
  l'écart modifierait l'interprétation. Ce n'est pas une valeur tirée de la littérature.
- Publiés pour information, sans effet sur la clôture : TN et TX annuelles, TM saisonnière, TM 1959-2019.

Limites assumées d'avance :
- ERA5 n'est **pas totalement indépendante** : elle assimile les mesures synoptiques de surface,
  vraisemblablement celles de Bordeaux-Mérignac, à 9 km. Elle n'est cependant ni homogénéisée par HOMER ni
  contrainte par les mêmes stations voisines, et repose sur un modèle physique. Un accord vaut recoupement,
  pas preuve indépendante.
- Une maille de 25 km n'est pas un point : un décalage **constant** est attendu et sans importance, seule
  une **dérive** de D compte.
- En cas d'échec, l'écart ne désigne pas la série fautive : ERA5 a ses propres inhomogénéités, liées à
  l'évolution des systèmes d'observation.

### Limites connues dès le départ

- R1 est régional (Nouvelle-Aquitaine), le composite est départemental : un écart peut être réel.
- R2 date de 2020 ; les séries LSH ont été réhomogénéisées depuis (fichiers produits le 13/03/2025).
  La méthode de régression d'ORACLE n'est pas documentée avec certitude (régression linéaire supposée).
- Les séries s'arrêtent en 2022 pour l'homogénéisé : les années 2023-2025 seront traitées en P2 avec
  les données quotidiennes, avec la mention « non homogénéisé ».

### Journal P1

- 22/10/2026 : premiers résultats. C1, C2, C3 TN, C5 à C9 conformes ; **écarts C3 TX et C4**, analysés
  dans `docs/validation-p1.md`. Critères non modifiés. Clôture suspendue à la décision de Grég.
- Le test de Pettitt est complété d'un test sur résidus détendancés : sans cela, toute série en tendance
  présente une « rupture » artificielle (constaté sur les 20 séries).
- pymannkendall 1.4.3 (PyPI) produit p = NaN dans certains cas : fonctions reprises du correctif amont
  dans `etl/stats/mannkendall.py`, recoupées en test.
- 23/10/2026 : décisions de Grég. C3 TX accepté ; C4 retiré (référence invalide) et remplacé par C4bis
  (recoupement ERA5), protocole et seuil commités avant tout téléchargement ERA5.
- 23/10/2026 : C4bis **conforme** (dérive LSH − ERA5 de +0,035 °C/déc., p = 0,19). Tous les critères de
  clôture sont satisfaits : **P1 close**. Réserve : écart significatif sur les minimales seules (+0,099,
  p = 0,002), compensé sur la moyenne. Mise en garde automatique ajoutée aux indicateurs TN. La règle de
  confiance n'est pas modifiée.
