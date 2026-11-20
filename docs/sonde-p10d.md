# Sonde P10.4 — cohérence physique : données disponibles (généré)

Produit le 20/11/2026 10:36 UTC par `etl/probe/p10d.py`. Inventaire seulement : aucune tendance, aucun rapport.

## 1. Séries déjà publiées sur le site

| Indicateur | Fréquence | Période | Valeurs | Unité | Source |
|---|---|---|---|---|---|
| niveau-mer-monde | annual | 1993-2024 | 32 | mm | NOAA NESDIS STAR — niveau moyen mondial de la mer par altimétrie (TOPEX/Jason/Se |
| ohc-700-monde | annual | 1955-2025 | 71 | 10²² J | NOAA NCEI — contenu thermique de l'océan mondial, 0-700 m |
| ohc-2000-monde | annual | 2005-2025 | 21 | 10²² J | NOAA NCEI — contenu thermique de l'océan mondial, 0-2000 m |
| desequilibre-energetique-monde | annual | 2001-2025 | 25 | W/m² | NASA LaRC — CERES EBAF-TOA Edition 4.2.1 (flux radiatifs au sommet de l'atmosphè |
| tlt-rss-monde | annual | 1979-2025 | 47 | °C | Remote Sensing Systems — RSS 4.0, température de la basse troposphère (satellite |
| tlt-uah-monde | annual | 1979-2025 | 47 | °C | University of Alabama in Huntsville — UAH 6.1, température de la basse troposphè |
| sst-hadsst-monde | annual | 1850-2025 | 176 | °C | Met Office Hadley Centre — HadSST 4.2, température de surface de la mer, moyenne |
| temperature-hadcrut5-monde | annual | 1850-2025 | 176 | °C | Met Office Hadley Centre / CRU — HadCRUT5, température globale |

## 2. Fichiers candidats

### Stratosphère

**RSS 4.0, basse stratosphère (TLS), moyenne mondiale** — https://data.remss.com/msu/graphics/TLS_v40/time_series/RSS_TS_channel_TLS_Global_Land_And_Sea_v04_0.txt
Statut : 200 ; 11900 o

```
Channel = TLS
Region  = Global
Latitude Range =  82.5S to  82.5N
year  mon  TLS Anomaly (K)
------------------------------------------
1978   1  -99.9000
1978   2  -99.9000
1978   3  -99.9000
…
2026   9   -0.4546
2026  10   -0.5331
2026  11  -99.9000
2026  12  -99.9000
```

**UAH 6.1, basse stratosphère (LS)** — https://www.nsstc.uah.edu/data/msu/v6.1/tls/uahncdc_ls_6.1.txt
Statut : 200 ; 102694 o

```
 Year Mo Globe  Land Ocean   NH   Land Ocean   SH   Land Ocean Trpcs  Land Ocean NoExt  Land Ocean SoExt  Land Ocean NoPol  Land Ocean SoPol  Land Ocean USA48 USA49  AUST CANADA
 1978 12  1.14  0.54  1.38  0.55 -0.04  0.92  1.74  1.87  1.71  1.37  1.33  1.39  0.09 -0.39  0.52  1.95  2.23  1.90 -1.13 -1.82 -0.34  2.18  2.38  2.08 -1.21 -1.95  2.97 -3.19
 1979  1  1.14  1.19  1.12  1.00  1.32  0.79  1.29  0.89  1.37  0.75  0.85  0.72  1.11  1.41  0.85  1.59  1.03  1.69 -1.95 -1.45 -2.52  1.14  0.99  1.21  2.34  1.77  0.39 -0.98
 1979  2  0.92  1.03  0.88  1.28  1.38  1.21  0.57  0.23  0.64 -0.14 -0.35 -0.08  2.04  1.86  2.20  0.93  0.60  0.99  4.01  3.65  4.42  0.80  0.77  0.82  1.62  2.13  0.35  4.15
 1979  3  0.99  1.32  0.86  1.09  1.61  0.76  0.88  0.67  0.93  0.13  0.11  0.13  1.65  2.02  1.31  1.23  1.05  1.27  4.36  4.38  4.33  0.95  1.07  0.90  0.59  0.47  0.56 -0.90
 1979  4  1.09  1.03  1.12  0.89  0.89  0.89  1.30  1.34  1.29  0.88  0.90  0.87  0.90  0.91  0.90  1.51  1.59  1.50  1.09  0.88  1.34  0.83  1.03  0.73  0.97  0.43  2.23 -0.76
 1979  5  1.12  1.17  1.11  1.22  1.22  1.22  1.03  1.07  1.02  1.01  1.05  0.99  1.30  1.25  1.35  1.07  1.12  1.06  0.64  0.58  0.71  0.04  0.26 -0.06  1.89  1.79  1.41  0.89
 1979  6  0.99  1.02  0.97  1.18  1.25  1.13  0.79  0.48  0.86  0.69  0.68  0.69  1.41  1.39  1.43  0.87  0.37  0.96  1.15  1.29  0.98 -0.22 -0.37 -0.16  1.44  1.34  1.44  1.47
…
  NOTE:  3/13 More accurate grid weighting for USA48
  NOTE:  3/13 Alaska added in USA49, Australia added
  GL 90S-90N, NH 0-90N, SH 90S-0, TRPCS 20S-20N
  NoExt 20N-90N, SoExt 90S-20S, NoPol 60N-90N, SoPol 90S-60S
```

**RSS 4.0, moyenne troposphère (TMT), information** — https://data.remss.com/msu/graphics/TMT_v40/time_series/RSS_TS_channel_TMT_Global_Land_And_Sea_v04_0.txt
Statut : 200 ; 11900 o

```
Channel = TMT
Region  = Global
Latitude Range =  82.5S to  82.5N
year  mon  TMT Anomaly (K)
------------------------------------------
1978   1  -99.9000
1978   2  -99.9000
1978   3  -99.9000
…
2026   9    0.9021
2026  10    0.9353
2026  11  -99.9000
2026  12  -99.9000
```

## 3. Répertoires et pages candidats

### Vapeur d'eau

**RSS, vapeur d'eau intégrée sur les océans (répertoire)** — https://data.remss.com/vapor/monthly_1deg/
Statut : 200 ; 1045 o

0 liens ; retenus (0) :
```
```

**RSS, vapeur d'eau (répertoire parent)** — https://data.remss.com/vapor/
Statut : 200 ; 664 o

0 liens ; retenus (0) :
```
```

**HadISDH (Met Office), humidité de surface : page d'accueil** — https://www.metoffice.gov.uk/hadobs/hadisdh/
Statut : 200 ; 34930 o

81 liens ; retenus (5) :
```
anomalymapmaterial_qBLEND.html
anomalymapmaterial_qLAND.html
anomalymapmaterial_qMARINE.html
http://www.ncei.noaa.gov
https://www.ncei.noaa.gov/products/land-based-station/us-historical-climatology-network
```

### Niveau marin : dilatation thermique

**NOAA NCEI, contenu thermique et niveau thermostérique, annuel (répertoire)** — https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/yearly/
Statut : 200 ; 5109 o

20 liens ; retenus (19) :
```
h22-a0-100m.dat
h22-a0-2000m.dat
h22-a0-300m.dat
h22-a0-700m.dat
h22-i0-100m.dat
h22-i0-2000m.dat
h22-i0-300m.dat
h22-i0-700m.dat
h22-p0-100m.dat
h22-p0-2000m.dat
h22-p0-300m.dat
h22-p0-700m.dat
h22-w0-100m.dat
h22-w0-2000m.dat
h22-w0-300m.dat
h22-w0-700m.dat
ohc2000m_levitus_climdash_yearly.csv
ohc_levitus_climdash_yearly.csv
ohc_levitus_climdash_yearly.txt
```

**NOAA NCEI, idem, pentadaire (répertoire)** — https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/pentad/
Statut : 200 ; 2771 o

9 liens ; retenus (8) :
```
pent_h22-a0-2000m.dat
pent_h22-a0-700m.dat
pent_h22-i0-2000m.dat
pent_h22-i0-700m.dat
pent_h22-p0-2000m.dat
pent_h22-p0-700m.dat
pent_h22-w0-2000m.dat
pent_h22-w0-700m.dat
```

**NOAA NCEI, idem (répertoire parent)** — https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/
Statut : 200 ; 5222 o

22 liens ; retenus (1) :
```
ohc2000m_levitus_climdash_seasonal.csv
```

### Niveau marin : masse (glaciers, calottes, eaux continentales)

**ESA CCI Sea Level Budget Closure (CEDA, répertoire)** — https://dap.ceda.ac.uk/neodc/esacci/sea_level_budget_closure/data/
Statut : erreur : URLError <urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1011)> ; 0 o

**IMBIE (bilan de masse des calottes), page de téléchargement** — https://imbie.org/data-downloads/
Statut : 404 ; 0 o

**NASA, GRACE / GRACE-FO, masse de l'océan (PO.DAAC)** — https://podaac.jpl.nasa.gov/dataset/OCEAN_MASS_TIME_SERIES_GRACE-FO_JPL_RL06.3_V4
Statut : erreur : URLError <urlopen error _ssl.c:994: The handshake operation timed out> ; 0 o

**NASA Vital Signs, masse des calottes (page)** — https://climate.nasa.gov/vital-signs/ice-sheets/
Statut : 200 ; 275485 o

228 liens ; retenus (10) :
```
https://science.nasa.gov/climate-change/faq/
https://science.nasa.gov/earth/explore/air-quality/
https://science.nasa.gov/wp-content/client-mu-plugins/uswds-framework/uswds/fonts-split/db-mono/aFTU7PB1QTsUX8KYthqQBA.woff2
https://science.nasa.gov/wp-content/client-mu-plugins/uswds-framework/uswds/fonts-split/inter/UcC73FwrK3iLTeHuS_fvQtMwCp50KnMa1ZL7.woff2
https://www.nasa.gov/humans-in-space/astronauts/la-nasa-refuerza-artemis-anade-una-mision-y-perfecciona-su-arquitectura-general/
https://www.nasa.gov/humans-in-space/becoming-an-astronaut-frequently-asked-questions/
https://www.nasa.gov/learning-resources/nasa-astronauts-to-answer-questions-from-florida-students-2/
https://www.nasa.gov/learning-resources/requests-for-exhibits-artifacts-or-speakers/
https://www.nasa.gov/organizations/budget-annual-reports/agency-financial-reports/
https://www.nasa.gov/space-travel-technology/liquid-oxygen-flight-demonstration/
```

