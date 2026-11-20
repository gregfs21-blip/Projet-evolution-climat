# Sonde P11 — localités extrêmes à l'instant t (généré)

Généré par `python -m etl.probe.p11` le 20/11/2026 11:10 UTC, depuis GitHub Actions. Aucun indicateur, aucun choix.

## 1. METAR mondiaux, fichier cache de l'AWC (NOAA)

```
GET https://aviationweather.gov/data/cache/metars.cache.csv.gz → 200 en 0.1 s, 256308 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=256308 ; Last-Modified=Fri, 20 Nov 2026 11:09:06 GMT ; Cache-Control=max-age=30
5178 lignes ; préambule : []
colonnes : raw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,wind_dir_degrees,wind_speed_kt,wind_gust_kt,visibility_statute_mi,altim_in_hg,sea_level_pressure_mb,corrected,auto,auto_station,maintenance_indicator_on,no_signal,lightning_sensor_off,freezing_rain_sensor_off,present_weather_sensor_off,wx_string,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,flight_category,three_hr_pressure_tendency_mb,maxT_c,minT_c,maxT24hr_c,minT24hr_c,precip_in,pcp3hr_in,pcp6hr_in,pcp24hr_in,snow_in,vert_vis_ft,metar_type,elevation_m
stations : 5177 ; avec température : 5133
âge des observations (min) : médiane 15, 90 % 20, max 80
stations au sud de 60° S : 23 ; au nord de 70° N : 28
10 plus chaudes (brut, sans contrôle) :
  +39.0 °C FAHS (-24.3810, 31.0440) âge 70 min : METAR FAHS 201000Z AUTO 28004KT //// // ////// 39/16 Q1014
  +38.0 °C FDSK (-26.3590, 31.7190) âge 10 min : METAR FDSK 201100Z 17011KT 9999 FEW040CB 38/17 Q1010 NOSIG
  +38.0 °C FQTT (-16.1080, 33.6400) âge 10 min : METAR FQTT 201100Z 16004KT 9999 SCT020 38/18 Q1012
  +37.0 °C FQXA (-25.0380, 33.6270) âge 70 min : METAR FQXA 201000Z 34008KT 290V050 9999 FEW020 37/20 Q1012
  +37.0 °C FAKN (-25.3830, 31.1060) âge 10 min : METAR FAKN 201100Z AUTO 05005G20KT //// // ////// 37/13 Q1016
  +36.0 °C FDMS (-26.5290, 31.3080) âge 10 min : METAR FDMS 201100Z 08003KT 9999 TS BKN035 FEW040CB 36/18 Q1013 NOSIG
  +35.0 °C HKLO (3.1220, 35.6090) âge 70 min : METAR HKLO 201000Z 06006KT 9999 SCT034 SCT280 35/15 Q1010
  +35.0 °C FTTA (9.1440, 18.3740) âge 70 min : METAR FTTA 201000Z 13004KT CAVOK 35/13 Q1014
  +35.0 °C FBPM (-21.1590, 27.4770) âge 10 min : METAR FBPM 201100Z 29006KT 230V350 9999 BKN030 35/11 Q1017
  +35.0 °C YNWN (-23.4170, 119.7990) âge 10 min : METAR YNWN 201100Z AUTO 35007KT 9999 // NCD 35/04 Q1010
10 plus froides (brut, sans contrôle) :
  -30.0 °C UEEE (62.0930, 129.7740) âge 10 min : METAR UEEE 201100Z 36002MPS 5000 -SN SCT020 M30/M34 Q1014 R23/490158 NOSIG RMK QNH760 QFE7
  -27.8 °C CWIJ (65.7560, -111.2460) âge 10 min : METAR CWIJ 201100Z AUTO 26001KT M28/M31 RMK AO1 SOG 05 5000 SLP299 T12781307
  -27.0 °C CYWE (64.1920, -114.0780) âge 10 min : METAR CYWE 201100Z AUTO 04005KT 9SM CLR M27/M30 A3024 RMK SLP297
  -27.0 °C CYEK (61.0980, -94.0720) âge 10 min : METAR CYEK 201100Z AUTO 27008KT 9SM CLR M27/M30 A3016 RMK SLP216
  -25.9 °C CYUS (68.7950, -93.4190) âge 10 min : METAR CYUS 201100Z AUTO ///// ////SM ////// M26/M28 A2983 RMK WND MISG VIS MISG CLD MISG T
  -24.2 °C CXWB (65.8790, -89.4460) âge 70 min : METAR CXWB 201000Z AUTO 34008KT M24/M28 RMK AO1 SOG 02 3008 SLP126 T12421284
  -24.0 °C CYRT (62.8110, -92.1000) âge 10 min : METAR CYRT 201100Z 31015KT 15SM FEW003 M24/M28 A3003 RMK SF1 SF TR SLP176
  -24.0 °C CYHK (68.6330, -95.8510) âge 10 min : METAR CYHK 201100Z AUTO 32012KT 9SM CLR M24/M26 A2990 RMK SLP137
  -24.0 °C CYZS (64.1880, -83.3510) âge 70 min : METAR CYZS 201000Z 34012KT 15SM SKC M24/M28 A2976 RMK SLP089
  -23.8 °C CWMT (63.1340, -117.2450) âge 10 min : METAR CWMT 201100Z AUTO 06004KT M24/M26 RMK AO1 SOG 02 3004 SLP274 T12381263
```

## 2. API METAR de l'AWC (JSON)

```
GET https://aviationweather.gov/api/data/metar?ids=LFBD,NZSP,OERK,KDRA&format=json → 200 en 0.2 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=1816
4 enregistrements ; clés : ['altim', 'clouds', 'cover', 'dewp', 'elev', 'fltCat', 'icaoId', 'lat', 'lon', 'metarType', 'name', 'obsTime', 'qcField', 'rawOb', 'receiptTime', 'reportTime', 'slp', 'temp', 'visib', 'wdir', 'wspd']
  KDRA 4.4 °C 2026-11-20T11:00:00.000Z Mercury/Desert Rock, NV, US
  LFBD 16 °C 2026-11-20T11:00:00.000Z Bordeaux/Mérignac Arpt, NA, FR
  NZSP -41 °C 2026-11-20T06:00:00.000Z Amundsen-South Pole, NZ, AQ
  OERK 29 °C 2026-11-20T11:00:00.000Z Riyadh/King Khaled Intl, RD, SA
```

## 2 bis. Noms des stations

```
GET https://aviationweather.gov/data/cache/stations.cache.json.gz → 200 en 0.2 s, 359430 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=359430 ; Last-Modified=Fri, 20 Nov 2026 00:15:10 GMT ; Cache-Control=max-age=30
9960 stations ; exemple : {"id": "32012", "icaoId": null, "iataId": null, "faaId": null, "wmoId": null, "site": "Woods Hole Stratus Wave Station", "lat": 19.691, "lon": -85.567, "elev": 0, "state": "", "country": null, "priority": 4, "siteType": []}
GET https://aviationweather.gov/api/data/stationinfo?ids=FYKT,UEEE,NZSP,LFBD&format=json → 200 en 0.2 s, 826 o
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=826
4 stations ; exemple : {"id": "FYKT", "icaoId": "FYKT", "iataId": "KMP", "faaId": null, "wmoId": "68312", "site": "Keetmanshoop Arpt", "lat": -26.54, "lon": 18.111, "elev": 1064, "state": "KA", "country": "NA", "priority": 3, "siteType": ["METAR", "TAF"]}
NZSP dans le cache METAR : non
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
GET https://api.open-meteo.com/v1/forecast?latitude=36.46,24.8,31.0,-78.46,-90.0,67.55,44.83,-26.359,-16.108,-24.381,62.093,65.756,61.098&longitude=-116.87,46.7,58.… → 200 en 0.0 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Access-Control-Allow-Origin=*
  Vallée de la Mort (36.46, -116.87) : 13.6 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle -58.0 m)
  Riyad (24.8, 46.7) : 28.8 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 651.0 m)
  Désert de Lut (31.0, 58.3) : 28.9 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 303.0 m)
  Vostok (-78.46, 106.84) : -33.1 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 3493.0 m)
  Pôle Sud (-90.0, 0.0) : -33.7 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 2836.0 m)
  Verkhoïansk (67.55, 133.38) : -29.8 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 135.0 m)
  Bordeaux-Mérignac (44.83, -0.69) : 13.9 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 45.0 m)
  METAR FDSK (+38.0 °C) (-26.359, 31.719) : 38.8 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 320.0 m)
  METAR FQTT (+38.0 °C) (-16.108, 33.64) : 36.7 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 143.0 m)
  METAR FAHS (+39.0 °C) (-24.381, 31.044) : 39.9 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 527.0 m)
  METAR UEEE (-30.0 °C) (62.093, 129.774) : -28.6 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 97.0 m)
  METAR CWIJ (-27.8 °C) (65.756, -111.246) : -25.6 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 494.0 m)
  METAR CYEK (-27.0 °C) (61.098, -94.072) : -23.6 °C à 2026-11-20T11:00 (intervalle 900 s ; altitude du modèle 9.0 m)
requête de 1000 points → 414 en 0.0 s ; b'<html>\r\n<head><title>414 Request-URI Too Large</title></head>\r\n<body>\r\n<center><h1>414 Request-URI Too Large</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'
```
