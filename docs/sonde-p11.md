# Sonde P11 — localités extrêmes à l'instant t (généré)

Généré par `python -m etl.probe.p11` le 18/11/2026 15:40 UTC, depuis GitHub Actions. Aucun indicateur, aucun choix.

## 1. METAR mondiaux, fichier cache de l'AWC (NOAA)

```
GET https://aviationweather.gov/data/cache/metars.cache.csv.gz → 200 en 0.1 s, 272088 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=272088 ; Last-Modified=Wed, 18 Nov 2026 15:39:20 GMT ; Cache-Control=max-age=30
5244 lignes ; préambule : []
colonnes : raw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,wind_dir_degrees,wind_speed_kt,wind_gust_kt,visibility_statute_mi,altim_in_hg,sea_level_pressure_mb,corrected,auto,auto_station,maintenance_indicator_on,no_signal,lightning_sensor_off,freezing_rain_sensor_off,present_weather_sensor_off,wx_string,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,flight_category,three_hr_pressure_tendency_mb,maxT_c,minT_c,maxT24hr_c,minT24hr_c,precip_in,pcp3hr_in,pcp6hr_in,pcp24hr_in,snow_in,vert_vis_ft,metar_type,elevation_m
stations : 5243 ; avec température : 5198
âge des observations (min) : médiane 40, 90 % 47, max 80
stations au sud de 60° S : 24 ; au nord de 70° N : 31
10 plus chaudes (brut, sans contrôle) :
  +40.0 °C FYKT (-26.5400, 18.1110) âge 40 min : METAR FYKT 181500Z 17003KT 9999 FEW045 40/M03 Q1014
  +40.0 °C GOSM (15.5970, -13.3260) âge 40 min : METAR GOSM 181500Z 14002KT CAVOK 40/09 Q1011
  +40.0 °C GOSP (16.6770, -14.9640) âge 40 min : METAR GOSP 181500Z 06008KT CAVOK 40/15 Q1011
  +39.0 °C FTTA (9.1440, 18.3740) âge 40 min : METAR FTTA 181500Z 06004KT CAVOK 39/09 Q1008
  +39.0 °C FAUP (-28.3990, 21.2600) âge 40 min : METAR FAUP 181500Z 20009KT CAVOK 39/M06 Q1013 NOSIG
  +39.0 °C GOSS (16.0510, -16.4610) âge 40 min : METAR GOSS 181500Z VRB02KT CAVOK 39/22 Q1011
  +38.0 °C GOOD (14.6500, -16.2300) âge 40 min : METAR GOOD 181500Z 18006KT CAVOK 38/16 Q1011
  +37.0 °C DRRN (13.4830, 2.1700) âge 40 min : METAR DRRN 181500Z 12007KT 090V160 CAVOK 37/M03 Q1011 NOSIG
  +37.0 °C GOOG (15.4000, -15.0840) âge 40 min : METAR GOOG 181500Z 18012KT CAVOK 37/16 Q1009
  +37.0 °C GOTT (13.7330, -13.6570) âge 40 min : METAR GOTT 181500Z 14006KT 090V210 9999 FEW015 37/16 Q1010 NOSIG
10 plus froides (brut, sans contrôle) :
  -38.0 °C UEEE (62.0930, 129.7740) âge 10 min : METAR UEEE 181530Z 02001MPS 0900 0600NE R23/1400N FG NSC M38/M42 Q1026 R23/450176 NOSIG RM
  -31.0 °C UHMM (59.9110, 150.7250) âge 40 min : METAR UHMM 181500Z 08003MPS 9999 NSC M31/M33 Q1011 RMK QNH758 QFE743/0991 R28/08003MPS
  -25.7 °C CXRB (74.7160, -94.9830) âge 40 min : METAR CXRB 181500Z AUTO 36011KT M26/M29 RMK AO1 9PAST HR SOG 13 6001 PK WND 02019/1402 SLP
  -25.0 °C CYCB (69.1060, -105.1160) âge 8 min : SPECI CYCB 181532Z 29012KT 15SM FEW002 M25/M28 A3005 RMK SF2 SLP183
  -25.0 °C CYLT (82.5120, -62.3170) âge 40 min : METAR CYLT 181500Z 33010G15KT 1 1/2SM IC DRSN SCT003 M25/M27 A3000 RMK ST3 DENSITY ALT -51
  -25.0 °C CYYH (69.5430, -93.5680) âge 40 min : METAR CYYH 181500Z 31013KT 15SM DRSN SCT130 M25/M28 A2982 RMK AC3 SLP104
  -25.0 °C CYBK (64.3060, -96.0780) âge 40 min : METAR CYBK 181500Z 28006KT 230V320 25SM FEW012 FEW025 M25/M28 A3009 RMK SC1SC1 SC TR SLP19
  -25.0 °C CYHK (68.6330, -95.8510) âge 40 min : METAR CYHK 181500Z 28010KT 10SM SCT012 M25/M27 A2991 RMK ST2 SLP137
  -25.0 °C CYRB (74.7130, -94.9820) âge 40 min : METAR CYRB 181500Z 03020KT 15SM IC DRSN SKC M25/M29 A2974 RMK SLP085
  -24.4 °C CZRP (75.3770, -105.7150) âge 40 min : METAR CZRP 181500Z AUTO 32023KT M24/M27 RMK AO1 SOG 86 3002 PK WND 32029/1428 SLP161 T1244
```

## 2. API METAR de l'AWC (JSON)

```
GET https://aviationweather.gov/api/data/metar?ids=LFBD,NZSP,OERK,KDRA&format=json → 200 en 9.5 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=1751
4 enregistrements ; clés : ['altim', 'clouds', 'cover', 'dewp', 'elev', 'fltCat', 'icaoId', 'lat', 'lon', 'metarType', 'name', 'obsTime', 'presTend', 'qcField', 'rawOb', 'receiptTime', 'reportTime', 'slp', 'temp', 'visib', 'wdir', 'wspd']
  KDRA 2.2 °C 2026-11-18T15:00:00.000Z Mercury/Desert Rock, NV, US
  LFBD 16 °C 2026-11-18T15:30:00.000Z Bordeaux/Mérignac Arpt, NA, FR
  NZSP -39 °C 2026-11-18T12:00:00.000Z Amundsen-South Pole, NZ, AQ
  OERK 23 °C 2026-11-18T15:00:00.000Z Riyadh/King Khaled Intl, RD, SA
```

## 2 bis. Noms des stations

```
GET https://aviationweather.gov/data/cache/stations.cache.json.gz → 200 en 0.1 s, 359430 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=359430 ; Last-Modified=Wed, 18 Nov 2026 00:15:06 GMT ; Cache-Control=max-age=30
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
GET https://api.open-meteo.com/v1/forecast?latitude=36.46,24.8,31.0,-78.46,-90.0,67.55,44.83,-26.54,15.597,16.677,62.093,59.911,74.716&longitude=-116.87,46.7,58.3,1… → 200 en 0.1 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Access-Control-Allow-Origin=*
  Vallée de la Mort (36.46, -116.87) : 10.4 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle -58.0 m)
  Riyad (24.8, 46.7) : 24.2 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 651.0 m)
  Désert de Lut (31.0, 58.3) : 23.1 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 303.0 m)
  Vostok (-78.46, 106.84) : -37.3 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 3493.0 m)
  Pôle Sud (-90.0, 0.0) : -31.7 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 2836.0 m)
  Verkhoïansk (67.55, 133.38) : -29.9 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 135.0 m)
  Bordeaux-Mérignac (44.83, -0.69) : 16.2 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 45.0 m)
  METAR FYKT (+40.0 °C) (-26.54, 18.111) : 39.1 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 1060.0 m)
  METAR GOSM (+40.0 °C) (15.597, -13.326) : 36.6 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 24.0 m)
  METAR GOSP (+40.0 °C) (16.677, -14.964) : 38.1 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 6.0 m)
  METAR UEEE (-38.0 °C) (62.093, 129.774) : -35.9 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 97.0 m)
  METAR UHMM (-31.0 °C) (59.911, 150.725) : -22.9 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 175.0 m)
  METAR CXRB (-25.7 °C) (74.716, -94.983) : -24.8 °C à 2026-11-18T15:30 (intervalle 900 s ; altitude du modèle 66.0 m)
requête de 1000 points → 414 en 0.1 s ; b'<html>\r\n<head><title>414 Request-URI Too Large</title></head>\r\n<body>\r\n<center><h1>414 Request-URI Too Large</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'
```
