# Sonde P11 — localités extrêmes à l'instant t (généré)

Généré par `python -m etl.probe.p11` le 20/11/2026 12:32 UTC, depuis GitHub Actions. Aucun indicateur, aucun choix.

## 1. METAR mondiaux, fichier cache de l'AWC (NOAA)

```
GET https://aviationweather.gov/data/cache/metars.cache.csv.gz → 200 en 0.1 s, 273565 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=273565 ; Last-Modified=Fri, 20 Nov 2026 12:32:07 GMT ; Cache-Control=max-age=30
5230 lignes ; préambule : []
colonnes : raw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,wind_dir_degrees,wind_speed_kt,wind_gust_kt,visibility_statute_mi,altim_in_hg,sea_level_pressure_mb,corrected,auto,auto_station,maintenance_indicator_on,no_signal,lightning_sensor_off,freezing_rain_sensor_off,present_weather_sensor_off,wx_string,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,flight_category,three_hr_pressure_tendency_mb,maxT_c,minT_c,maxT24hr_c,minT24hr_c,precip_in,pcp3hr_in,pcp6hr_in,pcp24hr_in,snow_in,vert_vis_ft,metar_type,elevation_m
stations : 5229 ; avec température : 5184
âge des observations (min) : médiane 33, 90 % 40, max 82
stations au sud de 60° S : 27 ; au nord de 70° N : 28
10 plus chaudes (brut, sans contrôle) :
  +40.0 °C FVCZ (-21.0080, 31.5780) âge 33 min : METAR FVCZ 201200Z 36004KT CAVOK 40/13 Q1011
  +40.0 °C FQXA (-25.0380, 33.6270) âge 33 min : METAR FQXA 201200Z 35007KT 310V060 9999 FEW020 40/16 Q1011
  +40.0 °C FAHS (-24.3810, 31.0440) âge 33 min : METAR FAHS 201200Z AUTO 02003KT //// // ////// 40/13 Q1012
  +39.0 °C FQTT (-16.1080, 33.6400) âge 33 min : METAR FQTT 201200Z 18004KT 9999 SCT020 FEW025TCU 39/19 Q1010 RMK TO NE/E
  +38.0 °C GOSP (16.6770, -14.9640) âge 33 min : METAR GOSP 201200Z 06008KT CAVOK 38/12 Q1014
  +38.0 °C GOSM (15.5970, -13.3260) âge 33 min : METAR GOSM 201200Z 08010KT CAVOK 38/06 Q1013
  +37.0 °C GOTT (13.7330, -13.6570) âge 33 min : METAR GOTT 201200Z 08008KT 020V110 8000 NSC 37/09 Q1012 NOSIG
  +37.0 °C DGLE (9.5540, -0.8620) âge 33 min : METAR DGLE 201200Z 14003KT 8000 NSC 37/14 Q1011 NOSIG
  +37.0 °C FDSK (-26.3590, 31.7190) âge 33 min : METAR FDSK 201200Z 13013KT 9999 SCT035 FEW040CB 37/19 Q1009 NOSIG
  +37.0 °C GOOG (15.4000, -15.0840) âge 33 min : METAR GOOG 201200Z 08008KT CAVOK 37/06 Q1011
10 plus froides (brut, sans contrôle) :
  -42.0 °C NZSP (-89.9800, 180.0000) âge 43 min : METAR NZSP 201150Z 07009KT 9999 FEW030 FEW080 M42/ A2829 RMK ALL WNDS GRID SDG/HDG
  -29.0 °C UEEE (62.0930, 129.7740) âge 33 min : METAR UEEE 201200Z 02003MPS 3200 -SN SCT017 M29/M32 Q1012 R23/490158 NOSIG RMK QNH759 QFE7
  -27.9 °C CWIJ (65.7560, -111.2460) âge 33 min : METAR CWIJ 201200Z AUTO 26003KT M28/M31 RMK AO1 SOG 05 8001 SLP296 T12791307
  -27.0 °C CYWE (64.1920, -114.0780) âge 33 min : METAR CYWE 201200Z AUTO 07006KT 9SM CLR M27/M31 A3022 RMK SLP293
  -27.0 °C CYEK (61.0980, -94.0720) âge 33 min : METAR CYEK 201200Z AUTO 28009KT 9SM CLR M27/M30 A3015 RMK SLP213
  -26.7 °C CYUS (68.7950, -93.4190) âge 33 min : METAR CYUS 201200Z AUTO ///// ////SM ////// M27/M29 A2983 RMK WND MISG VIS MISG CLD MISG T
  -26.0 °C CYZS (64.1880, -83.3510) âge 33 min : METAR CYZS 201200Z 32009KT 15SM SKC M26/M30 A2978 RMK SLP096
  -24.6 °C CXWB (65.8790, -89.4460) âge 33 min : METAR CXWB 201200Z AUTO 31009KT M25/M29 RMK AO1 SOG 02 1005 SLP127 T12461289
  -24.0 °C CYHK (68.6330, -95.8510) âge 33 min : METAR CYHK 201200Z AUTO 33012G18KT 9SM CLR M24/M26 A2991 RMK SLP139
  -24.0 °C CYRT (62.8110, -92.1000) âge 33 min : METAR CYRT 201200Z 31013G18KT 15SM FEW003 M24/M28 A3002 RMK SF1 SF TR SLP175
```

## 2. API METAR de l'AWC (JSON)

```
GET https://aviationweather.gov/api/data/metar?ids=LFBD,NZSP,OERK,KDRA&format=json → 200 en 0.3 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=1922
4 enregistrements ; clés : ['altim', 'clouds', 'cover', 'dewp', 'elev', 'fltCat', 'icaoId', 'lat', 'lon', 'maxT', 'metarType', 'minT', 'name', 'obsTime', 'presTend', 'qcField', 'rawOb', 'receiptTime', 'reportTime', 'slp', 'temp', 'visib', 'wdir', 'wspd']
  KDRA 3.9 °C 2026-11-20T12:00:00.000Z Mercury/Desert Rock, NV, US
  LFBD 17 °C 2026-11-20T12:00:00.000Z Bordeaux/Mérignac Arpt, NA, FR
  NZSP -42 °C 2026-11-20T12:00:00.000Z Amundsen-South Pole, NZ, AQ
  OERK 30 °C 2026-11-20T12:00:00.000Z Riyadh/King Khaled Intl, RD, SA
```

## 2 bis. Noms des stations

```
GET https://aviationweather.gov/data/cache/stations.cache.json.gz → 200 en 0.2 s, 359430 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=359430 ; Last-Modified=Fri, 20 Nov 2026 00:15:10 GMT ; Cache-Control=max-age=30
9960 stations ; exemple : {"id": "32012", "icaoId": null, "iataId": null, "faaId": null, "wmoId": null, "site": "Woods Hole Stratus Wave Station", "lat": 19.691, "lon": -85.567, "elev": 0, "state": "", "country": null, "priority": 4, "siteType": []}
GET https://aviationweather.gov/api/data/stationinfo?ids=FYKT,UEEE,NZSP,LFBD&format=json → 200 en 0.2 s, 826 o
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
GET https://api.open-meteo.com/v1/forecast?latitude=36.46,24.8,31.0,-78.46,-90.0,67.55,44.83,-25.038,-24.381,-21.008,-89.98,62.093,65.756&longitude=-116.87,46.7,58.… → 200 en 1.1 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Access-Control-Allow-Origin=*
  Vallée de la Mort (36.46, -116.87) : 13.2 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle -58.0 m)
  Riyad (24.8, 46.7) : 28.5 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 651.0 m)
  Désert de Lut (31.0, 58.3) : 28.2 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 303.0 m)
  Vostok (-78.46, 106.84) : -33.9 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 3493.0 m)
  Pôle Sud (-90.0, 0.0) : -33.8 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 2836.0 m)
  Verkhoïansk (67.55, 133.38) : -29.1 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 135.0 m)
  Bordeaux-Mérignac (44.83, -0.69) : 14.9 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 45.0 m)
  METAR FQXA (+40.0 °C) (-25.038, 33.627) : 38.7 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 2.0 m)
  METAR FAHS (+40.0 °C) (-24.381, 31.044) : 39.8 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 527.0 m)
  METAR FVCZ (+40.0 °C) (-21.008, 31.578) : 39.0 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 430.0 m)
  METAR NZSP (-42.0 °C) (-89.98, 180.0) : -33.9 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 2769.0 m)
  METAR UEEE (-29.0 °C) (62.093, 129.774) : -27.6 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 97.0 m)
  METAR CWIJ (-27.9 °C) (65.756, -111.246) : -25.6 °C à 2026-11-20T12:30 (intervalle 900 s ; altitude du modèle 494.0 m)
requête de 1000 points → 414 en 0.0 s ; b'<html>\r\n<head><title>414 Request-URI Too Large</title></head>\r\n<body>\r\n<center><h1>414 Request-URI Too Large</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'
```
