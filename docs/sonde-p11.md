# Sonde P11 — localités extrêmes à l'instant t (généré)

Généré par `python -m etl.probe.p11` le 19/11/2026 06:31 UTC, depuis GitHub Actions. Aucun indicateur, aucun choix.

## 1. METAR mondiaux, fichier cache de l'AWC (NOAA)

```
GET https://aviationweather.gov/data/cache/metars.cache.csv.gz → 200 en 0.1 s, 267233 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=267233 ; Last-Modified=Thu, 19 Nov 2026 06:31:05 GMT ; Cache-Control=max-age=30
5024 lignes ; préambule : []
colonnes : raw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,wind_dir_degrees,wind_speed_kt,wind_gust_kt,visibility_statute_mi,altim_in_hg,sea_level_pressure_mb,corrected,auto,auto_station,maintenance_indicator_on,no_signal,lightning_sensor_off,freezing_rain_sensor_off,present_weather_sensor_off,wx_string,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,flight_category,three_hr_pressure_tendency_mb,maxT_c,minT_c,maxT24hr_c,minT24hr_c,precip_in,pcp3hr_in,pcp6hr_in,pcp24hr_in,snow_in,vert_vis_ft,metar_type,elevation_m
stations : 5023 ; avec température : 4988
âge des observations (min) : médiane 32, 90 % 39, max 72
stations au sud de 60° S : 25 ; au nord de 70° N : 28
10 plus chaudes (brut, sans contrôle) :
  +38.0 °C YPKU (-15.7810, 128.7100) âge 32 min : METAR YPKU 190600Z AUTO 01011KT 9999 // NCD 38/22 Q1008
  +37.0 °C YCIN (-17.5740, 123.8310) âge 32 min : METAR YCIN 190600Z AUTO 26007KT 230V290 9999 // NCD 37/17 Q1009
  +36.0 °C YPTN (-14.5230, 132.3830) âge 32 min : METAR YPTN 190600Z AUTO 29006KT 9999 // FEW070 36/24 Q1009
  +36.0 °C VLPS (15.1320, 105.7810) âge 32 min : METAR VLPS 190600Z 22002KT 9999 FEW020 36/22 Q1014 NOSIG
  +35.0 °C WARR (-7.3800, 112.7870) âge 32 min : METAR WARR 190600Z 06013KT 9999 SCT020CB 35/26 Q1009 NOSIG
  +35.0 °C VLSK (16.5570, 104.7600) âge 32 min : METAR VLSK 190600Z 04010KT 9999 SCT020 FEW100 35/19 Q1016 NOSIG
  +35.0 °C YNWN (-23.4170, 119.7990) âge 32 min : METAR YNWN 190600Z AUTO 24010KT 9999 // NCD 35/05 Q1010
  +35.0 °C RPLB (14.7940, 120.2710) âge 32 min : METAR RPLB 190600Z 09013KT 9999 FEW020 35/24 Q1012 NOSIG RMK A2988
  +35.0 °C YPWR (-31.1560, 136.8050) âge 7 min : SPECI YPWR 190625Z AUTO 28016G26KT 9999 // NCD 35/08 Q1005
  +34.0 °C YBAS (-23.7950, 133.8890) âge 32 min : METAR YBAS 190600Z AUTO 28015KT 9999 // NCD 34/14 Q1012
10 plus froides (brut, sans contrôle) :
  -40.0 °C NZSP (-89.9800, 180.0000) âge 42 min : METAR NZSP 190550Z 01010KT 9999 FEW030 M40/ A2851 RMK ALL WNDS GRID SDG/HDG
  -33.0 °C UEEE (62.0930, 129.7740) âge 32 min : METAR UEEE 190600Z 00000MPS 5000 BR NSC M33/M37 Q1026 R23/490153 NOSIG RMK QNH770 QFE761
  -27.0 °C CYRB (74.7130, -94.9820) âge 19 min : SPECI CYRB 190613Z 35015G22KT 9SM IC DRSN OVC005 M27/M30 A2976 RMK IC1ST7 SLP093
  -27.0 °C UHMM (59.9110, 150.7250) âge 32 min : METAR UHMM 190600Z 06001MPS 9999 NSC M27/M30 Q1012 R10/85//49 NOSIG RMK QNH759 QFE744/0992
  -27.0 °C CYZS (64.1880, -83.3510) âge 32 min : METAR CYZS 190600Z 33007KT 15SM FEW030 M27/M31 A2981 RMK SC1 SLP106
  -26.2 °C CYUS (68.7950, -93.4190) âge 32 min : METAR CYUS 190600Z AUTO ///// ////SM ////// M26/M29 A2979 RMK WND MISG VIS MISG CLD MISG T
  -26.1 °C CXRB (74.7160, -94.9830) âge 32 min : METAR CXRB 190600Z AUTO 35015KT M26/M29 RMK AO1 SOG 13 6006 PK WND 34021/0503 SLP089 T1261
  -26.0 °C CYHK (68.6330, -95.8510) âge 32 min : METAR CYHK 190600Z AUTO 31015G21KT 9SM CLR M26/M28 A2986 RMK SLP123
  -26.0 °C CXSE (73.7660, -105.2960) âge 32 min : METAR CXSE 190600Z AUTO 27014KT M26/M29 RMK AO1 SOG 11 5002 PK WND 28017/0501 SLP171 T1260
  -25.0 °C CYCB (69.1060, -105.1160) âge 32 min : METAR CYCB 190600Z 30011KT 15SM DRSN FEW015 M25/M28 A3010 RMK SC1 CLD HGT EST CEILOMETER B
```

## 2. API METAR de l'AWC (JSON)

```
GET https://aviationweather.gov/api/data/metar?ids=LFBD,NZSP,OERK,KDRA&format=json → 200 en 0.1 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=1838
4 enregistrements ; clés : ['altim', 'clouds', 'cover', 'dewp', 'elev', 'fltCat', 'icaoId', 'lat', 'lon', 'maxT', 'metarType', 'minT', 'name', 'obsTime', 'presTend', 'qcField', 'rawOb', 'receiptTime', 'reportTime', 'slp', 'temp', 'visib', 'wdir', 'wspd']
  KDRA 8.3 °C 2026-11-19T06:00:00.000Z Mercury/Desert Rock, NV, US
  LFBD 11 °C 2026-11-19T06:00:00.000Z Bordeaux/Mérignac Arpt, NA, FR
  NZSP -40 °C 2026-11-19T06:00:00.000Z Amundsen-South Pole, NZ, AQ
  OERK 21 °C 2026-11-19T06:00:00.000Z Riyadh/King Khaled Intl, RD, SA
```

## 2 bis. Noms des stations

```
GET https://aviationweather.gov/data/cache/stations.cache.json.gz → 200 en 0.1 s, 359430 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=359430 ; Last-Modified=Thu, 19 Nov 2026 00:15:24 GMT ; Cache-Control=max-age=30
9960 stations ; exemple : {"id": "32012", "icaoId": null, "iataId": null, "faaId": null, "wmoId": null, "site": "Woods Hole Stratus Wave Station", "lat": 19.691, "lon": -85.567, "elev": 0, "state": "", "country": null, "priority": 4, "siteType": []}
GET https://aviationweather.gov/api/data/stationinfo?ids=FYKT,UEEE,NZSP,LFBD&format=json → 200 en 0.1 s, 826 o
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=826
4 stations ; exemple : {"id": "FYKT", "icaoId": "FYKT", "iataId": "KMP", "faaId": null, "wmoId": "68312", "site": "Keetmanshoop Arpt", "lat": -26.54, "lon": 18.111, "elev": 1064, "state": "KA", "country": "NA", "priority": 3, "siteType": ["METAR", "TAF"]}
NZSP dans le cache METAR : oui
NZCM dans le cache METAR : oui
FYKT dans le cache METAR : oui
KDRA dans le cache METAR : oui
OIZB dans le cache METAR : non
UEEE dans le cache METAR : oui
LFBD dans le cache METAR : oui
BGSC dans le cache METAR : non
```

## 3. Open-Meteo, température actuelle du modèle

```
GET https://api.open-meteo.com/v1/forecast?latitude=36.46,24.8,31.0,-78.46,-90.0,67.55,44.83,15.132,-17.574,-15.781,-89.98,62.093,59.911&longitude=-116.87,46.7,58.3… → 200 en 0.1 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Access-Control-Allow-Origin=*
  Vallée de la Mort (36.46, -116.87) : 17.9 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle -58.0 m)
  Riyad (24.8, 46.7) : 22.1 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 651.0 m)
  Désert de Lut (31.0, 58.3) : 24.7 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 303.0 m)
  Vostok (-78.46, 106.84) : -31.7 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 3493.0 m)
  Pôle Sud (-90.0, 0.0) : -33.1 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 2836.0 m)
  Verkhoïansk (67.55, 133.38) : -27.4 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 135.0 m)
  Bordeaux-Mérignac (44.83, -0.69) : 13.6 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 45.0 m)
  METAR VLPS (+36.0 °C) (15.132, 105.781) : 32.6 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 103.0 m)
  METAR YCIN (+37.0 °C) (-17.574, 123.831) : 37.6 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 83.0 m)
  METAR YPKU (+38.0 °C) (-15.781, 128.71) : 39.4 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 42.0 m)
  METAR NZSP (-40.0 °C) (-89.98, 180.0) : -33.0 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 2769.0 m)
  METAR UEEE (-33.0 °C) (62.093, 129.774) : -32.0 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 97.0 m)
  METAR UHMM (-27.0 °C) (59.911, 150.725) : -20.6 °C à 2026-11-19T06:30 (intervalle 900 s ; altitude du modèle 175.0 m)
requête de 1000 points → 414 en 0.2 s ; b'<html>\r\n<head><title>414 Request-URI Too Large</title></head>\r\n<body>\r\n<center><h1>414 Request-URI Too Large</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'
```
