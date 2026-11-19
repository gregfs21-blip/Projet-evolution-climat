# Sonde P11 — localités extrêmes à l'instant t (généré)

Généré par `python -m etl.probe.p11` le 19/11/2026 18:23 UTC, depuis GitHub Actions. Aucun indicateur, aucun choix.

## 1. METAR mondiaux, fichier cache de l'AWC (NOAA)

```
GET https://aviationweather.gov/data/cache/metars.cache.csv.gz → 200 en 0.5 s, 282078 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=282078 ; Last-Modified=Thu, 19 Nov 2026 18:23:08 GMT ; Cache-Control=max-age=30
5229 lignes ; préambule : []
colonnes : raw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,wind_dir_degrees,wind_speed_kt,wind_gust_kt,visibility_statute_mi,altim_in_hg,sea_level_pressure_mb,corrected,auto,auto_station,maintenance_indicator_on,no_signal,lightning_sensor_off,freezing_rain_sensor_off,present_weather_sensor_off,wx_string,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,flight_category,three_hr_pressure_tendency_mb,maxT_c,minT_c,maxT24hr_c,minT24hr_c,precip_in,pcp3hr_in,pcp6hr_in,pcp24hr_in,snow_in,vert_vis_ft,metar_type,elevation_m
stations : 5228 ; avec température : 5185
âge des observations (min) : médiane 24, 90 % 34, max 89
stations au sud de 60° S : 26 ; au nord de 70° N : 32
10 plus chaudes (brut, sans contrôle) :
  +39.0 °C SLAS (-15.9300, -63.1570) âge 24 min : METAR SLAS 191800Z 33015KT 8000 SCT017 BKN200 39/25 Q1008
  +38.0 °C SLRB (-18.3300, -59.7630) âge 24 min : METAR SLRB 191800Z 36015KT 9999 SCT020 BKN200 38/23 Q1009
  +38.0 °C SLJE (-17.8320, -60.7440) âge 24 min : METAR SLJE 191800Z 36008KT 9999 BKN017 FEW023CB 38/23 Q1007
  +38.0 °C SBTE (-5.0600, -42.8240) âge 24 min : METAR SBTE 191800Z 35004KT 9999 BKN025 38/18 Q1006
  +37.0 °C SLSB (-14.8570, -66.7380) âge 24 min : METAR SLSB 191800Z 34018KT 9999 SCT040 37/24 Q1005
  +37.0 °C SPST (-6.5090, -76.3730) âge 24 min : METAR SPST 191800Z 02015KT 9999 FEW015 37/22 Q1008 RMK PP000
  +37.0 °C GOOG (15.4000, -15.0840) âge 24 min : METAR GOOG 191800Z 08008KT CAVOK 37/08 Q1009
  +37.0 °C GOOD (14.6500, -16.2300) âge 24 min : METAR GOOD 191800Z 00000KT CAVOK 37/13 Q1010
  +37.0 °C SBTF (-3.3830, -64.7240) âge 24 min : METAR SBTF 191800Z 06005KT 9999 SCT020 37/25 Q1006
  +36.0 °C SBUF (-9.4000, -38.2500) âge 84 min : METAR SBUF 191700Z 09007KT 9999 FEW043 36/19 Q1010
10 plus froides (brut, sans contrôle) :
  -38.0 °C UEEE (62.0930, 129.7740) âge 24 min : METAR UEEE 191800Z 36001MPS 1700 R23/P2000N BR NSC M38/M41 Q1026 R23/450173 NOSIG RMK QNH7
  -38.0 °C NZSP (-89.9800, 180.0000) âge 34 min : METAR NZSP 191750Z 03012KT 9999 FEW040 M38/ A2846 RMK ALL WNDS GRID SDG/HDG
  -34.0 °C UHMM (59.9110, 150.7250) âge 24 min : METAR UHMM 191800Z 10002MPS 9999 NSC M34/M37 Q1007 RMK QNH755 QFE740/0987 R28/10002MPS
  -27.0 °C CYZS (64.1880, -83.3510) âge 24 min : METAR CYZS 191800Z 34009KT 15SM FEW025 M27/M31 A2971 RMK SC1 SLP075
  -26.0 °C CYRB (74.7130, -94.9820) âge 24 min : METAR CYRB 191800Z 33012KT 9SM IC DRSN SKC M26/M29 A2972 RMK SLP077
  -26.0 °C CXRB (74.7160, -94.9830) âge 24 min : METAR CXRB 191800Z AUTO 35014KT M26/M29 RMK AO1 4PAST HR SOG 13 5003 PK WND 34019/1726 SLP
  -25.0 °C CYCO (67.8170, -115.1350) âge 24 min : METAR CYCO 191800Z 22014KT 15SM IC VCFG FEW013 FEW080 M25/M28 A3037 RMK ST1AC1 ST TR AC TR
  -25.0 °C CYYH (69.5430, -93.5680) âge 24 min : METAR CYYH 191800Z 33022KT 15SM DRSN FEW040 M25/M28 A2976 RMK SC1 OCNL VCBLSN SLP083
  -25.0 °C CYHK (68.6330, -95.8510) âge 24 min : METAR CYHK 191800Z 30017KT 10SM DRSN FEW004 M25/M27 A2990 RMK ST1 ST TR SLP134
  -24.9 °C CWIJ (65.7560, -111.2460) âge 24 min : METAR CWIJ 191800Z AUTO 29004KT M25/M28 RMK AO1 SOG 05 3003 SLP279 T12491276
```

## 2. API METAR de l'AWC (JSON)

```
GET https://aviationweather.gov/api/data/metar?ids=LFBD,NZSP,OERK,KDRA&format=json → 200 en 0.4 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=1967
4 enregistrements ; clés : ['altim', 'clouds', 'cover', 'dewp', 'elev', 'fltCat', 'icaoId', 'lat', 'lon', 'maxT', 'metarType', 'minT', 'name', 'obsTime', 'pcp6hr', 'presTend', 'qcField', 'rawOb', 'receiptTime', 'reportTime', 'slp', 'temp', 'visib', 'wdir', 'wspd']
  KDRA 10 °C 2026-11-19T18:00:00.000Z Mercury/Desert Rock, NV, US
  LFBD 12 °C 2026-11-19T18:00:00.000Z Bordeaux/Mérignac Arpt, NA, FR
  NZSP -38 °C 2026-11-19T18:00:00.000Z Amundsen-South Pole, NZ, AQ
  OERK 19 °C 2026-11-19T18:00:00.000Z Riyadh/King Khaled Intl, RD, SA
```

## 2 bis. Noms des stations

```
GET https://aviationweather.gov/data/cache/stations.cache.json.gz → 200 en 0.3 s, 359430 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=359430 ; Last-Modified=Thu, 19 Nov 2026 00:15:24 GMT ; Cache-Control=max-age=30
9960 stations ; exemple : {"id": "32012", "icaoId": null, "iataId": null, "faaId": null, "wmoId": null, "site": "Woods Hole Stratus Wave Station", "lat": 19.691, "lon": -85.567, "elev": 0, "state": "", "country": null, "priority": 4, "siteType": []}
GET https://aviationweather.gov/api/data/stationinfo?ids=FYKT,UEEE,NZSP,LFBD&format=json → 200 en 0.6 s, 826 o
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
GET https://api.open-meteo.com/v1/forecast?latitude=36.46,24.8,31.0,-78.46,-90.0,67.55,44.83,-17.832,-5.06,-15.93,-89.98,62.093,59.911&longitude=-116.87,46.7,58.3,1… → 200 en 0.0 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Access-Control-Allow-Origin=*
  Vallée de la Mort (36.46, -116.87) : 19.4 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle -58.0 m)
  Riyad (24.8, 46.7) : 22.3 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 651.0 m)
  Désert de Lut (31.0, 58.3) : 20.6 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 303.0 m)
  Vostok (-78.46, 106.84) : -37.5 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 3493.0 m)
  Pôle Sud (-90.0, 0.0) : -33.0 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 2836.0 m)
  Verkhoïansk (67.55, 133.38) : -33.0 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 135.0 m)
  Bordeaux-Mérignac (44.83, -0.69) : 12.1 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 45.0 m)
  METAR SLJE (+38.0 °C) (-17.832, -60.744) : 33.4 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 285.0 m)
  METAR SBTE (+38.0 °C) (-5.06, -42.824) : 37.8 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 59.0 m)
  METAR SLAS (+39.0 °C) (-15.93, -63.157) : 34.0 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 244.0 m)
  METAR NZSP (-38.0 °C) (-89.98, 180.0) : -33.0 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 2769.0 m)
  METAR UEEE (-38.0 °C) (62.093, 129.774) : -34.1 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 97.0 m)
  METAR UHMM (-34.0 °C) (59.911, 150.725) : -25.5 °C à 2026-11-19T18:15 (intervalle 900 s ; altitude du modèle 175.0 m)
requête de 1000 points → 414 en 0.0 s ; b'<html>\r\n<head><title>414 Request-URI Too Large</title></head>\r\n<body>\r\n<center><h1>414 Request-URI Too Large</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'
```
