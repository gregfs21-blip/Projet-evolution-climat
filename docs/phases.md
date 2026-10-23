# Phases du projet

Chaque phase suit la même boucle : ETL → JSON → page → validation contre des valeurs publiées.
Une phase n'est close que lorsque les écarts avec les références sont expliqués.

| Phase | Contenu | Validation | État |
|---|---|---|---|
| P0 | Socle : arborescence, schéma, ETL, site, CI, workflow mensuel | Un indicateur factice traverse la chaîne jusqu'au site déployé | **close le 22/10/2026** |
| P1 | Températures Gironde : LSH TX/TN Mérignac + stations longues, anomalies 1961-1990 et 1991-2020, tendances Hamed-Rao, ruptures | Critères C1-C9 ci-dessous (C4 → C4bis) | **close le 23/10/2026** |
| P2 | Extrêmes et eau Gironde. **P2a** : extrêmes de température ; **P2b** : pluie, insolation, SPEI | P2a : critères E1-E10 fixés le 23/10/2026 (E4 : références en attente) | P2a en cours |
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

## P2a — Critères de clôture (fixés le 23/10/2026, avant tout calcul)

> **Décisions de Grég du 23/10/2026**, avant tout calcul : D-A découpage P2a puis P2b ; D-B méthode C
> (B en résultat principal, A en contrôle) ; D-C références R3/R4 à confirmer par Grég sur ClimatHD ;
> D-D critères E1-E10 validés tels quels.
>
> **E4 n'est pas encore fixé** : ses fourchettes seront commitées dès que Grég aura relevé les valeurs
> ClimatHD. D'ici là, **aucun indicateur P2a n'est calculé sur les données réelles** (entrées du registre
> désactivées), pour que la référence ne puisse pas être choisie après coup.

### Constat de la sonde (`docs/sonde-p2.md`, 23/10/2026)

- **Quotidien** (Licence Ouverte 2.0) : les 7 postes LSH de P1 ont des séries quotidiennes TN, TX, RR longues
  (Mérignac 1946-2025, Sauternes 1897-2025, Paulin 1953-2025…). Lacanau a des trous (1998, 2002, 2018).
  Les données quotidiennes **ne sont pas homogénéisées**. Code qualité 9 fréquent à certains postes
  (Villenave 34 %, Cap-Ferret 18 %, Paulin 8 %) : signification exacte à confirmer dans la notice Météo-France.
- **Précipitations homogénéisées (LSH RR)** : 9 séries en Gironde, homogénéisées de 1950/1953 à **2017**
  seulement (brut ensuite). Mérignac et Villenave n'en ont pas.
- **Insolation homogénéisée (LSH IN)** : **Mérignac seul**, 1931-**2014**. Le quotidien INST existe à Mérignac
  (jusqu'en 2025), Cap-Ferret et Cazaux (jusqu'en 2017), mais les capteurs d'insolation ont changé au fil
  des décennies : rupture instrumentale probable, non corrigée.

### Découpage (décision D-A : retenu)

- **P2a — Extrêmes de température** (7 postes de P1) : journées estivales TX ≥ 25 °C, chaudes TX ≥ 30 °C,
  très chaudes TX ≥ 35 °C, nuits tropicales TN ≥ 20 °C, jours de gel TN ≤ 0 °C. Réutilise toute
  l'infrastructure de P1 (stations, homogénéisation, validation).
- **P2b — Eau et soleil** : cumuls de précipitations (LSH RR), extrêmes de pluie (quotidien), insolation,
  SPEI (bilan RR − ETP Hargreaves, postes ayant TN, TX et RR homogénéisés : Paulin, Cap-Ferret, Cazaux,
  1962-2017). Critères fixés après la clôture de P2a.

### Le problème central de P2a : le quotidien n'est pas homogénéisé (décision D-B : méthode C retenue)

Un déplacement de station ou un changement d'abri décale toutes les températures d'une station : un
décalage de quelques dixièmes change sensiblement le nombre de jours au-dessus d'un seuil. Météo-France a
corrigé ces ruptures au pas mensuel (LSH), pas au pas quotidien. Trois méthodes possibles :

- **A. Brut, après la dernière rupture** : séries quotidiennes brutes, tendances calculées seulement après
  la dernière rupture d'homogénéité connue de la station (dates publiées dans les LSH). Aucune correction,
  mais des périodes plus courtes (souvent 1990-2022).
- **B. Brut corrigé par le décalage mensuel LSH** : chaque jour reçoit la correction de son mois,
  LSH homogénéisé − moyenne mensuelle brute. Périodes complètes ; corrige la moyenne mais pas la forme de
  la distribution (les queues peuvent rester biaisées).
- **C. B en résultat principal, A en contrôle** (recommandé) : la conclusion n'est publiée que si A et B
  concordent (critère E7).

### Références externes (décision D-C : confirmation par Grég sur ClimatHD)

Recueillies **de seconde main** (diagnostic de vulnérabilité du PNR Périgord-Limousin, oct. 2025, p. 28,
citant ClimatHD) pour la Nouvelle-Aquitaine, 1961-2018 :
- **R3** journées chaudes (TX > 25 °C) : +6 à +8 jours par décennie (zones intérieures) ;
- **R4** jours de gel : −1 à −2 jours par décennie.
Ces valeurs doivent être **confirmées sur ClimatHD lui-même** (définitions exactes, zone, période) avant
d'être commitées comme références. Faute de confirmation, E4 devient un critère d'information.

### Critères (décision D-D : validés tels quels, E4 en attente de ses références)

| # | Critère | Seuil proposé |
|---|---|---|
| E1 | Exhaustivité | 7 postes × 5 indices traités ; toute exclusion justifiée par écrit |
| E2 | Complétude (règle ETCCDI) | Un mois est manquant s'il lui manque plus de 3 jours ; une année est manquante si un de ses mois l'est. Aucune valeur complétée |
| E3 | Brut ≠ homogénéisé | Les années non corrigeables (après 2022, ou hors période homogénéisée LSH) sont affichées « brutes » et exclues des tendances et normales (comme C2) |
| E4 | Validation externe (R3, R4) | Composite Gironde 1961-2018 : TX > 25 °C dans [+6 ; +8] j/déc., gel dans [−2 ; −1] j/déc. (fourchettes publiées, sous réserve de confirmation) |
| E5 | Cohérence du correctif | Méthode B : la série corrigée reproduit la moyenne annuelle LSH à 0,05 °C près chaque année (contrôle automatique du calcul) |
| E6 | Cohérence inter-stations | Même signe de tendance à toutes les stations pour TX ≥ 25 °C et pour le gel ; tout signe opposé expliqué |
| E7 | Robustesse méthode | A et B : même signe et intervalles de confiance qui se recouvrent, pour chaque station et chaque indice |
| E8 | Robustesse qualité | Conclusions inchangées en excluant les valeurs de code qualité 9 |
| E9 | Indices rares | Si la médiane annuelle 1961-1990 est inférieure à 5 jours (ex. TX ≥ 35 °C, nuits tropicales sur le littoral), la pente de Sen n'est pas mise en avant : on publie l'écart entre normales 1961-1990 et 1991-2020, avec un test ; confiance au plus « moyenne » |
| E10 | Technique | Tests et CI verts, contrat v1.2, vocabulaire des variables complété, pages déployées |

**Règle de confiance** (analogue à C7) : « élevée » seulement si Hamed-Rao significatif, E4 et E7
satisfaits, et indice non rare (E9).

**Règle de clôture** : identique à P1 (critères satisfaits, ou chaque échec expliqué dans
`docs/validation-p2.md` et accepté par Grég).

### Affichage (à prévoir)

Pour le gel, une baisse traduit un réchauffement : la légende de l'échelle de couleur (bleu = baisse) devra
le dire. Unité de tendance « jours/décennie » à ajouter à `web/lib/heat.ts` avec sa propre saturation.

## Journal ergonomie (entre P1 et P2)

- 23/10/2026 : refonte de l'affichage, sans changement de calcul ni de contrat des indicateurs (v1.1).
  - Page d'échelle : constat calculé (aucun texte rédigé à la main), chiffres-clés des composites,
    stations superposées, matrice lieux × variables sur la période commune, carte avec sélecteur TN/TM/TX.
  - **Correction de la carte** : la couleur était normalisée entre le minimum et le maximum observés
    (0,343 en bleu, 0,361 en rouge pour un écart très inférieur à l'IC). Échelle désormais absolue et
    fixe (`web/lib/heat.ts`, ±0,5 °C/déc.), commune à la carte et à la matrice.
  - Page indicateur : bandeau tendance / cumul / normales, navigation entre lieux et variables, bascule
    anomalie ↔ valeur absolue, superposition du composite, justification du niveau de confiance calculée
    depuis le JSON, détail technique replié, export CSV et JSON.
  - Menu : rubriques sans contenu grisées avec leur phase.
  - `etl.validation.p1` publie aussi `data/processed/validation-p1.json` (schéma `ValidationReport` 1.0,
    contrôlé par `etl.validate`), affiché tel quel par le site. Il liste les indicateurs qu'il couvre.
- Dette assumée : la variable et le lieu sont lus dans l'identifiant (`tn-annuelle-<lieu>`). Un indicateur
  hors de ce motif reste listé normalement. À faire en P2 : ajouter `variable` et `place` au contrat.

## Journal contrat v1.2 (23/10/2026)

- Contrat 1.2 : `variable` (vocabulaire `etl/config/variables.yaml`) et `place` explicites dans chaque
  indicateur et dans le manifeste. Le site ne lit plus la variable dans l'identifiant ; familles par thème.
- Données régénérées : contenu identique à la v1.1 pour les 20 indicateurs, hors champs ajoutés (vérifié).
- Validation P1 restreinte explicitement à son périmètre (TN, TM, TX).
- Sonde P2 exécutée dans GitHub Actions (`.github/workflows/sonde.yml`), rapport `docs/sonde-p2.md`.

## Journal P2a

- 23/10/2026 : code de P2a écrit et testé sur données **synthétiques** uniquement (`etl/tests/test_extremes.py`) :
  source quotidienne (`etl/sources/meteofrance_quot.py`), indicateurs (`etl/indicators/extremes.py`, méthodes B et
  A, règle ETCCDI, indices rares), validation E1-E9 (`etl/validation/p2a.py`, rapport `validation-p2a.json`).
- Les 34 indicateurs P2a sont déclarés **désactivés** dans le registre : aucun calcul sur données réelles avant
  que les références de E4 soient commitées.
- Exclusions prévues (E1) : indices TX à Lacanau et Sauternes (pas de série LSH TX : ni correction B, ni dates de
  ruptures pour le contrôle A).
- Règle ajoutée à l'implémentation, dans l'esprit de C2 : une normale n'est calculée que si toutes ses années sont
  complètes et corrigées ; un indice rare sans normales complètes n'a pas d'écart publiable et reste « non établi ».
- Composite P2a : réseau constant sur 1961-2022 (couvre E4 1961-2018 et les deux normales), au moins 3 stations.
- Contrat 1.3 : `headline` (« trend » ou « normals ») et `normals_comparison`, pour que le site mette en avant
  l'écart entre normales d'un indice rare (E9) sans le deviner.
