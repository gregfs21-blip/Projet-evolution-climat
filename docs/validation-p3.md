# Validation P3 — analyse des écarts (rédigée à la main)

Résultats automatiques : `docs/validation-p3-resultats.md`. Critères : `docs/phases.md` (P3).

## H5 — contrôle croisé de l'humidité ERA5 non conforme

Mesuré : à Bordeaux-Mérignac, sur 1981-2025, l'écart annuel ERA5 − station vaut en moyenne −0,81 point d'humidité
relative, et il **dérive de +0,64 point par décennie (Hamed-Rao, p = 0,005)**. Aucune rupture établie. La station
devient donc relativement plus sèche qu'ERA5 au fil du temps. Cazaux ne permet pas de trancher : sa plus longue
suite d'années communes complètes ne compte que 15 ans, sous le minimum de 20 fixé avant calcul.

Deux causes possibles, que les données disponibles ne départagent pas :
- **côté station** : changement d'hygromètre ou de méthode de mesure (l'automatisation des stations a remplacé
  les psychromètres par des capteurs électroniques ; date à Mérignac non vérifiée), environnement de l'abri qui
  évolue (aéroport, urbanisation) ; les mesures sont brutes, sans homogénéisation ;
- **côté ERA5** : évolution du système d'observation assimilé (satellites, radiosondages), ou biais du modèle sur
  l'humidité près du sol.

Ce qui ne change pas : la règle H5 validée avant calcul s'applique, la confiance de l'humidité ERA5 est au plus
« faible ». Sa pente sur 1976-2025 (−0,41 point par décennie) n'étant pas significative, l'indicateur était déjà en
« signal non établi ». La dérive est affichée dans ses limites sur le site.

**Écart accepté par Grég le 28/10/2026, après calcul.** L'acceptation clôt la phase ; elle ne relève aucune
confiance. Piste si l'humidité devient un enjeu (P4, indicateurs sanitaires) : l'historique des capteurs de Mérignac
auprès de Météo-France, et un troisième poste à longue série d'humidité.

## H4 — référence R8 retrouvée de justesse

Pas un écart, mais à lire avec prudence : la pente de la SST ERA5 sur le golfe entier, 1982-2014, vaut
+0,218 °C par décennie, pour une fourchette [+0,21 ; +0,31] fixée avant calcul. La valeur publiée (+0,26) n'est pas
retrouvée au centre de la fourchette ; ERA5 (analyses OSTIA) et les données satellitaires utilisées par Costoya ne
sont pas les mêmes. La confiance « élevée » de la SST du golfe repose sur ce contrôle.

## Information sur le vent

Corrélation interannuelle de 0,58 entre les jours de vent fort ERA5 et les jours de rafale ≥ 16 m/s mesurés à
Mérignac (75 ans, mesures brutes). ERA5 suit la variabilité d'une année à l'autre sans être interchangeable avec la
mesure ; ses indicateurs de vent restent en confiance au plus « moyenne ».
