# Sonde P6 — accès CERES et CAMS (généré)

Généré par `python -m etl.probe.p6` le 31/10/2026 21:03 UTC. Aucun indicateur calculé.

## Déséquilibre énergétique (CERES EBAF, OPeNDAP avec jeton Earthdata)

jeton présent : oui

### `https://opendap.larc.nasa.gov/opendap/CERES/EBAF/Edition4.2.1/contents.html` → **403**

```
0 fichiers : []
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>ERROR: The request could not be satisfied</TITLE>
</HEAD><BODY>
<H1>403 ERROR</H1>
<H2>The request could 
```

### `https://opendap.larc.nasa.gov/opendap/CERES/EBAF/Edition4.2/contents.html` → **403**

```
0 fichiers : []
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>ERROR: The request could not be satisfied</TITLE>
</HEAD><BODY>
<H1>403 ERROR</H1>
<H2>The request could 
```

## Aérosols (CAMS EAC4 mensuel, Atmosphere Data Store)

→ **201**

```
{"processID":"cams-global-reanalysis-eac4-monthly","type":"process","jobID":"d9ad3643-44a3-44ff-a3a7-4e21c50ebde2","status":"accepted","created":"2026-10-31T21:03:07.283324","updated":"2026-10-31T21:03:07.283324","links":[{"href":"https://ads.atmosphere.copernicus.eu/api/retrieve/v1/processes/cams-global-reanalysis-eac4-monthly/execution","rel":"self"},{"href":"https://ads.atmosphere.copernicus.eu/api/retrieve/v1/jobs/d9ad3643-44a3-44ff-a3a7-4e21c50ebde2","rel":"monitor","type":"application/json","title":"job status info"}],"metadata":{"datasetMetadata":{"messages":[]},"origin":"api"}}
état après 31 s : successful
archive : data_allhours_sfc.nc (319587 o)
dimensions : valid_time=1, latitude=241, longitude=480
  valid_time ('valid_time',) (1,) seconds since 1970-01-01 time
  latitude ('latitude',) (241,) degrees_north latitude
  longitude ('longitude',) (480,) degrees_east longitude
  aod550 ('valid_time', 'latitude', 'longitude') (1, 241, 480) ~ Total Aerosol Optical Depth at 550nm
```
