# Sonde Copernicus CDS — ERA5 niveaux de pression, moyennes mensuelles (généré)

Généré par `python -m etl.probe.cds` le 25/10/2026 21:40 UTC. Aucun calcul : accès, délais et format constatés.

Jeu de données : `reanalysis-era5-pressure-levels-monthly-means`.

Clé présente dans l'environnement : **oui** (jamais affichée).

### 1. Point de Bordeaux, 3 variables × 3 niveaux, janvier 2024

```
PAS DE RÉPONSE après 8 min (requête encore en file d'attente ou en cours chez Copernicus)
```

### 2. Atlantique Nord (60° O-0°, 20-70° N), vent zonal 250 hPa, grille 1°, janvier 2024

```
PAS DE RÉPONSE après 8 min (requête encore en file d'attente ou en cours chez Copernicus)
```

### 3. Globe, température 850 hPa, grille 2,5°, 12 mois de 2024

```
ÉCHEC après 17 s
HTTPError : 400 Client Error: Bad Request for url: https://cds.climate.copernicus.eu/api/retrieve/v1/jobs/26b89e23-cb19-4ff2-a1e0-ce6c58a7e09d/results
The job has been rejected
Maximum number queued requests for this dataset has been reached. Please configure your scripts to request data sequentially
```

### 4. Point de Bordeaux, température 850 hPa, 1940-2025 (série complète : délai réel de la file)

```
ÉCHEC après 146 s
HTTPError : 400 Client Error: Bad Request for url: https://cds.climate.copernicus.eu/api/retrieve/v1/jobs/9df40ba6-dab8-4d70-a4e1-6ec34f933dd8/results
The job has been rejected
Maximum number queued requests for this dataset has been reached. Please configure your scripts to request data sequentially
```
