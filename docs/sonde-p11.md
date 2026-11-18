# Sonde P11 — localités extrêmes à l'instant t (généré)

Généré par `python -m etl.probe.p11` le 18/11/2026 11:55 UTC, depuis GitHub Actions. Aucun indicateur, aucun choix.

## 1. METAR mondiaux, fichier cache de l'AWC (NOAA)

```
GET https://aviationweather.gov/data/cache/metars.cache.csv.gz → 200 en 0.1 s, 257046 o
en-têtes : Content-Type=application/octet-stream ; Content-Length=257046 ; Last-Modified=Wed, 18 Nov 2026 11:54:14 GMT ; Cache-Control=max-age=30
5089 lignes ; préambule : []
colonnes : raw_text,station_id,observation_time,latitude,longitude,temp_c,dewpoint_c,wind_dir_degrees,wind_speed_kt,wind_gust_kt,visibility_statute_mi,altim_in_hg,sea_level_pressure_mb,corrected,auto,auto_station,maintenance_indicator_on,no_signal,lightning_sensor_off,freezing_rain_sensor_off,present_weather_sensor_off,wx_string,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,sky_cover,cloud_base_ft_agl,flight_category,three_hr_pressure_tendency_mb,maxT_c,minT_c,maxT24hr_c,minT24hr_c,precip_in,pcp3hr_in,pcp6hr_in,pcp24hr_in,snow_in,vert_vis_ft,metar_type,elevation_m
stations : 5088 ; avec température : 5052
âge des observations (min) : médiane 35, 90 % 62, max 85
stations au sud de 60° S : 22 ; au nord de 70° N : 29
10 plus chaudes (brut, sans contrôle) :
  +39.0 °C FYKT (-26.5400, 18.1110) âge 55 min : METAR FYKT 181100Z AUTO 36008KT //// // ////// 39/M02 Q1016
  +38.0 °C FAUP (-28.3990, 21.2600) âge 55 min : METAR FAUP 181100Z 12002KT CAVOK 38/M02 Q1015 NOSIG
  +36.0 °C FALW (-32.9720, 18.1580) âge 55 min : METAR FALW 181100Z AUTO 24009KT //// // ////// 36/08 Q1009
  +36.0 °C FYOA (-17.8780, 15.9530) âge 55 min : METAR FYOA 181100Z 08010KT CAVOK 36/11 Q1013
  +36.0 °C FTTJ (12.1340, 15.0340) âge 55 min : METAR FTTJ 181100Z 06011KT 020V100 7000 NSC 36/M01 Q1011 NOSIG
  +36.0 °C FBMN (-19.9730, 23.4310) âge 55 min : METAR FBMN 181100Z 07011KT 040V100 9999 SCT030 36/14 Q1017
  +35.0 °C GAMB (14.5120, -4.0840) âge 55 min : METAR GAMB 181100Z 12008KT CAVOK 35/M03 Q1013
  +35.0 °C FKKR (9.3360, 13.3700) âge 55 min : METAR FKKR 181100Z VRB04KT CAVOK 35/06 Q1011 NOSIG
  +35.0 °C DRRN (13.4830, 2.1700) âge 55 min : METAR DRRN 181100Z 08008KT 9000 NSC 35/M03 Q1014 NOSIG
  +35.0 °C DRRT (14.8780, 5.2700) âge 55 min : METAR DRRT 181100Z 07010KT 010V090 CAVOK 35/M04 Q1015
10 plus froides (brut, sans contrôle) :
  -38.0 °C UEEE (62.0930, 129.7740) âge 25 min : METAR UEEE 181130Z 32001MPS 1100 R23/P2000N BR NSC M38/M41 Q1026 R23/450171 NOSIG RMK QNH7
  -30.0 °C UERR (62.5380, 114.0560) âge 25 min : METAR UERR 181130Z 21002MPS 9999 FEW010 M30/M33 Q1020 R25/820345 NOSIG RMK QFE734/0979
  -30.0 °C UHMM (59.9110, 150.7250) âge 55 min : METAR UHMM 181100Z 09003MPS 9999 NSC M30/M32 Q1011 RMK QNH758 QFE743/0991 R28/10002MPS
  -29.4 °C CXRB (74.7160, -94.9830) âge 55 min : METAR CXRB 181100Z AUTO 29009KT M29/M32 RMK AO1 0PAST HR SOG 13 3002 SLP088 P0004 T1294132
  -26.0 °C CYCB (69.1060, -105.1160) âge 55 min : METAR CYCB 181100Z 30010KT 15SM FEW120 M26/M29 A3010 RMK AC1 SLP200
  -25.0 °C CYBK (64.3060, -96.0780) âge 55 min : METAR CYBK 181100Z 00000KT 15SM SKC M25/M28 A3010 RMK SLP198
  -25.0 °C CYRB (74.7130, -94.9820) âge 55 min : METAR CYRB 181100Z 34009KT 20SM IC SKC M25/M28 A2974 RMK SLP086
  -24.8 °C CXSE (73.7660, -105.2960) âge 55 min : METAR CXSE 181100Z AUTO 28012KT M25/M28 RMK AO1 SOG 11 3002 PK WND 30020/1021 SLP157 T1248
  -24.0 °C CYHK (68.6330, -95.8510) âge 55 min : METAR CYHK 181100Z AUTO 32020KT 7SM SCT005 M24/M26 A2990 RMK SLP134
  -23.3 °C CZRP (75.3770, -105.7150) âge 55 min : METAR CZRP 181100Z AUTO 32022KT M23/M26 RMK AO1 SOG 86 1009 PK WND 32029/1036 SLP155 T1233
```

## 2. API METAR de l'AWC (JSON)

```
GET https://aviationweather.gov/api/data/metar?ids=LFBD,NZSP,OERK,KDRA&format=json → 200 en 2.8 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=1844
4 enregistrements ; clés : ['altim', 'clouds', 'cover', 'dewp', 'elev', 'fltCat', 'icaoId', 'lat', 'lon', 'metarType', 'name', 'obsTime', 'qcField', 'rawOb', 'receiptTime', 'reportTime', 'slp', 'temp', 'visib', 'wdir', 'wspd']
  KDRA 1.1 °C 2026-11-18T11:00:00.000Z Mercury/Desert Rock, NV, US
  LFBD 17 °C 2026-11-18T11:30:00.000Z Bordeaux/Mérignac Arpt, NA, FR
  NZSP -38 °C 2026-11-18T06:00:00.000Z Amundsen-South Pole, NZ, AQ
  OERK 27 °C 2026-11-18T11:00:00.000Z Riyadh/King Khaled Intl, RD, SA
```

## 3. Open-Meteo, température actuelle du modèle

```
GET https://api.open-meteo.com/v1/forecast?latitude=36.46,24.8,31.0,-78.46,-90.0,67.55,44.83,12.134,-28.399,-26.54,62.093,59.911,62.538&longitude=-116.87,46.7,58.3,… → 429 en 0.0 s
en-têtes : Content-Type=application/json; charset=utf-8 ; Content-Length=86 ; Access-Control-Allow-Origin=*
requête de 1000 points → 414 en 0.0 s ; b'<html>\r\n<head><title>414 Request-URI Too Large</title></head>\r\n<body>\r\n<center><h1>414 Request-URI Too Large</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'
```
