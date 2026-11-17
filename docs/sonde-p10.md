# Sonde P10 — régression multiple : forçages et ENSO (généré)

Généré par `python -m etl.probe.p10` le 17/11/2026 21:16 UTC. Aucune régression, aucun indicateur calculé.

## 1. Dépôt ClimateIndicator/data (v2026.06.02) : racine

```
GET https://api.github.com/repos/ClimateIndicator/data/contents/?ref=v2026.06.02 → 200
  file .gitignore
  file CITATION.cff
  file LICENSE
  file README.md
  dir  data
GET https://api.github.com/repos/ClimateIndicator/data/contents/data?ref=v2026.06.02 → 200
  dir  data/anthropogenic_warming
  dir  data/anthropogenic_warming_by_species
  dir  data/carbon_budget
  dir  data/earth_energy_imbalance
  dir  data/effective_radiative_forcing
  dir  data/extreme_temperatures
  dir  data/global_land_precipitation
  dir  data/global_mean_temperatures
  dir  data/greenhouse_gas_concentrations
  dir  data/greenhouse_gas_emissions
  dir  data/marine_heatwave_days
  dir  data/sea_level_rise
```

## 2. IGCC 2025 : forçages et réchauffement attribué

```
GET https://api.github.com/repos/ClimateIndicator/data/git/trees/v2026.06.02?recursive=1 → 200
42 fichiers, dont 24 retenus (forçage, attribution, température) :
  data/anthropogenic_warming/Assessment-Extrapolation-2026_GMST_headlines.csv
  data/anthropogenic_warming/Assessment-Update-2025_GMST_headlines.csv
  data/anthropogenic_warming/Gillett_GMST_headlines.csv
  data/anthropogenic_warming/Gillett_GMST_rates.csv
  data/anthropogenic_warming/Gillett_GMST_timeseries.csv
  data/anthropogenic_warming/Gillett_GSAT_headlines.csv
  data/anthropogenic_warming/Ribes_GMST_headlines.csv
  data/anthropogenic_warming/Ribes_GMST_rates.csv
  data/anthropogenic_warming/Ribes_GMST_timeseries.csv
  data/anthropogenic_warming/Walsh_GMST_headlines.csv
  data/anthropogenic_warming/Walsh_GMST_rates.csv
  data/anthropogenic_warming/Walsh_GMST_timeseries.csv
  data/anthropogenic_warming/assessment_6thIPCC_headlines.csv
  data/anthropogenic_warming_by_species/ERF_relative_to_1750.csv
  data/anthropogenic_warming_by_species/temperature_relative_to_1750.csv
  data/effective_radiative_forcing/ERF_best.csv
  data/effective_radiative_forcing/ERF_best_aggregates.csv
  data/effective_radiative_forcing/ERF_p05_aggregates.csv
  data/effective_radiative_forcing/ERF_p95_aggregates.csv
  data/extreme_temperatures/txx_decadal_means.csv
  data/extreme_temperatures/txx_timeseries.csv
  data/global_mean_temperatures/annual_averages.csv
  data/global_mean_temperatures/decadal_averages.csv
  data/global_mean_temperatures/twenty_year_averages.csv

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Assessment-Extrapolation-2026_GMST_headlines.csv → 200
data/anthropogenic_warming/Assessment-Extrapolation-2026_GMST_headlines.csv : 7 lignes, 306 o ; début :
  time,timebound_lower,timebound_upper,anthropogenic_p05,anthropogenic_p50,anthropogenic_p95,notes
  2025.5,2025,2026,1.1,1.38,1.7,
  2025.5,2025,2026,1.1,1.37,1.7,SR1.5 definition
  2021,2016,2026,1,1.24,1.5,
  2026.5,2026,2027,1.1,1.41,1.8,
  2026.5,2026,2027,1.1,1.4,1.7,SR1.5 definition
fin :
  2021,2016,2026,1,1.24,1.5,
  2026.5,2026,2027,1.1,1.41,1.8,
  2026.5,2026,2027,1.1,1.4,1.7,SR1.5 definition
  2022,2017,2027,1,1.27,1.5,
colonnes (7) :
  [0] time
  [1] timebound_lower
  [2] timebound_upper
  [3] anthropogenic_p05
  [4] anthropogenic_p50
  [5] anthropogenic_p95
  [6] notes
  2025 : anthropogenic_p05=1.1, anthropogenic_p50=1.38, anthropogenic_p95=1.7

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Assessment-Update-2025_GMST_headlines.csv → 200
data/anthropogenic_warming/Assessment-Update-2025_GMST_headlines.csv : 7 lignes, 683 o ; début :
  time,timebound_lower,timebound_upper,anthropogenic_p05,anthropogenic_p50,anthropogenic_p95,ghg_p05,ghg_p50,ghg_p95,other_human_forcing_p05,other_human_forcing_p50,other_human_forcing_p95,natural_p05,natural_p50,natural_p95,notes
  2015,2010,2020,0.9,1.07,1.3,1,1.39,1.8,-0.8,-0.31,0.1,-0.1,0.05,0.2,
  2021,2016,2026,1,1.24,1.5,1.1,1.52,2,-0.8,-0.28,0.1,-0.1,0.04,0.2,
  2017.5,2017,2018,0.9,1.14,1.4,1,1.44,1.9,-0.8,-0.29,0.1,-0.1,0.05,0.2,
  2025.5,2025,2026,1.1,1.38,1.7,1.1,1.63,2.1,-0.8,-0.26,0.2,-0.1,0.04,0.2,
  2017.5,2017,2018,0.9,1.12,1.3,1,1.44,1.9,-0.8,-0.31,0.1,-0.1,0.05,0.2,SR15 definition
fin :
  2017.5,2017,2018,0.9,1.14,1.4,1,1.44,1.9,-0.8,-0.29,0.1,-0.1,0.05,0.2,
  2025.5,2025,2026,1.1,1.38,1.7,1.1,1.63,2.1,-0.8,-0.26,0.2,-0.1,0.04,0.2,
  2017.5,2017,2018,0.9,1.12,1.3,1,1.44,1.9,-0.8,-0.31,0.1,-0.1,0.05,0.2,SR15 definition
  2025.5,2025,2026,1.1,1.37,1.7,1.1,1.63,2.1,-0.8,-0.26,0.2,-0.1,0.04,0.2,SR15 definition
colonnes (16) :
  [0] time
  [1] timebound_lower
  [2] timebound_upper
  [3] anthropogenic_p05
  [4] anthropogenic_p50
  [5] anthropogenic_p95
  [6] ghg_p05
  [7] ghg_p50
  [8] ghg_p95
  [9] other_human_forcing_p05
  [10] other_human_forcing_p50
  [11] other_human_forcing_p95
  [12] natural_p05
  [13] natural_p50
  [14] natural_p95
  [15] notes
  2015 : anthropogenic_p05=0.9, anthropogenic_p50=1.07, anthropogenic_p95=1.3, natural_p05=-0.1, natural_p50=0.05, natural_p95=0.2
  2025 : anthropogenic_p05=1.1, anthropogenic_p50=1.38, anthropogenic_p95=1.7, natural_p05=-0.1, natural_p50=0.04, natural_p95=0.2

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Gillett_GMST_headlines.csv → 200
data/anthropogenic_warming/Gillett_GMST_headlines.csv : 7 lignes, 1599 o ; début :
  ﻿time,timebound_lower,timebound_upper,anthropogenic_p05,anthropogenic_p17,anthropogenic_p50,anthropogenic_p83,anthropogenic_p95,natural_p05,natural_p17,natural_p50,natural_p83,natural_p95,ghg_p05,ghg_p17,ghg_p50,ghg_p83,ghg_p95,other_human_forcing_p05,other_human_forcing_p17,other_human_forcing_p50,other_human_forcing_p83,other_human_forcing_p95,notes
  2017.5,2017,2018,1.013816688,1.077168433,1.164654178,1.252563993,1.316222825,-0.029452815,-0.011717806,0.012773395,0.037261217,0.054993778,1.217689689,1.307658643,1.431901484,1.557788519,1.648948095,-0.445984712,-0.362314753,-0.246770525,-0.132820721,-0.050305346,
  2025.5,2025,2026,1.248562704,1.342936944,1.473263275,1.604045436,1.69874976,-0.03897271,-0.019628456,0.007085037,0.033797577,0.05314114,1.402155767,1.503703242,1.64393547,1.786087344,1.889024908,-0.377392924,-0.299379676,-0.191647096,-0.084943706,-0.007675734,
  2017.5,2017,2018,1.003753495,,1.133375586,,1.263802828,-0.015714771,,0.017260603,,0.050222353,1.213358345,,1.419578158,,1.628663907,-0.457423262,,-0.258957288,,-0.063522521,SR15 definition
  2025.5,2025,2026,1.260824463,,1.438263252,,1.616649635,-0.040397108,,0.004767852,,0.049932053,1.398582265,,1.635312094,,1.875385931,-0.380141519,,-0.209003167,,-0.040167614,SR15 definition
  2015,2010,2020,0.971303193,,1.096467458,,1.222412159,-0.016636539,,0.01808896,,0.052800248,1.175333341,,1.373290611,,1.574068063,-0.441564027,,-0.250481712,,-0.062354725,
fin :
  2017.5,2017,2018,1.003753495,,1.133375586,,1.263802828,-0.015714771,,0.017260603,,0.050222353,1.213358345,,1.419578158,,1.628663907,-0.457423262,,-0.258957288,,-0.063522521,SR15 definition
  2025.5,2025,2026,1.260824463,,1.438263252,,1.616649635,-0.040397108,,0.004767852,,0.049932053,1.398582265,,1.635312094,,1.875385931,-0.380141519,,-0.209003167,,-0.040167614,SR15 definition
  2015,2010,2020,0.971303193,,1.096467458,,1.222412159,-0.016636539,,0.01808896,,0.052800248,1.175333341,,1.373290611,,1.574068063,-0.441564027,,-0.250481712,,-0.062354725,
  2021,2016,2026,1.138217335,,1.29037283,,1.4434176,-0.028658595,,0.009862266,,0.048379318,1.303231338,,1.521970002,,1.74401808,-0.404105719,,-0.226972737,,-0.052505646,
colonnes (24) :
  [0] ﻿time
  [1] timebound_lower
  [2] timebound_upper
  [3] anthropogenic_p05
  [4] anthropogenic_p17
  [5] anthropogenic_p50
  [6] anthropogenic_p83
  [7] anthropogenic_p95
  [8] natural_p05
  [9] natural_p17
  [10] natural_p50
  [11] natural_p83
  [12] natural_p95
  [13] ghg_p05
  [14] ghg_p17
  [15] ghg_p50
  [16] ghg_p83
  [17] ghg_p95
  [18] other_human_forcing_p05
  [19] other_human_forcing_p17
  [20] other_human_forcing_p50
  [21] other_human_forcing_p83
  [22] other_human_forcing_p95
  [23] notes
  2015 : anthropogenic_p05=0.971303193, anthropogenic_p17=, anthropogenic_p50=1.096467458, anthropogenic_p83=, anthropogenic_p95=1.222412159, natural_p05=-0.016636539, natural_p17=, natural_p50=0.01808896, natural_p83=, natural_p95=0.052800248
  2025 : anthropogenic_p05=1.248562704, anthropogenic_p17=1.342936944, anthropogenic_p50=1.473263275, anthropogenic_p83=1.604045436, anthropogenic_p95=1.69874976, natural_p05=-0.03897271, natural_p17=-0.019628456, natural_p50=0.007085037, natural_p83=0.033797577, natural_p95=0.05314114

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Gillett_GMST_rates.csv → 200
data/anthropogenic_warming/Gillett_GMST_rates.csv : 3 lignes, 193 o ; début :
  time,timebound_lower,timebound_upper,anthropogenic_p05,anthropogenic_p50,anthropogenic_p95
  2015,2010,2020,0.016442612,0.026636931,0.036836921
  2021,2016,2026,0.025183996,0.039441928,0.053708749
fin :
  time,timebound_lower,timebound_upper,anthropogenic_p05,anthropogenic_p50,anthropogenic_p95
  2015,2010,2020,0.016442612,0.026636931,0.036836921
  2021,2016,2026,0.025183996,0.039441928,0.053708749
colonnes (6) :
  [0] time
  [1] timebound_lower
  [2] timebound_upper
  [3] anthropogenic_p05
  [4] anthropogenic_p50
  [5] anthropogenic_p95
  2015 : anthropogenic_p05=0.016442612, anthropogenic_p50=0.026636931, anthropogenic_p95=0.036836921

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Gillett_GMST_timeseries.csv → 200
data/anthropogenic_warming/Gillett_GMST_timeseries.csv : 177 lignes, 46521 o ; début :
  time,timebound_lower,timebound_upper,anthropogenic_p05,anthropogenic_p17,anthropogenic_p50,anthropogenic_p83,anthropogenic_p95,natural_p05,natural_p17,natural_p50,natural_p83,natural_p95,ghg_p05,ghg_p17,ghg_p50,ghg_p83,ghg_p95,other_human_forcing_p05,other_human_forcing_p17,other_human_forcing_p50,other_human_forcing_p83,other_human_forcing_p95
  1850.5,1850,1851,-0.164278772,-0.119981787,-0.058809761,0.002360716,0.046656578,-0.058630106,-0.040385865,-0.015191435,0.01000764,0.028255246,-0.123017322,-0.105104714,-0.080368256,-0.055659471,-0.037766903,-0.059689013,-0.026947796,0.018266266,0.063502906,0.096260473
  1851.5,1851,1852,-0.169634469,-0.136928615,-0.091763387,-0.046603272,-0.013901119,-0.014071346,0.000772179,0.021270381,0.041757383,0.056592798,-0.086469156,-0.067546033,-0.041414101,-0.015289123,0.003628966,-0.097597243,-0.070031897,-0.031965467,0.006018727,0.033524523
  1852.5,1852,1853,-0.157579713,-0.122297395,-0.073574193,-0.024854038,0.010426075,-0.002755871,0.014265409,0.037770987,0.061245756,0.078244726,-0.082038669,-0.060098834,-0.029800966,0.000493796,0.022431383,-0.098892009,-0.069151008,-0.028080102,0.012932009,0.042630434
  1853.5,1853,1854,-0.112444934,-0.085060492,-0.047243882,-0.00942889,0.01795438,-0.017313566,5.60E-05,0.024042558,0.048016882,0.065377599,-0.113744955,-0.092158279,-0.062348107,-0.032551751,-0.01097508,-0.044668716,-0.020414414,0.013079622,0.046589285,0.070854904
  1854.5,1854,1855,-0.173903583,-0.10643015,-0.013252553,0.079924992,0.147398388,-0.019387967,-0.002728314,0.020277875,0.043274995,0.059928082,-0.116971302,-0.096342788,-0.067855793,-0.039385923,-0.01876981,-0.077349533,-0.028092034,0.039930225,0.108024181,0.157333597
fin :
  2022.5,2022,2023,1.167116188,1.234720837,1.328079637,1.421954984,1.489933684,-0.062551016,-0.041559504,-0.012571225,0.016419818,0.037413333,1.329661736,1.425178194,1.557081873,1.690918362,1.78783444,-0.408485101,-0.332204516,-0.226864659,-0.123030809,-0.047840779
  2023.5,2023,2024,1.132693247,1.225351951,1.353309208,1.48165828,1.574600712,-0.047833523,-0.025619751,0.005056411,0.035732149,0.057945615,1.354513028,1.451907464,1.586404543,1.722869251,1.821688523,-0.441027277,-0.352811284,-0.230989198,-0.110514947,-0.023274971
  2024.5,2024,2025,1.160972712,1.286402535,1.459615148,1.633164653,1.758838433,-0.041096229,-0.0229556,0.002095743,0.027146998,0.045287561,1.382505742,1.483645245,1.623314082,1.7649673,1.867543768,-0.41301002,-0.317661446,-0.185989606,-0.055124233,0.039640348
  2025.5,2025,2026,1.248562673,1.342936926,1.473263275,1.604045436,1.69874976,-0.03897271,-0.019628456,0.007085037,0.033797577,0.05314114,1.40226104,1.5037643,1.64393547,1.786134203,1.8891057,-0.377376088,-0.299369912,-0.191647096,-0.084972822,-0.007725935
colonnes (23) :
  [0] time
  [1] timebound_lower
  [2] timebound_upper
  [3] anthropogenic_p05
  [4] anthropogenic_p17
  [5] anthropogenic_p50
  [6] anthropogenic_p83
  [7] anthropogenic_p95
  [8] natural_p05
  [9] natural_p17
  [10] natural_p50
  [11] natural_p83
  [12] natural_p95
  [13] ghg_p05
  [14] ghg_p17
  [15] ghg_p50
  [16] ghg_p83
  [17] ghg_p95
  [18] other_human_forcing_p05
  [19] other_human_forcing_p17
  [20] other_human_forcing_p50
  [21] other_human_forcing_p83
  [22] other_human_forcing_p95
  1850 : anthropogenic_p05=-0.164278772, anthropogenic_p17=-0.119981787, anthropogenic_p50=-0.058809761, anthropogenic_p83=0.002360716, anthropogenic_p95=0.046656578, natural_p05=-0.058630106, natural_p17=-0.040385865, natural_p50=-0.015191435, natural_p83=0.01000764, natural_p95=0.028255246
  1900 : anthropogenic_p05=0.008039638, anthropogenic_p17=0.041480215, anthropogenic_p50=0.087660058, anthropogenic_p83=0.133844464, anthropogenic_p95=0.167288344, natural_p05=-0.045864033, natural_p17=-0.024081117, natural_p50=0.006000052, natural_p83=0.036080614, natural_p95=0.05786309
  1991 : anthropogenic_p05=0.405680389, anthropogenic_p17=0.464539531, anthropogenic_p50=0.545821202, anthropogenic_p83=0.627203302, anthropogenic_p95=0.686135168, natural_p05=-0.08136794, natural_p17=-0.059297855, natural_p50=-0.028820119, natural_p83=0.001671438, natural_p95=0.023751531
  2000 : anthropogenic_p05=0.601369179, anthropogenic_p17=0.661013204, anthropogenic_p50=0.743378763, anthropogenic_p83=0.825928063, anthropogenic_p95=0.885705143, natural_p05=-0.027550295, natural_p17=-0.001267404, natural_p50=0.035028016, natural_p83=0.071306285, natural_p95=0.097576755
  2015 : anthropogenic_p05=0.906732394, anthropogenic_p17=0.96637614, anthropogenic_p50=1.048741313, anthropogenic_p83=1.131471784, anthropogenic_p95=1.191380057, natural_p05=-0.026566026, natural_p17=-0.004940232, natural_p50=0.024923961, natural_p83=0.0547776, natural_p95=0.076395753
  2020 : anthropogenic_p05=0.987270637, anthropogenic_p17=1.100213649, anthropogenic_p50=1.25618257, anthropogenic_p83=1.412428629, anthropogenic_p95=1.525572328, natural_p05=-0.03976164, natural_p17=-0.014060713, natural_p50=0.021431043, natural_p83=0.056916234, natural_p95=0.082612407
  2023 : anthropogenic_p05=1.132693247, anthropogenic_p17=1.225351951, anthropogenic_p50=1.353309208, anthropogenic_p83=1.48165828, anthropogenic_p95=1.574600712, natural_p05=-0.047833523, natural_p17=-0.025619751, natural_p50=0.005056411, natural_p83=0.035732149, natural_p95=0.057945615
  2024 : anthropogenic_p05=1.160972712, anthropogenic_p17=1.286402535, anthropogenic_p50=1.459615148, anthropogenic_p83=1.633164653, anthropogenic_p95=1.758838433, natural_p05=-0.041096229, natural_p17=-0.0229556, natural_p50=0.002095743, natural_p83=0.027146998, natural_p95=0.045287561
  2025 : anthropogenic_p05=1.248562673, anthropogenic_p17=1.342936926, anthropogenic_p50=1.473263275, anthropogenic_p83=1.604045436, anthropogenic_p95=1.69874976, natural_p05=-0.03897271, natural_p17=-0.019628456, natural_p50=0.007085037, natural_p83=0.033797577, natural_p95=0.05314114

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Gillett_GSAT_headlines.csv → 200
data/anthropogenic_warming/Gillett_GSAT_headlines.csv : 5 lignes, 1105 o ; début :
  ﻿time,timebound_lower,timebound_upper,anthropogenic_p05,anthropogenic_p17,anthropogenic_p50,anthropogenic_p83,anthropogenic_p95,natural_p05,natural_p17,natural_p50,natural_p83,natural_p95,ghg_p05,ghg_p17,ghg_p50,ghg_p83,ghg_p95,other_human_forcing_p05,other_human_forcing_p17,other_human_forcing_p50,other_human_forcing_p83,other_human_forcing_p95,notes
  2015,2010,2020,1.020927511, ,1.152113142, ,1.284120874,-0.017891696, ,0.018507825, ,0.054893153,1.225017916, ,1.431214654, ,1.640428278,-0.449153213, ,-0.254719547, ,-0.063309452,
  2021,2016,2026,1.197184122, ,1.356403983, ,1.516562839,-0.03020414, ,0.009842823, ,0.049886138,1.360832307, ,1.589280729, ,1.821062129,-0.411439177, ,-0.230976288, ,-0.053232739,
  2017.5,2017,2018,1.055909182, ,1.191421157, ,1.327784175,-0.01679392, ,0.017849898, ,0.052479845,1.264976908, ,1.47989278, ,1.697788718,-0.465181695, ,-0.263300448, ,-0.064633006,SR15 definition
  2025.5,2025,2026,1.327535084, ,1.512838256, ,1.699145317,-0.042118378, ,0.004299893, ,0.050717563,1.4621945, ,1.709583949, ,1.960577083,-0.386446394, ,-0.212266063, ,-0.040430533,SR15 definition
fin :
  2015,2010,2020,1.020927511, ,1.152113142, ,1.284120874,-0.017891696, ,0.018507825, ,0.054893153,1.225017916, ,1.431214654, ,1.640428278,-0.449153213, ,-0.254719547, ,-0.063309452,
  2021,2016,2026,1.197184122, ,1.356403983, ,1.516562839,-0.03020414, ,0.009842823, ,0.049886138,1.360832307, ,1.589280729, ,1.821062129,-0.411439177, ,-0.230976288, ,-0.053232739,
  2017.5,2017,2018,1.055909182, ,1.191421157, ,1.327784175,-0.01679392, ,0.017849898, ,0.052479845,1.264976908, ,1.47989278, ,1.697788718,-0.465181695, ,-0.263300448, ,-0.064633006,SR15 definition
  2025.5,2025,2026,1.327535084, ,1.512838256, ,1.699145317,-0.042118378, ,0.004299893, ,0.050717563,1.4621945, ,1.709583949, ,1.960577083,-0.386446394, ,-0.212266063, ,-0.040430533,SR15 definition
colonnes (24) :
  [0] ﻿time
  [1] timebound_lower
  [2] timebound_upper
  [3] anthropogenic_p05
  [4] anthropogenic_p17
  [5] anthropogenic_p50
  [6] anthropogenic_p83
  [7] anthropogenic_p95
  [8] natural_p05
  [9] natural_p17
  [10] natural_p50
  [11] natural_p83
  [12] natural_p95
  [13] ghg_p05
  [14] ghg_p17
  [15] ghg_p50
  [16] ghg_p83
  [17] ghg_p95
  [18] other_human_forcing_p05
  [19] other_human_forcing_p17
  [20] other_human_forcing_p50
  [21] other_human_forcing_p83
  [22] other_human_forcing_p95
  [23] notes
  2015 : anthropogenic_p05=1.020927511, anthropogenic_p17=, anthropogenic_p50=1.152113142, anthropogenic_p83=, anthropogenic_p95=1.284120874, natural_p05=-0.017891696, natural_p17=, natural_p50=0.018507825, natural_p83=, natural_p95=0.054893153
  2025 : anthropogenic_p05=1.327535084, anthropogenic_p17=, anthropogenic_p50=1.512838256, anthropogenic_p83=, anthropogenic_p95=1.699145317, natural_p05=-0.042118378, natural_p17=, natural_p50=0.004299893, natural_p83=, natural_p95=0.050717563

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Ribes_GMST_headlines.csv → 200
data/anthropogenic_warming/Ribes_GMST_headlines.csv : 7 lignes, 1446 o ; début :
  time,timebound_lower,timebound_upper,natural_p05,natural_p17,natural_p50,natural_p83,natural_p95,ghg_p05,ghg_p17,ghg_p50,ghg_p83,ghg_p95,other_human_forcing_p05,other_human_forcing_p17,other_human_forcing_p50,other_human_forcing_p83,other_human_forcing_p95,total_p05,total_p17,total_p50,total_p83,total_p95,anthropogenic_p05,anthropogenic_p17,anthropogenic_p50,anthropogenic_p83,anthropogenic_p95,
  2017.5,2017,2018,0.042,0.05,0.06,0.072,0.081,1.203,1.358,1.541,1.705,1.86,-0.71,-0.57,-0.42,-0.249,-0.122,1.048,1.102,1.182,1.256,1.307,0.984,1.041,1.122,1.193,1.247,
  2025.5,2025,2026,0.03,0.036,0.044,0.052,0.059,1.337,1.525,1.728,1.913,2.088,-0.705,-0.559,-0.391,-0.208,-0.065,1.221,1.292,1.381,1.464,1.533,1.176,1.248,1.337,1.421,1.491,
  2017.5,2017,2018,0.043,0.051,0.061,0.073,0.082,1.203,1.358,1.541,1.705,1.859,-0.716,-0.575,-0.424,-0.255,-0.126,1.045,1.1,1.179,1.253,1.304,0.979,1.037,1.117,1.188,1.242,SR15 definition
  2025.5,2025,2026,0.028,0.033,0.041,0.048,0.054,1.337,1.525,1.728,1.913,2.088,-0.708,-0.562,-0.394,-0.209,-0.069,1.215,1.285,1.375,1.458,1.527,1.174,1.245,1.334,1.417,1.488,SR15 definition
  2015,2010,2020,0.042,0.05,0.061,0.072,0.081,1.162,1.308,1.483,1.642,1.788,-0.71,-0.571,-0.425,-0.262,-0.137,0.988,1.041,1.119,1.19,1.244,0.924,0.983,1.058,1.128,1.181,
fin :
  2017.5,2017,2018,0.043,0.051,0.061,0.073,0.082,1.203,1.358,1.541,1.705,1.859,-0.716,-0.575,-0.424,-0.255,-0.126,1.045,1.1,1.179,1.253,1.304,0.979,1.037,1.117,1.188,1.242,SR15 definition
  2025.5,2025,2026,0.028,0.033,0.041,0.048,0.054,1.337,1.525,1.728,1.913,2.088,-0.708,-0.562,-0.394,-0.209,-0.069,1.215,1.285,1.375,1.458,1.527,1.174,1.245,1.334,1.417,1.488,SR15 definition
  2015,2010,2020,0.042,0.05,0.061,0.072,0.081,1.162,1.308,1.483,1.642,1.788,-0.71,-0.571,-0.425,-0.262,-0.137,0.988,1.041,1.119,1.19,1.244,0.924,0.983,1.058,1.128,1.181,
  2021,2016,2026,0.034,0.04,0.049,0.058,0.065,1.26,1.432,1.623,1.797,1.959,-0.708,-0.569,-0.408,-0.23,-0.102,1.118,1.181,1.264,1.34,1.402,1.067,1.132,1.216,1.292,1.352,
colonnes (29) :
  [0] time
  [1] timebound_lower
  [2] timebound_upper
  [3] natural_p05
  [4] natural_p17
  [5] natural_p50
  [6] natural_p83
  [7] natural_p95
  [8] ghg_p05
  [9] ghg_p17
  [10] ghg_p50
  [11] ghg_p83
  [12] ghg_p95
  [13] other_human_forcing_p05
  [14] other_human_forcing_p17
  [15] other_human_forcing_p50
  [16] other_human_forcing_p83
  [17] other_human_forcing_p95
  [18] total_p05
  [19] total_p17
  [20] total_p50
  [21] total_p83
  [22] total_p95
  [23] anthropogenic_p05
  [24] anthropogenic_p17
  [25] anthropogenic_p50
  [26] anthropogenic_p83
  [27] anthropogenic_p95
  [28] 
  2015 : natural_p05=0.042, natural_p17=0.05, natural_p50=0.061, natural_p83=0.072, natural_p95=0.081, total_p05=0.988, total_p17=1.041, total_p50=1.119, total_p83=1.19, total_p95=1.244, anthropogenic_p05=0.924, anthropogenic_p17=0.983, anthropogenic_p50=1.058, anthropogenic_p83=1.128, anthropogenic_p95=1.181
  2025 : natural_p05=0.03, natural_p17=0.036, natural_p50=0.044, natural_p83=0.052, natural_p95=0.059, total_p05=1.221, total_p17=1.292, total_p50=1.381, total_p83=1.464, total_p95=1.533, anthropogenic_p05=1.176, anthropogenic_p17=1.248, anthropogenic_p50=1.337, anthropogenic_p83=1.421, anthropogenic_p95=1.491

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Ribes_GMST_rates.csv → 200
data/anthropogenic_warming/Ribes_GMST_rates.csv : 3 lignes, 712 o ; début :
  ﻿time,timebound_lower,timebound_upper,natural_p05,natural_p17,natural_p50,natural_p83,natural_p95,ghg_p05,ghg_p17,ghg_p50,ghg_p83,ghg_p95,other_human_forcing_p05,other_human_forcing_p17,other_human_forcing_p50,other_human_forcing_p83,other_human_forcing_p95,total_p05,total_p17,total_p50,total_p83,total_p95,anthropogenic_p05,anthropogenic_p17,anthropogenic_p50,anthropogenic_p83,anthropogenic_p95
  2015,2010,2020,-0.001,0,0,0,0,0.017,0.02,0.023,0.026,0.029,-0.004,-0.001,0.002,0.006,0.008,0.02,0.022,0.025,0.028,0.03,0.021,0.023,0.025,0.028,0.03
  2021,2016,2026,-0.003,-0.003,-0.002,-0.002,-0.002,0.017,0.02,0.023,0.027,0.029,-0.003,0,0.004,0.007,0.009,0.019,0.021,0.025,0.028,0.03,0.022,0.024,0.027,0.03,0.032
fin :
  ﻿time,timebound_lower,timebound_upper,natural_p05,natural_p17,natural_p50,natural_p83,natural_p95,ghg_p05,ghg_p17,ghg_p50,ghg_p83,ghg_p95,other_human_forcing_p05,other_human_forcing_p17,other_human_forcing_p50,other_human_forcing_p83,other_human_forcing_p95,total_p05,total_p17,total_p50,total_p83,total_p95,anthropogenic_p05,anthropogenic_p17,anthropogenic_p50,anthropogenic_p83,anthropogenic_p95
  2015,2010,2020,-0.001,0,0,0,0,0.017,0.02,0.023,0.026,0.029,-0.004,-0.001,0.002,0.006,0.008,0.02,0.022,0.025,0.028,0.03,0.021,0.023,0.025,0.028,0.03
  2021,2016,2026,-0.003,-0.003,-0.002,-0.002,-0.002,0.017,0.02,0.023,0.027,0.029,-0.003,0,0.004,0.007,0.009,0.019,0.021,0.025,0.028,0.03,0.022,0.024,0.027,0.03,0.032
colonnes (28) :
  [0] ﻿time
  [1] timebound_lower
  [2] timebound_upper
  [3] natural_p05
  [4] natural_p17
  [5] natural_p50
  [6] natural_p83
  [7] natural_p95
  [8] ghg_p05
  [9] ghg_p17
  [10] ghg_p50
  [11] ghg_p83
  [12] ghg_p95
  [13] other_human_forcing_p05
  [14] other_human_forcing_p17
  [15] other_human_forcing_p50
  [16] other_human_forcing_p83
  [17] other_human_forcing_p95
  [18] total_p05
  [19] total_p17
  [20] total_p50
  [21] total_p83
  [22] total_p95
  [23] anthropogenic_p05
  [24] anthropogenic_p17
  [25] anthropogenic_p50
  [26] anthropogenic_p83
  [27] anthropogenic_p95
  2015 : natural_p05=-0.001, natural_p17=0, natural_p50=0, natural_p83=0, natural_p95=0, total_p05=0.02, total_p17=0.022, total_p50=0.025, total_p83=0.028, total_p95=0.03, anthropogenic_p05=0.021, anthropogenic_p17=0.023, anthropogenic_p50=0.025, anthropogenic_p83=0.028, anthropogenic_p95=0.03

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Ribes_GMST_timeseries.csv → 200
data/anthropogenic_warming/Ribes_GMST_timeseries.csv : 177 lignes, 30591 o ; début :
  time,timebound_lower,timebound_upper,natural_p05,natural_p17,natural_p50,natural_p83,natural_p95,ghg_p05,ghg_p17,ghg_p50,ghg_p83,ghg_p95,other_human_forcing_p05,other_human_forcing_p17,other_human_forcing_p50,other_human_forcing_p83,other_human_forcing_p95,total_p05,total_p17,total_p50,total_p83,total_p95,anthropogenic_p05,anthropogenic_p17,anthropogenic_p50,anthropogenic_p83,anthropogenic_p95
  1850.5,1850,1851,0.017,0.021,0.025,0.03,0.033,-0.17,-0.147,-0.113,-0.079,-0.053,0.018,0.052,0.1,0.146,0.183,-0.051,-0.023,0.013,0.048,0.078,-0.076,-0.048,-0.012,0.023,0.052
  1851.5,1851,1852,0.023,0.027,0.033,0.039,0.044,-0.162,-0.14,-0.108,-0.077,-0.052,0.018,0.051,0.096,0.14,0.175,-0.039,-0.013,0.021,0.055,0.083,-0.073,-0.046,-0.012,0.021,0.049
  1852.5,1852,1853,0.027,0.032,0.039,0.046,0.052,-0.155,-0.134,-0.104,-0.074,-0.051,0.018,0.049,0.092,0.134,0.167,-0.031,-0.006,0.027,0.06,0.086,-0.069,-0.044,-0.012,0.02,0.047
  1853.5,1853,1854,0.019,0.022,0.027,0.032,0.036,-0.147,-0.128,-0.1,-0.071,-0.05,0.018,0.048,0.089,0.127,0.158,-0.039,-0.014,0.016,0.046,0.072,-0.065,-0.042,-0.011,0.018,0.044
  1854.5,1854,1855,0.01,0.012,0.014,0.017,0.019,-0.14,-0.122,-0.095,-0.068,-0.049,0.018,0.046,0.085,0.121,0.151,-0.048,-0.026,0.003,0.031,0.057,-0.062,-0.039,-0.011,0.017,0.041
fin :
  2022.5,2022,2023,0.029,0.035,0.042,0.051,0.057,1.286,1.463,1.658,1.834,2.003,-0.706,-0.565,-0.403,-0.223,-0.09,1.146,1.213,1.298,1.376,1.439,1.104,1.171,1.255,1.334,1.398
  2023.5,2023,2024,0.031,0.037,0.044,0.053,0.059,1.303,1.484,1.681,1.861,2.032,-0.705,-0.563,-0.399,-0.219,-0.079,1.173,1.24,1.327,1.408,1.471,1.129,1.196,1.283,1.364,1.429
  2024.5,2024,2025,0.031,0.037,0.045,0.054,0.06,1.321,1.505,1.705,1.888,2.06,-0.707,-0.561,-0.395,-0.212,-0.071,1.197,1.267,1.355,1.437,1.503,1.152,1.221,1.31,1.392,1.461
  2025.5,2025,2026,0.03,0.036,0.044,0.052,0.059,1.338,1.525,1.728,1.912,2.088,-0.705,-0.559,-0.391,-0.208,-0.065,1.221,1.292,1.381,1.464,1.533,1.176,1.248,1.337,1.421,1.491
colonnes (28) :
  [0] time
  [1] timebound_lower
  [2] timebound_upper
  [3] natural_p05
  [4] natural_p17
  [5] natural_p50
  [6] natural_p83
  [7] natural_p95
  [8] ghg_p05
  [9] ghg_p17
  [10] ghg_p50
  [11] ghg_p83
  [12] ghg_p95
  [13] other_human_forcing_p05
  [14] other_human_forcing_p17
  [15] other_human_forcing_p50
  [16] other_human_forcing_p83
  [17] other_human_forcing_p95
  [18] total_p05
  [19] total_p17
  [20] total_p50
  [21] total_p83
  [22] total_p95
  [23] anthropogenic_p05
  [24] anthropogenic_p17
  [25] anthropogenic_p50
  [26] anthropogenic_p83
  [27] anthropogenic_p95
  1850 : natural_p05=0.017, natural_p17=0.021, natural_p50=0.025, natural_p83=0.03, natural_p95=0.033, total_p05=-0.051, total_p17=-0.023, total_p50=0.013, total_p83=0.048, total_p95=0.078, anthropogenic_p05=-0.076, anthropogenic_p17=-0.048, anthropogenic_p50=-0.012, anthropogenic_p83=0.023, anthropogenic_p95=0.052
  1900 : natural_p05=0.035, natural_p17=0.042, natural_p50=0.051, natural_p83=0.061, natural_p95=0.068, total_p05=0.023, total_p17=0.041, total_p50=0.069, total_p83=0.094, total_p95=0.112, anthropogenic_p05=-0.03, anthropogenic_p17=-0.008, anthropogenic_p50=0.018, anthropogenic_p83=0.042, anthropogenic_p95=0.059
  1991 : natural_p05=0.002, natural_p17=0.003, natural_p50=0.003, natural_p83=0.004, natural_p95=0.004, total_p05=0.427, total_p17=0.476, total_p50=0.55, total_p83=0.617, total_p95=0.674, anthropogenic_p05=0.424, anthropogenic_p17=0.473, anthropogenic_p50=0.547, anthropogenic_p83=0.614, anthropogenic_p95=0.671
  2000 : natural_p05=0.031, natural_p17=0.037, natural_p50=0.045, natural_p83=0.054, natural_p95=0.061, total_p05=0.644, total_p17=0.695, total_p50=0.765, total_p83=0.832, total_p95=0.889, anthropogenic_p05=0.598, anthropogenic_p17=0.648, anthropogenic_p50=0.719, anthropogenic_p83=0.786, anthropogenic_p95=0.843
  2015 : natural_p05=0.049, natural_p17=0.059, natural_p50=0.071, natural_p83=0.085, natural_p95=0.095, total_p05=1.01, total_p17=1.063, total_p50=1.141, total_p83=1.212, total_p95=1.266, anthropogenic_p05=0.936, anthropogenic_p17=0.993, anthropogenic_p50=1.07, anthropogenic_p83=1.14, anthropogenic_p95=1.193
  2020 : natural_p05=0.03, natural_p17=0.035, natural_p50=0.043, natural_p83=0.051, natural_p95=0.058, total_p05=1.1, total_p17=1.161, total_p50=1.244, total_p83=1.319, total_p95=1.379, anthropogenic_p05=1.055, anthropogenic_p17=1.118, anthropogenic_p50=1.201, anthropogenic_p83=1.276, anthropogenic_p95=1.336
  2023 : natural_p05=0.031, natural_p17=0.037, natural_p50=0.044, natural_p83=0.053, natural_p95=0.059, total_p05=1.173, total_p17=1.24, total_p50=1.327, total_p83=1.408, total_p95=1.471, anthropogenic_p05=1.129, anthropogenic_p17=1.196, anthropogenic_p50=1.283, anthropogenic_p83=1.364, anthropogenic_p95=1.429
  2024 : natural_p05=0.031, natural_p17=0.037, natural_p50=0.045, natural_p83=0.054, natural_p95=0.06, total_p05=1.197, total_p17=1.267, total_p50=1.355, total_p83=1.437, total_p95=1.503, anthropogenic_p05=1.152, anthropogenic_p17=1.221, anthropogenic_p50=1.31, anthropogenic_p83=1.392, anthropogenic_p95=1.461
  2025 : natural_p05=0.03, natural_p17=0.036, natural_p50=0.044, natural_p83=0.052, natural_p95=0.059, total_p05=1.221, total_p17=1.292, total_p50=1.381, total_p83=1.464, total_p95=1.533, anthropogenic_p05=1.176, anthropogenic_p17=1.248, anthropogenic_p50=1.337, anthropogenic_p83=1.421, anthropogenic_p95=1.491

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Walsh_GMST_headlines.csv → 200
data/anthropogenic_warming/Walsh_GMST_headlines.csv : 7 lignes, 8443 o ; début :
  time,timebound_lower,timebound_upper,ghg_p05,ghg_p17,ghg_p50,ghg_p83,ghg_p95,natural_p05,natural_p17,natural_p50,natural_p83,natural_p95,other_human_forcing_p05,other_human_forcing_p17,other_human_forcing_p50,other_human_forcing_p83,other_human_forcing_p95,anthropogenic_p05,anthropogenic_p17,anthropogenic_p50,anthropogenic_p83,anthropogenic_p95,total_p05,total_p17,total_p50,total_p83,total_p95,res
  2017.5,2017,2018,1.053098645,1.213267012,1.352145076,1.496031459,1.629343712,0.01382712,0.036391446,0.067831209,0.102446877,0.129405475,-0.483099492,-0.359627877,-0.230667381,-0.110456205,0.041149394,1.02779963,1.06802065,1.122715497,1.173792748,1.210010052,1.113698695,1.145120668,1.190357447,1.23505497,1.268346766,-0.074737493,-0.04100158,0.004202434,0.049742211,0.081399282,-0.650666217,-0.468497
  2025.5,2025,2026,1.18521683,1.365223924,1.522277856,1.685063513,1.834932886,0.015215669,0.040333635,0.075005755,0.112411205,0.141966503,-0.484951405,-0.326764559,-0.188130751,-0.063546405,0.106671697,1.204317448,1.262431832,1.330203724,1.396180773,1.445851569,1.294786783,1.345909997,1.405251265,1.466563237,1.51324401,-0.107171308,-0.060211478,0.001735329,0.061761171,0.112713003,-0.673623114,-0.467
  2017.5,2017,2018,1.048969799,1.208577949,1.34701426,1.490486564,1.62340769,0.013503017,0.035513155,0.0661972,0.100159584,0.126874428,-0.500500738,-0.375712034,-0.24471093,-0.122747839,0.028256361,1.011125712,1.049898999,1.103854919,1.153489637,1.188129431,1.094406097,1.125107666,1.169732898,1.213360176,1.245360476,-0.101388874,-0.069706163,-0.026715695,0.017487021,0.047540995,-0.668607181,-0.48284
  2025.5,2025,2026,1.182090038,1.361732913,1.518341679,1.680645828,1.830094289,0.01303304,0.034197582,0.064026946,0.097697961,0.125052128,-0.470367289,-0.31975033,-0.18334219,-0.059857348,0.111820862,1.208541818,1.264983403,1.332036722,1.397963552,1.447785557,1.287974271,1.338755754,1.396422914,1.45756635,1.504109621,-0.078310508,-0.032403994,0.027698513,0.083998141,0.134545223,-0.658532154,-0.45889
  2015,2010,2020,1.014399041,1.168644941,1.302314186,1.440803568,1.569363607,0.013326675,0.035102558,0.065351754,0.098528553,0.124334229,-0.500445843,-0.377698507,-0.248742272,-0.129560865,0.015370678,0.965057644,1.00236549,1.054715037,1.102086735,1.134497288,1.047917002,1.076588702,1.119464946,1.160693244,1.189656496,-0.101926508,-0.073878548,-0.033465092,0.009443546,0.036862252,-0.658057922,-0.476
fin :
  2017.5,2017,2018,1.048969799,1.208577949,1.34701426,1.490486564,1.62340769,0.013503017,0.035513155,0.0661972,0.100159584,0.126874428,-0.500500738,-0.375712034,-0.24471093,-0.122747839,0.028256361,1.011125712,1.049898999,1.103854919,1.153489637,1.188129431,1.094406097,1.125107666,1.169732898,1.213360176,1.245360476,-0.101388874,-0.069706163,-0.026715695,0.017487021,0.047540995,-0.668607181,-0.48284
  2025.5,2025,2026,1.182090038,1.361732913,1.518341679,1.680645828,1.830094289,0.01303304,0.034197582,0.064026946,0.097697961,0.125052128,-0.470367289,-0.31975033,-0.18334219,-0.059857348,0.111820862,1.208541818,1.264983403,1.332036722,1.397963552,1.447785557,1.287974271,1.338755754,1.396422914,1.45756635,1.504109621,-0.078310508,-0.032403994,0.027698513,0.083998141,0.134545223,-0.658532154,-0.45889
  2015,2010,2020,1.014399041,1.168644941,1.302314186,1.440803568,1.569363607,0.013326675,0.035102558,0.065351754,0.098528553,0.124334229,-0.500445843,-0.377698507,-0.248742272,-0.129560865,0.015370678,0.965057644,1.00236549,1.054715037,1.102086735,1.134497288,1.047917002,1.076588702,1.119464946,1.160693244,1.189656496,-0.101926508,-0.073878548,-0.033465092,0.009443546,0.036862252,-0.658057922,-0.476
  2021,2016,2026,1.11019243,1.27894992,1.425680637,1.577728741,1.718199251,0.012903596,0.033848151,0.063322866,0.09640395,0.122834681,-0.479478326,-0.343114518,-0.210441574,-0.089132003,0.070301491,1.10933313,1.155040073,1.21405524,1.270577741,1.311970499,1.189939612,1.228390718,1.277626705,1.328272847,1.366322614,-0.085008497,-0.047836887,0.001437185,0.049357308,0.087158132,-0.655276221,-0.46477841
colonnes (99) :
  [0] time
  [1] timebound_lower
  [2] timebound_upper
  [3] ghg_p05
  [4] ghg_p17
  [5] ghg_p50
  [6] ghg_p83
  [7] ghg_p95
  [8] natural_p05
  [9] natural_p17
  [10] natural_p50
  [11] natural_p83
  [12] natural_p95
  [13] other_human_forcing_p05
  [14] other_human_forcing_p17
  [15] other_human_forcing_p50
  [16] other_human_forcing_p83
  [17] other_human_forcing_p95
  [18] anthropogenic_p05
  [19] anthropogenic_p17
  [20] anthropogenic_p50
  [21] anthropogenic_p83
  [22] anthropogenic_p95
  [23] total_p05
  [24] total_p17
  [25] total_p50
  [26] total_p83
  [27] total_p95
  [28] residual_p05
  [29] residual_p17
  [30] residual_p50
  [31] residual_p83
  [32] residual_p95
  [33] aerosol-cloud_interactions_p05
  [34] aerosol-cloud_interactions_p17
  [35] aerosol-cloud_interactions_p50
  [36] aerosol-cloud_interactions_p83
  [37] aerosol-cloud_interactions_p95
  [38] aerosol-radiation_interactions_p05
  [39] aerosol-radiation_interactions_p17
  [40] aerosol-radiation_interactions_p50
  [41] aerosol-radiation_interactions_p83
  [42] aerosol-radiation_interactions
  [43] bc_snow_p05
  [44] bc_snow_p17
  [45] bc_snow_p50
  [46] bc_snow_p83
  [47] bc_snow_p95
  [48] ch4_p05
  [49] ch4_p17
  [50] ch4_p50
  [51] ch4_p83
  [52] ch4_p95
  [53] co2_p05
  [54] co2_p17
  [55] co2_p50
  [56] co2_p83
  [57] co2_p95
  [58] contrails_p05
  [59] contrails_p17
  [60] contrails_p50
  [61] contrails_p83
  [62] contrails_p95
  [63] h2o_strat_p05
  [64] h2o_strat_p17
  [65] h2o_strat_p50
  [66] h2o_strat_p83
  [67] h2o_strat_p95
  [68] halogen_p05
  [69] halogen_p17
  [70] halogen_p50
  [71] halogen_p83
  [72] halogen_p95
  [73] land_use_p05
  [74] land_use_p17
  [75] land_use_p50
  [76] land_use_p83
  [77] land_use_p95
  [78] n2o_p05
  [79] n2o_p17
  [80] n2o_p50
  [81] n2o_p83
  [82] n2o_p95
  [83] o3_p05
  [84] o3_p17
  [85] o3_p50
  [86] o3_p83
  [87] o3_p95
  [88] solar_p05
  [89] solar_p17
  [90] solar_p50
  [91] solar_p83
  [92] solar_p95
  [93] volcanic_p05
  [94] volcanic_p17
  [95] volcanic_p50
  [96] volcanic_p83
  [97] volcanic_p95
  [98] notes
  2015 : natural_p05=0.013326675, natural_p17=0.035102558, natural_p50=0.065351754, natural_p83=0.098528553, natural_p95=0.124334229, anthropogenic_p05=0.965057644, anthropogenic_p17=1.00236549, anthropogenic_p50=1.054715037, anthropogenic_p83=1.102086735, anthropogenic_p95=1.134497288, total_p05=1.047917002, total_p17=1.076588702, total_p50=1.119464946, total_p83=1.160693244, total_p95=1.189656496, aerosol-cloud_interactions_p05=-0.658057922, aerosol-cloud_interactions_p17=-0.476793706, aerosol-cloud_interactions_p50=-0.314405227, aerosol-cloud_interactions_p83=-0.21116133, aerosol-cloud_interactions_p95=-0.153267283, aerosol-radiation_interactions_p05=-0.274666256, aerosol-radiation_interactions_p17=-0.192837913, aerosol-radiation_interactions_p50=-0.109092928, aerosol-radiation_interactions_p83=-0.047471344, aerosol-radiation_interactions=0.008276092, co2_p05=0.623633654, co2_p17=0.720255738, co2_p50=0.809488004, co2_p83=0.899507745, co2_p95=0.976459765, solar_p05=-0.013294489, solar_p17=-0.006603885, solar_p50=0.000342256, solar_p83=0.005733728, solar_p95=0.012093258, volcanic_p05=0.013413011, volcanic_p17=0.035619135, volcanic_p50=0.066084643, volcanic_p83=0.098351682, volcanic_p95=0.122270341
  2025 : natural_p05=0.015215669, natural_p17=0.040333635, natural_p50=0.075005755, natural_p83=0.112411205, natural_p95=0.141966503, anthropogenic_p05=1.204317448, anthropogenic_p17=1.262431832, anthropogenic_p50=1.330203724, anthropogenic_p83=1.396180773, anthropogenic_p95=1.445851569, total_p05=1.294786783, total_p17=1.345909997, total_p50=1.405251265, total_p83=1.466563237, total_p95=1.51324401, aerosol-cloud_interactions_p05=-0.673623114, aerosol-cloud_interactions_p17=-0.467340795, aerosol-cloud_interactions_p50=-0.284308147, aerosol-cloud_interactions_p83=-0.18528754, aerosol-cloud_interactions_p95=-0.132667246, aerosol-radiation_interactions_p05=-0.236348967, aerosol-radiation_interactions_p17=-0.164451751, aerosol-radiation_interactions_p50=-0.092627799, aerosol-radiation_interactions_p83=-0.040538858, aerosol-radiation_interactions=0.000997626, co2_p05=0.754961966, co2_p17=0.871923439, co2_p50=0.980036885, co2_p83=1.089149269, co2_p95=1.182399398, solar_p05=-0.001953411, solar_p17=0.002452427, solar_p50=0.010498155, solar_p83=0.021752227, solar_p95=0.033220922, volcanic_p05=0.012844707, volcanic_p17=0.033992382, volcanic_p50=0.063089174, volcanic_p83=0.094333067, volcanic_p95=0.118675588

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Walsh_GMST_rates.csv → 200
data/anthropogenic_warming/Walsh_GMST_rates.csv : 77 lignes, 88477 o ; début :
  time,timebound_lower,timebound_upper,ghg_p05,ghg_p17,ghg_p50,ghg_p83,ghg_p95,natural_p05,natural_p17,natural_p50,natural_p83,natural_p95,other_human_forcing_p05,other_human_forcing_p17,other_human_forcing_p50,other_human_forcing_p83,other_human_forcing_p95,anthropogenic_p05,anthropogenic_p17,anthropogenic_p50,anthropogenic_p83,anthropogenic_p95,total_p05,total_p17,total_p50,total_p83,total_p95,res
  1946,1941,1951,0.003126506,0.003684858,0.004333984,0.004979652,0.005505528,2.10E-05,0.000177526,0.000514199,0.000993094,0.00143989,-0.001474786,-0.001031073,-0.000412254,0.000388976,0.001202627,0.003277358,0.003513032,0.003919193,0.004528404,0.005082588,0.00367815,0.003985744,0.004506309,0.005219756,0.00590042,-0.061089827,-0.051141599,-0.035795391,-0.020915658,-0.011378627,-0.001818548,-0.0013835
  1947,1942,1952,0.002938432,0.003479673,0.004116363,0.004755561,0.005270751,0.000296774,0.000657445,0.001263147,0.00201851,0.002670626,-0.001423158,-0.00098539,-0.000399266,0.000312882,0.001109043,0.003057385,0.003298001,0.003701242,0.004317123,0.004804267,0.003889102,0.004312139,0.005048509,0.005943876,0.00669585,-0.053732819,-0.046342386,-0.031569567,-0.017560663,-0.009674586,-0.00177417,-0.00134
  1948,1943,1953,0.00284855,0.003365501,0.003981097,0.00460978,0.00511612,0.000466409,0.001027632,0.00184752,0.002771752,0.003525922,-0.001704106,-0.001280694,-0.000740451,-9.44E-06,0.000770255,0.002487917,0.002778964,0.003227571,0.00394988,0.004490638,0.003634339,0.004213961,0.005152222,0.006261456,0.00714578,-0.042725658,-0.036105351,-0.023618485,-0.011389015,-0.004365739,-0.001960988,-0.001526045
  1949,1944,1954,0.002888269,0.003376709,0.00396396,0.004576918,0.005076971,0.000483752,0.001062014,0.001864285,0.002717366,0.003390891,-0.0024528,-0.002008106,-0.001411644,-0.000574164,0.000145538,0.001598482,0.002016023,0.002559776,0.0033712,0.003984855,0.002854896,0.003483178,0.00445561,0.005620467,0.00654972,-0.02571566,-0.021568219,-0.010081671,-0.000554268,0.00460757,-0.002625602,-0.002079106,
  1950,1945,1955,0.003041776,0.003509973,0.004070074,0.004665755,0.005162403,0.000302142,0.000653094,0.001186599,0.001768814,0.002224216,-0.003673286,-0.003046858,-0.002253945,-0.001316696,-0.0005717,0.000541085,0.001106368,0.001813854,0.002702037,0.003416787,0.001376802,0.002114435,0.003023189,0.004106101,0.005027074,-0.011795744,-0.006800685,0.001165714,0.008635209,0.012475454,-0.003700808,-0.0028
fin :
  2018,2013,2023,0.016471403,0.018543946,0.020787171,0.023224342,0.025406732,-0.003563012,-0.002816561,-0.001862774,-0.001000198,-0.000441494,0.002074113,0.004793403,0.007100571,0.009368133,0.011141923,0.021798728,0.024711725,0.027853967,0.030939242,0.033447533,0.019256983,0.022522743,0.026004167,0.029322214,0.031860273,-0.016447683,-0.01368447,-0.009946571,-0.006005024,-0.002583899,-0.002282385,0.0
  2019,2014,2024,0.016589624,0.018682168,0.020953193,0.023417603,0.025621004,-0.003499846,-0.002845082,-0.001955653,-0.001082606,-0.000481451,0.001083705,0.004403773,0.006771439,0.008968364,0.010669291,0.021264154,0.024424152,0.027621276,0.030724416,0.033225299,0.018742145,0.022176412,0.025705589,0.029050379,0.031585303,-0.011073086,-0.008318114,-0.004637852,-0.000768563,0.002712252,-0.003105438,0.0
  2020,2015,2025,0.016688115,0.018799042,0.021095572,0.023584917,0.025806988,-0.002082742,-0.001648386,-0.001085489,-0.000589333,-0.000263844,-0.001994004,0.003238989,0.006073397,0.008233437,0.009905376,0.019553862,0.023428335,0.026906762,0.030068723,0.032469392,0.018198264,0.022180064,0.025805769,0.029079745,0.031492296,-0.005525843,-0.002871472,0.000702345,0.004552618,0.008550377,-0.006098364,0.00
  2021,2016,2026,0.016781167,0.018910082,0.021230944,0.02374423,0.025984565,-0.000738647,-0.000373902,7.57E-06,0.00044548,0.000944644,-0.004404242,0.002245548,0.005500277,0.007633318,0.009327072,0.017880502,0.022638782,0.026387504,0.029561823,0.031860977,0.017901976,0.022657667,0.026435909,0.029624907,0.031910754,-0.00327852,-0.000733014,0.002842725,0.006961142,0.011678812,-0.008613881,-0.000345205,
colonnes (98) :
  [0] time
  [1] timebound_lower
  [2] timebound_upper
  [3] ghg_p05
  [4] ghg_p17
  [5] ghg_p50
  [6] ghg_p83
  [7] ghg_p95
  [8] natural_p05
  [9] natural_p17
  [10] natural_p50
  [11] natural_p83
  [12] natural_p95
  [13] other_human_forcing_p05
  [14] other_human_forcing_p17
  [15] other_human_forcing_p50
  [16] other_human_forcing_p83
  [17] other_human_forcing_p95
  [18] anthropogenic_p05
  [19] anthropogenic_p17
  [20] anthropogenic_p50
  [21] anthropogenic_p83
  [22] anthropogenic_p95
  [23] total_p05
  [24] total_p17
  [25] total_p50
  [26] total_p83
  [27] total_p95
  [28] residual_p05
  [29] residual_p17
  [30] residual_p50
  [31] residual_p83
  [32] residual_p95
  [33] aerosol-cloud_interactions_p05
  [34] aerosol-cloud_interactions_p17
  [35] aerosol-cloud_interactions_p50
  [36] aerosol-cloud_interactions_p83
  [37] aerosol-cloud_interactions_p95
  [38] aerosol-radiation_interactions_p05
  [39] aerosol-radiation_interactions_p17
  [40] aerosol-radiation_interactions_p50
  [41] aerosol-radiation_interactions_p83
  [42] aerosol-radiation_interactions
  [43] bc_snow_p05
  [44] bc_snow_p17
  [45] bc_snow_p50
  [46] bc_snow_p83
  [47] bc_snow_p95
  [48] ch4_p05
  [49] ch4_p17
  [50] ch4_p50
  [51] ch4_p83
  [52] ch4_p95
  [53] co2_p05
  [54] co2_p17
  [55] co2_p50
  [56] co2_p83
  [57] co2_p95
  [58] contrails_p05
  [59] contrails_p17
  [60] contrails_p50
  [61] contrails_p83
  [62] contrails_p95
  [63] h2o_strat_p05
  [64] h2o_strat_p17
  [65] h2o_strat_p50
  [66] h2o_strat_p83
  [67] h2o_strat_p95
  [68] halogen_p05
  [69] halogen_p17
  [70] halogen_p50
  [71] halogen_p83
  [72] halogen_p95
  [73] land_use_p05
  [74] land_use_p17
  [75] land_use_p50
  [76] land_use_p83
  [77] land_use_p95
  [78] n2o_p05
  [79] n2o_p17
  [80] n2o_p50
  [81] n2o_p83
  [82] n2o_p95
  [83] o3_p05
  [84] o3_p17
  [85] o3_p50
  [86] o3_p83
  [87] o3_p95
  [88] solar_p05
  [89] solar_p17
  [90] solar_p50
  [91] solar_p83
  [92] solar_p95
  [93] volcanic_p05
  [94] volcanic_p17
  [95] volcanic_p50
  [96] volcanic_p83
  [97] volcanic_p95
  1991 : natural_p05=-0.017991582, natural_p17=-0.014901933, natural_p50=-0.010586095, natural_p83=-0.006080257, natural_p95=-0.002750104, anthropogenic_p05=0.015460232, anthropogenic_p17=0.018040272, anthropogenic_p50=0.020350806, anthropogenic_p83=0.022082228, anthropogenic_p95=0.023316057, total_p05=0.000224023, total_p17=0.004335367, total_p50=0.009611672, total_p83=0.014722015, total_p95=0.018348023, aerosol-cloud_interactions_p05=-0.011331402, aerosol-cloud_interactions_p17=-0.006605969, aerosol-cloud_interactions_p50=-0.001761397, aerosol-cloud_interactions_p83=-0.000334934, aerosol-cloud_interactions_p95=0.000201845, aerosol-radiation_interactions_p05=-0.001301461, aerosol-radiation_interactions_p17=-0.000710049, aerosol-radiation_interactions_p50=8.23E-06, aerosol-radiation_interactions_p83=0.000766908, aerosol-radiation_interactions=0.001705899, co2_p05=0.008796501, co2_p17=0.009926178, co2_p50=0.011134031, co2_p83=0.01248582, co2_p95=0.013678373, solar_p05=0.000125219, solar_p17=0.000286763, solar_p50=0.000591257, solar_p83=0.000983407, solar_p95=0.001328391, volcanic_p05=-0.019067902, volcanic_p17=-0.015810992, volcanic_p50=-0.011236773, volcanic_p83=-0.006453586, volcanic_p95=-0.002917419
  2000 : natural_p05=0.002204397, natural_p17=0.004841473, natural_p50=0.008555589, natural_p83=0.012588622, natural_p95=0.015588772, anthropogenic_p05=0.01777822, anthropogenic_p17=0.019224277, anthropogenic_p50=0.021026333, anthropogenic_p83=0.022837728, anthropogenic_p95=0.024231199, total_p05=0.022841689, total_p17=0.025650016, total_p50=0.029711856, total_p83=0.033727109, total_p95=0.036720159, aerosol-cloud_interactions_p05=-0.003147704, aerosol-cloud_interactions_p17=-0.001182819, aerosol-cloud_interactions_p50=0.000526126, aerosol-cloud_interactions_p83=0.001376146, aerosol-cloud_interactions_p95=0.00206329, aerosol-radiation_interactions_p05=-0.000179343, aerosol-radiation_interactions_p17=0.000250771, aerosol-radiation_interactions_p50=0.000654249, aerosol-radiation_interactions_p83=0.001189515, aerosol-radiation_interactions=0.001739587, co2_p05=0.009921059, co2_p17=0.011183272, co2_p50=0.012512221, co2_p83=0.014007144, co2_p95=0.015317361, solar_p05=0.000233674, solar_p17=0.000533641, solar_p50=0.001092604, solar_p83=0.001813321, solar_p95=0.002440557, volcanic_p05=0.001895235, volcanic_p17=0.004140006, volcanic_p50=0.007352873, volcanic_p83=0.010941855, volcanic_p95=0.013590031
  2015 : natural_p05=0.000131165, natural_p17=0.000341486, natural_p50=0.00072756, natural_p83=0.00121778, natural_p95=0.001677131, anthropogenic_p05=0.021580598, anthropogenic_p17=0.023796082, anthropogenic_p50=0.026542671, anthropogenic_p83=0.029341349, anthropogenic_p95=0.031620204, total_p05=0.022420536, total_p17=0.024558869, total_p50=0.027330279, total_p83=0.030130311, total_p95=0.03244052, aerosol-cloud_interactions_p05=-0.001188357, aerosol-cloud_interactions_p17=0.000948782, aerosol-cloud_interactions_p50=0.00274906, aerosol-cloud_interactions_p83=0.004509908, aerosol-cloud_interactions_p95=0.006072889, aerosol-radiation_interactions_p05=-0.000122445, aerosol-radiation_interactions_p17=0.000826957, aerosol-radiation_interactions_p50=0.001828812, aerosol-radiation_interactions_p83=0.00321648, aerosol-radiation_interactions=0.004418471, co2_p05=0.012213565, co2_p17=0.013767433, co2_p50=0.015410315, co2_p83=0.0172581, co2_p95=0.018879602, solar_p05=1.76E-05, solar_p17=6.77E-05, solar_p50=0.00020661, solar_p83=0.000418201, solar_p95=0.000623391, volcanic_p05=8.95E-05, volcanic_p17=0.000212256, volcanic_p50=0.000456203, volcanic_p83=0.00086305, volcanic_p95=0.001313065
  2020 : natural_p05=-0.002082742, natural_p17=-0.001648386, natural_p50=-0.001085489, natural_p83=-0.000589333, natural_p95=-0.000263844, anthropogenic_p05=0.019553862, anthropogenic_p17=0.023428335, anthropogenic_p50=0.026906762, anthropogenic_p83=0.030068723, anthropogenic_p95=0.032469392, total_p05=0.018198264, total_p17=0.022180064, total_p50=0.025805769, total_p83=0.029079745, total_p95=0.031492296, aerosol-cloud_interactions_p05=-0.006098364, aerosol-cloud_interactions_p17=0.000557527, aerosol-cloud_interactions_p50=0.002989218, aerosol-cloud_interactions_p83=0.005073371, aerosol-cloud_interactions_p95=0.006778024, aerosol-radiation_interactions_p05=-0.000655544, aerosol-radiation_interactions_p17=0.000611931, aerosol-radiation_interactions_p50=0.001842817, aerosol-radiation_interactions_p83=0.00329142, aerosol-radiation_interactions=0.004509603, co2_p05=0.012866549, co2_p17=0.014507842, co2_p50=0.01626081, co2_p83=0.018227671, co2_p95=0.019957787, solar_p05=3.69E-05, solar_p17=0.000102893, solar_p50=0.000247932, solar_p83=0.000483363, solar_p95=0.000728849, volcanic_p05=-0.002512663, volcanic_p17=-0.002045968, volcanic_p50=-0.001408237, volcanic_p83=-0.000781372, volcanic_p95=-0.000347715

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/Walsh_GMST_timeseries.csv → 200
data/anthropogenic_warming/Walsh_GMST_timeseries.csv : 177 lignes, 202355 o ; début :
  time,timebound_lower,timebound_upper,ghg_p05,ghg_p17,ghg_p50,ghg_p83,ghg_p95,natural_p05,natural_p17,natural_p50,natural_p83,natural_p95,other_human_forcing_p05,other_human_forcing_p17,other_human_forcing_p50,other_human_forcing_p83,other_human_forcing_p95,anthropogenic_p05,anthropogenic_p17,anthropogenic_p50,anthropogenic_p83,anthropogenic_p95,total_p05,total_p17,total_p50,total_p83,total_p95,res
  1850.5,1850,1851,-0.06655252,-0.06118012,-0.05507367,-0.049222764,-0.042502932,0.000828465,0.0050893,0.020570863,0.039545734,0.051843901,0.012979169,0.019187218,0.032298081,0.060601075,0.084955927,-0.039088488,-0.033907753,-0.021654971,0.002907658,0.026034958,-0.032452415,-0.020383179,0.00333257,0.032976473,0.057338091,-0.201066882,-0.142918038,-0.074637474,-0.004937692,0.040830551,0.01081469,0.01
  1851.5,1851,1852,-0.065213702,-0.059951448,-0.053969988,-0.048237658,-0.041652399,0.003897375,0.011627749,0.027750805,0.048078787,0.06187881,0.012821832,0.018912686,0.031755003,0.059173934,0.082842583,-0.038176917,-0.033101803,-0.02111016,0.00263927,0.025050987,-0.028327344,-0.014108874,0.011202353,0.041908289,0.066385342,-0.057984188,0.00474057,0.084860469,0.156526025,0.203097285,0.010693678,0.01
  1852.5,1852,1853,-0.06373002,-0.058586397,-0.052739964,-0.047138825,-0.040705213,0.005387812,0.015793092,0.033511125,0.05464161,0.069647238,0.012693644,0.018752757,0.031634108,0.059187803,0.083102441,-0.037089411,-0.032059318,-0.019982272,0.003939816,0.026517346,-0.025189384,-0.009027751,0.01800919,0.050081174,0.075443584,-0.005837071,0.045777136,0.117877782,0.188518113,0.239434505,0.010678602,0.0
  1853.5,1853,1854,-0.062105288,-0.057090167,-0.051391236,-0.045933855,-0.039666925,0.004935662,0.01440154,0.030158457,0.049470739,0.063480181,0.012511967,0.018483692,0.031233049,0.058401006,0.082203502,-0.035949581,-0.031007723,-0.019036565,0.004572938,0.02697647,-0.024790685,-0.009795086,0.015353745,0.046056725,0.070925943,-0.048955676,0.011380812,0.080489171,0.142589109,0.194380131,0.010595391,0.
  1854.5,1854,1855,-0.060407154,-0.055527368,-0.049983805,-0.044677171,-0.038582787,0.001108137,0.00389114,0.013432785,0.02794254,0.03781346,0.012179055,0.017891854,0.029955929,0.055080626,0.077206427,-0.034949451,-0.030218624,-0.018968275,0.002734478,0.023447434,-0.029647968,-0.020410806,-0.001832134,0.023635707,0.045538777,-0.038116705,0.00338037,0.064955568,0.123784367,0.163804365,0.010275514,0.0
fin :
  2022.5,2022,2023,1.127974867,1.310038586,1.462112956,1.619395866,1.762255468,0.010152353,0.027905863,0.053903502,0.084097495,0.10907988,-0.468200024,-0.337451387,-0.204379206,-0.08206496,0.08478046,1.14414568,1.194397789,1.256577046,1.317606735,1.361899727,1.215547197,1.259244347,1.31026972,1.367191438,1.408199124,-0.249512254,-0.20813364,-0.15115747,-0.0999048,-0.056039081,-0.638198542,-0.458667,
  2023.5,2023,2024,1.144239023,1.328929608,1.483315228,1.642991841,1.787935435,0.011165044,0.031008073,0.05902583,0.090610905,0.116609159,-0.474475709,-0.33760361,-0.201944984,-0.078294929,0.091054488,1.163011831,1.215477323,1.279206955,1.341941739,1.387573121,1.238745343,1.285063525,1.337803411,1.396503607,1.439037516,0.028592863,0.07145006,0.1303776,0.183415285,0.229035827,-0.647874434,-0.46374140
  2024.5,2024,2025,1.16098926,1.348408635,1.505144125,1.667245722,1.814317435,0.01324408,0.037180448,0.070123083,0.105397263,0.133678833,-0.49968474,-0.345907584,-0.202502897,-0.076015625,0.094679524,1.171359071,1.230297069,1.297786242,1.36291955,1.410133904,1.25754196,1.310118178,1.367147946,1.428063536,1.473118295,0.053035906,0.098454742,0.159810325,0.217267981,0.2694278,-0.677848431,-0.479959264,
  2025.5,2025,2026,1.178379525,1.368643908,1.52778702,1.69237029,1.841610444,0.014192212,0.039877749,0.075281449,0.112937261,0.142760451,-0.48458768,-0.335874398,-0.195111952,-0.068285999,0.106286845,1.202633962,1.261089927,1.328893675,1.395797737,1.444800655,1.294159464,1.345284769,1.403426391,1.466481146,1.513346119,-0.107241424,-0.060109655,0.003516306,0.062291682,0.113324407,-0.667155008,-0.4730
colonnes (98) :
  [0] time
  [1] timebound_lower
  [2] timebound_upper
  [3] ghg_p05
  [4] ghg_p17
  [5] ghg_p50
  [6] ghg_p83
  [7] ghg_p95
  [8] natural_p05
  [9] natural_p17
  [10] natural_p50
  [11] natural_p83
  [12] natural_p95
  [13] other_human_forcing_p05
  [14] other_human_forcing_p17
  [15] other_human_forcing_p50
  [16] other_human_forcing_p83
  [17] other_human_forcing_p95
  [18] anthropogenic_p05
  [19] anthropogenic_p17
  [20] anthropogenic_p50
  [21] anthropogenic_p83
  [22] anthropogenic_p95
  [23] total_p05
  [24] total_p17
  [25] total_p50
  [26] total_p83
  [27] total_p95
  [28] residual_p05
  [29] residual_p17
  [30] residual_p50
  [31] residual_p83
  [32] residual_p95
  [33] aerosol-cloud_interactions_p05
  [34] aerosol-cloud_interactions_p17
  [35] aerosol-cloud_interactions_p50
  [36] aerosol-cloud_interactions_p83
  [37] aerosol-cloud_interactions_p95
  [38] aerosol-radiation_interactions_p05
  [39] aerosol-radiation_interactions_p17
  [40] aerosol-radiation_interactions_p50
  [41] aerosol-radiation_interactions_p83
  [42] aerosol-radiation_interactions_p95
  [43] bc_snow_p05
  [44] bc_snow_p17
  [45] bc_snow_p50
  [46] bc_snow_p83
  [47] bc_snow_p95
  [48] ch4_p05
  [49] ch4_p17
  [50] ch4_p50
  [51] ch4_p83
  [52] ch4_p95
  [53] co2_p05
  [54] co2_p17
  [55] co2_p50
  [56] co2_p83
  [57] co2_p95
  [58] contrails_p05
  [59] contrails_p17
  [60] contrails_p50
  [61] contrails_p83
  [62] contrails_p95
  [63] h2o_strat_p05
  [64] h2o_strat_p17
  [65] h2o_strat_p50
  [66] h2o_strat_p83
  [67] h2o_strat_p95
  [68] halogen_p05
  [69] halogen_p17
  [70] halogen_p50
  [71] halogen_p83
  [72] halogen_p95
  [73] land_use_p05
  [74] land_use_p17
  [75] land_use_p50
  [76] land_use_p83
  [77] land_use_p95
  [78] n2o_p05
  [79] n2o_p17
  [80] n2o_p50
  [81] n2o_p83
  [82] n2o_p95
  [83] o3_p05
  [84] o3_p17
  [85] o3_p50
  [86] o3_p83
  [87] o3_p95
  [88] solar_p05
  [89] solar_p17
  [90] solar_p50
  [91] solar_p83
  [92] solar_p95
  [93] volcanic_p05
  [94] volcanic_p17
  [95] volcanic_p50
  [96] volcanic_p83
  [97] volcanic_p95
  1850 : natural_p05=0.000828465, natural_p17=0.0050893, natural_p50=0.020570863, natural_p83=0.039545734, natural_p95=0.051843901, anthropogenic_p05=-0.039088488, anthropogenic_p17=-0.033907753, anthropogenic_p50=-0.021654971, anthropogenic_p83=0.002907658, anthropogenic_p95=0.026034958, total_p05=-0.032452415, total_p17=-0.020383179, total_p50=0.00333257, total_p83=0.032976473, total_p95=0.057338091, aerosol-cloud_interactions_p05=0.01081469, aerosol-cloud_interactions_p17=0.015434799, aerosol-cloud_interactions_p50=0.02679638, aerosol-cloud_interactions_p83=0.054935847, aerosol-cloud_interactions_p95=0.078965173, aerosol-radiation_interactions_p05=-0.003960027, aerosol-radiation_interactions_p17=0.00014031, aerosol-radiation_interactions_p50=0.003738983, aerosol-radiation_interactions_p83=0.007756779, aerosol-radiation_interactions_p95=0.011741097, co2_p05=-0.043939669, co2_p17=-0.040483919, co2_p50=-0.03645954, co2_p83=-0.0324341, co2_p95=-0.027679513, solar_p05=0.000353175, solar_p17=0.001668769, solar_p50=0.004002998, solar_p83=0.007152644, solar_p95=0.009932864, volcanic_p05=-0.001330619, volcanic_p17=0.00183052, volcanic_p50=0.016383705, volcanic_p83=0.033471556, volcanic_p95=0.044029784
  1900 : natural_p05=0.00749991, natural_p17=0.021417391, natural_p50=0.04030244, natural_p83=0.057970256, natural_p95=0.069802901, anthropogenic_p05=-0.013052482, anthropogenic_p17=0.005338627, anthropogenic_p50=0.025216865, anthropogenic_p83=0.039137821, anthropogenic_p95=0.046031821, total_p05=0.02634441, total_p17=0.042482801, total_p50=0.062718091, total_p83=0.081511685, total_p95=0.093812247, aerosol-cloud_interactions_p05=-0.087351259, aerosol-cloud_interactions_p17=-0.064123808, aerosol-cloud_interactions_p50=-0.040958966, aerosol-cloud_interactions_p83=-0.026479784, aerosol-cloud_interactions_p95=-0.01887146, aerosol-radiation_interactions_p05=-0.02403583, aerosol-radiation_interactions_p17=-0.016951442, aerosol-radiation_interactions_p50=-0.009238632, aerosol-radiation_interactions_p83=-0.00335013, aerosol-radiation_interactions_p95=0.002922629, co2_p05=0.040797272, co2_p17=0.04781375, co2_p50=0.053718399, co2_p83=0.059615623, co2_p95=0.064700788, solar_p05=-0.008622696, solar_p17=-0.006133794, solar_p50=-0.003373943, solar_p83=-0.001364674, solar_p95=-0.000249107, volcanic_p05=0.008178919, volcanic_p17=0.023432985, volcanic_p50=0.044201335, volcanic_p83=0.063486638, volcanic_p95=0.076181414
  1991 : natural_p05=0.007513282, natural_p17=0.020959872, natural_p50=0.042938659, natural_p83=0.06943395, natural_p95=0.092035126, anthropogenic_p05=0.469525499, anthropogenic_p17=0.50275312, anthropogenic_p50=0.554694725, anthropogenic_p83=0.597369124, anthropogenic_p95=0.627372223, total_p05=0.528948303, total_p17=0.556850417, total_p50=0.5981698, total_p83=0.63522225, total_p95=0.661761727, aerosol-cloud_interactions_p05=-0.580079696, aerosol-cloud_interactions_p17=-0.447410966, aerosol-cloud_interactions_p50=-0.320053654, aerosol-cloud_interactions_p83=-0.222718361, aerosol-cloud_interactions_p95=-0.164984673, aerosol-radiation_interactions_p05=-0.312753057, aerosol-radiation_interactions_p17=-0.226405242, aerosol-radiation_interactions_p50=-0.130538079, aerosol-radiation_interactions_p83=-0.060424317, aerosol-radiation_interactions_p95=0.001684987, co2_p05=0.386009543, co2_p17=0.452214605, co2_p50=0.508439326, co2_p83=0.56490632, co2_p95=0.613448456, solar_p05=-0.00259395, solar_p17=0.001012467, solar_p50=0.0065373, solar_p83=0.014462197, solar_p95=0.022770625, volcanic_p05=0.005676616, volcanic_p17=0.016723441, volcanic_p50=0.035526655, volcanic_p83=0.058004207, volcanic_p95=0.077370653
  2000 : natural_p05=0.010158727, natural_p17=0.028563827, natural_p50=0.054262776, natural_p83=0.081930093, natural_p95=0.104743719, anthropogenic_p05=0.660056702, anthropogenic_p17=0.695594159, anthropogenic_p50=0.745589982, anthropogenic_p83=0.788047628, anthropogenic_p95=0.8145343, total_p05=0.731455238, total_p17=0.759883378, total_p50=0.798456913, total_p83=0.835326425, total_p95=0.861711687, aerosol-cloud_interactions_p05=-0.628946895, aerosol-cloud_interactions_p17=-0.469253497, aerosol-cloud_interactions_p50=-0.320805886, aerosol-cloud_interactions_p83=-0.219486632, aerosol-cloud_interactions_p95=-0.162256106, aerosol-radiation_interactions_p05=-0.292272564, aerosol-radiation_interactions_p17=-0.209602973, aerosol-radiation_interactions_p50=-0.11935526, aerosol-radiation_interactions_p83=-0.053535612, aerosol-radiation_interactions_p95=0.007270844, co2_p05=0.462906671, co2_p17=0.542292465, co2_p50=0.609746207, co2_p83=0.677572515, co2_p95=0.735924305, solar_p05=-0.005179208, solar_p17=-0.000419133, solar_p50=0.004603232, solar_p83=0.012011115, solar_p95=0.019885833, volcanic_p05=0.009213428, volcanic_p17=0.026022437, volcanic_p50=0.049077508, volcanic_p83=0.072928022, volcanic_p95=0.092801913
  2015 : natural_p05=0.013329569, natural_p17=0.037369796, natural_p50=0.070481284, natural_p83=0.105706424, natural_p95=0.132990997, anthropogenic_p05=0.969489558, anthropogenic_p17=1.007047001, anthropogenic_p50=1.059970146, anthropogenic_p83=1.107868407, anthropogenic_p95=1.140360008, total_p05=1.05789773, total_p17=1.085704212, total_p50=1.12917584, total_p83=1.171743714, total_p95=1.202090009, aerosol-cloud_interactions_p05=-0.663079647, aerosol-cloud_interactions_p17=-0.485168487, aerosol-cloud_interactions_p50=-0.319969167, aerosol-cloud_interactions_p83=-0.215678541, aerosol-cloud_interactions_p95=-0.158590202, aerosol-radiation_interactions_p05=-0.278975605, aerosol-radiation_interactions_p17=-0.198559448, aerosol-radiation_interactions_p50=-0.112024192, aerosol-radiation_interactions_p83=-0.048558575, aerosol-radiation_interactions_p95=0.008769271, co2_p05=0.621215451, co2_p17=0.727726253, co2_p50=0.818305216, co2_p83=0.909397509, co2_p95=0.987760714, solar_p05=-0.008189085, solar_p17=-0.002156416, solar_p50=0.003286466, solar_p83=0.010602598, solar_p95=0.018531868, volcanic_p05=0.012611172, volcanic_p17=0.035450965, volcanic_p50=0.066816799, volcanic_p83=0.099598555, volcanic_p95=0.124003536
  2020 : natural_p05=0.010395852, natural_p17=0.028479013, natural_p50=0.055533635, natural_p83=0.086761882, natural_p95=0.112055586, anthropogenic_p05=1.097696861, anthropogenic_p17=1.143016127, anthropogenic_p50=1.2018431, anthropogenic_p83=1.258660436, anthropogenic_p95=1.299161542, total_p05=1.171357514, total_p17=1.209441703, total_p50=1.25716798, total_p83=1.309434602, total_p95=1.346800372, aerosol-cloud_interactions_p05=-0.645349704, aerosol-cloud_interactions_p17=-0.466323247, aerosol-cloud_interactions_p50=-0.297449071, aerosol-cloud_interactions_p83=-0.197258167, aerosol-cloud_interactions_p95=-0.143812374, aerosol-radiation_interactions_p05=-0.252136838, aerosol-radiation_interactions_p17=-0.178231335, aerosol-radiation_interactions_p50=-0.100055567, aerosol-radiation_interactions_p83=-0.043094692, aerosol-radiation_interactions_p95=0.005511044, co2_p05=0.68351283, co2_p17=0.800709354, co2_p50=0.900357599, co2_p83=1.000541688, co2_p95=1.086721854, solar_p05=-0.018426847, solar_p17=-0.010616094, solar_p50=-0.002192195, solar_p83=0.002337923, solar_p95=0.008252134, volcanic_p05=0.01126935, volcanic_p17=0.031324682, volcanic_p50=0.059928172, volcanic_p83=0.091143957, volcanic_p95=0.115277996
  2023 : natural_p05=0.011165044, natural_p17=0.031008073, natural_p50=0.05902583, natural_p83=0.090610905, natural_p95=0.116609159, anthropogenic_p05=1.163011831, anthropogenic_p17=1.215477323, anthropogenic_p50=1.279206955, anthropogenic_p83=1.341941739, anthropogenic_p95=1.387573121, total_p05=1.238745343, total_p17=1.285063525, total_p50=1.337803411, total_p83=1.396503607, total_p95=1.439037516, aerosol-cloud_interactions_p05=-0.647874434, aerosol-cloud_interactions_p17=-0.463741409, aerosol-cloud_interactions_p50=-0.288799627, aerosol-cloud_interactions_p83=-0.189454166, aerosol-cloud_interactions_p95=-0.137585597, aerosol-radiation_interactions_p05=-0.242144755, aerosol-radiation_interactions_p17=-0.170477123, aerosol-radiation_interactions_p50=-0.095629959, aerosol-radiation_interactions_p83=-0.041423567, aerosol-radiation_interactions_p95=0.00276098, co2_p05=0.72017627, co2_p17=0.843631914, co2_p50=0.948723736, co2_p83=1.054435342, co2_p95=1.145343012, solar_p05=-0.008506581, solar_p17=-0.002109151, solar_p50=0.003713982, solar_p83=0.011533405, solar_p95=0.019916511, volcanic_p05=0.010346603, volcanic_p17=0.028723445, volcanic_p50=0.054902014, volcanic_p83=0.083846642, volcanic_p95=0.10701639
  2024 : natural_p05=0.01324408, natural_p17=0.037180448, natural_p50=0.070123083, natural_p83=0.105397263, natural_p95=0.133678833, anthropogenic_p05=1.171359071, anthropogenic_p17=1.230297069, anthropogenic_p50=1.297786242, anthropogenic_p83=1.36291955, anthropogenic_p95=1.410133904, total_p05=1.25754196, total_p17=1.310118178, total_p50=1.367147946, total_p83=1.428063536, total_p95=1.473118295, aerosol-cloud_interactions_p05=-0.677848431, aerosol-cloud_interactions_p17=-0.479959264, aerosol-cloud_interactions_p50=-0.293606728, aerosol-cloud_interactions_p83=-0.191158206, aerosol-cloud_interactions_p95=-0.138687655, aerosol-radiation_interactions_p05=-0.245809578, aerosol-radiation_interactions_p17=-0.172547181, aerosol-radiation_interactions_p50=-0.09683258, aerosol-radiation_interactions_p83=-0.042454099, aerosol-radiation_interactions_p95=0.000898955, co2_p05=0.733106345, co2_p17=0.858779718, co2_p50=0.965757181, co2_p83=1.073368615, co2_p95=1.16591608, solar_p05=-0.0039603, solar_p17=0.00097324, solar_p50=0.008059378, solar_p83=0.018127333, solar_p95=0.028554828, volcanic_p05=0.011519984, volcanic_p17=0.032277191, volcanic_p50=0.060821613, volcanic_p83=0.091295205, volcanic_p95=0.11532172
  2025 : natural_p05=0.014192212, natural_p17=0.039877749, natural_p50=0.075281449, natural_p83=0.112937261, natural_p95=0.142760451, anthropogenic_p05=1.202633962, anthropogenic_p17=1.261089927, anthropogenic_p50=1.328893675, anthropogenic_p83=1.395797737, anthropogenic_p95=1.444800655, total_p05=1.294159464, total_p17=1.345284769, total_p50=1.403426391, total_p83=1.466481146, total_p95=1.513346119, aerosol-cloud_interactions_p05=-0.667155008, aerosol-cloud_interactions_p17=-0.47306968, aerosol-cloud_interactions_p50=-0.28930449, aerosol-cloud_interactions_p83=-0.1882406, aerosol-cloud_interactions_p95=-0.136369611, aerosol-radiation_interactions_p05=-0.241449171, aerosol-radiation_interactions_p17=-0.169413104, aerosol-radiation_interactions_p50=-0.094962585, aerosol-radiation_interactions_p83=-0.041368705, aerosol-radiation_interactions_p95=0.001256522, co2_p05=0.746765021, co2_p17=0.874786947, co2_p50=0.983735423, co2_p83=1.09332223, co2_p95=1.187571417, solar_p05=-0.00205664, solar_p17=0.002479892, solar_p50=0.010624567, solar_p83=0.021969978, solar_p95=0.033617892, volcanic_p05=0.011966952, volcanic_p17=0.033549177, volcanic_p50=0.063212067, volcanic_p83=0.094614771, volcanic_p95=0.119119292

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming/assessment_6thIPCC_headlines.csv → 200
data/anthropogenic_warming/assessment_6thIPCC_headlines.csv : 3 lignes, 458 o ; début :
  time,timebound_lower,timebound_upper,total_p05,total_p50,total_p95,anthropogenic_p05,anthropogenic_p50,anthropogenic_p95,ghg_p05,ghg_p50,ghg_p95,natural_p05,natural_p50,natural_p95,other_human_forcing_p05,other_human_forcing_p50,other_human_forcing_p95,internal_variability_p05,internal_variability_p50,internal_variability_p95
  2015,2010,2020,0.88,1.06,1.21,0.8,1.07,1.3,1,1.4,2,-0.1,0.03,0.1,-0.8,-0.32,0,-0.2,0,0.2
  2017.5,2017,2018,,,,0.8,1,1.2,,,,,,,,,,,,
fin :
  time,timebound_lower,timebound_upper,total_p05,total_p50,total_p95,anthropogenic_p05,anthropogenic_p50,anthropogenic_p95,ghg_p05,ghg_p50,ghg_p95,natural_p05,natural_p50,natural_p95,other_human_forcing_p05,other_human_forcing_p50,other_human_forcing_p95,internal_variability_p05,internal_variability_p50,internal_variability_p95
  2015,2010,2020,0.88,1.06,1.21,0.8,1.07,1.3,1,1.4,2,-0.1,0.03,0.1,-0.8,-0.32,0,-0.2,0,0.2
  2017.5,2017,2018,,,,0.8,1,1.2,,,,,,,,,,,,
colonnes (21) :
  [0] time
  [1] timebound_lower
  [2] timebound_upper
  [3] total_p05
  [4] total_p50
  [5] total_p95
  [6] anthropogenic_p05
  [7] anthropogenic_p50
  [8] anthropogenic_p95
  [9] ghg_p05
  [10] ghg_p50
  [11] ghg_p95
  [12] natural_p05
  [13] natural_p50
  [14] natural_p95
  [15] other_human_forcing_p05
  [16] other_human_forcing_p50
  [17] other_human_forcing_p95
  [18] internal_variability_p05
  [19] internal_variability_p50
  [20] internal_variability_p95
  2015 : total_p05=0.88, total_p50=1.06, total_p95=1.21, anthropogenic_p05=0.8, anthropogenic_p50=1.07, anthropogenic_p95=1.3, natural_p05=-0.1, natural_p50=0.03, natural_p95=0.1

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming_by_species/ERF_relative_to_1750.csv → 200
data/anthropogenic_warming_by_species/ERF_relative_to_1750.csv : 11 lignes, 849 o ; début :
  Compound emitted,Total_p5,Total_p50,Total_p95,CO2,CH4,N2O,CFC+HCFC+other,HFC,Ozone,Strat H2O,ARI,ACI,LAPSI,Land use
  CO2,1.913,2.216,2.533,2.295,-0.021,-0.002,0,0,-0.054,-0.003,0,0,0,0
  CH4,0.889,1.063,1.233,0.078,0.638,-0.009,0,0,0.301,0.059,-0.004,0,0,0
  N2O,0.195,0.242,0.287,0.003,-0.034,0.222,0,0,0.055,-0.004,-0.003,0,0,0
  CFC+HCFC+HFC,0.221,0.375,0.532,0.01,0.01,0,0.354,0.052,-0.053,0.001,0,0,0,0
  NOx,-0.561,-0.408,-0.257,-0.009,-0.288,0.004,0,0,-0.067,-0.042,-0.006,0,0,0
fin :
  SO2,-1.629,-0.906,-0.41,-0.046,0.014,0,0,0,0.028,0.002,-0.218,-0.685,0,0
  Organic carbon,-0.223,-0.142,-0.067,-0.006,0.003,0,0,0,0.007,0,-0.084,-0.062,0,0
  Black carbon,0.028,0.178,0.329,-0.011,0.002,0,0,0,0.005,0,0.133,-0.032,0.081,0
  Ammonia,-0.044,-0.039,-0.034,-0.001,0,0,0,0,0.001,0,-0.039,0,0,0
colonnes (15) :
  [0] Compound emitted
  [1] Total_p5
  [2] Total_p50
  [3] Total_p95
  [4] CO2
  [5] CH4
  [6] N2O
  [7] CFC+HCFC+other
  [8] HFC
  [9] Ozone
  [10] Strat H2O
  [11] ARI
  [12] ACI
  [13] LAPSI
  [14] Land use

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/anthropogenic_warming_by_species/temperature_relative_to_1750.csv → 200
data/anthropogenic_warming_by_species/temperature_relative_to_1750.csv : 11 lignes, 839 o ; début :
  Compound emitted,Total_p5,Total_p50,Total_p95,CO2,CH4,N2O,CFC+HCFC+other,HFC,Ozone,Strat H2O,ARI,ACI,LAPSI,Land use
  CO2,0.835,1.097,1.478,1.134,-0.01,-0.001,0,0,-0.025,-0.001,0,0,0,0
  CH4,0.39,0.559,0.831,0.042,0.328,-0.005,0,0,0.16,0.035,-0.002,0,0,0
  N2O,0.086,0.121,0.179,0.003,-0.016,0.11,0,0,0.027,-0.002,-0.001,0,0,0
  CFC+HCFC+HFC,0.099,0.188,0.298,0.007,0.005,0,0.173,0.025,-0.023,0.001,0,0,0,0
  NOx,-0.3,-0.185,-0.098,-0.004,-0.124,0.002,0,0,-0.041,-0.016,-0.003,0,0,0
fin :
  SO2,-1.016,-0.438,-0.161,-0.016,0.006,0,0,0,0.012,0.001,-0.115,-0.325,0,0
  Organic carbon,-0.131,-0.068,-0.028,-0.003,0.001,0,0,0,0.003,0,-0.039,-0.03,0,0
  Black carbon,0.014,0.085,0.164,-0.006,0.001,0,0,0,0.002,0,0.066,-0.014,0.035,0
  Ammonia,-0.028,-0.019,-0.014,0,0,0,0,0,0.001,0,-0.02,0,0,0
colonnes (15) :
  [0] Compound emitted
  [1] Total_p5
  [2] Total_p50
  [3] Total_p95
  [4] CO2
  [5] CH4
  [6] N2O
  [7] CFC+HCFC+other
  [8] HFC
  [9] Ozone
  [10] Strat H2O
  [11] ARI
  [12] ACI
  [13] LAPSI
  [14] Land use

GET https://raw.githubusercontent.com/ClimateIndicator/data/v2026.06.02/data/effective_radiative_forcing/ERF_best_aggregates.csv → 200
data/effective_radiative_forcing/ERF_best_aggregates.csv : 277 lignes, 63032 o ; début :
  time,timebound_lower,timebound_upper,CO2,CH4,N2O,aerosol-radiation_interactions,aerosol-cloud_interactions,O3,contrails,land_use,BC_on_snow,H2O_stratospheric,solar,volcanic,aerosol,nonco2wmghg,halogen,anthro,total,minor
  1750.5,1750,1751,0,0,0,0,0,0,0,0,0,0,0.02159121,0.234943996,0,0,0,0,0.256535206,0
  1751.5,1751,1752,0.001417292,0.00050833,7.45E-05,0.00063088,0.003830106,-0.000441436,0,-0.000102748,-0.000373548,3.45E-05,0.000780029,0.243453584,0.004460986,0.000582811,7.96E-10,0.005577837,0.249811451,-0.000441816
  1752.5,1752,1753,0.002834247,0.001016353,0.000148952,0.001155533,0.005575433,-0.000409538,0,-0.000208278,-0.000498196,6.90E-05,-0.009079541,0.240777285,0.006730966,0.001165307,1.59E-09,0.009683466,0.24138121,-0.000637515
  1753.5,1753,1754,0.004250863,0.00152407,0.000223415,0.000637431,0.003859007,-0.000148817,0,-0.000316458,-0.000373606,0.000103439,-0.023619287,0.096083654,0.004496438,0.001747487,2.39E-09,0.009759347,0.082223714,-0.000586625
  1754.5,1754,1755,0.005667143,0.00203148,0.00029787,-0.000531038,-0.000976127,0.000746417,0,-0.000427292,5.40E-05,0.000137919,-0.042745605,-0.028037303,-0.001507165,0.002329353,3.18E-09,0.007000389,-0.063782518,-0.000235359
fin :
  2022.5,2022,2023,2.254943801,0.56043814,0.220709783,-0.186828766,-0.738823282,0.471179781,0.046869746,-0.190703752,0.070228328,0.051972021,0.049297854,-0.035362432,-0.925652049,1.19186273,0.410714806,2.970700606,2.984636029,-0.021633657
  2023.5,2023,2024,2.28600009,0.564151658,0.224036374,-0.242386944,-0.888389074,0.50112113,0.058994272,-0.191346276,0.083364666,0.052421773,0.10892329,0.168161177,-1.130776018,1.199269908,0.411081876,2.859049545,3.136134012,0.003434435
  2024.5,2024,2025,2.33245544,0.566915515,0.227302407,-0.215542654,-0.850660996,0.502505798,0.06487882,-0.191844339,0.082753389,0.052759033,0.123899855,0.16631884,-1.066203649,1.20582544,0.411607518,2.983129933,3.273348628,0.008546903
  2025.5,2025,2026,2.370924636,0.569585072,0.231590531,-0.198500872,-0.763304221,0.482354429,0.067500187,-0.192211005,0.069986847,0.053087731,0.10486714,0.157269385,-0.961805093,1.213710883,0.41253528,3.103548614,3.365685139,-0.001636241
colonnes (21) :
  [0] time
  [1] timebound_lower
  [2] timebound_upper
  [3] CO2
  [4] CH4
  [5] N2O
  [6] aerosol-radiation_interactions
  [7] aerosol-cloud_interactions
  [8] O3
  [9] contrails
  [10] land_use
  [11] BC_on_snow
  [12] H2O_stratospheric
  [13] solar
  [14] volcanic
  [15] aerosol
  [16] nonco2wmghg
  [17] halogen
  [18] anthro
  [19] total
  [20] minor
  1750 : CO2=0, aerosol-radiation_interactions=0, aerosol-cloud_interactions=0, solar=0.02159121, volcanic=0.234943996, aerosol=0, nonco2wmghg=0, anthro=0, total=0.256535206
  1850 : CO2=0.140085694, aerosol-radiation_interactions=-0.002316131, aerosol-cloud_interactions=-0.080306524, solar=0.024056105, volcanic=0.243994885, aerosol=-0.082622655, nonco2wmghg=0.056794685, anthro=0.114934428, total=0.382985418
  1900 : CO2=0.346108024, aerosol-radiation_interactions=-0.051813175, aerosol-cloud_interactions=-0.314563739, solar=-0.044321265, volcanic=0.222365168, aerosol=-0.366376914, nonco2wmghg=0.150632696, anthro=0.125888349, total=0.303932252
  1991 : CO2=1.351444166, aerosol-radiation_interactions=-0.373625409, aerosol-cloud_interactions=-1.115266116, solar=0.0533072, volcanic=-0.528646173, aerosol=-1.488891524, nonco2wmghg=0.970215698, anthro=1.200070662, total=0.724731689
  2000 : CO2=1.561558246, aerosol-radiation_interactions=-0.290258149, aerosol-cloud_interactions=-0.928315266, solar=0.08413396, volcanic=0.221501502, aerosol=-1.218573414, nonco2wmghg=1.041393174, anthro=1.759140547, total=2.064776008
  2015 : CO2=2.012418971, aerosol-radiation_interactions=-0.258297055, aerosol-cloud_interactions=-0.935952187, solar=0.045194898, volcanic=0.138081906, aerosol=-1.194249242, nonco2wmghg=1.13002918, anthro=2.420625177, total=2.603901981
  2020 : CO2=2.191284528, aerosol-radiation_interactions=-0.18793836, aerosol-cloud_interactions=-0.768604485, solar=-0.03483611, volcanic=0.031984631, aerosol=-0.956542844, nonco2wmghg=1.169907089, anthro=2.831608041, total=2.828756563
  2023 : CO2=2.28600009, aerosol-radiation_interactions=-0.242386944, aerosol-cloud_interactions=-0.888389074, solar=0.10892329, volcanic=0.168161177, aerosol=-1.130776018, nonco2wmghg=1.199269908, anthro=2.859049545, total=3.136134012
  2024 : CO2=2.33245544, aerosol-radiation_interactions=-0.215542654, aerosol-cloud_interactions=-0.850660996, solar=0.123899855, volcanic=0.16631884, aerosol=-1.066203649, nonco2wmghg=1.20582544, anthro=2.983129933, total=3.273348628
  2025 : CO2=2.370924636, aerosol-radiation_interactions=-0.198500872, aerosol-cloud_interactions=-0.763304221, solar=0.10486714, volcanic=0.157269385, aerosol=-0.961805093, nonco2wmghg=1.213710883, anthro=3.103548614, total=3.365685139
```

## 3. Archive Zenodo de l'IGCC 2025

```
GET https://zenodo.org/records/20499280/files/ClimateIndicator/data-v2026.06.02.zip?download=1 → 200 (URL finale : https://zenodo.org/records/20499280/files/ClimateIndicator/data-v2026.06.02.zip?download=1, 350903 o)
56 fichiers dans l'archive, dont :
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Assessment-Extrapolation-2026_GMST_headlines.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Assessment-Update-2025_GMST_headlines.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Gillett_GMST_headlines.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Gillett_GMST_rates.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Gillett_GMST_timeseries.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Gillett_GSAT_headlines.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Ribes_GMST_headlines.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Ribes_GMST_rates.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Ribes_GMST_timeseries.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Walsh_GMST_headlines.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Walsh_GMST_rates.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/Walsh_GMST_timeseries.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming/assessment_6thIPCC_headlines.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming_by_species/
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming_by_species/ERF_relative_to_1750.csv
  ClimateIndicator-data-fc025c5/data/anthropogenic_warming_by_species/temperature_relative_to_1750.csv
  ClimateIndicator-data-fc025c5/data/effective_radiative_forcing/
  ClimateIndicator-data-fc025c5/data/effective_radiative_forcing/ERF_best.csv
  ClimateIndicator-data-fc025c5/data/effective_radiative_forcing/ERF_best_aggregates.csv
  ClimateIndicator-data-fc025c5/data/effective_radiative_forcing/ERF_p05_aggregates.csv
  ClimateIndicator-data-fc025c5/data/effective_radiative_forcing/ERF_p95_aggregates.csv
```

## 4. Dépôt ClimateIndicator/forcing-timeseries (repli)

```
GET https://raw.githubusercontent.com/ClimateIndicator/forcing-timeseries/main/output/ERF_best_aggregates_1750-2025.csv → 404
GET https://raw.githubusercontent.com/ClimateIndicator/forcing-timeseries/main/output/ERF_best_aggregates_1750-2024.csv → 200
forcing-timeseries ERF_best_aggregates_1750-2024.csv : 276 lignes, 95978 o ; début :
  ,CO2,CH4,N2O,aerosol-radiation_interactions,aerosol-cloud_interactions,O3,contrails,land_use,BC_on_snow,H2O_stratospheric,solar,volcanic,aerosol,nonco2wmghg,halogen,anthro,total,minor
  1750.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0975902619928896,0.2036797672164808,0.0,0.0,0.0,0.0,0.3012700292093704,0.0
  1751.5,0.0014172921112884,0.0005083303609513,7.447998437287891e-05,0.0006308845061278,0.003830106252043,-0.0004415655030818,0.0,-0.000113617374201,-0.0003735479174186,3.4468962545778735e-05,0.0792439729303896,0.2373240566550054,0.0044609907581708,0.0005828111411251383,7.95800959445302e-10,0.005566832178428717,0.3221348617638237,-0.0004526963290738213
  1752.5,0.0028342465443867,0.0010163534983993,0.0001489516272727,0.0011555409039767,0.0055754332059953,-0.0004098011126201,0.0,-0.0002300173155576,-0.0004981963309232,6.893792509155747e-05,0.0491660432428896,0.2400695263145829,0.006730974109972,0.0011653067172739187,1.591601918863499e-09,0.009661450537623278,0.2988970200950957,-0.0006592757213892426
  1753.5,0.0042508634756802,0.0015240699051992,0.0002234149335544,0.0006374366449913,0.0038590068802683,-0.0001489097387128,0.0,-0.0003491008768811,-0.0003736060615026,0.0001034068876373,0.0129882844538271,0.0911636178130514,0.0044964435252596,0.0017474872261564781,2.387402878335906e-09,0.009726584437637078,0.11387848670451557,-0.0006193000507464
  1754.5,0.0056671430814174,0.0020314800728868,0.0002978699080647,-0.0005310392494566,-0.0009761265788652,0.0007465910272211,0.0,-0.0004708188548886,5.401428737235632e-05,0.0001378758501831,-0.0214266081242978,-0.0719729641034113,-0.0015071658283218,0.0023293531641553375,3.183203837781208e-09,0.006956992727138894,-0.0864425795005702,-0.00027892871733314363
fin :
  2021.5,2.2223692156599286,0.5547832151468962,0.2167063744038503,-0.2129940421958346,-0.825746342811742,0.4767560342775575,0.0369090627768414,-0.1914143052782708,0.0775411129827013,0.0512760990279225,0.0195572424081152,0.1324089539306302,-1.0387403850075765,1.1813158367908003,0.40982624724005406,2.8160126712299043,2.9679788675686503,-0.025688030490805577
  2022.5,2.2549438356653644,0.5607529946756031,0.220700848405676,-0.1868332168426101,-0.7388232821735552,0.4713554533020591,0.0468697462071381,-0.1916025012428275,0.0702283277354315,0.0519933963798796,0.0593930607808931,0.1717053055526579,-0.9256564990161653,1.1921714467504767,0.4107176036691978,2.9703032057813568,3.201401572114908,-0.02251103092037829
  2023.5,2.286000327446032,0.5644983923879584,0.2240016540417672,-0.2424531061694524,-0.8883890739449806,0.5009257923665269,0.0513603146136405,-0.1921963728308303,0.0833646662746049,0.0524469006511292,0.0819815979437634,0.2649792325799306,-1.130842180114433,1.1995668865399325,0.41106684011020683,2.8506263349466034,3.197587165470297,-0.005024491291455713
  2024.5,2.332456921700882,0.5672422484317926,0.2271160775123725,-0.2155527774242096,-0.8506609955749056,0.5025805833884345,0.0563846932171489,-0.1925630395096181,0.082753389301028,0.0527814782084932,0.0908372542604376,0.2379542280569292,-1.0662137729991152,1.2058561645268213,0.41149783858265576,2.974036417834073,3.3028279001514402,-0.0006434787829479871
colonnes (19) :
  [0] 
  [1] CO2
  [2] CH4
  [3] N2O
  [4] aerosol-radiation_interactions
  [5] aerosol-cloud_interactions
  [6] O3
  [7] contrails
  [8] land_use
  [9] BC_on_snow
  [10] H2O_stratospheric
  [11] solar
  [12] volcanic
  [13] aerosol
  [14] nonco2wmghg
  [15] halogen
  [16] anthro
  [17] total
  [18] minor
  1750 : CO2=0.0, aerosol-radiation_interactions=0.0, aerosol-cloud_interactions=0.0, solar=0.0975902619928896, volcanic=0.2036797672164808, aerosol=0.0, nonco2wmghg=0.0, anthro=0.0, total=0.3012700292093704
  1850 : CO2=0.1400856935210565, aerosol-radiation_interactions=-0.0023160861633848, aerosol-cloud_interactions=-0.0803065241491151, solar=0.0075280793757021, volcanic=0.2441423707854478, aerosol=-0.0826226103124999, nonco2wmghg=0.05679468548653064, anthro=0.11356126326124073, total=0.36523171342239064
  1900 : CO2=0.3461080235138764, aerosol-radiation_interactions=-0.0518133510845896, aerosol-cloud_interactions=-0.3145637387449568, solar=-0.0372456022649228, volcanic=0.1787201674541813, aerosol=-0.3663770898295464, nonco2wmghg=0.1506326958413889, anthro=0.12357342364926949, total=0.26504798883852815
  1991 : CO2=1.3514441660271503, aerosol-radiation_interactions=-0.373625265439717, aerosol-cloud_interactions=-1.115266115505352, solar=0.1041113069147646, volcanic=-0.6050179917349862, aerosol=-1.488891380945069, nonco2wmghg=0.9702156983459485, anthro=1.1974786070737489, total=0.6965719222535276
  2000 : CO2=1.5615582458017463, aerosol-radiation_interactions=-0.2902575648366037, aerosol-cloud_interactions=-0.9283152657699796, solar=0.1100083283991396, volcanic=0.2207802836460415, aerosol=-1.2185728306065833, nonco2wmghg=1.0413931736729356, anthro=1.7571766423666408, total=2.0879652544118223
  2015 : CO2=2.012418970596195, aerosol-radiation_interactions=-0.2582986921108368, aerosol-cloud_interactions=-0.9359521868428032, solar=0.0291972932428896, volcanic=0.1539105435566783, aerosol=-1.19425087895364, nonco2wmghg=1.1300039122140795, anthro=2.419641587830629, total=2.602749424630198
  2020 : CO2=2.191284519486243, aerosol-radiation_interactions=-0.1879439714940403, aerosol-cloud_interactions=-0.7686044845934813, solar=-0.0169686341312789, volcanic=0.074220309491307, aerosol=-0.9565484560875216, nonco2wmghg=1.1702882637857224, anthro=2.831289520854589, total=2.8885411962146166
  2023 : CO2=2.286000327446032, aerosol-radiation_interactions=-0.2424531061694524, aerosol-cloud_interactions=-0.8883890739449806, solar=0.0819815979437634, volcanic=0.2649792325799306, aerosol=-1.130842180114433, nonco2wmghg=1.1995668865399325, anthro=2.8506263349466034, total=3.197587165470297
  2024 : CO2=2.332456921700882, aerosol-radiation_interactions=-0.2155527774242096, aerosol-cloud_interactions=-0.8506609955749056, solar=0.0908372542604376, volcanic=0.2379542280569292, aerosol=-1.0662137729991152, nonco2wmghg=1.2058561645268213, anthro=2.974036417834073, total=3.3028279001514402
```

## 5. Niño 3.4 HadISST1.1 (NOAA PSL)

```
GET https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/nino34.long.data → 404 (URL finale : https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/nino34.long.data)

GET https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/nino34.long.anom.data → 404 (URL finale : https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/nino34.long.anom.data)

GET https://psl.noaa.gov/data/timeseries/month/data/nino34.long.data → 200 (URL finale : https://psl.noaa.gov/data/timeseries/month/data/nino34.long.data)
nino34.long.data : 162 lignes, 16186 o ; début :
            1870        2025
   1870    25.58   25.57   26.43   26.96   26.59   26.61   26.19   25.99   26.22   25.82   25.86   25.79
   1871    26.33   26.18   26.83   27.27   27.16   27.16   26.62   26.54   26.51   26.40   26.35   26.01
   1872    25.86   26.14   26.76   27.00   27.25   27.16   26.91   26.02   25.73   25.79   25.86   25.71
fin :
   2023    25.80   26.14   27.13   28.01   28.34   28.63   28.43   28.44   28.41   28.32   28.66   28.40
   2024    28.29   28.24   28.36   28.70   28.27   27.94   27.42   26.89   26.65   26.49   26.60   26.01
   2025    25.82   26.37   27.31   27.69   27.79   27.69   27.19   26.76  -99.99  -99.99  -99.99  -99.99
    -99.99
    NINA34
   5N-5S 170W-120W 
   HadISST 
   https://psl.noaa.gov/data/timeseries/month/
lignes annuelles à 13 champs : 156 (1870 → 2025), années complètes : 155 (1870 → 2024)

GET https://psl.noaa.gov/data/timeseries/month/data/nino34.long.anom.data → 200 (URL finale : https://psl.noaa.gov/data/timeseries/month/data/nino34.long.anom.data)
nino34.long.anom.data : 165 lignes, 16327 o ; début :
            1870        2026
   1870    -1.00   -1.20   -0.83   -0.81   -1.27   -1.08   -1.04   -0.88   -0.53   -0.92   -0.79   -0.79
   1871    -0.25   -0.58   -0.43   -0.50   -0.71   -0.53   -0.60   -0.33   -0.24   -0.33   -0.31   -0.58
   1872    -0.72   -0.62   -0.50   -0.77   -0.62   -0.52   -0.32   -0.85   -1.02   -0.94   -0.79   -0.88
fin :
   2026    -0.54   -0.25   -0.12    0.38    0.80    1.37    1.90    2.37    2.63  -99.99  -99.99  -99.99
    -99.99
    NINA34
   5N-5S 170W-120W 
   HadISST 
    Anomaly from 1981-2010
   https://psl.noaa.gov/data/timeseries/month/
    units=degC
lignes annuelles à 13 champs : 157 (1870 → 2026), années complètes : 156 (1870 → 2025)

```
