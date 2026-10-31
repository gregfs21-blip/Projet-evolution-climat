# Phases du projet

Chaque phase suit la même boucle : ETL → JSON → page → validation contre des valeurs publiées.
Une phase n'est close que lorsque les écarts avec les références sont expliqués.

| Phase | Contenu | Validation | État |
|---|---|---|---|
| P0 | Socle : arborescence, schéma, ETL, site, CI, workflow mensuel | Un indicateur factice traverse la chaîne jusqu'au site déployé | **close le 22/10/2026** |
| P1 | Températures Gironde : LSH TX/TN Mérignac + stations longues, anomalies 1961-1990 et 1991-2020, tendances Hamed-Rao, ruptures | Critères C1-C9 ci-dessous (C4 → C4bis) | **close le 23/10/2026** |
| P2 | Extrêmes et eau Gironde. **P2a** : extrêmes de température ; **P2b** : pluie, insolation, SPEI | P2a : critères E1-E10 fixés le 23/10/2026, références E4 fixées le même jour avant calcul ; P2b : critères F1-F11 validés le 26/10/2026 (R7 en attente de ClimatHD) | P2a close (écarts E4 littoral, E7, E8 acceptés) ; P2b close (F4, F6 acceptés) |
| P3 | Atmosphère et littoral Gironde : vent, humidité, pression (ERA5), SST golfe de Gascogne, niveau marin | critères H1-H8 validés le 27/10/2026 | **close le 28/10/2026** (écart H5 humidité accepté) |
| P4 | Impacts Gironde : vendanges, danger météo incendie, CatNat (avec avertissement exposition/déclarations) | critères I1-I9 validés le 28/10/2026 | **close le 29/10/2026** (écart I4 accepté) |
| P5 | France : indicateur thermique national (LSH), cartes de tendances, extension P2-P4 | critères J1-J8 validés le 29/10/2026 | **close le 29/10/2026** (carte et extrêmes quotidiens hors P5) |
| P6 | Monde : GES, températures croisées, océans, niveau marin, cryosphère, ozone, ENSO, EEI (CERES), puits de carbone | critères K1-K8 validés le 31/10/2026 | **close le 31/10/2026** |
| P7 | Exploratoire : jet stream, Z500, blocages (CDS), proxy foudre — statut « signal non établi » | critères L1-L5 proposés le 31/10/2026 | en cours |
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
> **E4 fixé le 23/10/2026 (décision de Grég), avant tout calcul sur données réelles.** ClimatHD n'étant pas
> lisible hors navigateur, la référence repose sur deux sources concordantes citant les données Météo-France
> (voir « Références externes »). Les indicateurs P2a ne sont activés qu'à partir de ce commit.

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
**Fixation du 23/10/2026 (Grég), avant tout calcul.** Seconde source, concordante et plus détaillée :
CNPF Nouvelle-Aquitaine, « Le changement climatique et la forêt en Nouvelle-Aquitaine », brochure 2023, p. 5-6,
« d'après les données de Météo France », période **1960-2010** : journées chaudes (TX > 25 °C) **+4 à +5 j/déc.
sur la côte**, **+6 à +8 j/déc. à l'intérieur** ; gelées **−1 à −2 j/déc.** E4 devient donc :

| Référence | Définition | Postes | Période | Fourchette (j/déc.) |
|---|---|---|---|---|
| R3 littoral | TX > 25 °C (strict) | Cap-Ferret, Cazaux | 1961-2010 | [+4 ; +5] |
| R3 intérieur | TX > 25 °C (strict) | Bordeaux-Mérignac, Villenave-d'Ornon | 1961-2010 | [+6 ; +8] |
| R4 | TN ≤ 0 °C | composite TN à réseau constant | 1961-2010 | [−2 ; −1] |

Fourchettes publiées prises telles quelles (pas d'élargissement), comme C3 en P1. Limites : sources de seconde
main ; le seuil des « gelées » n'est pas précisé (TN ≤ 0 °C, convention Météo-France, retenue) ; Bordeaux-Paulin
(TX depuis 1962, centre urbain) n'entre pas dans le groupe « intérieur ».

### Critères (décision D-D : validés tels quels, E4 en attente de ses références)

| # | Critère | Seuil proposé |
|---|---|---|
| E1 | Exhaustivité | 7 postes × 5 indices traités ; toute exclusion justifiée par écrit |
| E2 | Complétude (règle ETCCDI) | Un mois est manquant s'il lui manque plus de 3 jours ; une année est manquante si un de ses mois l'est. Aucune valeur complétée |
| E3 | Brut ≠ homogénéisé | Les années non corrigeables (après 2022, ou hors période homogénéisée LSH) sont affichées « brutes » et exclues des tendances et normales (comme C2) |
| E4 | Validation externe (R3, R4) | Fixé le 23/10/2026, voir le tableau des références ci-dessus (1961-2010, littoral, intérieur, gel) |
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

## P2b — Critères de clôture (proposés et validés le 26/10/2026, avant tout calcul)

> **Décisions de Grég du 26/10/2026, avant tout calcul** : D-E périmètre et indices validés tels quels ; D-F
> correction multiplicative B′ avec contrôle A validée ; D-G référence R6 (ETP) acceptée avec sa limite de méthode,
> **R7 (pluies intenses) : Grég consulte ClimatHD** — aucun indice de pluie intense ne sera calculé avant que R7 soit
> fixée (ou abandonnée) et commitée ; D-H critère F8 appliqué à P2b et, en diagnostic, à P2a.
>
> **R7 abandonnée (Grég, 26/10/2026, avant tout calcul)** : ClimatHD n'affiche pour la région que le cumul annuel
> (captures de Sauternes, Pau-Uzein, Dax, Agen : pas d'indicateur de pluies fortes). Les indices de pluie intense
> n'ont donc pas de référence externe : confiance au plus « moyenne ». Les captures recoupent les cumuls annuels
> (Sauternes : moyenne glissante proche de 100 % de la normale sur 1959-2025), mais ces cumuls étant déjà calculés,
> ce recoupement n'a pas valeur de validation en aveugle. Déjà publiés hors P2b (méthode « largeur d'abord », non recalculés) :
> cumuls annuels de pluie (LSH RR, 9 postes et composite, référence « pas de tendance significative » fixée le
> 23/10/2026) et insolation de Mérignac (LSH IN, 1931-2014, sans référence).

### Précisions de mise en œuvre (26/10/2026, avant tout calcul d'indice)

Fixées en écrivant le code (`etl/indicators/pluie.py`, `etl/indicators/eau.py`), avant toute exécution :
- **B′ exige des mois complets** (tous les jours présents) : avec des jours absents, le rapport LSH ÷ brut
  attribuerait la pluie des jours manquants aux jours présents et fausserait les maxima. C'est plus strict que la
  règle ETCCDI de F2 ; une année complète au sens ETCCDI mais non entièrement corrigeable est affichée brute.
- **F1** : un poste est retenu s'il a au moins 30 années corrigeables ; composite à réseau constant sur 1961-2017
  (au moins 3 postes), sinon composite exclu avec motif. Les postes retenus sont lus dans une sonde de
  disponibilité (`docs/sonde-p2b.md`), qui ne calcule aucun indice.
- **F8** : écart du poste à la moyenne des autres postes retenus, années antérieures à sa dernière rupture LSH,
  au moins 15 années ; rupture « établie » si significative aussi après retrait de la tendance ; sans rupture LSH,
  « sans objet ».
- **F9** ne s'applique qu'aux indices de jours (R10mm, R20mm), comme E9. Conséquence assumée : la pluie n'étant
  homogénéisée que jusqu'en 2017, la normale 1991-2020 est toujours incomplète ; un indice rare n'a donc ni pente
  mise en avant ni écart entre normales : « non établi ».
- **Mois secs (SPEI-3 ≤ −1)** : compte de mois, hors F9 ; tendance calculée normalement.
- **Loi du SPEI** : log-logistique à 3 paramètres dans la forme de Hosking (logistique généralisée), ajustée par
  L-moments non biaisés, comme le recommandent Beguería et al. (2014) ; la paramétrisation d'origine de
  Vicente-Serrano (2010) dégénère pour des bilans peu asymétriques (constaté sur données synthétiques).
- **SPEI** : calé et calculé sur les seuls mois homogénéisés (pluie et températures) ; un mois manquant interrompt
  les cumuls de 3 ou 12 mois (aucune valeur complétée).

### Périmètre

- **Pluies intenses** (indices ETCCDI, données quotidiennes) : jours de pluie ≥ 10 mm (R10mm), jours ≥ 20 mm
  (R20mm), cumul maximal en 1 jour (RX1day) et en 5 jours consécutifs (RX5day). Postes : ceux des 9 séries LSH RR
  qui ont aussi un quotidien RR couvrant leur période homogénéisée (attendus d'après `docs/sonde-p2.md` :
  Bordeaux-Paulin, Lacanau, Cap-Ferret, Sauternes, Cazaux, Captieux ; Hourtin, Belin-Béliet et Saint-Symphorien
  à vérifier, le quotidien semblant plus court ou porté par un autre numéro de poste) ; composite à réseau constant.
- **Demande en eau et sécheresse** (données mensuelles LSH, toutes homogénéisées) : ETP de Hargreaves (TN, TX),
  bilan climatique P − ETP, SPEI à 3 et 12 mois. Postes ayant TN, TX et RR homogénéisés : Bordeaux-Paulin,
  Cap-Ferret, Cazaux, 1962-2017 (fin de l'homogénéisation RR).
- **Contrôle de la correction sur la période ancienne** (dette de P2a) : appliqué aux nouveaux indices ET, à titre
  de diagnostic, aux 5 indices de température de P2a (en particulier l'écart E4 littoral).

### Méthodes proposées

- **Correction du quotidien de pluie (méthode B′, multiplicative)** : chaque jour d'un mois est multiplié par
  LSH homogénéisé ÷ cumul brut du mois. Un mois sans pluie brute mais avec un cumul LSH positif (ou l'inverse) n'est
  pas corrigeable : il est compté manquant. Contrôle A : brut après la dernière rupture LSH RR du poste. Résultat
  principal B′, publié seulement si A et B′ concordent (même règle que la méthode C de P2a).
- **ETP de Hargreaves** (FAO-56, éq. 52) au pas mensuel : 0,0023 × Ra × (TM + 17,8) × √(TX − TN), Ra calculé
  à partir de la latitude du poste et du jour médian du mois.
- **SPEI** (Vicente-Serrano et al., 2010) : P − ETP cumulé sur 3 et 12 mois, loi log-logistique ajustée par
  L-moments pour chaque mois calendaire sur 1962-2017. Indicateurs publiés : SPEI-12 de décembre (bilan de l'année)
  et nombre de mois par an où SPEI-3 ≤ −1 (mois secs).

### Références externes proposées (à fixer avant calcul)

| # | Énoncé publié | Source | Contrôle proposé |
|---|---|---|---|
| R5 | Cumul annuel : tendances « pas statistiquement significatives », « pas de tendance marquée, à la hausse ou à la baisse » en Nouvelle-Aquitaine (séries homogénéisées Météo-France, 1959-2019) | ORACLE Nouvelle-Aquitaine 2020, Chambres d'agriculture, p. 47 | Seconde source concordante avec la référence déjà fixée le 23/10/2026 pour les cumuls ; **aucun nouveau contrôle** (les cumuls sont déjà calculés : ajouter une référence après coup ne serait plus « en aveugle ») |
| R6 | ETP annuelle : + 24 mm par décennie en Gironde ; + 95 à + 183 mm en 60 ans selon les départements de Nouvelle-Aquitaine (chaîne SIM de Météo-France, 1959-2019) | ORACLE 2020, p. 61 | Pente de l'ETP de Hargreaves, 1962-2019, dans **[+16 ; +30] mm/déc.** (fourchette des départements). Limite : méthode différente (Hargreaves, température seule, contre Penman-Monteith dans SIM) |
| R7 | Pluies intenses en Gironde | **Aucune source trouvée** | Proposition : Grég consulte ClimatHD (Nouvelle-Aquitaine, « précipitations ») comme pour R3/R4 ; à défaut, pas de référence et confiance au plus « moyenne » |

### Critères proposés

| # | Critère | Seuil proposé |
|---|---|---|
| F1 | Exhaustivité | Tous les postes du périmètre × tous les indices ; toute exclusion justifiée par écrit (ex. quotidien trop court) |
| F2 | Complétude | Quotidien : règle ETCCDI de P2a (mois manquant au-delà de 3 jours absents) ; mensuel : une année exige ses 12 mois ; SPEI-12 exige 12 mois consécutifs. Aucune valeur complétée |
| F3 | Brut ≠ homogénéisé | Années après 2017 (fin de l'homogénéisation RR) affichées brutes, exclues des tendances et normales (règle C2) |
| F4 | Validation externe | R6 pour l'ETP ; R7 pour les pluies intenses si Grég la fixe ; sinon confiance au plus « moyenne » |
| F5 | Cohérence du correctif | Après B′, la somme des jours corrigés reproduit le cumul mensuel LSH à 0,5 mm près pour chaque mois corrigé (contrôle automatique) |
| F6 | Cohérence inter-stations | Même signe de tendance à tous les postes pour R10mm et pour l'ETP ; tout signe opposé expliqué |
| F7 | Robustesse méthode | A et B′ : même signe et intervalles de confiance qui se recouvrent, pour chaque poste et chaque indice de pluie |
| F8 | **Période ancienne (nouveau)** | Pour chaque poste et indice corrigé : test de Pettitt sur la série des écarts au composite des autres postes, avant la dernière rupture LSH. Aucune rupture établie (significative aussi après retrait de la tendance) ; sinon tendance limitée à la période postérieure et confiance au plus « moyenne ». Appliqué aussi, en diagnostic, aux indices de P2a |
| F9 | Indices rares | Même règle que E9 (médiane 1961-1990 < 5 → écart entre normales, confiance au plus « moyenne ») ; concerne probablement R20mm sur certains postes |
| F10 | Contrôle du SPEI | Sur 1962-2017, moyenne de chaque SPEI à ±0,05 et écart-type à ±0,1 de 0 et 1 (contrôle de l'ajustement) |
| F11 | Technique | Tests et CI verts, contrat à jour, vocabulaire complété, pages déployées |

**Règle de confiance proposée** : « élevée » seulement si Hamed-Rao significatif, référence externe satisfaite
(F4), F7 et F8 satisfaits, et indice non rare (F9). Sans référence fixée : au plus « moyenne ».

**Règle de clôture** : identique à P1 et P2a (critères satisfaits, ou chaque échec expliqué dans
`docs/validation-p2b.md` et accepté par Grég).

### Décisions demandées à Grég

- **D-E** : périmètre et indices (R10mm, R20mm, RX1day, RX5day ; ETP, P − ETP, SPEI-3 et SPEI-12).
- **D-F** : correction multiplicative B′ avec contrôle A (comme la méthode C de P2a).
- **D-G** : référence R6 (ETP, [+16 ; +30] mm/déc., méthode différente assumée) ; R7 : consultation de ClimatHD
  par Grég, ou absence de référence.
- **D-H** : critère F8, y compris en diagnostic sur P2a.

### Décisions de Grég du 26/10/2026, APRÈS le premier calcul P2b

Analyse : `docs/validation-p2b.md` et `docs/validation-p2a.md`.
- **F4** (ETP de Cap-Ferret +14,5 mm/déc. pour [+16 ; +30]) : écart expliqué par la formule de Hargreaves, accepté.
- **F6** (signes mélangés des jours ≥ 10 mm, aucune pente significative) : expliqué, accepté.
- **P2a, E4 R3 littoral** : F8 ne trouve aucun défaut de correction ; écart attribué à la référence, accepté. Un
  écart accepté clôt la phase mais ne relève pas la confiance (`external_validation_passed` exige une référence
  réellement retrouvée).
- **Règle nouvelle** : pas de pente pour un indice de pluie sur moins de 30 années consécutives corrigées (Lacanau).
- P2a et P2b closes.

## P3 — Critères (proposés et validés le 27/10/2026, avant tout calcul)

> **Décisions de Grég du 27/10/2026, avant tout calcul** : H5 validé tel quel (échec → confiance au plus
> « faible » ; succès insuffisant pour « élevée ») ; R8 fixée avec la fourchette **[+0,21 ; +0,31] °C/déc.**
> (± 20 %, source sans incertitude publiée), contrôlée sur une boîte « golfe entier » 1982-2014 ; niveau marin :
> **altimétrie satellite** (Copernicus, depuis 1993), après une sonde du jeu de données ; critères H1-H8 validés.
>
> Statut d'origine : proposition. Sondes : `docs/sonde-p3.md`, `docs/sonde-p3b.md`. Déjà publiés hors P3 (« largeur
> d'abord ») : pression, humidité, vent fort et rafale maximale ERA5 à Bordeaux ; rafales FXI (tendance indicative) ;
> marégraphe d'Arcachon (2002-2024, lacunaire : aucune tendance calculable).

### Constat des sondes

- **Mesures de station** (quotidien Météo-France « autres paramètres », bruts) : pression au niveau de la mer
  (PMERM) et humidité moyenne (UM) à Bordeaux-Mérignac et Cazaux sur 1950-2024 (75 ans), Cap-Ferret 1951-2019
  (pression). Rien d'homogénéisé.
- **Température de la mer** : le serveur ERDDAP de la NOAA est injoignable depuis GitHub. ERA5 « single levels »
  (Copernicus) fournit la SST mensuelle depuis 1940 : la requête 44-46° N, 3-1° O a abouti en quelques minutes.
- **Mouvements du sol** (GNSS, SONEL ULR7a) : Cap-Ferret 2005-2012 seulement, Royan 2007-2020, La Rochelle
  2000-2020. Positions quotidiennes, pas de vitesses publiées dans ce flux.
- **Marégraphes** : aucune série longue en Gironde (Arcachon 19 années, Le Verdon 6). Séries longues voisines :
  Saint-Nazaire 1965-2024, Boucau 1969-2024, La Rochelle (1942-2023, lacunaire).

### Périmètre proposé

- **A. Pression et humidité** : les séries ERA5 de Bordeaux restent l'indicateur ; les mesures de Mérignac et
  Cazaux servent de **contrôle croisé** (elles sont brutes, donc sans tendance propre, règle C2).
- **B. Vent** : rafales ERA5 inchangées ; corrélation interannuelle avec le vent moyen mesuré (FFM) en information.
- **C. Température de la mer** : SST ERA5, boîte côtière 44-46° N, 3-1° O (au large de la Gironde), 1940-2025.
- **D. Niveau marin** : trois options, voir les décisions.

### Références proposées

| # | Énoncé | Source | Contrôle proposé |
|---|---|---|---|
| R8 | Golfe de Gascogne : + 0,26 °C par décennie depuis 1982 (bassin entier), réchauffement plus fort au printemps et en automne ; refroidissement hivernal le long de la côte sous l'influence des panaches de la Loire et de la Gironde (2002-2014) | Thèse de X. Costoya, université de Vigo, 2016 ; Costoya et al., Journal of Marine Systems, 2015 (1982-2014) | Pente de la SST ERA5 sur une boîte « golfe entier » (43,5-48° N, 10-1° O, requête à ajouter), 1982-2014, dans une fourchette à décider |
| — | Pression, humidité | aucune référence publiée locale | confiance au plus « moyenne » |

### Critères proposés

| # | Critère | Seuil proposé |
|---|---|---|
| H1 | Exhaustivité | Tout le périmètre retenu ; exclusions justifiées |
| H2 | Complétude | Station : année de 12 mois, mois ETCCDI (au plus 3 jours absents) ; ERA5 : années complètes |
| H3 | Brut ≠ homogénéisé | Mesures de station sans tendance publiée (C2) ; elles ne servent qu'au contrôle H5 |
| H4 | Validation externe | R8 pour la SST ; sinon confiance au plus « moyenne » |
| H5 | **Contrôle croisé ERA5 − station** (pression, humidité) | Série annuelle des écarts ERA5 − Mérignac et ERA5 − Cazaux : pente non significative ET aucune rupture établie (Pettitt, aussi après retrait de tendance). Échec → confiance de l'indicateur ERA5 au plus « faible » |
| H6 | Cohérence entre stations | Les écarts ERA5 − station ont le même comportement à Mérignac et Cazaux ; sinon expliqué |
| H7 | Plausibilité | Valeurs annuelles dans des bornes fixées (pression 1005-1025 hPa, humidité 55-95 %, SST 10-20 °C) |
| H8 | Technique | Tests, CI, contrat, pages |

**Limite à assumer** : ERA5 assimile les pressions mesurées au sol, probablement celles de Mérignac. H5 détecte donc
un défaut grossier (rupture, dérive), mais ne constitue pas une validation indépendante. Il ne permet pas, à lui
seul, la confiance « élevée ».

### Relevés P3 (27/10/2026), contrôles avant activation, sans calcul de tendance

- SST au large de la Gironde (ERA5) : 1940-2025, 63 mailles de mer chaque mois, moyennes annuelles 14,3 à 17,1 °C.
- Altimétrie (C3S DT2024) : 1993-2025, 396 mois, 78 mailles chaque mois, moyennes annuelles −19 à + 132 mm. La
  requête d'un seul tenant dépassait la limite de coût du CDS : relevé par tranches de 4 ans, réunies sans trou.
- SST du golfe entier : relevée le 27/10 au soir (1940-2025, mailles de mer constantes) ; activée le 28/10.

### Décision de Grég du 28/10/2026, APRÈS calcul

Analyse : `docs/validation-p3.md`. Six critères conformes ; R8 retrouvée de justesse (+0,218 pour [+0,21 ; +0,31]).
- **H5 humidité** (dérive de l'écart ERA5 − Mérignac, +0,64 point/déc., p = 0,005 ; Cazaux 15 ans communs) : cause
  non tranchée (capteur ou ERA5), **écart accepté**. La règle H5 s'applique : humidité ERA5 au plus « faible »
  (elle était déjà en « signal non établi »).
- P3 close.

## P7 — Critères (proposition du 31/10/2026, avant tout calcul)

> Statut : **proposition**, à valider par Grég. Sonde : `docs/sonde-p7.md`. Déjà publiés hors P7 : jet stream
> (vitesse et latitude, ERA5, « signal non établi »), géopotentiel 500 hPa au-dessus de Bordeaux (ERA5 et
> radiosondages).

### Constat de la sonde

- **Z500 quotidien** (ERA5, statistiques quotidiennes) : disponible depuis 1940 ; un mois sur 30-85° N, 60° O-60° E
  à 2,5° traité en 6 minutes. Les 86 ans demandent des requêtes annuelles relevées sur plusieurs jours.
- **Foudre** : la densité d'éclairs du modèle **n'existe pas** dans les moyennes mensuelles ERA5 (requête rejetée) ;
  seule l'énergie potentielle de convection (CAPE) y figure. Aucune série ouverte d'impacts de foudre.

### Périmètre proposé

- **A. Blocages euro-atlantiques** : indice de Tibaldi et Molteni (1990) sur le Z500 quotidien ; jours bloqués par
  hiver (décembre-février) et par été (juin-août), secteur 30° O-30° E.
- **B. Z500 moyen Atlantique-Europe** (35-70° N, 30° O-30° E), moyenne annuelle, mêmes données.
- **C. Indicateur indirect d'orages en Gironde** : CAPE moyenne de juin à août (ERA5 mensuel). Faible : la CAPE dit
  l'instabilité possible, pas les orages ni les éclairs.

### Méthode proposée pour A (fixée avant calcul)

Z en mètres géopotentiels (z / 9,80665). Pour chaque longitude et chaque décalage Δ ∈ {−5° ; 0 ; +5°} :
φN = 80° + Δ, φ0 = 60° + Δ, φS = 40° + Δ ; GHGS = (Z(φ0) − Z(φS)) / (φ0 − φS), GHGN = (Z(φN) − Z(φ0)) / (φN − φ0).
Longitude bloquée si GHGS > 0 et GHGN < −10 m par degré, pour au moins un Δ. Jour bloqué dans le secteur si au moins
3 longitudes contiguës (7,5°) y sont bloquées ; épisode = au moins 5 jours bloqués consécutifs ; indicateur = jours
appartenant à un épisode, par saison.

### Références et confiance

Aucune référence chiffrée : la littérature ne retient pas de tendance robuste observée des blocages (Woollings et
al., 2018). Proposition : comme annoncé pour la P7, **confiance plafonnée à « signal non établi »** pour A et C
(exploratoires) ; B suit la règle ERA5 (au plus « moyenne »).

### Critères proposés

| # | Critère | Seuil proposé |
|---|---|---|
| L1 | Exhaustivité | Tout le périmètre retenu |
| L2 | Complétude | Saison retenue si tous ses jours (A) ou ses 3 mois (C) existent ; année complète (B) |
| L3 | Plausibilité climatologique | Hiver : la fréquence moyenne de blocage 1981-2010 est plus forte que l'été, et comprise entre 5 et 40 % des jours (repère des climatologies publiées) |
| L4 | Robustesse | Mêmes conclusions de signe avec un secteur décalé (20° O-40° E), en information |
| L5 | Technique | Tests, CI, contrat, pages |

### Décisions demandées à Grég

- **D-T** : périmètre (A à C).
- **D-U** : méthode de A telle que décrite.
- **D-V** : plafond « signal non établi » pour A et C.

## P6 — Critères (proposés et validés le 31/10/2026, avant tout calcul)

> **Décisions de Grég du 31/10/2026, avant tout calcul** : D-Q périmètre **A à G** (F et G après ses démarches :
> compte Earthdata, conditions de l'ADS ; leurs références seront fixées après la sonde d'accès, avant calcul) ;
> D-R niveau marin **NOAA STAR jusqu'en 2025** (sans correction isostatique, limite assumée) ; D-S R12 avec la
> fourchette **[−0,0023 ; −0,0015] pH/an** (± 20 %) ; **critères K1-K8 validés**.
>
> Statut d'origine : proposition. Sonde : `docs/sonde-p6.md`. Déjà publiés pour le monde hors P6
> (« largeur d'abord ») : températures de surface (HadCRUT5, GISTEMP, Berkeley), SST (NOAA, HadSST), CO₂, CH₄, N₂O,
> chaleur de l'océan 0-700 et 0-2000 m, banquise, ONI, ouragans et ACE, jet stream (ERA5).

### Constat de la sonde

- **Niveau marin mondial** : NOAA STAR (TOPEX/Jason/Sentinel-6, annuel retiré, **sans correction isostatique**,
  1992-2025, tendance du fichier 3,11 mm/an) ; Université du Colorado (correction isostatique appliquée, s'arrête en
  2023) ; CSIRO (s'arrête en 2015).
- **Acidification** : station HOT (Hawaï), 355 campagnes 1988-2024, pH in situ calculé et mesuré.
- **Ozone** : NASA Ozone Watch, surface moyenne du trou (7 sept.-13 oct.) et ozone minimal, 1979-2025 (1995 absent).
- **Puits de carbone** : Global Carbon Budget 2025 (puits océanique et terrestre, 1959-2024, GtC/an), en CSV via
  openclimatedata (le site officiel renvoie 404, ICOS demande l'acceptation d'une licence dans un navigateur).
- **Troposphère** : satellites UAH 6.1 et RSS 4.0, anomalies mensuelles globales 1979-2026.
- **Déséquilibre énergétique (CERES)** : **accès refusé sans compte NASA Earthdata** (gratuit).
- **Aérosols (CAMS EAC4, 2003-2025)** : **conditions de l'Atmosphere Data Store non acceptées** sur le compte.

### Périmètre proposé

- **A. Niveau marin mondial** (altimétrie).
- **B. Acidification** : pH de surface à HOT, moyenne annuelle des campagnes.
- **C. Ozone** : surface du trou d'ozone antarctique (affichée en deux périodes : 1979-2000 creusement, depuis 2000
  début de résorption attendue).
- **D. Puits de carbone** : puits océanique, puits terrestre, et part des émissions absorbée par les deux.
- **E. Troposphère** : UAH et RSS, moyenne annuelle ; contrôle croisé avec la surface.
- **F. Déséquilibre énergétique** (CERES, 2000-) : seulement si Grég crée un compte Earthdata.
- **G. Aérosols** (CAMS, 2003-) : seulement si Grég accepte les conditions de l'ADS.

### Références proposées

| # | Énoncé | Source | Contrôle proposé |
|---|---|---|---|
| R11 | Niveau marin mondial : + 3,7 [3,2 à 4,2] mm/an sur 2006-2018 | GIEC AR6, GT1, résumé A.1.7 | Pente annuelle 2006-2018 dans **[3,2 ; 4,2] mm/an** ; limite : NOAA STAR sans correction isostatique (− 0,2 à − 0,5 mm/an) |
| R12 | Station ALOHA (HOT) : pH de surface − 0,0019 ± 0,0002 par an (environ 20 ans depuis 1988) | Dore et al., PNAS 106, 2009 | Pente du pH in situ annuel sur 1989-2007 dans **[−0,0023 ; −0,0015] par an** |
| — | Ozone, puits, troposphère | aucune référence retenue (puits : la source est la référence elle-même) | confiance au plus « moyenne » |

### Critères proposés

| # | Critère | Seuil proposé |
|---|---|---|
| K1 | Exhaustivité | Tout le périmètre retenu ; exclusions justifiées |
| K2 | Complétude | Année retenue si complète selon la règle propre à chaque série (12 mois ; HOT : au moins 6 campagnes dans l'année) |
| K3 | Produits publiés | Séries reprises sans modification, unités contrôlées (C2 : pas de série brute de station) |
| K4 | Validation externe | R11, R12 ; sinon confiance au plus « moyenne » |
| K5 | **Contrôle croisé surface / troposphère (nouveau)** | Corrélation interannuelle entre la température de surface HadCRUT5 et chaque série TLT, 1979-2025 : r ≥ 0,8 |
| K6 | Cohérence entre produits | UAH et RSS : même signe de pente ; écart publié en information |
| K7 | Plausibilité | Bornes fixées par série (niveau marin ± 200 mm, pH 7,9-8,2, trou d'ozone 0-35 millions de km², puits 0-6 GtC/an, TLT ± 2 °C) |
| K8 | Technique | Tests, CI, contrat, pages |

### Choix de mise en œuvre fixés AVANT le premier calcul (31/10/2026, A à E ; `etl/sources/globaux.py`, `etl/indicators/monde.py`)

- **Niveau marin** (NOAA STAR, TOPEX/Jason/Sentinel-6, annuel retiré) : valeur d'une ligne = première mission
  renseignée ; moyenne de l'année civile, retenue si chaque mois a au moins une valeur (1993-2025).
- **pH (HOT)** : pH in situ calculé (`pHcalc_insitu`, complet depuis 1988 ; le pH mesuré manque avant 1992) ; −999 =
  absent ; moyenne annuelle des campagnes, année retenue si au moins 6 campagnes.
- **Trou d'ozone** : surface moyenne 7 sept.-13 oct. ; tendance mise en avant sur **2000-2025** (après le maximum des
  substances destructrices, période de la résorption attendue), tendance 1979-1994 publiée à côté (1995 manque).
- **Puits de carbone** (GCB 2025) : première colonne de valeurs de chaque fichier (estimation GCB), contrôlée par son
  en-tête ; **part absorbée** = (puits océanique + puits terrestre) / (émissions fossiles + changement d'usage des
  sols), en %.
- **Troposphère** : UAH 6.1 colonne « Globe », RSS 4.0 « Global » ; moyenne des 12 mois ; anomalies telles que
  publiées (références de période différentes : comparer les pentes, pas les niveaux). K5 : HadCRUT5 annuel.

### F et G : accès et choix fixés AVANT le premier calcul (31/10/2026)

Sondes : `docs/sonde-p6c.md` (CAMS : requête de janvier 2020 aboutie en 31 s, variable `aod550`, grille 0,75°),
`docs/sonde-p6d.md` (CERES : OPeNDAP refusé depuis GitHub ; fichier EBAF-TOA Ed4.2.1 de 900 Mo accessible par le
catalogue CMR avec le jeton Earthdata). **Décision de Grég : aucune référence pour F et G** (confiance au plus
« moyenne ») ; Loeb et al. 2021 (+0,50 ± 0,47 W/m² par décennie, mi-2005 à mi-2019) calculé sur les mêmes données
CERES : affiché en information seulement.

- **F, déséquilibre énergétique** (`etl/sources/ceres.py`) : CERES EBAF-TOA Edition 4.2.1, variable du flux net
  global moyen au sommet de l'atmosphère, toutes conditions de ciel (`gtoa_net_all_mon`, W/m²) ; moyenne des 12 mois
  (années complètes 2001-2025). Fichier retéléchargé seulement quand le granule change.
- **G, aérosols** (`etl/sources/ads_aod.py`) : CAMS EAC4 mensuel, épaisseur optique totale à 550 nm (`aod550`),
  moyenne mondiale pondérée par le cosinus de la latitude, puis moyenne des 12 mois (2003-2025).

### Décisions demandées à Grég

- **D-Q** : périmètre (A à G).
- **D-R** : source du niveau marin (NOAA STAR jusqu'en 2025 sans correction isostatique, ou Colorado avec correction
  jusqu'en 2023).
- **D-S** : fourchette de R12.
- **Actions** : compte Earthdata (F) et conditions de l'ADS (G), si retenus.

## P5 bis — Carte départementale des tendances (demande de Grég du 30/10/2026, choix fixés AVANT calcul)

Grég a vu les résultats nationaux de la P5 ; les tendances départementales n'ont jamais été calculées ni affichées.
Décisions de Grég : **tendance 1959-2021** en °C par décennie ; **TN, TM, TX** avec sélecteur. Choix de mise en
œuvre (`etl/carte.py`) :

- **Données** : les anomalies de station de la P5 (réseau constant 220 stations, 1959-2021) ; série d'un département =
  moyenne des anomalies de ses stations ; pente de Sen et test de Mann-Kendall corrigé Hamed-Rao, comme partout.
- **Département** : deux premiers chiffres du poste (zéro rétabli) ; la Corse (« 20 ») colore 2A et 2B à l'identique.
  Département sans station au réseau : **gris, aucune valeur** (rien n'est interpolé). Le nombre de stations est affiché.
- **Couleurs** : échelle absolue et fixe du site (± 0,5 °C/déc., `web/lib/heat.ts`) ; tendance non significative
  (p ≥ 0,05) en **teinte pâle**.
- **Contours** : contours administratifs Etalab (dérivés d'Admin Express, IGN), millésime 2025, généralisés à
  1 000 m, Licence Ouverte (`docs/sonde-p5b.md`) ; métropole seulement.
- **Aucune référence par département** : la carte ne porte pas de niveau de confiance « élevée » ; pas de nouveau
  critère de clôture (P5 close). Contrôle publié en information : moyenne des pentes départementales comparée à la
  pente France.

### Carte départementale de la pluie (demande de Grég du 30/10/2026, choix fixés AVANT calcul)

Décisions de Grég : tendance en **% par décennie** (relative à la moyenne 1961-1990 du département) ; **année et
quatre saisons** avec sélecteur. Choix de mise en œuvre (`etl/carte.py`) :

- **Réseau** : celui de la pluie France de la P5 (RR homogénéisé sur les 12 mois de chaque année 1961-2014).
- **Saisons** : hiver = décembre de l'année précédente à février (hivers 1962-2014), printemps = mars-mai, été =
  juin-août, automne = septembre-novembre ; année = janvier-décembre (1961-2014). Cumul de chaque station.
- **Département** : moyenne des cumuls de ses stations ; pente de Sen (mm/déc.) divisée par la moyenne 1961-1990 du
  département, × 100 ; significativité : Mann-Kendall corrigé Hamed-Rao sur la série en mm.
- **France** (repère sous la carte) : moyenne des départements, même calcul.
- **Couleurs** : échelle fixe **± 10 % par décennie**, bleu = plus de pluie, brun = moins ; pâle si non significatif ;
  gris sans station. Même contours que la carte des températures.
- **Premier calcul (30/10/2026)** : 95 départements ; pentes significatives : 4 (année), 4 (hiver), 0 (printemps),
  6 (été), 1 (automne), soit 15 sur 475 tests, **moins que les ~24 attendus par le seul hasard** au seuil de 5 %.
  Aucune tendance départementale robuste de la pluie sur 1961-2014. Mise en garde « tests multiples » ajoutée aux
  limites après ce calcul (lecture seulement, aucune valeur modifiée).

## P5 — Critères (proposés et validés le 29/10/2026, avant tout calcul)

> **Décisions de Grég du 29/10/2026, avant tout calcul** : D-M périmètre **A et C** (températures et pluie de la
> France ; carte des tendances B écartée ; D hors P5) ; D-N réseau constant **1959-2021** ; D-O pondération **par
> département** ; D-P R10 avec la fourchette publiée **[+0,2 ; +0,4] °C/déc.** ; **critères J1-J8 validés**, J5
> calculé en contrôle interne (pentes par station jamais publiées, la carte étant écartée).
>
> Statut d'origine : proposition. Sonde : `docs/sonde-p5.md` (inventaire seulement, aucune valeur de
> température lue). Déjà publiés pour la France hors P5 : CatNat (tous périls, sécheresse), marégraphe de Brest.

### Constat de la sonde

- **Les LSH ne commencent qu'en 1953-1959** pour presque toutes les séries : l'indicateur thermique national depuis
  1900 de Météo-France (30 stations, séries anciennes) **ne peut pas être reproduit** avec ce produit.
- **Températures** : 294 séries TN, 321 TX, 255 postes avec les deux ; homogénéisées jusqu'en 2022 ou 2023 pour la
  plupart. Réseau constant TN et TX : 220 stations sur 1959-2021, 226 sur 1961-2022.
- **Pluie** : 1 279 séries, homogénéisées jusqu'en 2014-2021 ; réseau constant 300 stations sur 1961-2020.
- **Insolation** : 27 séries, toutes arrêtées en 2014.
- Défaut de la sonde : les postes des départements 01 à 09 sont comptés sous un mauvais numéro (zéro initial absent) ;
  la liste « départements sans série » est fausse pour eux, les comptages de stations sont justes.

### Périmètre proposé

- **A. Températures de la France** : composites TN, TM, TX à réseau constant, en **anomalies** par rapport à 1961-1990
  (les stations de montagne ne pèsent pas sur le niveau) ; années dont les 12 mois sont homogénéisés pour toutes les
  stations du réseau.
- **B. Carte des tendances** : une tendance TM par station du réseau constant (indicateurs de station, échelle France).
- **C. Pluie de la France** : composite du cumul annuel, réseau constant 1961-2020.
- **D. Extension des P2-P4** (extrêmes quotidiens, Huglin, canicule) : demande le quotidien des 96 départements
  (plusieurs Go) ; proposée **hors P5**, à traiter à part.

### Références proposées

| # | Énoncé | Source | Contrôle proposé |
|---|---|---|---|
| R10 | Température moyenne annuelle, séries homogénéisées de métropole, 1959-2021 : environ + 0,3 °C par décennie, entre + 0,2 et + 0,4 selon les séries | ONERC / Météo-France, indicateur « température de l'air en France métropolitaine » | Pente du composite TM sur 1959-2021 dans **[+0,2 ; +0,4] °C/déc.** (fourchette publiée) |
| — | + 1,9 °C en 2015-2024 par rapport à 1961-1990 (indicateur thermique national) | ONERC / Météo-France | non contrôlable : LSH homogénéisées jusqu'en 2022 ; information |
| — | Pluie annuelle nationale | aucune tendance publiée | confiance au plus « moyenne » |

### Critères proposés

| # | Critère | Seuil proposé |
|---|---|---|
| J1 | Exhaustivité | Tout le périmètre retenu ; exclusions justifiées |
| J2 | Complétude | Année de station = 12 mois homogénéisés ; réseau constant sur toute la période du composite |
| J3 | Brut ≠ homogénéisé | Aucune année non homogénéisée dans tendances, normales, références (C2) |
| J4 | Validation externe | R10 pour le composite TM ; sinon confiance au plus « moyenne » |
| J5 | Cohérence spatiale | Au moins 95 % des stations de la carte avec une pente TM positive ; toute pente négative expliquée |
| J6 | Robustesse de la pondération | Pente du composite TM pondéré par département et pente de la moyenne simple des stations : écart ≤ 0,05 °C/déc. |
| J7 | Plausibilité | TM annuel de station entre −10 et + 20 °C ; cumul de pluie entre 300 et 3 000 mm (bornes portées à 100 et 5 000 mm le 29/10/2026, après calcul) |
| J8 | Technique | Tests, CI, contrat, pages |

### Choix de mise en œuvre fixés AVANT le premier calcul (29/10/2026, `etl/indicators/france.py`)

- **Réseau des températures** : postes dont TN et TX sont homogénéisés sur les 12 mois de chaque année 1959-2021 ; le
  même réseau sert à TN, TM et TX ; TM = (TN + TX) / 2 au pas mensuel.
- **Anomalie de station** : moyenne annuelle des 12 mois, moins sa moyenne 1961-1990.
- **Département** : deux premiers chiffres du numéro de poste sur 8 chiffres (zéro initial rétabli ; Corse = « 20 »).
  Moyenne des anomalies des stations du département, puis moyenne des départements.
- **Années publiées** : celles où toutes les stations du réseau ont leurs 12 mois ; homogénéisées (tendance, normales,
  R10) si toutes le sont. Série de 63 ans : tendance sur toute la période homogénéisée.
- **Pluie** : postes dont RR est homogénéisé sur les 12 mois de chaque année 1961-2020 ; cumul annuel en mm, moyenne
  par département puis moyenne des départements (pas d'anomalie : réseau constant).
- **J5** : pente de Sen de l'anomalie TM de chaque station du réseau sur 1959-2021. **J6** : même composite TM sans
  pondération (moyenne simple des stations), pente sur 1959-2021.

### Décision de Grég APRÈS le premier calcul (29/10/2026)

- **J7, pluie** : le plancher de 300 mm bloquait la publication (poste 13001009, Bouches-du-Rhône : 252 mm en 1967,
  299 mm en 1989, années sèches crédibles). Le seuil sert à détecter une erreur d'unité ; **plancher abaissé à
  100 mm** par Grég. Décision postérieure au calcul, tracée comme telle ; les températures avaient passé leurs bornes.
- **J7, pluie (bis)** : le plafond de 3 000 mm bloquait ensuite (poste 48036001, Lozère : 3 273 mm en 1996, année
  d'épisodes méditerranéens crédible). **Plafond relevé à 5 000 mm** par Grég, même motif, après calcul.
- **Réseau de la pluie** : sur 1961-2020, 300 stations mais **31 départements seulement**, surtout au sud (la pluie
  n'est pas homogénéisée jusqu'à la même année partout). Composite non représentatif de la France ; **réseau ramené à
  1961-2014** par Grég, après calcul (tendance non significative dans les deux cas : la décision ne dépend pas du
  résultat).

### Décisions demandées à Grég

- **D-M** : périmètre (A à C ; D hors P5).
- **D-N** : réseau constant du composite : 1959-2021 (220 stations, période exacte de R10) ou 1961-2022.
- **D-O** : pondération : moyenne des départements (chaque département pèse autant, proche d'une moyenne par surface)
  ou moyenne simple des stations.
- **D-P** : R10 avec sa fourchette publiée [+0,2 ; +0,4].

## P4 — Critères (proposés et validés le 28/10/2026, avant tout calcul)

> **Décisions de Grég du 28/10/2026, avant tout calcul** : D-I périmètre A à D retenu en entier ; D-J R9 avec la
> fourchette **[+102 ; +152] °C·j** (± 20 %, source sans incertitude publiée) ; D-K jours de danger = **FWI ≥ 21,3**
> (classe EFFIS « très élevé ») ; D-L BDIFF **abandonné** (au mieux 20 ans, aucun accès automatique) ; **critères I1-I9 validés** (I5 à r ≤ −0,6).
>
> Statut d'origine : proposition. Sondes : `docs/sonde-p4.md`, `docs/sonde-p4b.md`. Déjà publié hors P4
> (« largeur d'abord ») : reconnaissances CatNat en Gironde, tous périls confondus.

### Constat des sondes

- **Dates de vendanges** : la série « Bordeaux » de la base européenne Daux et al. 2012 (NOAA Paleo) est complète de
  1800 à 2006, en jours après le 31 août ; elle s'arrête en 2006. La série Saint-Émilion de l'ONERC (INRAE, Bordeaux
  Sciences Agro, 1892-2025) n'est publiée qu'en image : aucune donnée téléchargeable.
- **Danger météorologique d'incendie** : indices du système canadien (dont l'IFM/FWI) calculés par le CEMS sur ERA5,
  quotidiens, 0,25°, depuis 1940 (Copernicus EWDS, `cems-fire-historical-v1`, version 4.1, données consolidées).
  Requête d'abord refusée (conditions d'utilisation de l'EWDS), acceptées par Grég le 29/10/2026 ; la requête de juillet
  2022 aboutit en moins de 3 minutes (`docs/sonde-p4c.md`).
- **Feux observés (BDIFF)** : portail seulement (pas de fichier sur data.gouv.fr), depuis 2006 ; injoignable depuis
  GitHub (chaîne de certificats incomplète côté serveur). 20 ans au mieux : pas de tendance possible.
- **CatNat par péril** (GASPAR, Gironde, 7 676 reconnaissances) : séries dominées par le droit et par des événements
  isolés (tempête de 1982 seulement, « chocs des vagues » de 1999, « mouvements de terrain » de 1999). Les tempêtes
  sortent du régime CatNat en 1990. Aucune lecture climatique possible par péril.

### Périmètre proposé

- **A. Viticulture** (stations LSH, quotidien corrigé de la P2a, méthode C) : indice de Huglin (1er avril-30 septembre,
  K = 1,04 à 44-46° N) ; indice de fraîcheur des nuits (TN moyen de septembre, Tonietto) ; gelées tardives (jours
  TN ≤ 0 °C du 1er avril au 15 mai). Dates de vendanges de Bordeaux (Daux, 1800-2006), produit publié.
- **B. Danger météo d'incendie** : FWI ERA5 (CEMS) moyen sur les mailles de la Gironde ; moyenne de juin à septembre
  et nombre de jours avec FWI ≥ 21,3 (classe EFFIS « très élevé », D-K).
- **C. Canicule** (santé) : jours d'épisode caniculaire à Mérignac, moyennes sur 3 jours de TN ≥ 21 °C et de
  TX ≥ 35 °C (seuils préfectoraux de la Gironde), quotidien corrigé. Indice rare : règle E9.
- **D. CatNat par péril** : affichage seulement (inondations, sécheresse, submersion), sans tendance ni normale.

### Références proposées

| # | Énoncé | Source | Contrôle proposé |
|---|---|---|---|
| R9 | Bordelais : indice de Huglin + 127 °C·j entre 1980-1999 et 2000-2019 (SAFRAN, points de grille du vignoble) | Ollat et al., Climatologie 18, 2021, doi:10.1051/climat/202118003 | Écart des moyennes 2000-2019 − 1980-1999 du Huglin de chaque station dans **[+102 ; +152] °C·j** |
| — | Saint-Émilion : début des vendanges vers le 26 septembre au XXe siècle, vers le 15 septembre depuis les années 2010 | ONERC (INRAE, Bordeaux Sciences Agro) | information seulement : autre vignoble, autre période que Daux |
| — | FWI, canicule | aucune référence locale chiffrée | confiance au plus « moyenne » |

### Critères proposés

| # | Critère | Seuil proposé |
|---|---|---|
| I1 | Exhaustivité | Tout le périmètre retenu ; exclusions justifiées |
| I2 | Complétude | Stations : règle ETCCDI de la P2a (mois à 3 jours absents au plus) sur la saison concernée ; ERA5 : saisons complètes |
| I3 | Brut ≠ homogénéisé | Indices de station sur les seules années corrigées (C2) |
| I4 | Validation externe | R9 pour le Huglin ; sinon confiance au plus « moyenne » |
| I5 | **Cohérence physique (nouveau)** | Corrélation interannuelle entre la date de vendange Daux et le Huglin du composite, sur la période commune : r ≤ −0,6. Échec → la série des vendanges reste « signal non établi » |
| I6 | Cohérence entre stations | Même signe de tendance du Huglin à toutes les stations ; sinon expliqué |
| I7 | Plausibilité | Huglin 1 200-2 800 °C·j ; date de vendange −30 à + 60 j ; FWI moyen estival 0-60 |
| I8 | CatNat par péril | Aucune tendance ni normale publiée ; avertissement d'exposition et de règles affiché |
| I9 | Technique | Tests, CI, contrat, pages |

**Limites à assumer** : la date de vendange dépend aussi des pratiques (recherche d'une maturité plus poussée depuis les
années 1980-1990, qui retarde la récolte) : sa tendance sous-estime l'effet du climat. Le FWI ERA5 hérite des limites
de la réanalyse (pluie et humidité près du sol, cf. H5 en P3).

### Choix de mise en œuvre fixés AVANT le premier calcul (28/10/2026, `etl/indicators/impacts.py`)

- **Années** : une année de station est calculée si TN et TX sont complets (au plus 3 jours absents par mois) ; elle
  n'entre dans les tendances, les normales et R9 que si TN et TX sont corrigés sur les 12 mois (comme en P2a).
- **Huglin** : 5 stations disposant de TN et TX homogénéisés (Bordeaux-Paulin, Cap-Ferret, Bordeaux-Mérignac,
  Cazaux, Villenave-d'Ornon) ; composite à réseau constant 1961-2022 (même règle que la P2a). R9 est contrôlée pour
  chaque station et pour le composite (moyenne 2000-2019 − moyenne 1980-1999).
- **Fraîcheur des nuits** et **gelées tardives** : les 7 stations disposant de TN homogénéisé ; fraîcheur sur la série
  mensuelle LSH (TN de septembre).
- **Canicule** : fenêtres de 3 jours consécutifs, tous présents, prises de mai à septembre ; un jour compte s'il
  appartient à au moins une fenêtre au-dessus des deux seuils ; Mérignac seulement (station des seuils).
- **Comptages rares** (médiane 1961-1990 < 5 jours) : règle E9 de la P2a (écart entre normales, Mann-Whitney).
- **Vendanges** : colonne « Bor » telle que publiée, toutes les années ; série de plus de 80 ans, donc tendance mise
  en avant sur les 50 dernières années (1957-2006, règle du 23/10/2026). I5 : années homogénéisées du Huglin
  composite communes avec la série, au moins 30.
- **CatNat par péril** : libellés contenant « inondation » (inondations et coulées de boue, remontées de nappe),
  « sécheresse », « vagues » (chocs mécaniques des vagues) ; mêmes règles que la série tous périls (depuis 1982, deux
  dernières années exclues) ; affichage seul.
- **Confiance** : Huglin, règle des séries simples avec R9 (« élevée » si tendance significative et R9 retrouvée) ;
  autres indicateurs sans référence, au plus « moyenne » ; vendanges, « non établi » si I5 échoue.
- **FWI** (fixé le 29/10/2026 après la sonde de format `docs/sonde-p4c.md`, avant tout calcul ; `etl/sources/ewds_fire.py`) :
  CEMS `cems-fire-historical-v1`, réanalyse, données consolidées, version 4.1, 0,25° ; boîte 44,2-45,6° N,
  1,3° O-0,4° E, colonne la plus à l'ouest écartée (en mer) : 36 mailles ; moyenne quotidienne pondérée par le cosinus
  de la latitude ; saison juin-septembre, une année n'est retenue que si ses 122 jours existent. `fwi-ete` = moyenne de
  la saison ; `jours-fwi` = jours où la moyenne de la boîte atteint 21,3 (D-K). Produit de réanalyse publié : toutes
  les années complètes entrent dans la tendance (règle ERA5 du lot 2) ; série de plus de 80 ans, tendance mise en
  avant sur les 50 dernières années. Aucune référence : confiance au plus « moyenne » ; `jours-fwi` suit la règle
  E9 s'il est rare.

### Premier calcul (28/10/2026) et décision de Grég APRÈS calcul

Analyse : `docs/validation-p4.md`. Hors feu de forêt (en attente de l'accès EWDS) : I3, I5, I6, I8 conformes.
- **I4, R9 non retrouvée** : + 158 °C·j pour le composite, + 148 (Cazaux, seule dans la fourchette) à + 165 selon les
  stations, pour [+102 ; +152] ; Villenave-d'Ornon non mesurable (homogénéisée jusqu'en 2001). **Écart accepté** : il
  clôt le critère, il ne relève aucune confiance.
- **Correctif de présentation** : I7 comptait aussi les indicateurs manquants, déjà comptés par I1 ; corrigé.
- **FWI** (29/10/2026) : 86 saisons complètes relevées ; I1 satisfait ; tous les critères comptant pour la clôture
  sont satisfaits (I4 par écart accepté). Réserve : sur 1940-2025, pas de tendance significative (années 1940 aussi
  élevées que les récentes) ; hausse significative sur 1976-2025. **P4 close.**

### Décisions demandées à Grég

- **D-I** : périmètre (A à D).
- **D-J** : fourchette de R9.
- **D-K** : seuil de jours du FWI.
- **D-L** : feux observés (BDIFF) : export manuel par Grég depuis le portail, ou abandon.
- **Action** : accepter les conditions d'utilisation de l'EWDS (Copernicus), puis nouvelle sonde du FWI.

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
- 23/10/2026 : références E4 fixées (décision de Grég, deux sources concordantes, période 1961-2010, littoral et
  intérieur distingués). Les 34 indicateurs P2a sont activés dans le même commit, avant le premier calcul réel.
- 23/10/2026, après le premier calcul : correction d'un écart entre le code et la règle de confiance fixée. Un indice
  rare avec écart significatif entre normales était classé « faible » quand le contrôle A n'était pas évaluable ; la
  règle dit « au plus moyenne », il est donc « moyenne ». Aucun chiffre ne change (3 libellés de confiance).

### Décisions du 23/10/2026 (Grég), APRÈS le premier calcul réel

Analyse : `docs/validation-p2a.md`.
- **E4 R3 littoral** (+5,83 j/déc. pour [+4 ; +5]) : **écart maintenu, non accepté**. Les indices TX restent en
  confiance « moyenne » au plus tant qu'il n'est pas expliqué (effet de la correction B à Cap-Ferret notamment).
- **E4 R3 intérieur** : non évaluable (Villenave incomplète en 2002, erreur de choix de station au moment de fixer la
  référence). **Évalué sur Bordeaux-Mérignac seul.** Décision prise **après** la publication des pentes de Mérignac :
  ce n'est pas une référence fixée en aveugle, et elle doit être lue comme telle.
- **E7** (11 non évaluables, contrôle faible par construction) et **E8** (3 pertes de significativité, même signe) :
  **écarts expliqués et acceptés.** Les indicateurs concernés restent en confiance « moyenne » au plus.
- À faire pour P2b : un contrôle de la correction qui porte sur la période ancienne (là où elle agit), pas seulement
  sur la période après la dernière rupture.
- Publication en production décidée avec les écarts affichés (validation non close).

## Méthode « largeur d'abord » (décision de Grég du 23/10/2026)

Constat : après P0-P2a, une seule case sur 37 de la couverture (paramètres × échelles des instructions du projet)
était publiée. Décision : publier d'abord **un indicateur par paramètre**, avec une référence publiée fixée avant
calcul en une ligne et un niveau de confiance affiché ; la validation lourde (critères complets) reste réservée aux
indicateurs phares. Une page « Couverture » montre l'état de chaque paramètre, trous compris.

- Sonde des sources : `docs/sonde-largeur.md` (formats constatés avant d'écrire les lecteurs).
- Constructeur générique : `etl/indicators/serie.py` ; lecteurs : `etl/sources/globaux.py`.
- **Règle de confiance des séries simples** (fixée le 23/10/2026, avant le premier calcul) : « élevée » si tendance
  significative (Hamed-Rao) et référence publiée satisfaite ; « moyenne » si significative sans référence ou avec une
  référence non retrouvée ; « faible » si significative seulement sans correction ; « non établi » sinon.
- Références : dans `etl/config/indicators.yaml`, commitées avant le calcul (champ `fixed_on`). Les régressions
  de référence (`rate`, `relative_slope`) acceptent jusqu'à 20 % d'années manquantes, sans les compléter.
- Limite assumée pour les gaz à effet de serre : la référence (taux NOAA) vient du même réseau de mesure que la série ;
  le contrôle vérifie notre lecture et notre calcul, pas la mesure elle-même.
- Sources non retenues à ce stade (sonde) : HadSST4 (404), altimétrie NOAA STAR (404), CSIRO et NASA Ozone Watch
  (injoignables), Global Carbon Budget (404), CERES (compte requis). Foudre : aucune série ouverte longue.
- Règle ajoutée le 23/10/2026 **après** le premier calcul des séries simples (choix de présentation, appliqué à toutes) :
  pour une série de plus de 80 ans, la tendance mise en avant porte sur les 50 dernières années ; la tendance sur toute
  la série reste publiée. Motif : sur 1850-2025, la pente globale (+0,06 °C/déc.) noie le réchauffement récent.
  Les références et leur verdict ne changent pas.

### Lot 2 (25/10/2026) — choix fixés AVANT le premier calcul

Sonde : `docs/sonde-largeur2.md` et `docs/sonde-catnat.md`. Lecteurs : `etl/sources/globaux.py` (mer, IBTrACS, GASPAR),
`etl/sources/igra.py`, `etl/sources/openmeteo_era5.py` ; constructeurs : `etl/indicators/serie.py` et
`etl/indicators/atmosphere.py`. Ces choix sont commités avant toute exécution de l'ETL sur ces séries.

- **Séries brutes de station (rafales FXI, radiosondages IGRA)** : la règle C2 s'applique — publiées **sans tendance
  ni normale** (confiance « non établi »), avec la raison affichée. Aucune exception n'est faite sans décision de Grég.
- **ERA5 (réanalyse)** : traitée comme un produit publié (au même titre que les séries NOAA ou NASA), tendance calculée,
  provenance marquée « non homogénéisée ». Aucune référence locale : confiance au plus « moyenne ».
- **Nouveau type de référence `mean`** (niveau moyen sur une période) : il contrôle la lecture des données, pas
  l'évolution ; il **ne permet pas** la confiance « élevée ».
- **Références fixées** : température de surface de l'océan (NOAAGlobalTemp, HadSST) : GIEC AR6 GT1 ch. 9,
  +0,88 °C [0,68 à 1,01] entre 1850-1900 et 2011-2020 ; ouragans de l'Atlantique Nord : moyenne NOAA 1991-2020 de
  7 par saison (fourchette 6,5 à 7,5, valeur arrondie). Pas de référence pour l'ACE, ERA5, OISST, CatNat.
- **Ouragans et ACE** : depuis 1966 (ère satellitaire), trajectoires principales (`main` et `PROVISIONAL`), saison
  en cours exclue ; ouragan = catégorie Saffir-Simpson ≥ 1 ; ACE = vent² / 10⁴ aux heures synoptiques, catégorie ≥ 0.
- **Rafales mesurées** : jours avec FXI ≥ 27,8 m/s (100 km/h), années complètes au sens ETCCDI (≤ 3 jours absents
  par mois). Vent fort ERA5 : rafale ≥ 57,6 km/h (16 m/s, seuil Météo-France).
- **Radiosondages** : 12 UTC seulement ; un mois exige 15 sondages valides, une année ses 12 mois ; drapeaux IGRA
  « A », « B » ou blanc acceptés.
- **CatNat** : reconnaissances (arrêté × commune × péril, doublons retirés) par année de début de l'événement, depuis
  1982 ; les deux dernières années exclues (reconnaissances tardives) ; sécheresse = libellé contenant « sécheresse ».
- **OISST** : maille 45,125° N ; 1,875° O ; années d'au moins 360 jours.

### Lot 2 — constats et corrections APRÈS le premier calcul (25/10/2026)

- **OISST (mer au large de la Gironde) suspendu** : le serveur ERDDAP de NOAA CoastWatch a dépassé le délai (série
  entière), puis renvoyé une erreur 503 (requêtes annuelles). Lecteur conservé, indicateur désactivé.
- **NOAAGlobalTemp (océan)** : référence GIEC non retrouvée de justesse (+0,668 °C mesuré pour [0,68 ; 1,01]) ;
  confiance « moyenne ». Rien n'est ajusté : la fourchette reste celle fixée avant calcul. HadSST la retrouve (+0,87 °C).
- **Correctif de présentation** : la tendance « période commune des stations 1962-2017 », prévue pour les seules
  séries LSH, s'ajoutait aussi aux séries ERA5 (sans objet). Elle est retirée de ERA5 ; aucune autre série n'est touchée.
- **Radiosondages** : 44 années complètes sur 1965-2025 ; trou 1989-1999 (mois à moins de 15 sondages de 12 UTC).
- **Correctif d'affichage (toutes les séries simples, lots 1 et 2)** : les séries simples n'étaient soumises à aucun
  test de rupture, alors que le site affichait « aucune rupture détectée (test de Pettitt) ». Le test de Pettitt (avec
  contrôle après retrait de la tendance, même règle que P1) est désormais appliqué ; il ne change pas la règle de
  confiance des séries simples. Pour une série brute, le site dit qu'aucun test n'est fait.
- **Libellés coupés** : deux libellés de `variables.yaml` contenant une virgule non protégée étaient tronqués
  (ONI, vent fort). Corrigés ; le vocabulaire refuse désormais toute clé inattendue.
- **Période du test de rupture des séries simples** (choix fait APRÈS un premier calcul sur toute la série) : sur
  1850-2025, la droite ne capte pas l'accélération récente et le test signalait une « rupture établie » vers 1937 pour
  toutes les températures globales. Le test porte désormais sur les années de la tendance mise en avant. Restent
  signalées : CO₂ (2002) et chaleur de l'océan 0-700 m (1991), deux accélérations connues — la note le dit.

### Décision de Grég du 25/10/2026 — exception à la règle C2 pour les séries brutes (APRÈS avoir vu les séries)

Contexte : les rafales mesurées (FXI, Mérignac, Cazaux, Cap-Ferret) et les radiosondages de Mérignac (T850, T500,
Z500) avaient été publiés bruts, sans tendance, en application de C2. Grég a vu ces séries publiées (sans pente) avant
de décider : la décision est donc **postérieure aux données**, mais antérieure au calcul des pentes elles-mêmes.

Décision : **tendance indicative** autorisée sur ces seules séries (`indicative: true` au registre), avec des bornes
inscrites dans le contrat (v1.5, champ `indicative`) et vérifiées par l'ETL et par le site :
- confiance « faible » si la tendance est significative après correction de Hamed-Rao, « non établi » sinon —
  jamais au-dessus, quelle que soit la pente ;
- aucune normale, aucune référence publiée ; points marqués « bruts » sur le graphique ;
- tendance sur la plus longue suite d'années complètes consécutives (exigence de Hamed-Rao) : selon les lacunes,
  ce n'est pas forcément la période la plus récente ;
- test de rupture de Pettitt appliqué et affiché ;
- avertissement sur chaque page : un changement d'instrument ou d'emplacement peut à lui seul créer la pente.

Recommandation contraire de Claude, consignée : garder C2 (radiosondages lacunaires 1989-1999, changements de sondes
connus ; anémomètres jamais homogénéisés). Les bornes ci-dessus limitent le risque de lire ces pentes comme établies.

## Copernicus CDS — ERA5 niveaux de pression (26/10/2026)

- Accès : compte et licence de Grég (25/10/2026), clé dans le secret `CDSAPI_KEY` du dépôt. Sonde : `docs/sonde-cds.md`.
- Constat : une requête attend **3 à 7 heures** en file avant un traitement de quelques secondes, et le CDS rejette
  au-delà de trois requêtes en attente par utilisateur. Deux requêtes de test inutiles (janvier 2024) ont été annulées.
- Conception retenue : workflow quotidien « Copernicus » qui relève les travaux aboutis, commite de petites séries
  extraites (`data/sources/era5-pl/`) et soumet ce qui manque ; l'ETL ne lit que ces CSV (aucune attente).
- Indicateurs prévus, choix fixés AVANT tout calcul (`etl/indicators/altitude.py`) : T850, T500 et Z500 au-dessus de
  Bordeaux (maille ERA5 44,75° N ; 0,75° O, moyennes annuelles de 12 mois) ; vitesse et latitude du jet stream de
  l'Atlantique Nord en hiver (DJF, vent zonal 250 hPa moyenné sur 60° O-0°, 20-70° N, maximum du profil, latitude
  affinée par parabole). ERA5 traitée comme les autres séries ERA5 : confiance au plus « moyenne », sans référence.
  Ils restent désactivés au registre tant que les séries n'ont pas été relevées.

### Constat du 26/10/2026 sur le vent à 250 hPa (avant tout calcul de tendance du jet)

Premier relevé (vent zonal 250 hPa, 60° O-0°, 20-70° N, 1940-2025). En lisant la seule distribution de l'indice
(aucune pente calculée), le profil moyen d'hiver a **deux maxima** : le jet subtropical, au bord sud de la boîte
(≈ 20° N, 25,6 m/s), et le jet des tempêtes (≈ 45° N, 24,9 m/s). L'indice fixé le 26/10 (maximum du profil) passe
de l'un à l'autre : 36 hivers sur 85 au jet subtropical, dont 33 tronqués au bord de la boîte, surtout avant 1970.
Une tendance calculée ainsi mesurerait ce basculement, pas l'évolution du jet. Les deux indicateurs du jet
**restent désactivés** ; le changement d'indice est soumis à Grég. Requête préparée : vent zonal à 850 hPa,
0-60° O, 15-75° N (indice de Woollings et al., 2010).

**Décision de Grég du 26/10/2026** (après la distribution à 250 hPa, avant tout calcul de tendance) : indice de
**Woollings et al. (2010)** — vent zonal à 850 hPa, 0-60° O, 15-75° N, profil moyen de l'hiver (DJF), vitesse et
latitude du maximum (parabole). Limite assumée : moyennes mensuelles au lieu de valeurs quotidiennes filtrées, ce qui
lisse les déplacements du jet au sein de l'hiver. La série à 250 hPa déjà relevée n'est pas utilisée.

**27/10/2026** : séries relevées (Bordeaux 1940-2025, vent zonal à 850 hPa 1940-2025). Contrôles avant activation,
sans calcul de tendance : valeurs annuelles dans les bornes plausibles (T850 4,4 à 8,4 °C, cohérent avec les
radiosondages ; Z500 5 618 à 5 706 m) ; profil d'hiver à 850 hPa à un seul maximum (≈ 45-50° N), latitude du jet
entre 34 et 59° N, jamais au bord de la boîte. Les cinq indicateurs sont activés.
