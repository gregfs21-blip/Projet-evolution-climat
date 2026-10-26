# Sonde Copernicus CDS — ERA5 niveaux de pression, moyennes mensuelles (généré)

Généré par `python -m etl.probe.cds` le 26/10/2026 07:05 UTC. Aucun calcul : accès, délais et format constatés.

Jeu de données : `reanalysis-era5-pressure-levels-monthly-means`.

Clé présente dans l'environnement : **oui** (jamais affichée).

### 0. Travaux déjà soumis

```
a1495af4-be1f-45e1-9dc1-cbe46880ddae rejected créé 2026-10-25T22:18:23.601726 début None fin 2026-10-25T22:18:36.631355
dad5d85c-229f-4328-ba07-d521d5192dfb rejected créé 2026-10-25T22:15:27.161152 début None fin 2026-10-25T22:16:01.304708
9df40ba6-dab8-4d70-a4e1-6ec34f933dd8 rejected créé 2026-10-25T21:58:21.967232 début None fin 2026-10-25T21:58:40.409205
26b89e23-cb19-4ff2-a1e0-ce6c58a7e09d rejected créé 2026-10-25T21:56:03.885243 début None fin 2026-10-25T21:56:13.666146
14c71edd-e872-46c9-999b-41277d0bc5de accepted créé 2026-10-25T21:48:06.630267 début None fin None
55875211-dff8-4682-abca-59c589116bf2 accepted créé 2026-10-25T21:40:05.221490 début None fin None
804221bb-5ec5-49aa-8b04-9efdbfd643c7 successful créé 2026-10-25T20:53:45.940291 début 2026-10-26T03:54:23.605847 fin 2026-10-26T03:54:26.627031
6bc350ea-8892-47fb-bc66-b6e779f28fd2 successful créé 2026-10-25T20:52:51.984220 début 2026-10-25T20:53:14.955001 fin 2026-10-25T23:53:17.267182
```

```
Résultat du travail 804221bb-5ec5-49aa-8b04-9efdbfd643c7 :
0.05 Mo en 1 s
49 ko, début b'\x89HDF\r\n\x1a\n'
dimensions : valid_time=1, pressure_level=3, latitude=3, longitude=3
  number () () {'units': '1', 'long_name': 'ensemble member numerical id'} : [0]
  valid_time ('valid_time',) (1,) {'units': 'seconds since 1970-01-01', 'long_name': 'time'} : [1704067200]
  pressure_level ('pressure_level',) (3,) {'units': 'hPa', 'long_name': 'pressure'} : [850.0, 500.0, 250.0]
  latitude ('latitude',) (3,) {'units': 'degrees_north', 'long_name': 'latitude'} : [45.0, 44.75, 44.5]
  longitude ('longitude',) (3,) {'units': 'degrees_east', 'long_name': 'longitude'} : [-1.0, -0.75, -0.5]
  expver () () {} : ['0001']
  t ('valid_time', 'pressure_level', 'latitude', 'longitude') (1, 3, 3, 3) {'units': 'K', 'long_name': 'Temperature'} : [277.1600341796875, 277.1033935546875, 277.0389404296875, 277.3387451171875]
  z ('valid_time', 'pressure_level', 'latitude', 'longitude') (1, 3, 3, 3) {'units': 'm**2 s**-2', 'long_name': 'Geopotential'} : [14784.56640625, 14782.44140625, 14779.94140625, 14806.06640625]
  u ('valid_time', 'pressure_level', 'latitude', 'longitude') (1, 3, 3, 3) {'units': 'm s**-1', 'long_name': 'U component of wind'} : [6.740517616271973, 6.783486366271973, 6.862587928771973, 6.661416053771973]
```

```
Résultat du travail 6bc350ea-8892-47fb-bc66-b6e779f28fd2 :
non téléchargé : 78.6 Go (au-delà de 200 Mo, pas une requête de la sonde)
0 ko, début b''
lecture netCDF impossible : OSError [Errno -51] NetCDF: Unknown file format: '/tmp/tmpg6sb0qtj/6bc350ea-8892-47fb-bc66-b6e779f28fd2.nc'
```

### Soumission des requêtes utiles (sans attendre)

```
bordeaux-1940-2025 : soumise, travail 3d621529-27a5-40d6-abff-945b68958c3b (accepted)
atlantique-u250-1940-2025 : soumise, travail 099ad076-6f8a-4146-bb3d-d2d42631e731 (accepted)
```

Mode relevé : aucune requête bloquante (le CDS traite en plusieurs heures).
