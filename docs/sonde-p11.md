# Sonde P11 — localités extrêmes à l'instant t (généré)

Généré par `python -m etl.probe.p11` le 19/11/2026 13:45 UTC, depuis GitHub Actions. Aucun indicateur, aucun choix.

## 1. METAR mondiaux, fichier cache de l'AWC (NOAA)

```
GET https://aviationweather.gov/data/cache/metars.cache.csv.gz → 200 en 0.0 s, 264275 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=264275 ; Last-Modified=Thu, 19 Nov 2026 13:44:07 GMT ; Cache-Control=max-age=30
5250 lignes ; préambule : []
colonnes : raw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,wind_dir_degrees,wind_speed_kt,wind_gust_kt,visibility_statute_mi,altim_in_hg,sea_level_pressure_mb,corrected,auto,auto_station,maintenance_indicator_on,no_signal,lightning_sensor_off,freezing_rain_sensor_off,present_weather_sensor_off,wx_string,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,flight_category,three_hr_pressure_tendency_mb,maxT_c,minT_c,maxT24hr_c,minT24hr_c,precip_in,pcp3hr_in,pcp6hr_in,pcp24hr_in,snow_in,vert_vis_ft,metar_type,elevation_m
stations : 5249 ; avec température : 5209
âge des observations (min) : médiane 42, 90 % 52, max 90
stations au sud de 60° S : 25 ; au nord de 70° N : 31
10 plus chaudes (brut, sans contrôle) :
  +41.0 °C FAUP (-28.3990, 21.2600) âge 45 min : METAR FAUP 191300Z 28006KT 9999 SCT050 41/M00 Q1012 NOSIG
  +39.0 °C FLLS (-15.3290, 28.4480) âge 45 min : METAR FLLS 191300Z 11058KT CAVOK FEW080 39/21 Q1010
  +39.0 °C FTTA (9.1440, 18.3740) âge 45 min : METAR FTTA 191300Z 18006KT CAVOK 39/09 Q1010
  +38.0 °C FKKR (9.3360, 13.3700) âge 45 min : METAR FKKR 191300Z VRB02KT CAVOK 38/00 Q1010 NOSIG
  +38.0 °C KTOP (39.0725, -95.6260) âge 25 min : SPECI KTOP 191320Z COR 120/03KT 7SM CLR 38/37 A3028
  +37.0 °C DGLE (9.5540, -0.8620) âge 45 min : METAR DGLE 191300Z 05003KT CAVOK 37/08 Q1010 NOSIG
  +37.0 °C DRRN (13.4830, 2.1700) âge 45 min : METAR DRRN 191300Z 08010KT 050V140 CAVOK 37/M03 Q1012 NOSIG
  +37.0 °C GOTT (13.7330, -13.6570) âge 45 min : METAR GOTT 191300Z 08006KT CAVOK 37/12 Q1012 NOSIG
  +37.0 °C FAKM (-28.8030, 24.7650) âge 45 min : METAR FAKM 191300Z 34007KT 9999 FEW050 37/02 Q1016 NOSIG
  +37.0 °C GQNO (18.3100, -15.9700) âge 15 min : METAR GQNO 191330Z 06010KT 030V090 8000 FEW020 37/05 Q1013 NOSIG
10 plus froides (brut, sans contrôle) :
  -36.0 °C UEEE (62.0930, 129.7740) âge 15 min : METAR UEEE 191330Z 01001MPS 5000 BR NSC M36/M39 Q1027 R23/450173 NOSIG RMK QNH770 QFE762
  -32.0 °C UHMM (59.9110, 150.7250) âge 45 min : METAR UHMM 191300Z 08003MPS 9999 NSC M32/M35 Q1010 RMK QNH758 QFE743/0991 R28/08003MPS
  -26.0 °C CYUT (66.5250, -86.2300) âge 21 min : SPECI CYUT 191324Z 35006KT 15SM FEW030 M26/M30 A2977 RMK SC2 SNW CVR/TRACE LOOSE SLP086
  -26.0 °C CYRB (74.7130, -94.9820) âge 45 min : METAR CYRB 191300Z 33021KT 9SM IC DRSN SKC M26/M29 A2972 RMK IC2 SLP079
  -25.9 °C CXRB (74.7160, -94.9830) âge 45 min : METAR CXRB 191300Z AUTO 32014KT M26/M29 RMK AO1 4PAST HR SOG 13 8010 PK WND 35020/1230 SLP
  -25.0 °C CYCB (69.1060, -105.1160) âge 45 min : METAR CYCB 191300Z 30012KT 15SM FEW020 M25/M28 A3012 RMK SC2 CLD HGT EST CEILOMETER BKN SL
  -25.0 °C CYBK (64.3060, -96.0780) âge 45 min : METAR CYBK 191300Z 27010KT 15SM SKC M25/M28 A3008 RMK SLP192
  -24.0 °C CYRT (62.8110, -92.1000) âge 45 min : METAR CYRT 191300Z 33012KT 15SM FEW003 FEW140 M24/M27 A2999 RMK ST1AC1 AC TR SLP162
  -24.0 °C CYHK (68.6330, -95.8510) âge 45 min : METAR CYHK 191300Z AUTO 32019G25KT 5SM BR FEW004 M24/M26 A2989 RMK SLP131
  -23.9 °C CXWB (65.8790, -89.4460) âge 45 min : METAR CXWB 191300Z AUTO 32011KT M24/M29 RMK AO1 SOG 02 8003 SLP109 T12391286
```

## 2. API METAR de l'AWC (JSON)

```
GET https://aviationweather.gov/api/data/metar?ids=LFBD,NZSP,OERK,KDRA&format=json → 200 en 0.1 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=1868
4 enregistrements ; clés : ['altim', 'clouds', 'cover', 'dewp', 'elev', 'fltCat', 'icaoId', 'lat', 'lon', 'metarType', 'name', 'obsTime', 'qcField', 'rawOb', 'receiptTime', 'reportTime', 'slp', 'temp', 'visib', 'wdir', 'wspd']
  KDRA 10 °C 2026-11-19T13:00:00.000Z Mercury/Desert Rock, NV, US
  LFBD 13 °C 2026-11-19T13:30:00.000Z Bordeaux/Mérignac Arpt, NA, FR
  NZSP -39 °C 2026-11-19T12:00:00.000Z Amundsen-South Pole, NZ, AQ
  OERK 27 °C 2026-11-19T13:00:00.000Z Riyadh/King Khaled Intl, RD, SA
```

## 2 bis. Noms des stations

```
GET https://aviationweather.gov/data/cache/stations.cache.json.gz → 200 en 0.1 s, 359430 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=359430 ; Last-Modified=Thu, 19 Nov 2026 00:15:24 GMT ; Cache-Control=max-age=30
9960 stations ; exemple : {"id": "32012", "icaoId": null, "iataId": null, "faaId": null, "wmoId": null, "site": "Woods Hole Stratus Wave Station", "lat": 19.691, "lon": -85.567, "elev": 0, "state": "", "country": null, "priority": 4, "siteType": []}
GET https://aviationweather.gov/api/data/stationinfo?ids=FYKT,UEEE,NZSP,LFBD&format=json → 200 en 0.1 s, 826 o
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
GET https://api.open-meteo.com/v1/forecast?latitude=36.46,24.8,31.0,-78.46,-90.0,67.55,44.83,-15.329,9.144,-28.399,62.093,59.911,66.525&longitude=-116.87,46.7,58.3,… → 200 en 0.1 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Access-Control-Allow-Origin=*
  Vallée de la Mort (36.46, -116.87) : 16.8 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle -58.0 m)
  Riyad (24.8, 46.7) : 25.8 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 651.0 m)
  Désert de Lut (31.0, 58.3) : 26.4 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 303.0 m)
  Vostok (-78.46, 106.84) : -35.2 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 3493.0 m)
  Pôle Sud (-90.0, 0.0) : -32.4 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 2836.0 m)
  Verkhoïansk (67.55, 133.38) : -30.3 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 135.0 m)
  Bordeaux-Mérignac (44.83, -0.69) : 12.8 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 45.0 m)
  METAR FLLS (+39.0 °C) (-15.329, 28.448) : 27.0 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 1148.0 m)
  METAR FTTA (+39.0 °C) (9.144, 18.374) : 39.1 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 363.0 m)
  METAR FAUP (+41.0 °C) (-28.399, 21.26) : 39.9 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 842.0 m)
  METAR UEEE (-36.0 °C) (62.093, 129.774) : -33.9 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 97.0 m)
  METAR UHMM (-32.0 °C) (59.911, 150.725) : -23.8 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 175.0 m)
  METAR CYUT (-26.0 °C) (66.525, -86.23) : -28.9 °C à 2026-11-19T13:45 (intervalle 900 s ; altitude du modèle 19.0 m)
requête de 1000 points → 414 en 0.1 s ; b'<html>\r\n<head><title>414 Request-URI Too Large</title></head>\r\n<body>\r\n<center><h1>414 Request-URI Too Large</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'
```
