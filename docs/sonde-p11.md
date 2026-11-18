# Sonde P11 — localités extrêmes à l'instant t (généré)

Généré par `python -m etl.probe.p11` le 18/11/2026 11:58 UTC, depuis GitHub Actions. Aucun indicateur, aucun choix.

## 1. METAR mondiaux, fichier cache de l'AWC (NOAA)

```
GET https://aviationweather.gov/data/cache/metars.cache.csv.gz → 200 en 0.0 s, 269336 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=269336 ; Last-Modified=Wed, 18 Nov 2026 11:57:13 GMT ; Cache-Control=max-age=30
5097 lignes ; préambule : []
colonnes : raw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,wind_dir_degrees,wind_speed_kt,wind_gust_kt,visibility_statute_mi,altim_in_hg,sea_level_pressure_mb,corrected,auto,auto_station,maintenance_indicator_on,no_signal,lightning_sensor_off,freezing_rain_sensor_off,present_weather_sensor_off,wx_string,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,flight_category,three_hr_pressure_tendency_mb,maxT_c,minT_c,maxT24hr_c,minT24hr_c,precip_in,pcp3hr_in,pcp6hr_in,pcp24hr_in,snow_in,vert_vis_ft,metar_type,elevation_m
stations : 5096 ; avec température : 5061
âge des observations (min) : médiane 27, 90 % 59, max 89
stations au sud de 60° S : 22 ; au nord de 70° N : 29
10 plus chaudes (brut, sans contrôle) :
  +39.0 °C FYKT (-26.5400, 18.1110) âge 59 min : METAR FYKT 181100Z AUTO 36008KT //// // ////// 39/M02 Q1016
  +38.0 °C FAUP (-28.3990, 21.2600) âge 59 min : METAR FAUP 181100Z 12002KT CAVOK 38/M02 Q1015 NOSIG
  +36.0 °C FBMN (-19.9730, 23.4310) âge 59 min : METAR FBMN 181100Z 07011KT 040V100 9999 SCT030 36/14 Q1017
  +36.0 °C FTTJ (12.1340, 15.0340) âge 59 min : METAR FTTJ 181100Z 06011KT 020V100 7000 NSC 36/M01 Q1011 NOSIG
  +36.0 °C FALW (-32.9720, 18.1580) âge 59 min : METAR FALW 181100Z AUTO 24009KT //// // ////// 36/08 Q1009
  +36.0 °C FYOA (-17.8780, 15.9530) âge 59 min : METAR FYOA 181100Z 08010KT CAVOK 36/11 Q1013
  +35.0 °C HTMG (-6.7970, 37.6520) âge 59 min : METAR HTMG 181100Z 07008KT 9999 BKN028 FEW029CB 35/17 Q1013
  +35.0 °C HKLO (3.1220, 35.6090) âge 59 min : METAR HKLO 181100Z 09010KT 9999 FEW033 BKN280 35/13 Q1008
  +35.0 °C HKWJ (1.7400, 40.0870) âge 59 min : METAR HKWJ 181100Z 12008KT 9999 BKN028 35/17 Q1009
  +35.0 °C FTTC (13.8470, 20.8440) âge 59 min : METAR FTTC 181100Z 05006KT CAVOK 35/M00 Q1013
10 plus froides (brut, sans contrôle) :
  -38.0 °C UEEE (62.0930, 129.7740) âge 29 min : METAR UEEE 181130Z 32001MPS 1100 R23/P2000N BR NSC M38/M41 Q1026 R23/450171 NOSIG RMK QNH7
  -30.0 °C UERR (62.5380, 114.0560) âge 29 min : METAR UERR 181130Z 21002MPS 9999 FEW010 M30/M33 Q1020 R25/820345 NOSIG RMK QFE734/0979
  -30.0 °C UHMM (59.9110, 150.7250) âge 59 min : METAR UHMM 181100Z 09003MPS 9999 NSC M30/M32 Q1011 RMK QNH758 QFE743/0991 R28/10002MPS
  -29.4 °C CXRB (74.7160, -94.9830) âge 59 min : METAR CXRB 181100Z AUTO 29009KT M29/M32 RMK AO1 0PAST HR SOG 13 3002 SLP088 P0004 T1294132
  -26.0 °C CYCB (69.1060, -105.1160) âge 59 min : METAR CYCB 181100Z 30010KT 15SM FEW120 M26/M29 A3010 RMK AC1 SLP200
  -25.0 °C CYRB (74.7130, -94.9820) âge 59 min : METAR CYRB 181100Z 34009KT 20SM IC SKC M25/M28 A2974 RMK SLP086
  -25.0 °C CYBK (64.3060, -96.0780) âge 59 min : METAR CYBK 181100Z 00000KT 15SM SKC M25/M28 A3010 RMK SLP198
  -24.8 °C CXSE (73.7660, -105.2960) âge 59 min : METAR CXSE 181100Z AUTO 28012KT M25/M28 RMK AO1 SOG 11 3002 PK WND 30020/1021 SLP157 T1248
  -24.0 °C CYHK (68.6330, -95.8510) âge 59 min : METAR CYHK 181100Z AUTO 32020KT 7SM SCT005 M24/M26 A2990 RMK SLP134
  -23.3 °C CZRP (75.3770, -105.7150) âge 59 min : METAR CZRP 181100Z AUTO 32022KT M23/M26 RMK AO1 SOG 86 1009 PK WND 32029/1036 SLP155 T1233
```

## 2. API METAR de l'AWC (JSON)

```
GET https://aviationweather.gov/api/data/metar?ids=LFBD,NZSP,OERK,KDRA&format=json → 200 en 0.1 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=1918
4 enregistrements ; clés : ['altim', 'clouds', 'cover', 'dewp', 'elev', 'fltCat', 'icaoId', 'lat', 'lon', 'maxT', 'metarType', 'minT', 'name', 'obsTime', 'pcp24hr', 'presTend', 'qcField', 'rawOb', 'receiptTime', 'reportTime', 'slp', 'temp', 'visib', 'wdir', 'wspd']
  KDRA 1.1 °C 2026-11-18T12:00:00.000Z Mercury/Desert Rock, NV, US
  LFBD 17 °C 2026-11-18T11:30:00.000Z Bordeaux/Mérignac Arpt, NA, FR
  OERK 27 °C 2026-11-18T11:00:00.000Z Riyadh/King Khaled Intl, RD, SA
  NZSP -38 °C 2026-11-18T06:00:00.000Z Amundsen-South Pole, NZ, AQ
```

## 2 bis. Noms des stations

```
GET https://aviationweather.gov/data/cache/stations.cache.json.gz → 200 en 0.1 s, 359430 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=359430 ; Last-Modified=Wed, 18 Nov 2026 00:15:06 GMT ; Cache-Control=max-age=30
9960 stations ; exemple : {"id": "32012", "icaoId": null, "iataId": null, "faaId": null, "wmoId": null, "site": "Woods Hole Stratus Wave Station", "lat": 19.691, "lon": -85.567, "elev": 0, "state": "", "country": null, "priority": 4, "siteType": []}
GET https://aviationweather.gov/api/data/stationinfo?ids=FYKT,UEEE,NZSP,LFBD&format=json → 200 en 0.3 s, 826 o
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
GET https://api.open-meteo.com/v1/forecast?latitude=36.46,24.8,31.0,-78.46,-90.0,67.55,44.83,12.134,-28.399,-26.54,62.093,59.911,62.538&longitude=-116.87,46.7,58.3,… → 200 en 0.1 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Access-Control-Allow-Origin=*
  Vallée de la Mort (36.46, -116.87) : 12.2 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle -58.0 m)
  Riyad (24.8, 46.7) : 26.8 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 651.0 m)
  Désert de Lut (31.0, 58.3) : 27.6 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 303.0 m)
  Vostok (-78.46, 106.84) : -35.4 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 3493.0 m)
  Pôle Sud (-90.0, 0.0) : -31.3 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 2836.0 m)
  Verkhoïansk (67.55, 133.38) : -29.9 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 135.0 m)
  Bordeaux-Mérignac (44.83, -0.69) : 17.0 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 45.0 m)
  METAR FTTJ (+36.0 °C) (12.134, 15.034) : 35.4 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 294.0 m)
  METAR FAUP (+38.0 °C) (-28.399, 21.26) : 38.3 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 842.0 m)
  METAR FYKT (+39.0 °C) (-26.54, 18.111) : 39.5 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 1060.0 m)
  METAR UEEE (-38.0 °C) (62.093, 129.774) : -36.1 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 97.0 m)
  METAR UHMM (-30.0 °C) (59.911, 150.725) : -22.7 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 175.0 m)
  METAR UERR (-30.0 °C) (62.538, 114.056) : -25.5 °C à 2026-11-18T11:45 (intervalle 900 s ; altitude du modèle 351.0 m)
requête de 1000 points → 414 en 0.1 s ; b'<html>\r\n<head><title>414 Request-URI Too Large</title></head>\r\n<body>\r\n<center><h1>414 Request-URI Too Large</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'
```
