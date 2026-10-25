# Sonde Copernicus CDS — ERA5 niveaux de pression, moyennes mensuelles (généré)

Généré par `python -m etl.probe.cds` le 25/10/2026 21:59 UTC. Aucun calcul : accès, délais et format constatés.

Jeu de données : `reanalysis-era5-pressure-levels-monthly-means`.

Clé présente dans l'environnement : **oui** (jamais affichée).

### 0. Travaux déjà soumis

```
9df40ba6-dab8-4d70-a4e1-6ec34f933dd8 reanalysis-era5-pressure-levels-monthly-means rejected créé 2026-10-25T21:58:21.967232 début None fin 2026-10-25T21:58:40.409205
26b89e23-cb19-4ff2-a1e0-ce6c58a7e09d reanalysis-era5-pressure-levels-monthly-means rejected créé 2026-10-25T21:56:03.885243 début None fin 2026-10-25T21:56:13.666146
14c71edd-e872-46c9-999b-41277d0bc5de reanalysis-era5-pressure-levels-monthly-means accepted créé 2026-10-25T21:48:06.630267 début None fin None
55875211-dff8-4682-abca-59c589116bf2 reanalysis-era5-pressure-levels-monthly-means accepted créé 2026-10-25T21:40:05.221490 début None fin None
804221bb-5ec5-49aa-8b04-9efdbfd643c7 reanalysis-era5-pressure-levels-monthly-means accepted créé 2026-10-25T20:53:45.940291 début None fin None
6bc350ea-8892-47fb-bc66-b6e779f28fd2 reanalysis-era5-pressure-levels-monthly-means running créé 2026-10-25T20:52:51.984220 début 2026-10-25T20:53:14.955001 fin None
```

File : encore 4 travail(aux) en attente après 15 min

### 1. Point de Bordeaux, 3 variables × 3 niveaux, janvier 2024

```
ÉCHEC après 54 s
HTTPError : 400 Client Error: Bad Request for url: https://cds.climate.copernicus.eu/api/retrieve/v1/jobs/dad5d85c-229f-4328-ba07-d521d5192dfb/results
The job has been rejected
Maximum number queued requests for this dataset has been reached. Please configure your scripts to request data sequentially
```

### 4. Point de Bordeaux, température 850 hPa, 1940-2025 (série complète : délai réel de la file)

```
ÉCHEC après 141 s
HTTPError : 400 Client Error: Bad Request for url: https://cds.climate.copernicus.eu/api/retrieve/v1/jobs/a1495af4-be1f-45e1-9dc1-cbe46880ddae/results
The job has been rejected
Maximum number queued requests for this dataset has been reached. Please configure your scripts to request data sequentially
```
