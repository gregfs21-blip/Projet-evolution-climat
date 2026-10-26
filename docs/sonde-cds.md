# Sonde Copernicus CDS — ERA5 niveaux de pression, moyennes mensuelles (généré)

Généré par `python -m etl.probe.cds` le 26/10/2026 06:48 UTC. Aucun calcul : accès, délais et format constatés.

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
lecture netCDF impossible : AttributeError 'str' object has no attribute 'ravel'
```

```
Résultat du travail 6bc350ea-8892-47fb-bc66-b6e779f28fd2 :
interrompu après 300 s : 1074.8 Mo sur 78648.951398 Mo
1074790 ko, début b'PK\x03\x04-\x00\x00\x00'
lecture netCDF impossible : OSError [Errno -51] NetCDF: Unknown file format: '/tmp/tmpup68n37x/6bc350ea-8892-47fb-bc66-b6e779f28fd2.nc'
```

File : encore 2 travail(aux) en attente après 10 min

Aucune nouvelle requête soumise : travaux précédents encore en file.
