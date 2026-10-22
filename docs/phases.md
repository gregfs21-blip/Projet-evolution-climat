# Phases du projet

Chaque phase suit la même boucle : ETL → JSON → page → validation contre des valeurs publiées.
Une phase n'est close que lorsque les écarts avec les références sont expliqués.

| Phase | Contenu | Validation | État |
|---|---|---|---|
| P0 | Socle : arborescence, schéma, ETL, site, CI, workflow mensuel | Un indicateur factice traverse la chaîne jusqu'au site déployé | en cours |
| P1 | Températures Gironde : LSH TX/TN Mérignac + stations longues, anomalies 1961-1990 et 1991-2020, tendances Hamed-Rao, ruptures | ClimatHD Nouvelle-Aquitaine | à faire |
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
