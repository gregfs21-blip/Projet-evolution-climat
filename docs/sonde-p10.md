# Sonde P10 — régression multiple : forçages et ENSO (généré)

Généré par `python -m etl.probe.p10` le 20/11/2026 10:52 UTC. Aucune régression, aucun indicateur calculé.

## 1. Dépôt ClimateIndicator/data (v2026.06.02) : racine

```
GET https://api.github.com/repos/ClimateIndicator/data/contents/?ref=v2026.06.02 → 403
GET https://api.github.com/repos/ClimateIndicator/data/contents/data?ref=v2026.06.02 → 403
```

## 2. IGCC 2025 : forçages et réchauffement attribué

```
GET https://api.github.com/repos/ClimateIndicator/data/git/trees/v2026.06.02?recursive=1 → 403
0 fichiers, dont 0 retenus (forçage, attribution, température) :
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
