# Sonde « largeur d'abord », lot 2 (généré)

Généré par `python -m etl.probe.largeur2` le 25/10/2026 08:24 UTC. Aucun calcul : formats et couverture constatés.

## 1. Vent dans le quotidien Météo-France (département 33)

Fichiers : QUOT_departement_33_periode_avant-1949_RR-T-Vent, QUOT_departement_33_periode_1950-2024_RR-T-Vent, QUOT_departement_33_periode_2025-2026_RR-T-Vent

Colonnes : NUM_POSTE, NOM_USUEL, LAT, LON, ALTI, AAAAMMJJ, RR, QRR, TN, QTN, HTN, QHTN, TX, QTX, HTX, QHTX, TM, QTM, TNTXM, QTNTXM, TAMPLI, QTAMPLI, TNSOL, QTNSOL, TN50, QTN50, DG, QDG, FFM, QFFM, FF2M, QFF2M, FXY, QFXY, DXY, QDXY, HXY, QHXY, FXI, QFXI, DXI, QDXI, HXI, QHXI, FXI2, QFXI2, DXI2, QDXI2, HXI2, QHXI2, FXI3S, QFXI3S, DXI3S, QDXI3S, HXI3S, QHXI3S, DRR, QDRR, STATUS_FXI3S, STATUS_DXI3S

| Poste | Nom | Années FXI ≥ 330 j | Plage FXI | Années FFM ≥ 330 j | Années FXI3S ≥ 330 j |
|---|---|---|---|---|---|
| 33529001 | CAZAUX | 76 | 1949-2025 | 76 | 45 |
| 33281001 | BORDEAUX-MERIGNAC | 76 | 1950-2025 | 77 | 45 |
| 33236002 | CAP-FERRET | 54 | 1971-2025 | 70 | 44 |
| 33415001 | ST GERVAIS | 26 | 1996-2025 | 30 | 26 |
| 33482001 | ST SULPICE DE POMMIERS | 22 | 2004-2025 | 23 | 22 |
| 33116001 | CAZATS | 22 | 2004-2025 | 23 | 22 |
| 33314005 | PAUILLAC | 21 | 2005-2025 | 21 | 21 |

## 2. ERA5 via Open-Meteo (Bordeaux-Mérignac) : variables quotidiennes disponibles

### Open-Meteo archive, 1940

`https://archive-api.open-meteo.com/v1/archive?latitude=44.831&longitude=-0.691&start_date=1940-01-01&end_date=1940-01-05&daily=pressure_msl_mean%2Crelative_humidity_2m_mean%2Cwind_speed_10m_max%2Cwind_gusts_10m_max%2Cprecipitation_sum%2Cshortwave_radiation_sum&models=era5&timezone=Europe%2FParis` → **200**

```
{"latitude":44.75,"longitude":-0.75,"generationtime_ms":66.23077392578125,"utc_offset_seconds":3600,"timezone":"Europe/Paris","timezone_abbreviation":"GMT+1","elevation":46.0,"daily_units":{"time":"iso8601","pressure_msl_mean":"hPa","relative_humidity_2m_mean":"%","wind_speed_10m_max":"km/h","wind_gusts_10m_max":"km/h","precipitation_sum":"mm","shortwave_radiation_sum":"MJ/m²"},"daily":{"time":["1940-01-01","1940-01-02","1940-01-03","1940-01-04","1940-01-05"],"pressure_msl_mean":[1013.2,1008.0,1000.6,1000.7,1010.5],"relative_humidity_2m_mean":[55,75,91,90,95],"wind_speed_10m_max":[17.5,19.8,19.5,15.8,9.7],"wind_gusts_10m_max":[35.6,34.2,49.3,29.2,23.0],"precipitation_sum":[null,0.00,2.10,0.70,1.60],"shortwave_radiation_sum":[null,6.61,3.59,5.41,3.65]}}
```

## 3. Température de la mer

### NOAA Climate at a Glance — océan mondial, annuel

`https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/ocean/tavg/land_ocean/12/12/1850-2025/data.csv` → **404**

```
```

### NOAA Climate at a Glance — océan mondial, annuel (autre forme)

`https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/ocean/12/12/1850-2025/data.csv` → **200**

```
# Title: "Global Ocean January - December Average Temperature Departures"
# Units: Degrees Celsius
# Base Period: 1901-2000
Year,Departure from Average
1850,0
1851,0.06
1852,0.08
1853,0.07
1854,0.02
1855,0.02
1856,-0.07
1857,-0.15
1858,-0.04
1859,0.01
1860,-0.02
```

### ERDDAP OISST v2.1 mensuel, point golfe de Gascogne (45 N, 2 W)

`https://coastwatch.pfeg.noaa.gov/erddap/griddap/ncdcOisst21Agg_LonPM180.csv?sst%5B(2024-01-16):1:(2024-01-16)%5D%5B(0.0)%5D%5B(45.125)%5D%5B(-1.875)%5D` → **200**

```
time,zlev,latitude,longitude,sst
UTC,m,degrees_north,degrees_east,degree_C
2024-01-16T12:00:00Z,0.0,45.125,-1.875,13.37
```

### HadSST4 — page des données

`https://www.metoffice.gov.uk/hadobs/hadsst4/data/download.html` → **200**

```
[page HTML] liens :
data/HadSST.4.2.0.0_actuals_ensemble_members_1-50.zip
data/HadSST.4.2.0.0_actuals_ensemble_members_101-150.zip
data/HadSST.4.2.0.0_actuals_ensemble_members_151-200.zip
data/HadSST.4.2.0.0_actuals_ensemble_members_51-100.zip
data/HadSST.4.2.0.0_actuals_median.nc
data/HadSST.4.2.0.0_annual_6060.csv
data/HadSST.4.2.0.0_annual_GLOBE.csv
data/HadSST.4.2.0.0_annual_NHEM.csv
data/HadSST.4.2.0.0_annual_SHEM.csv
data/HadSST.4.2.0.0_annual_TROP.csv
data/HadSST.4.2.0.0_ensemble_members_1-50.zip
data/HadSST.4.2.0.0_ensemble_members_101-150.zip
data/HadSST.4.2.0.0_ensemble_members_151-200.zip
data/HadSST.4.2.0.0_ensemble_members_51-100.zip
data/HadSST.4.2.0.0_error_covariance_1850-1899.zip
data/HadSST.4.2.0.0_error_covariance_1900-1949.zip
data/HadSST.4.2.0.0_error_covariance_1950-1999.zip
data/HadSST.4.2.0.0_error_covariance_2000-present.zip
data/HadSST.4.2.0.0_measurement_and_sampling_uncertainty.nc
data/HadSST.4.2.0.0_median.nc
data/HadSST.4.2.0.0_monthly_6060.csv
data/HadSST.4.2.0.0_monthly_GLOBE.csv
data/HadSST.4.2.0.0_monthly_NHEM.csv
data/HadSST.4.2.0.0_monthly_SHEM.csv
data/HadSST.4.2.0.0_monthly_TROP.csv
```

## 4. Radiosondages IGRA (Bordeaux-Mérignac, FRM00007510)

### Liste des stations IGRA

`https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/doc/igra2-station-list.txt` → **200**

```
FRM00007510  44.8306   -0.6914   51.0    BORDEAUX MERIGNAC              1920 2026  66381
```

### Répertoire monthly-por

`https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/monthly-por/` → **200**

```
ghgt_00z-mly.txt.zip
ghgt_12z-mly.txt.zip
temp_00z-mly.txt.zip
temp_12z-mly.txt.zip
uwnd_00z-mly.txt.zip
uwnd_12z-mly.txt.zip
vapr_00z-mly.txt.zip
vapr_12z-mly.txt.zip
vwnd_00z-mly.txt.zip
vwnd_12z-mly.txt.zip
```

### Répertoire data-por

`https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/data-por/` → **200**

```
..
ACM00078861-data.txt.zip
AEM00041217-data.txt.zip
AEXUAE05467-data.txt.zip
AFM00040911-data.txt.zip
AFM00040913-data.txt.zip
AFM00040938-data.txt.zip
AFM00040948-data.txt.zip
AFM00040990-data.txt.zip
AGM00060355-data.txt.zip
AGM00060360-data.txt.zip
AGM00060390-data.txt.zip
AGM00060402-data.txt.zip
AGM00060419-data.txt.zip
AGM00060425-data.txt.zip
AGM00060430-data.txt.zip
AGM00060445-data.txt.zip
AGM00060475-data.txt.zip
AGM00060490-data.txt.zip
AGM00060511-data.txt.zip
AGM00060525-data.txt.zip
AGM00060535-data.txt.zip
AGM00060549-data.txt.zip
AGM00060550-data.txt.zip
AGM00060559-data.txt.zip
AGM00060566-data.txt.zip
AGM00060571-data.txt.zip
AGM00060580-data.txt.zip
AGM00060590-data.txt.zip
AGM00060602-data.txt.zip
```

### IGRA data-por, Mérignac

`https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/data-por/FRM00007510-data.txt.zip` → **200**

```
[36.9 Mo]
FRM00007510-data.txt
#FRM00007510 1920 01 11 99 1300    2          erac-hud  448306    -6914
30 -9999  -9999   500 -9999 -9999 -9999   248   220
30 -9999  -9999  1000 -9999 -9999 -9999   270   280
#FRM00007510 1920 01 14 99 1300    4          erac-hud  448306    -6914
30 -9999  -9999   500 -9999 -9999 -9999     0    40
30 -9999  -9999  1000 -9999 -9999 -9999   292    60
30 -9999  -9999  1500 -9999 -9999 -9999   292   100
30 -9999  -9999  2000 -9999 -9999 -9999   315   120
#FRM00007510 1920 01 15 99 1300    4          erac-hud  448306    -6914
30 -9999  -9999   500 -9999 -9999 -9999   135    40
30 -9999  -9999  1000 -9999 -9999 -9999    90    80
30 -9999  -9999  1500 -9999 -9999 -9999   112    40
30 -9999  -9999  2000 -9999 -9999 -9999   112    20
#FRM00007510 1920 01 16 99 1300    4          erac-hud  448306    -6914
30 -9999  -9999   500 -9999 -9999 -9999    90    80
30 -9999  -9999  1000 -9999 -9999 -9999    90    40
30 -9999  -9999  1500 -9999 -9999 -9999    90    10
30 -9999  -9999  2000 -9999 -9999 -9999    22    40
#FRM00007510 1920 01 16 99 1800    4          erac-hud  448306    -6914
30 -9999  -9999   500 -9999 -9999 -9999   135    40
30 -9999  -9999  1000 -9999 -9999 -9999    90    40
30 -9999  -9999  1500 -9999 -9999 -9999    67   100
30 -9999  -9999  2000 -9999 -9999 -9999    90    20
#FRM00007510 1920 01 19 99 1300    2          erac-hud  448306    -6914
30 -9999  -9999   500 -9999 -9999 -9999   248    80
```

## 5. IBTrACS Atlantique Nord : colonnes utiles

### IBTrACS NA

`https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.NA.list.v04r01.csv` → **200**

```
57.6 Mo, 128182 lignes
Colonnes retenues : SID, SEASON, NAME, ISO_TIME, NATURE, WMO_WIND, TRACK_TYPE, USA_WIND, USA_SSHS
Saisons : 1851-2026
NATURE : Counter({'TS': 106575, 'ET': 13593, 'DS': 4495, 'SS': 2369, 'MX': 975, 'NR': 173})
TRACK_TYPE : Counter({'main': 126734, 'spur-merge': 618, 'PROVISIONAL': 452, 'spur-other': 364, 'spur-split': 12})
```

## 6. Catastrophes naturelles : base GASPAR (data.gouv.fr)

### Recherche GASPAR

`https://www.data.gouv.fr/api/1/datasets/?q=gaspar%20catnat&page_size=5` → **200**

```
```
