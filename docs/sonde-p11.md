# Sonde P11 — localités extrêmes à l'instant t (généré)

Généré par `python -m etl.probe.p11` le 19/11/2026 12:56 UTC, depuis GitHub Actions. Aucun indicateur, aucun choix.

## 1. METAR mondiaux, fichier cache de l'AWC (NOAA)

```
GET https://aviationweather.gov/data/cache/metars.cache.csv.gz → 200 en 0.2 s, 267173 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=267173 ; Last-Modified=Thu, 19 Nov 2026 12:56:14 GMT ; Cache-Control=max-age=30
5172 lignes ; préambule : []
colonnes : raw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,wind_dir_degrees,wind_speed_kt,wind_gust_kt,visibility_statute_mi,altim_in_hg,sea_level_pressure_mb,corrected,auto,auto_station,maintenance_indicator_on,no_signal,lightning_sensor_off,freezing_rain_sensor_off,present_weather_sensor_off,wx_string,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,flight_category,three_hr_pressure_tendency_mb,maxT_c,minT_c,maxT24hr_c,minT24hr_c,precip_in,pcp3hr_in,pcp6hr_in,pcp24hr_in,snow_in,vert_vis_ft,metar_type,elevation_m
stations : 5171 ; avec température : 5137
âge des observations (min) : médiane 27, 90 % 61, max 87
stations au sud de 60° S : 25 ; au nord de 70° N : 30
10 plus chaudes (brut, sans contrôle) :
  +40.0 °C FAUP (-28.3990, 21.2600) âge 57 min : METAR FAUP 191200Z 31009KT 9999 FEW050 40/M03 Q1012 NOSIG
  +37.0 °C GOSP (16.6770, -14.9640) âge 57 min : METAR GOSP 191200Z 04002KT CAVOK 37/14 Q1015
  +37.0 °C FKKR (9.3360, 13.3700) âge 57 min : METAR FKKR 191200Z VRB05KT CAVOK 37/00 Q1011 NOSIG
  +37.0 °C GAMB (14.5120, -4.0840) âge 57 min : METAR GAMB 191200Z 02003KT 010V120 CAVOK 37/M03 Q1014
  +37.0 °C FAKM (-28.8030, 24.7650) âge 57 min : METAR FAKM 191200Z 35006KT 9999 FEW050 37/02 Q1017 NOSIG
  +37.0 °C HKLO (3.1220, 35.6090) âge 57 min : METAR HKLO 191200Z 07007KT 9999 FEW035 BKN280 37/13 Q1007
  +37.0 °C GQNO (18.3100, -15.9700) âge 27 min : METAR GQNO 191230Z 04007KT 360V070 8000 FEW020 37/04 Q1014 NOSIG
  +36.0 °C FYKT (-26.5400, 18.1110) âge 57 min : METAR FYKT 191200Z AUTO 22012KT //// // ////// 36/05 Q1017
  +36.0 °C FAUT (-31.5460, 28.6730) âge 57 min : METAR FAUT 191200Z 01004KT 9999 FEW030 36/13 Q1010
  +36.0 °C DRRN (13.4830, 2.1700) âge 57 min : METAR DRRN 191200Z 09013KT 070V130 CAVOK 36/M03 Q1013 NOSIG
10 plus froides (brut, sans contrôle) :
  -39.0 °C NZSP (-89.9800, 180.0000) âge 67 min : METAR NZSP 191150Z 01016KT 9999 FEW040 M39/ A2850 RMK ALL WNDS GRID SDG/HDG
  -35.0 °C UEEE (62.0930, 129.7740) âge 27 min : METAR UEEE 191230Z 35001MPS 5000 BR NSC M35/M39 Q1028 R23/450173 NOSIG RMK QNH771 QFE762
  -31.0 °C UHMM (59.9110, 150.7250) âge 57 min : METAR UHMM 191200Z 08004MPS 9999 FEW040 M31/M34 Q1011 RMK QNH758 QFE743/0991 R28/08004MPS
  -25.5 °C CXRB (74.7160, -94.9830) âge 57 min : METAR CXRB 191200Z AUTO 33011G16KT M26/M28 RMK AO1 SOG 13 8001 PK WND 33019/1116 SLP083 T1
  -25.0 °C CYBK (64.3060, -96.0780) âge 57 min : METAR CYBK 191200Z 28009KT 15SM SKC M25/M28 A3007 RMK SLP186
  -25.0 °C CYRB (74.7130, -94.9820) âge 57 min : METAR CYRB 191200Z 35022KT 9SM IC DRSN SKC M25/M29 A2972 RMK IC2 PRESFR SLP077
  -25.0 °C CYCB (69.1060, -105.1160) âge 57 min : METAR CYCB 191200Z 31014KT 15SM FEW020 M25/M28 A3011 RMK SC2 CLD HGT EST CEILOMETER BKN SL
  -24.6 °C CYUS (68.7950, -93.4190) âge 57 min : METAR CYUS 191200Z AUTO ///// ////SM ////// M25/M27 A2980 RMK WND MISG VIS MISG CLD MISG T
  -24.2 °C CWPX (69.0360, -107.8230) âge 57 min : METAR CWPX 191200Z AUTO 33021KT ////SM ////// M24/M28 A//// RMK VIS MISG CLD MISG T1242128
  -24.0 °C CYHK (68.6330, -95.8510) âge 57 min : METAR CYHK 191200Z AUTO 32021G26KT 5SM BR CLR M24/M26 A2988 RMK SLP128
```

## 2. API METAR de l'AWC (JSON)

```
GET https://aviationweather.gov/api/data/metar?ids=LFBD,NZSP,OERK,KDRA&format=json → 200 en 0.8 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=1890
4 enregistrements ; clés : ['altim', 'clouds', 'cover', 'dewp', 'elev', 'fltCat', 'icaoId', 'lat', 'lon', 'metarType', 'name', 'obsTime', 'qcField', 'rawOb', 'receiptTime', 'reportTime', 'slp', 'temp', 'visib', 'wdir', 'wspd']
  KDRA 10 °C 2026-11-19T13:00:00.000Z Mercury/Desert Rock, NV, US
  LFBD 11 °C 2026-11-19T12:30:00.000Z Bordeaux/Mérignac Arpt, NA, FR
  NZSP -39 °C 2026-11-19T12:00:00.000Z Amundsen-South Pole, NZ, AQ
  OERK 28 °C 2026-11-19T12:00:00.000Z Riyadh/King Khaled Intl, RD, SA
```

## 2 bis. Noms des stations

```
GET https://aviationweather.gov/data/cache/stations.cache.json.gz → 200 en 0.3 s, 359430 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=359430 ; Last-Modified=Thu, 19 Nov 2026 00:15:24 GMT ; Cache-Control=max-age=30
9960 stations ; exemple : {"id": "32012", "icaoId": null, "iataId": null, "faaId": null, "wmoId": null, "site": "Woods Hole Stratus Wave Station", "lat": 19.691, "lon": -85.567, "elev": 0, "state": "", "country": null, "priority": 4, "siteType": []}
GET https://aviationweather.gov/api/data/stationinfo?ids=FYKT,UEEE,NZSP,LFBD&format=json → 200 en 6.8 s, 826 o
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
GET https://api.open-meteo.com/v1/forecast?latitude=36.46,24.8,31.0,-78.46,-90.0,67.55,44.83,16.677,18.31,-28.399,-89.98,62.093,59.911&longitude=-116.87,46.7,58.3,1… → 200 en 0.2 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Access-Control-Allow-Origin=*
  Vallée de la Mort (36.46, -116.87) : 16.1 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle -58.0 m)
  Riyad (24.8, 46.7) : 26.5 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle 651.0 m)
  Désert de Lut (31.0, 58.3) : 28.1 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle 303.0 m)
  Vostok (-78.46, 106.84) : -34.5 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle 3493.0 m)
  Pôle Sud (-90.0, 0.0) : -32.9 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle 2836.0 m)
  Verkhoïansk (67.55, 133.38) : -30.2 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle 135.0 m)
  Bordeaux-Mérignac (44.83, -0.69) : 12.9 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle 45.0 m)
  METAR GOSP (+37.0 °C) (16.677, -14.964) : 36.7 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle 6.0 m)
  METAR GQNO (+37.0 °C) (18.31, -15.97) : 35.5 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle -1.0 m)
  METAR FAUP (+40.0 °C) (-28.399, 21.26) : 40.9 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle 842.0 m)
  METAR NZSP (-39.0 °C) (-89.98, 180.0) : -32.9 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle 2769.0 m)
  METAR UEEE (-35.0 °C) (62.093, 129.774) : -34.0 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle 97.0 m)
  METAR UHMM (-31.0 °C) (59.911, 150.725) : -22.7 °C à 2026-11-19T12:45 (intervalle 900 s ; altitude du modèle 175.0 m)
requête de 1000 points → 414 en 0.1 s ; b'<html>\r\n<head><title>414 Request-URI Too Large</title></head>\r\n<body>\r\n<center><h1>414 Request-URI Too Large</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'
```
