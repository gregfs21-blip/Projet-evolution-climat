# Sonde P11 — localités extrêmes à l'instant t (généré)

Généré par `python -m etl.probe.p11` le 20/11/2026 14:04 UTC, depuis GitHub Actions. Aucun indicateur, aucun choix.

## 1. METAR mondiaux, fichier cache de l'AWC (NOAA)

```
GET https://aviationweather.gov/data/cache/metars.cache.csv.gz → 200 en 0.0 s, 263663 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=263663 ; Last-Modified=Fri, 20 Nov 2026 14:03:07 GMT ; Cache-Control=max-age=30
5276 lignes ; préambule : []
colonnes : raw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,wind_dir_degrees,wind_speed_kt,wind_gust_kt,visibility_statute_mi,altim_in_hg,sea_level_pressure_mb,corrected,auto,auto_station,maintenance_indicator_on,no_signal,lightning_sensor_off,freezing_rain_sensor_off,present_weather_sensor_off,wx_string,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,flight_category,three_hr_pressure_tendency_mb,maxT_c,minT_c,maxT24hr_c,minT24hr_c,precip_in,pcp3hr_in,pcp6hr_in,pcp24hr_in,snow_in,vert_vis_ft,metar_type,elevation_m
stations : 5275 ; avec température : 5234
âge des observations (min) : médiane 12, 90 % 65, max 90
stations au sud de 60° S : 27 ; au nord de 70° N : 30
10 plus chaudes (brut, sans contrôle) :
  +40.0 °C FAHS (-24.3810, 31.0440) âge 65 min : METAR FAHS 201300Z AUTO 06005KT //// // ////// 40/12 Q1011
  +39.0 °C FQTT (-16.1080, 33.6400) âge 5 min : METAR FQTT 201400Z 10007KT 9999 SCT020 FEW025CB 39/19 Q1009 RMK CB TO N/NE
  +38.0 °C GAMB (14.5120, -4.0840) âge 65 min : METAR GAMB 201300Z 05006KT CAVOK 38/M01 Q1013
  +38.0 °C GOTT (13.7330, -13.6570) âge 65 min : METAR GOTT 201300Z 07010KT CAVOK 38/05 Q1011 NOSIG
  +38.0 °C GOSS (16.0510, -16.4610) âge 65 min : METAR GOSS 201300Z 12006KT CAVOK 38/13 Q1013
  +38.0 °C DGLE (9.5540, -0.8620) âge 65 min : METAR DGLE 201300Z 14003KT 8000 NSC 38/13 Q1010 NOSIG
  +38.0 °C GAKD (14.4820, -11.4040) âge 35 min : METAR GAKD 201330Z 06009KT 020V090 CAVOK 38/02 Q1011
  +38.0 °C GQNO (18.3100, -15.9700) âge 35 min : METAR GQNO 201330Z 10012KT 070V130 8000 NSC 38/01 Q1013 NOSIG
  +37.0 °C HKLO (3.1220, 35.6090) âge 65 min : METAR HKLO 201300Z 08010KT 9999 FEW035 SCT290 37/16 Q1007
  +37.0 °C FTTJ (12.1340, 15.0340) âge 65 min : METAR FTTJ 201300Z 15004KT 080V200 8000 NSC 37/M02 Q1011 NOSIG
10 plus froides (brut, sans contrôle) :
  -28.2 °C CYUS (68.7950, -93.4190) âge 65 min : METAR CYUS 201300Z AUTO ///// ////SM ////// M28/M31 A2984 RMK WND MISG VIS MISG CLD MISG T
  -28.0 °C UEEE (62.0930, 129.7740) âge 35 min : METAR UEEE 201330Z 01003MPS 5000 -SN SCT015 M28/M31 Q1011 R23/490346 NOSIG RMK QNH758 QFE7
  -28.0 °C CYWE (64.1920, -114.0780) âge 65 min : METAR CYWE 201300Z AUTO 05009KT 9SM CLR M28/M31 A3022 RMK SLP294
  -26.6 °C CWIJ (65.7560, -111.2460) âge 65 min : METAR CWIJ 201300Z AUTO 30002KT M27/M29 RMK AO1 SOG 05 8001 SLP293 T12661293
  -26.0 °C CYEK (61.0980, -94.0720) âge 65 min : METAR CYEK 201300Z 30007KT 15SM SKC M26/M29 A3015 RMK SNW CVR/MEDIUM PACK SLP213
  -25.0 °C CYZS (64.1880, -83.3510) âge 65 min : METAR CYZS 201300Z 35011KT 15SM SKC M25/M29 A2978 RMK SLP097
  -24.3 °C CWMT (63.1340, -117.2450) âge 65 min : METAR CWMT 201300Z AUTO 06003KT M24/M27 RMK AO1 SOG 02 5003 SLP271 T12431269
  -24.2 °C CXWB (65.8790, -89.4460) âge 65 min : METAR CXWB 201300Z AUTO 32012KT M24/M29 RMK AO1 SOG 02 1001 PK WND 31017/1220 SLP127 T1242
  -24.0 °C CYHK (68.6330, -95.8510) âge 65 min : METAR CYHK 201300Z 32018KT 10SM SKC M24/M27 A2992 RMK SNW CVR/HARD PACK SLP143
  -24.0 °C CYRT (62.8110, -92.1000) âge 65 min : METAR CYRT 201300Z 29011KT 15SM FEW003 M24/M28 A3003 RMK SC1 SLP177
```

## 2. API METAR de l'AWC (JSON)

```
GET https://aviationweather.gov/api/data/metar?ids=LFBD,NZSP,OERK,KDRA&format=json → 200 en 0.1 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=1879
4 enregistrements ; clés : ['altim', 'clouds', 'cover', 'dewp', 'elev', 'fltCat', 'icaoId', 'lat', 'lon', 'metarType', 'name', 'obsTime', 'qcField', 'rawOb', 'receiptTime', 'reportTime', 'slp', 'temp', 'visib', 'wdir', 'wspd']
  KDRA 2.2 °C 2026-11-20T14:00:00.000Z Mercury/Desert Rock, NV, US
  LFBD 13 °C 2026-11-20T14:00:00.000Z Bordeaux/Mérignac Arpt, NA, FR
  NZSP -42 °C 2026-11-20T12:00:00.000Z Amundsen-South Pole, NZ, AQ
  OERK 27 °C 2026-11-20T14:00:00.000Z Riyadh/King Khaled Intl, RD, SA
```

## 2 bis. Noms des stations

```
GET https://aviationweather.gov/data/cache/stations.cache.json.gz → 200 en 0.3 s, 359430 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=359430 ; Last-Modified=Fri, 20 Nov 2026 00:15:10 GMT ; Cache-Control=max-age=30
9960 stations ; exemple : {"id": "32012", "icaoId": null, "iataId": null, "faaId": null, "wmoId": null, "site": "Woods Hole Stratus Wave Station", "lat": 19.691, "lon": -85.567, "elev": 0, "state": "", "country": null, "priority": 4, "siteType": []}
GET https://aviationweather.gov/api/data/stationinfo?ids=FYKT,UEEE,NZSP,LFBD&format=json → 200 en 0.0 s, 826 o
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
GET https://api.open-meteo.com/v1/forecast?latitude=36.46,24.8,31.0,-78.46,-90.0,67.55,44.83,18.31,-16.108,-24.381,68.795,62.093,64.192&longitude=-116.87,46.7,58.3,… → 200 en 0.3 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Access-Control-Allow-Origin=*
  Vallée de la Mort (36.46, -116.87) : 12.5 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle -58.0 m)
  Riyad (24.8, 46.7) : 27.1 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle 651.0 m)
  Désert de Lut (31.0, 58.3) : 25.8 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle 303.0 m)
  Vostok (-78.46, 106.84) : -34.8 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle 3493.0 m)
  Pôle Sud (-90.0, 0.0) : -33.9 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle 2836.0 m)
  Verkhoïansk (67.55, 133.38) : -27.8 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle 135.0 m)
  Bordeaux-Mérignac (44.83, -0.69) : 15.3 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle 45.0 m)
  METAR GQNO (+38.0 °C) (18.31, -15.97) : 37.0 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle -1.0 m)
  METAR FQTT (+39.0 °C) (-16.108, 33.64) : 36.5 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle 143.0 m)
  METAR FAHS (+40.0 °C) (-24.381, 31.044) : 40.1 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle 527.0 m)
  METAR CYUS (-28.2 °C) (68.795, -93.419) : -27.5 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle 42.0 m)
  METAR UEEE (-28.0 °C) (62.093, 129.774) : -27.4 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle 97.0 m)
  METAR CYWE (-28.0 °C) (64.192, -114.078) : -24.2 °C à 2026-11-20T14:00 (intervalle 900 s ; altitude du modèle 369.0 m)
requête de 1000 points → 414 en 0.1 s ; b'<html>\r\n<head><title>414 Request-URI Too Large</title></head>\r\n<body>\r\n<center><h1>414 Request-URI Too Large</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'
```
