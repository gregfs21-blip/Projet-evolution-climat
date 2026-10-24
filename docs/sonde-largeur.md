# Sonde « largeur d'abord » — sources candidates (généré)

Généré par `python -m etl.probe.largeur` le 23/10/2026 21:16 UTC. Aucun calcul : accessibilité et format constaté.

| Source | Paramètre | Statut | Taille | Type |
|---|---|---|---|---|
| `co2-mlo` | GES — CO₂ Mauna Loa annuel | 200 | 3 ko | text/csv |
| `co2-gl` | GES — CO₂ global annuel | 200 | 3 ko | text/csv |
| `ch4-gl` | GES — CH₄ global annuel | 200 | 3 ko | text/csv |
| `n2o-gl` | GES — N₂O global annuel | 200 | 2 ko | text/csv |
| `gistemp` | Température globale — NASA GISTEMP v4 | 200 | 13 ko | text/csv |
| `hadcrut5` | Température globale — HadCRUT5 | 200 | 7 ko | text/csv |
| `berkeley` | Température globale — Berkeley Earth | 200 | 26 ko | text/plain |
| `hadsst4` | Température de la mer — HadSST4 global annuel | 404 | 0 ko |  |
| `oni` | El Niño — indice ONI (NOAA CPC) | 200 | 23 ko | text/plain; charset=utf-8 |
| `nsidc-n09-v3` | Fonte des glaces — banquise arctique de septembre (v3) | 404 | 0 ko |  |
| `nsidc-n09-v4` | Fonte des glaces — banquise arctique de septembre (v4) | 200 | 2 ko | application/octet-stream |
| `nsidc-s02-v4` | Fonte des glaces — banquise antarctique de février (v4) | 200 | 2 ko | application/octet-stream |
| `ohc-700` | Contenu thermique des océans 0-700 m (NOAA NCEI) | 200 | 4 ko |  |
| `ohc-2000` | Contenu thermique des océans 0-2000 m (NOAA NCEI) | 200 | 1 ko |  |
| `gmsl-star` | Niveau des océans — altimétrie (NOAA STAR) | 404 | 0 ko |  |
| `gmsl-csiro` | Niveau des océans — reconstruction CSIRO (Church & White) | erreur : URLError <urlopen error [Errno 101] Network is unreachable> | 0 ko |  |
| `psmsl-list` | Niveau des océans — liste des marégraphes PSMSL (annuel RLR) | 200 | 141 ko | text/plain; charset=UTF-8 |
| `ozone-hole` | Couche d'ozone — trou antarctique (NASA Ozone Watch) | erreur : URLError <urlopen error [Errno 101] Network is unreachable> | 0 ko |  |
| `ibtracs-na` | Ouragans — IBTrACS Atlantique Nord (NOAA) | 200 | 40000 ko | text/csv |
| `igra-merignac` | Température en altitude — radiosondages Mérignac, dérivés (IGRA) | 200 | 40000 ko | application/zip |
| `gcb` | Puits de carbone — Global Carbon Budget (liste des fichiers) | 404 | 0 ko |  |
| `ceres` | Déséquilibre énergétique — CERES EBAF (page d'accès) | 200 | 6746 ko | text/html; charset=utf-8 |

### `co2-mlo` — GES — CO₂ Mauna Loa annuel

https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.csv

```
# --------------------------------------------------------------------
# USE OF NOAA GML DATA
#
# These data are made freely available to the public and the scientific
# community in the belief that their wide dissemination will lead to
# greater understanding and new scientific insights. To ensure that GML
# receives fair credit for their work please include relevant citation
# text in publications. We encourage users to contact the data providers,
# who can provide detailed information about the measurements and
# scientific insight.  In cases where the data are central to a
# publication, coauthorship for data providers may be appropriate.
#
#
#
```

### `co2-gl` — GES — CO₂ global annuel

https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_gl.csv

```
# --------------------------------------------------------------------
# USE OF NOAA GML DATA
#
# These data are made freely available to the public and the scientific
# community in the belief that their wide dissemination will lead to
# greater understanding and new scientific insights. To ensure that GML
# receives fair credit for their work please include relevant citation
# text in publications. We encourage users to contact the data providers,
# who can provide detailed information about the measurements and
# scientific insight.  In cases where the data are central to a
# publication, coauthorship for data providers may be appropriate.
#
#
#
```

### `ch4-gl` — GES — CH₄ global annuel

https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_annmean_gl.csv

```
# --------------------------------------------------------------------
# USE OF NOAA GML DATA
#
# These data are made freely available to the public and the scientific
# community in the belief that their wide dissemination will lead to
# greater understanding and new scientific insights. To ensure that GML
# receives fair credit for their work please include relevant citation
# text in publications. We encourage users to contact the data providers,
# who can provide detailed information about the measurements and
# scientific insight.  In cases where the data are central to a
# publication, coauthorship for data providers may be appropriate.
#
#
#
```

### `n2o-gl` — GES — N₂O global annuel

https://gml.noaa.gov/webdata/ccgg/trends/n2o/n2o_annmean_gl.csv

```
# --------------------------------------------------------------------
# USE OF NOAA GML DATA
#
# These data are made freely available to the public and the scientific
# community in the belief that their wide dissemination will lead to
# greater understanding and new scientific insights. To ensure that GML
# receives fair credit for their work please include relevant citation
# text in publications. We encourage users to contact the data providers,
# who can provide detailed information about the measurements and
# scientific insight.  In cases where the data are central to a
# publication, coauthorship for data providers may be appropriate.
#
#
#
```

### `gistemp` — Température globale — NASA GISTEMP v4

https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv

```
Land-Ocean: Global Means
Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D,D-N,DJF,MAM,JJA,SON
1880,-.19,-.25,-.09,-.16,-.10,-.21,-.19,-.10,-.15,-.23,-.22,-.18,-.17,***,***,-.12,-.17,-.20
1881,-.20,-.14,.03,.05,.06,-.19,.00,-.03,-.15,-.22,-.19,-.07,-.09,-.10,-.17,.05,-.07,-.18
1882,.16,.13,.04,-.16,-.14,-.22,-.16,-.08,-.15,-.23,-.17,-.36,-.11,-.09,.07,-.09,-.16,-.18
1883,-.29,-.37,-.12,-.18,-.18,-.07,-.08,-.14,-.22,-.11,-.24,-.11,-.18,-.20,-.34,-.16,-.10,-.19
1884,-.13,-.08,-.36,-.40,-.33,-.35,-.30,-.28,-.27,-.25,-.33,-.31,-.28,-.27,-.11,-.36,-.31,-.28
1885,-.58,-.34,-.27,-.42,-.45,-.44,-.34,-.31,-.28,-.23,-.24,-.10,-.33,-.35,-.41,-.38,-.36,-.25
1886,-.44,-.51,-.43,-.28,-.24,-.35,-.18,-.30,-.23,-.27,-.28,-.25,-.31,-.30,-.35,-.32,-.28,-.26
1887,-.72,-.57,-.35,-.35,-.30,-.25,-.26,-.35,-.25,-.35,-.26,-.33,-.36,-.35,-.51,-.33,-.29,-.29
1888,-.34,-.36,-.42,-.21,-.22,-.17,-.11,-.16,-.12,.01,.02,-.04,-.18,-.20,-.35,-.28,-.14,-.03
1889,-.09,.16,.06,.09,-.01,-.10,-.08,-.20,-.24,-.25,-.34,-.29,-.11,-.09,.01,.05,-.13,-.28
1890,-.42,-.45,-.40,-.30,-.39,-.25,-.28,-.39,-.37,-.25,-.44,-.32,-.36,-.35,-.39,-.37,-.31,-.35
1891,-.34,-.46,-.18,-.27,-.16,-.21,-.18,-.17,-.15,-.22,-.31,-.04,-.22,-.25,-.37,-.21,-.19,-.23
```

### `hadcrut5` — Température globale — HadCRUT5

https://www.metoffice.gov.uk/hadobs/hadcrut5/data/HadCRUT.5.0.2.0/analysis/diagnostics/HadCRUT.5.0.2.0.analysis.summary_series.global.annual.csv

```
Time,Anomaly (deg C),Lower confidence limit (2.5%),Upper confidence limit (97.5%)
1850,-0.4177114,-0.58925647,-0.2461663
1851,-0.2333498,-0.41186792,-0.054831687
1852,-0.22939907,-0.40938243,-0.04941572
1853,-0.27035445,-0.43000934,-0.110699534
1854,-0.29152083,-0.4327115,-0.15033019
1855,-0.29691675,-0.43931878,-0.15451474
1856,-0.32035372,-0.46809322,-0.1726142
1857,-0.46723005,-0.61632216,-0.31813794
1858,-0.3887657,-0.53688604,-0.24064532
1859,-0.28126517,-0.42392084,-0.1386095
1860,-0.39016518,-0.5389766,-0.24135375
1861,-0.42911294,-0.597001,-0.26122484
1862,-0.5363694,-0.70365995,-0.3690788
```

### `berkeley` — Température globale — Berkeley Earth

https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_summary.txt

```
% This file contains a brief summary of the changes in Earth's global average
% surface temperature estimated by combining the Berkeley Earth land-surface
% temperature field with a reinterpolated version of the HadSST4 ocean temperature 
% field.  
% 
% The current citation for this dataset is: 
% 
%    Rohde, R. A. and Hausfather, Z.: The Berkeley Earth Land/Ocean Temperature
%    Record, Earth Syst. Sci. Data, 12, 3469�3479, 
%    https://doi.org/10.5194/essd-12-3469-2020, 2020.
% 
% The dataset differs slightly from the dataset as described in the citation as 
% HadSST3 has been replaced with the newer HadSST4, and associated interpolation 
% parameters have been refit accordingly.  No other changes in methods were needed 
```

### `hadsst4` — Température de la mer — HadSST4 global annuel

https://www.metoffice.gov.uk/hadobs/hadsst4/data/csv/HadSST.4.0.1.0_annual_GLOBE.csv

```
(aucune donnée)
```

### `oni` — El Niño — indice ONI (NOAA CPC)

https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt

```
 SEAS  YR   TOTAL   ANOM
  DJF 1950  25.01  -1.32
  JFM 1950  25.36  -1.20
  FMA 1950  25.88  -1.12
  MAM 1950  26.24  -1.08
  AMJ 1950  26.35  -1.10
  MJJ 1950  26.32  -0.90
  JJA 1950  26.24  -0.62
  JAS 1950  25.94  -0.57
  ASO 1950  25.76  -0.56
  SON 1950  25.60  -0.62
  OND 1950  25.55  -0.66
  NDJ 1950  25.41  -0.79
  DJF 1951  25.67  -0.66
```

### `nsidc-n09-v3` — Fonte des glaces — banquise arctique de septembre (v3)

https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/data/N_09_extent_v3.0.csv

```
(aucune donnée)
```

### `nsidc-n09-v4` — Fonte des glaces — banquise arctique de septembre (v4)

https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/data/N_09_extent_v4.0.csv

```
year, mo,source_dataset, region, extent,   area
1979,  9,    NSIDC-0051,      N,   7.05,   4.58
1980,  9,    NSIDC-0051,      N,   7.67,   4.87
1981,  9,    NSIDC-0051,      N,   7.14,   4.44
1982,  9,    NSIDC-0051,      N,   7.30,   4.43
1983,  9,    NSIDC-0051,      N,   7.39,   4.70
1984,  9,    NSIDC-0051,      N,   6.81,   4.11
1985,  9,    NSIDC-0051,      N,   6.70,   4.23
1986,  9,    NSIDC-0051,      N,   7.41,   4.72
1987,  9,    NSIDC-0051,      N,   7.28,   5.64
1988,  9,    NSIDC-0051,      N,   7.37,   5.36
1989,  9,    NSIDC-0051,      N,   7.01,   4.86
1990,  9,    NSIDC-0051,      N,   6.14,   4.55
1991,  9,    NSIDC-0051,      N,   6.47,   4.51
```

### `nsidc-s02-v4` — Fonte des glaces — banquise antarctique de février (v4)

https://noaadata.apps.nsidc.org/NOAA/G02135/south/monthly/data/S_02_extent_v4.0.csv

```
year, mo,source_dataset, region, extent,   area
1979,  2,    NSIDC-0051,      S,   3.14,   2.11
1980,  2,    NSIDC-0051,      S,   2.82,   1.85
1981,  2,    NSIDC-0051,      S,   2.87,   1.74
1982,  2,    NSIDC-0051,      S,   3.13,   1.86
1983,  2,    NSIDC-0051,      S,   3.07,   1.91
1984,  2,    NSIDC-0051,      S,   2.68,   1.75
1985,  2,    NSIDC-0051,      S,   2.84,   1.83
1986,  2,    NSIDC-0051,      S,   3.19,   2.00
1987,  2,    NSIDC-0051,      S,   3.25,   2.00
1988,  2,    NSIDC-0051,      S,   2.89,   1.90
1989,  2,    NSIDC-0051,      S,   2.98,   2.03
1990,  2,    NSIDC-0051,      S,   3.04,   2.21
1991,  2,    NSIDC-0051,      S,   3.16,   2.09
```

### `ohc-700` — Contenu thermique des océans 0-700 m (NOAA NCEI)

https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/yearly/h22-w0-700m.dat

```
    YEAR      WO    WOse      NH    NHse      SH    SHse
1955.500  -3.201   1.700  -1.439   0.937  -1.762   0.771
1956.500  -2.608   0.719  -1.843   0.385  -0.765   0.533
1957.500  -4.613   0.396  -2.242   0.186  -2.371   0.278
1958.500  -1.533   0.687  -0.190   0.163  -1.343   0.676
1959.500  -2.189   0.863  -0.554   0.545  -1.636   0.419
1960.500  -1.442   0.499   0.295   0.695  -1.737   0.586
1961.500  -2.115   0.421  -1.282   0.602  -0.833   0.282
1962.500  -1.075   0.947  -0.468   0.581  -0.607   0.471
1963.500  -2.272   0.650  -1.911   0.385  -0.361   0.744
1964.500  -3.121   0.922  -1.232   0.376  -1.890   0.705
1965.500  -3.060   0.307  -1.157   0.371  -1.903   0.331
1966.500  -3.944   0.456  -1.383   0.497  -2.560   0.262
1967.500  -4.361   0.372  -2.207   0.107  -2.154   0.476
```

### `ohc-2000` — Contenu thermique des océans 0-2000 m (NOAA NCEI)

https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/yearly/h22-w0-2000m.dat

```
    YEAR      WO    WOse      NH    NHse      SH    SHse
2005.500  10.171   0.835   6.004   0.133   4.167   0.807
2006.500  12.638   0.327   6.548   0.348   6.090   0.394
2007.500  12.394   0.434   6.787   0.278   5.607   0.497
2008.500  13.257   0.519   6.987   0.391   6.270   0.159
2009.500  13.431   0.636   6.441   0.062   6.990   0.653
2010.500  14.537   0.527   6.822   0.115   7.715   0.626
2011.500  15.394   0.507   6.156   0.245   9.239   0.365
2012.500  16.187   0.473   6.984   0.216   9.203   0.426
2013.500  18.650   1.059   8.530   0.107  10.120   1.011
2014.500  20.110   0.589   7.743   0.360  12.367   0.454
2015.500  22.401   0.385   8.408   0.362  13.993   0.242
2016.500  20.799   0.832   9.870   0.419  10.929   1.172
2017.500  23.589   0.563  10.936   0.263  12.653   0.591
```

### `gmsl-star` — Niveau des océans — altimétrie (NOAA STAR)

https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_gbl_free_txj1j2_90.csv

```
(aucune donnée)
```

### `gmsl-csiro` — Niveau des océans — reconstruction CSIRO (Church & White)

https://www.cmar.csiro.au/sealevel/downloads/church_white_gmsl_2011_up.zip

```
(aucune donnée)
```

### `psmsl-list` — Niveau des océans — liste des marégraphes PSMSL (annuel RLR)

https://psmsl.org/data/obtaining/rlr.annual.data/filelist.txt

```
    1;  48.382850;   -4.494838; BREST                                   ; 190; 091; N
    2;  53.916667;   14.233333; SWINOUJSCIE                             ; 110; 092; N
    3;  51.445639;    0.743444; SHEERNESS                               ; 170; 101; N
    5;  53.313944;   -4.620444; HOLYHEAD                                ; 170; 191; Y
    7;  53.866667;    8.716667; CUXHAVEN 2                              ; 140; 012; N
    8;  53.898889;   11.458056; WISMAR 2                                ; 120; 022; N
    9;  51.917500;    4.249722; MAASSLUIS                               ; 150; 061; N
   10;  37.806667; -122.465000; SAN FRANCISCO                           ; 823; 031; N
   11;  54.169722;   12.103333; WARNEMUNDE 2                            ; 120; 012; N
   12;  40.700000;  -74.013333; NEW YORK (THE BATTERY)                  ; 960; 121; N
   13;  53.958056;   10.872222; TRAVEMUNDE                              ; 125; 001; N
   14;  60.153633;   24.956217; HELSINKI                                ; 060; 351; N
   15;  53.400000;   -3.000000; LIVERPOOL GEORGES AND PRINCES PIERS     ; 170; 211; Y
   16;  60.850000;   21.183333; LYOKKI                                  ; 060; 221; N

[stations façade atlantique française]
    1;  48.382850;   -4.494838; BREST                                   ; 190; 091; N
  457;  47.270000;   -2.200000; ST. NAZAIRE                             ; 190; 111; N
  459;  45.550000;   -1.066667; LE VERDON                               ; 190; 131; N
  466;  46.158478;   -1.220736; LA ROCHELLE-LA PALLICE                  ; 190; 121; N
  469;  43.395239;   -1.681623; ST JEAN DE LUZ (SOCOA)                  ; 190; 141; N
 1801;  43.527302;   -1.514830; BOUCAU                                  ; 190; 139; N
 1918;  44.665001;   -1.163550; ARCACHON-EYRAC                          ; 190; 140; N
```

### `ozone-hole` — Couche d'ozone — trou antarctique (NASA Ozone Watch)

https://ozonewatch.gsfc.nasa.gov/meteorology/annual_data.txt

```
(aucune donnée)
```

### `ibtracs-na` — Ouragans — IBTrACS Atlantique Nord (NOAA)

https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.NA.list.v04r01.csv

```
SID,SEASON,NUMBER,BASIN,SUBBASIN,NAME,ISO_TIME,NATURE,LAT,LON,WMO_WIND,WMO_PRES,WMO_AGENCY,TRACK_TYPE,DIST2LAND,LANDFALL,IFLAG,USA_AGENCY,USA_ATCF_ID,USA_LAT,USA_LON,USA_RECORD,USA_STATUS,USA_WIND,USA_PRES,USA_SSHS,USA_R34_NE,USA_R34_SE,USA_R34_SW,USA_R34_NW,USA_R50_NE,USA_R50_SE,USA_R50_SW,USA_R50_NW,USA_R64_NE,USA_R64_SE,USA_R64_SW,USA_R64_NW,USA_POCI,USA_ROCI,USA_RMW,USA_EYE,TOKYO_LAT,TOKYO_LON,TOKYO_GRADE,TOKYO_WIND,TOKYO_PRES,TOKYO_R50_DIR,TOKYO_R50_LONG,TOKYO_R50_SHORT,TOKYO_R30_DIR,TOKYO_R30_LONG,TOKYO_R30_SHORT,TOKYO_LAND,CMA_LAT,CMA_LON,CMA_CAT,CMA_WIND,CMA_PRES,HKO_LAT,HKO_LON,HKO_CAT,HKO_WIND,HKO_PRES,KMA_LAT,KMA_LON,KMA_CAT,KMA_WIND,KMA_PRES,KMA_R50_DIR,KMA_R50_LONG,KMA_R50_SHORT,KMA_R30_DIR,KMA_R30_LONG,KMA_R30_SHORT,NEWDELHI_LAT,NEWDELHI_LON,NEWDELHI_GRADE,NEWDELHI_WIND,NEWDELHI_PRES,NEWDELHI_CI,NEWDELHI_DP,NEWDELHI_POCI,REUNION_LAT,REUNION_LON,REUNION_TYPE,REUNION_WIND,REUNION_PRES,REUNION_TNUM,REUNION_CI,REUNION_RMW,REUNION_R34_NE,REUNION_R34_SE,REUNION_R34_SW,REUNION_R34_NW,REUNION_R50_NE,REUNION_R50_SE,REUNION_R50_SW,REUNION_R50_NW,REUNION_R64_NE,REUNION_R64_SE,REUNION_R64_SW,REUNION_R64_NW,BOM_LAT,BOM_LON,BOM_TYPE,BOM_WIND,BOM_PRES,BOM_TNUM,BOM_CI,BOM_RMW,BOM_R34_NE,BOM_R34_SE,BOM_R34_SW,BOM_R34_NW,BOM_R50_NE,BOM_R50_SE,BOM_R50_SW,BOM_R50_NW,BOM_R64_NE,BOM_R64_SE,BOM_R64_SW,BOM_R64_NW,BOM_ROCI,BOM_POCI,BOM_EYE,BOM_POS_METHOD,BOM_PRES_METHOD,NADI_LAT,NADI_LON,NADI_CAT,NADI_WIND,NADI_PRES,WELLINGTON_LAT,WELLINGTON_LON,WELLINGTON_WIND,WELLINGTON_PRES,DS824_LAT,DS824_LON,DS824_STAGE,DS824_WIND,DS824_PRES,TD9636_LAT,TD9636_LON,TD9636_STAGE,TD9636_WIND,TD9636_PRES,TD9635_LAT,TD9635_LON,TD9635_WIND,TD9635_PRES,TD9635_ROCI,NEUMANN_LAT,NEUMANN_LON,NEUMANN_CLASS,NEUMANN_WIND,NEUMANN_PRES,MLC_LAT,MLC_LON,MLC_CLASS,MLC_WIND,MLC_PRES,USA_GUST,BOM_GUST,BOM_GUST_PER,REUNION_GUST,REUNION_GUST_PER,USA_SEAHGT,USA_SEARAD_NE,USA_SEARAD_SE,USA_SEARAD_SW,USA_SEARAD_NW,STORM_SPEED,STORM_DIR
 ,Year, , , , , , ,degrees_north,degrees_east,kts,mb, , ,km,km, , , ,degrees_north,degrees_east, , ,kts,mb,1,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,mb,nmile,nmile,nmile,degrees_north,degrees_east,1,kts,mb, ,nmile,nmile, ,nmile,nmile,1,degrees_north,degrees_east,1,kts,mb,degrees_north,degrees_east, ,kts,mb,degrees_north,degrees_east, ,kts,mb, ,nmile,nmile, ,nmile,nmile,degrees_north,degrees_east, ,kts,mb,1,mb,mb,degrees_north,degrees_east, ,kts,mb,1,1,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,degrees_north,degrees_east, ,kts,mb,1,1,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,nmile,mb,nmile, , ,degrees_north,degrees_east,1,kts,mb,degrees_north,degrees_east,kts,mb,degrees_north,degrees_east, ,kts,mb,degrees_north,degrees_east, ,kts,mb,degrees_north,degrees_east,kts,mb,nmile,degrees_north,degrees_east, ,kts,mb,degrees_north,degrees_east, ,kts,mb,kts,kts,second,kts,second,ft,nmile,nmile,nmile,nmile,kts,degrees
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-23 12:00:00,TS,26.1,-90.4, , , ,main,335,323,______________O, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,26.1,-90.4,TD,30, , , , , , , , , , , ,6,290
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-23 15:00:00,TS,26.2,-90.7, , , ,main,323,312,______________P, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,26.2,-90.7,TD,30, , , , , , , , , , , ,6,290
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-23 18:00:00,TS,26.3,-91.0, , , ,main,312,302,______________O, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,26.3,-91.0,TD,30, , , , , , , , , , , ,6,290
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-23 21:00:00,TS,26.4,-91.3, , , ,main,304,296,______________P, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,26.4,-91.3,TD,33, , , , , , , , , , , ,6,290
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-24 00:00:00,TS,26.5,-91.6, , , ,main,298,292,______________O, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,26.5,-91.6,TS,35, , , , , , , , , , , ,6,290
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-24 03:00:00,TS,26.6,-91.9, , , ,main,295,292,______________P, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,26.6,-91.9,TS,35, , , , , , , , , , , ,6,290
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-24 06:00:00,TS,26.7,-92.2, , , ,main,296,295,______________O, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,26.7,-92.2,TS,35, , , , , , , , , , , ,6,290
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-24 09:00:00,TS,26.8,-92.5, , , ,main,300,292,______________P, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,26.8,-92.5,TS,40, , , , , , , , , , , ,6,290
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-24 12:00:00,TS,26.9,-92.8, , , ,main,294,287,______________O, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,26.9,-92.8,TS,45, , , , , , , , , , , ,6,290
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-24 15:00:00,TS,27.0,-93.1, , , ,main,289,275,______________P, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,27.0,-93.1,TS,45, , , , , , , , , , , ,6,290
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-24 18:00:00,TS,27.1,-93.4, , , ,main,275,248,______________O, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,27.1,-93.4,TS,45, , , , , , , , , , , ,6,290
1851175N26270,1851,5,NA,GM,UNNAMED,1851-06-24 21:00:00,TS,27.2,-93.7, , , ,main,248,193,______________P, , , , , , , , ,-5, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,27.2,-93.7,TS,50, , , , , , , , , , , ,9,300
```

### `igra-merignac` — Température en altitude — radiosondages Mérignac, dérivés (IGRA)

https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/derived-por/FRM00007510-drvd.txt.zip

```
[archive illisible : File is not a zip file]
```

### `gcb` — Puits de carbone — Global Carbon Budget (liste des fichiers)

https://globalcarbonbudgetdata.org/latest-data.html

```
(aucune donnée)
```

### `ceres` — Déséquilibre énergétique — CERES EBAF (page d'accès)

https://ceres.larc.nasa.gov/data/

```
[page HTML] liens de données trouvés :
```
