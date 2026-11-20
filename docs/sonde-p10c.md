# Sonde P10.3 — amplification régionale : données disponibles (généré)

Produit le 20/11/2026 10:57 UTC par `etl/probe/p10c.py`. Inventaire seulement : aucun facteur, aucune régression.

## 1. Séries publiées sur le site

| Indicateur | Période | Valeurs | Années manquantes | Années brutes | Référence |
|---|---|---|---|---|---|
| france/tm-france | 1959-2021 | 63 | aucune | aucune | 1961-1990 |
| france/tx-france | 1959-2021 | 63 | aucune | aucune | 1961-1990 |
| france/tn-france | 1959-2021 | 63 | aucune | aucune | 1961-1990 |
| gironde/tm-annuelle-gironde | 1953-2024 | 72 | aucune | 2023, 2024 | 1961-1990 |
| gironde/tx-annuelle-gironde | 1953-2024 | 72 | aucune | 2023, 2024 | 1961-1990 |
| gironde/tn-annuelle-gironde | 1953-2024 | 72 | aucune | 2023, 2024 | 1961-1990 |
| gironde/tm-annuelle-bordeaux-merignac | 1953-2024 | 72 | aucune | 2023, 2024 | 1961-1990 |
| gironde/tm-annuelle-cap-ferret | 1953-2024 | 72 | aucune | 2023, 2024 | 1961-1990 |
| gironde/tm-annuelle-cazaux | 1953-2024 | 72 | aucune | 2023, 2024 | 1961-1990 |
| gironde/tm-annuelle-villenave-d-ornon | 1953-2024 | 72 | aucune | 2023, 2024 | 1961-1990 |
| gironde/tm-annuelle-bordeaux-paulin | 1962-2024 | 63 | aucune | 2023, 2024 | 1962-1990 |
| monde/temperature-gistemp-monde | 1880-2025 | 146 | aucune | aucune | 1961-1990 |
| monde/temperature-hadcrut5-monde | 1850-2025 | 176 | aucune | aucune | 1961-1990 |
| monde/temperature-berkeley-monde | 1850-2024 | 175 | aucune | aucune | 1961-1990 |

## 2. Réseau France (composite P5, réseau constant 1959-2021)

Postes du réseau : 220.

| Année | Postes avec 12 mois de TN et TX | dont homogénéisés (TN et TX) | Départements couverts |
|---|---|---|---|
| 2019 | 220 | 220 | 88 |
| 2020 | 220 | 220 | 88 |
| 2021 | 220 | 220 | 88 |
| 2022 | 219 | 209 | 88 |
| 2023 | 217 | 57 | 88 |
| 2024 | 217 | 0 | 88 |
| 2025 | 0 | 0 | 0 |

Fin de la période homogénéisée (min TN, TX) : 2021 : 11, 2022 : 152, 2023 : 57.
Production des fichiers TN : 13/03/2 : 220.
Dernier mois présent (TN) : 2022-07 : 1, 2022-12 : 1, 2023-01 : 1, 2024-12 : 217.

## 3. Postes du composite Gironde (LSH)

| Poste | Nom | TN homogénéisé | TX homogénéisé | Dernier mois TN | Dernier mois TX | Mois 2025 (TN/TX) |
|---|---|---|---|---|---|---|
| 33236002 | Cap-Ferret | 1953-2022 | 1953-2022 | 2024-12 | 2024-12 | 0/0 |
| 33281001 | Bordeaux-Merignac | 1953-2022 | 1953-2022 | 2024-12 | 2024-12 | 0/0 |
| 33529001 | Cazaux | 1953-2022 | 1953-2022 | 2024-12 | 2024-12 | 0/0 |
| 33550001 | Villenave D'Ornon-Inrae | 1953-2022 | 1953-2022 | 2024-12 | 2024-12 | 0/0 |

## 4. Températures mondiales des terres émergées

### CRUTEM5 (Met Office / CRU), terres, moyenne mondiale annuelle

URL : https://www.metoffice.gov.uk/hadobs/crutem5/data/CRUTEM.5.0.2.0/diagnostics/CRUTEM.5.0.2.0.summary_series.global.annual.csv
Statut : 200 ; 6768 o

```
Time,Anomaly (deg C),Lower confidence limit (2.5%),Upper confidence limit (97.5%)
1850,,,
1851,,,
1852,,,
1853,,,
…
2022,1.0425435,0.9224144,1.1517144
2023,1.46848,1.3468349,1.578823
2024,1.6332033,1.5055592,1.7496485
2025,1.7044811,1.2550224,2.1507611
```

### Berkeley Earth, terres (TAVG), résumé annuel

URL : https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_summary.txt
Statut : 200 ; 18561 o

```
% This file contains a brief summary of the land-surface average results 
% produced by the Berkeley Averaging method.  Temperatures are in 
% Celsius and reported as anomalies relative to the Jan 1951-Dec 1980
% average. Uncertainties represent the 95% confidence interval for 
% statistical and spatial undersampling effects.
…
  2021       1.242        0.038            1.391           0.038
  2022       1.236        0.043            1.488           0.037
  2023       1.635        0.035              NaN             NaN
  2024       1.830        0.043              NaN             NaN
```

### NOAA Climate at a Glance, terres, annuel

URL : https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land/12/12/1850-2025/data.csv
Statut : 200 ; 1998 o

```
# Title: "Global Land January - December Average Temperature Departures"
# Units: Degrees Celsius
# Base Period: 1901-2000
Year,Departure from Average
1850,-0.52
…
2022,1.37
2023,1.77
2024,1.93
2025,1.75
```

### NASA GISTEMP v4, stations météorologiques seules (Ts)

URL : https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts.csv
Statut : 200 ; 12998 o

```
Station: Global Means
Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D,D-N,DJF,MAM,JJA,SON
1880,-.28,-.49,-.33,-.54,-.24,-.41,-.35,.22,-.40,-.63,-.31,-.30,-.34,***,***,-.37,-.18,-.45
1881,-.69,-.24,-.13,-.06,.17,-.91,-.26,-.25,-.19,-.35,-.43,.12,-.27,-.30,-.41,-.01,-.47,-.32
1882,.13,-.17,-.04,-.55,-.63,-.91,-.57,-.28,-.18,-.24,-.51,-.80,-.40,-.32,.02,-.41,-.59,-.31
…
2023,1.15,1.26,1.49,1.29,1.16,1.38,1.48,1.42,1.88,1.57,1.64,1.61,1.44,1.40,1.15,1.31,1.43,1.70
2024,1.52,1.79,1.65,1.57,1.36,1.40,1.47,1.67,1.46,1.67,1.64,1.67,1.57,1.57,1.64,1.53,1.51,1.59
2025,1.77,1.61,1.69,1.55,1.37,1.36,1.26,1.49,1.60,1.61,1.57,1.36,1.52,1.55,1.68,1.54,1.37,1.59
2026,1.41,1.59,1.58,1.44,1.32,1.38,1.37,1.74,1.54,1.76,***,***,***,***,1.45,1.45,1.50,***
```

