# Validation P11 — localités la plus chaude et la plus froide à l'instant t

Critères Q1-Q5 et décisions D-AJ à D-AL validés par Grég le 18/11/2026, avant tout développement (`docs/phases.md`,
P11). Pas de calcul de tendance : la validation porte sur le contrôle qualité, la fraîcheur et l'honnêteté de
l'affichage.

## Préversion du 18/11/2026 (12 h 48 UTC)

4 559 stations retenues sur 5 231 dans le fichier METAR. Plus chaude : Keetmanshoop (Namibie), +40 °C ; plus froide :
pôle Sud (Amundsen-Scott), −39 °C ; repère Bordeaux-Mérignac : 17 °C. Exclusions : 627 pour maintenance (12 %),
36 sans température, 5 températures différentes du METAR brut, 4 points de rosée supérieurs à la température.

## Relecture indépendante (agent séparé, 18/11/2026)

Contrôle qualité fidèle à D-AL, aucun bug de calcul trouvé. Dix signalements, traités :

| | Signalement | Traitement |
|---|---|---|
| 1 | Le fichier METAR passait par le cache de données de Next.js : une régénération pouvait utiliser un fichier plus ancien que l'heure de lecture affichée (Q1) | Téléchargement direct par le module `https` de Node, hors cache : chaque régénération lit le fichier du moment |
| 2 | « il y a N min » figé à la génération, faux sur une page servie plus tard | « N min avant la lecture », avec l'heure UTC de la mesure ; l'âge de la lecture est signalé dans le navigateur au-delà de 30 min |
| 3 | Q5 : panne de la source non testée | `loadForPage` testé avec une source en panne, au déploiement (page d'attente) et en régénération (erreur relancée) |
| 4-7 | Limites de l'Antarctique contradictoires ; « paraît plus froid » faux (l'air d'altitude est réellement plus froid) ; bandeau et page d'attente imprécis | Textes corrigés |
| 8 | Heure dans le futur classée « trop ancienne » | Motif distinct « heure invalide » |
| 9 | Station indexée par un indicatif OACI vide | Repli sur l'identifiant, testé |
| 10 | Cas d'exclusion surtout synthétiques dans les tests | Non traité : le bac à sable n'a pas accès au fichier du jour ; les cas acceptés sont des METAR réels de la sonde |

Point à surveiller, sans changement de règle (D-AL) : l'indicateur de maintenance « $ » des stations automatiques
signale un besoin d'entretien de n'importe quel capteur, pas seulement du thermomètre ; la règle écarte donc aussi des
températures valides (12 % des stations, surtout nord-américaines). La modifier est une décision de Grég.

## Critères

| # | Statut | Mesure |
|---|---|---|
| Q1 | ✅ | Régénération au plus toutes les 10 min (`revalidate = 600`, sortie du build : « /instantane 10m ») ; âge ≤ 2 h contrôlé ; heure de lecture affichée et égale à l'heure du téléchargement |
| Q2 | ✅ | Chaque règle testée (`web/tests/metar.test.mjs`, 11 tests) ; cas acceptés sur des METAR réels |
| Q3 | ✅ | Température comparée au groupe du METAR brut (groupe T des remarques s'il existe), exclusion sinon |
| Q4 | ✅ | « parmi les N stations retenues sur M » ; limites de couverture et d'altitude écrites sur la page |
| Q5 | ✅ | Tests et CI verts (`npm test` dans `ci.yml`) ; panne de la source testée ; bandeau au-delà de 30 min |

Essai en préversion Vercel le 18/11/2026 : page construite à 13 h 14 UTC, revisitée à 15 h 21 UTC sans visite
entre-temps ; le premier visiteur a reçu l'ancienne page avec le bandeau « Cette lecture date de 127 minutes », et la
visite suivante une page régénérée (lecture de 15 h 20 UTC). C'est le fonctionnement voulu de la régénération : une
page ancienne n'est jamais présentée comme actuelle.

P11 close le 18/11/2026.
