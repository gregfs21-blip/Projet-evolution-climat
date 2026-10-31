# Sonde P6 — sources mondiales (généré)

Généré par `python -m etl.probe.p6` le 31/10/2026 20:39 UTC. Aucun indicateur calculé.

## Niveau marin mondial (altimétrie)

### `https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_gbl_free_ref_90.csv` → **200**

```
1563 lignes
#title = mean sea level anomaly global ocean (Annual signals removed) 
#institution = NOAA/Laboratory for Satellite Altimetry 
#references = NOAA Sea Level Rise (http://www.star.nesdis.noaa.gov/sod/lsa/SeaLevelRise/) and Radar Altimeter Database System (https://www.star.nesdis.noaa.gov/socd/lsa/RADS.php) 
#comment = Data use policy: In publications, presentations, or on web pages based on LSA data the following acknowledgment should be included: 'Altimetry data are provided by NOAA Laboratory for Satellite Altimetry.' 
#trend = 3.11 mm/year (no glacial isostatic adjustment correction) 
year,TOPEX/Poseidon,Jason-1,Jason-2,Jason-3,Sentinel-6MF
1992.96140,-19.33000,,,,
1992.98650,-22.59000,,,,
1993.01230,-24.03000,,,,
1993.04060,-23.94000,,,,
1993.06410,-24.22000,,,,
1993.09750,-23.31000,,,,
…
2025.04840,,,,,82.60000
2025.07560,,,,,81.77000
2025.10270,,,,,82.01000
2025.12680,,,,,83.60000
```

### `https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_gbl_free_all_66.csv` → **200**

```
1563 lignes
#title = mean sea level anomaly global ocean (66S to 66N) (Annual signals removed) 
#institution = NOAA/Laboratory for Satellite Altimetry 
#references = NOAA Sea Level Rise (http://www.star.nesdis.noaa.gov/sod/lsa/SeaLevelRise/) and Radar Altimeter Database System (https://www.star.nesdis.noaa.gov/socd/lsa/RADS.php) 
#comment = Data use policy: In publications, presentations, or on web pages based on LSA data the following acknowledgment should be included: 'Altimetry data are provided by NOAA Laboratory for Satellite Altimetry.' 
#trend = 3.17 mm/year (no glacial isostatic adjustment correction) 
year,TOPEX/Poseidon,Jason-1,Jason-2,Jason-3,Sentinel-6MF
1992.96140,-19.38000,,,,
1992.98650,-22.65000,,,,
1993.01230,-24.09000,,,,
1993.04060,-24.00000,,,,
1993.06410,-24.28000,,,,
1993.09750,-23.37000,,,,
…
2025.04840,,,,,84.02000
2025.07560,,,,,83.19000
2025.10270,,,,,83.43000
2025.12680,,,,,85.02000
```

### `https://sealevel.colorado.edu/files/2023_rel2/gmsl_2023rel2_seasons_rmvd.txt` → **200**

```
1100 lignes
# Date      2023_rel2 w/ seasonal signals and GIA removed (mm)
1992.96      -31.072
1992.985      -33.087
1993.01      -31.335
1993.039      -34.274
1993.064      -36.142
1993.096      -37.563
1993.119      -34.633
1993.147      -29.119
1993.175      -28.328
1993.202      -29.048
1993.229      -29.575
…
2023.609      80.729
2023.636      79.726
2023.663      81.715
2023.685      80.75
```

### `https://sealevel.colorado.edu/files/2024_rel1/gmsl_2024rel1_seasons_rmvd.txt` → **404**

```
HTML, 233 caractères ; liens : 
```

### `https://www.cmar.csiro.au/sealevel/downloads/church_white_gmsl_2011_up.zip` → **200**

```
archive : church_white_gmsl_2011_up/ (0 o), church_white_gmsl_2011_up/CSIRO_ALT_gmsl_mo_2015.csv (5073 o), church_white_gmsl_2011_up/CSIRO_ALT_gmsl_mo_2015.txt (4788 o), church_white_gmsl_2011_up/CSIRO_ALT_gmsl_yr_2015.csv (371 o), church_white_gmsl_2011_up/CSIRO_ALT_gmsl_yr_2015.txt (330 o), church
```

### `https://podaac-opendap.jpl.nasa.gov/opendap/allData/merged_alt/L2/TP_J1_OSTM/global_mean_sea_level/` → **erreur : URLError <urlopen error [Errno -2] Name or service not known>**

```
0 lignes
…
```

## Acidification (station HOT, Hawaï)

### `https://hahana.soest.hawaii.edu/hot/hotco2/HOT_surface_CO2.txt` → **200**

```
363 lignes
HOT_surface_CO2.txt																					
Hawaii Ocean Time-series surface CO2 system data product																					
Created 5 October 2009 by J.E. Dore																					
Last updated 1 January 2026 by J.E. Dore																					
"See HOT_surface_CO2_readme.pdf for explanatory material, metadata, and notes (https://hahana.soest.hawaii.edu/hot/hotco2/hotco2.html)"																					
"When using this data product please cite as adapted from: Dore, J.E., R. Lukas, D.W. Sadler, M.J. Church, and D.M. Karl.  2009.  Physical and biogeochemical modulation of ocean acidification in the central North Pacific.  Proc Natl Acad Sci USA 106:12235-12240."																					
Please direct questions or comments regarding this data product to John Dore: jdore@montana.edu																					
cruise	days	date	temp	sal	phos	sil	DIC	TA	nDIC	nTA	pHmeas_25C	pHmeas_insitu	pHcalc_25C	pHcalc_insitu	pCO2calc_insitu	pCO2calc_20C	aragsatcalc_insitu	calcsatcalc_insitu	freeCO2_insitu	carbonate_insitu	notes
1	30	31-Oct-88	26.283	35.186	0.08	0.71	1963.91	2319.5	1953.5	2307.2	-999	-999	8.1292	8.1097	330.9	256.3	3.98	6.02	9.06	250.2	abc
2	62	2-Dec-88	25.659	34.984	0.09	0.99	1958.94	2304.9	1959.8	2306	-999	-999	8.1193	8.1092	330.6	262.6	3.87	5.86	9.2	243.5	bc
3	99	8-Jan-89	24.61	35.028	0.07	0.93	1963.77	2305	1962.2	2303.2	-999	-999	8.1113	8.1168	324.3	268.7	3.8	5.77	9.27	240.1	c
4	148	26-Feb-89	23.479	34.883	0.09	0.88	1957.8	2295.5	1964.4	2303.2	-999	-999	8.1091	8.1316	310.9	269.7	3.74	5.69	9.15	237.2	cd
…
352	13105	18-Aug-24	26.587	35.127	0.11	1.27	2005.15	2313.0	1997.9	2304.6	-999	-999	8.0545	8.0307	414.0	317.5	3.50	5.28	11.26	219.3	c
353	13126	8-Sep-24	26.988	35.131	0.05	1.03	1999.75	2313.0	1992.3	2304.4	8.071	8.041	8.0636	8.0338	409.9	309.3	3.56	5.37	11.04	222.9	
354	13160	12-Oct-24	26.741	35.114	0.09	1.06	2005.60	2313.0	1999.1	2305.5	8.062	8.036	8.0540	8.0279	417.2	318.0	3.50	5.28	11.30	219.1	
355	13229	20-Dec-24	25.095	35.396	0.04	0.91	2018.15	2331.0	1995.6	2304.9	8.061	8.059	8.0568	8.0550	389.9	317.2	3.52	5.33	10.99	222.5	
```

## Ozone (NASA Ozone Watch)

### `https://ozonewatch.gsfc.nasa.gov/statistics/annual_data.txt` → **200**

```
55 lignes
# http://ozonewatch.gsfc.nasa.gov/meteorology/annual_data.txt
# TOMS. OMI. and OMPS data
# Missing data filled from NASA GMAO MERRA, MERRA-2, and GEOS FP
# Southern Hemisphere
# Ozone hole area mean (07 September -- 13 October)
# Minimum ozone (21 September -- 16 October)
      O3 Hole Area Minimum Ozone
Year     (mil km2)          (DU)
----  ------------ -------------
1979           0.1         225.0
1980           1.4         203.0
1981           0.6         209.5
…
2022          23.2         112.5
2023          23.1         115.2
2024          19.6         121.0
2025          18.7         138.3
```

## Puits de carbone (Global Carbon Budget)

### `https://globalcarbonbudgetdata.org/downloads/latest-data/Global_Carbon_Budget_2025_v1.0.xlsx` → **404**

```
HTML, 2000 caractères ; liens : https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css https://globalcarbonbudget.org https://unpkg.com/aos@2.3.1/dist/aos.css https://use.typekit.net/tos4gsm.css
```

### `https://globalcarbonbudgetdata.org/downloads/latest-data/Global_Carbon_Budget_2025_v1.0.csv` → **404**

```
HTML, 2000 caractères ; liens : https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css https://globalcarbonbudget.org https://unpkg.com/aos@2.3.1/dist/aos.css https://use.typekit.net/tos4gsm.css
```

### `https://data.icos-cp.eu/objects/26QlKAL0-2D7QhMZ62n1R9PW` → **200**

```
HTML, 61963 caractères ; liens : #main-content / /data-services/about-data-portal/data-license http://www.icos-etc.eu/ https://bsky.app/profile/icos-ri.eu https://cdn.jsdelivr.net/gh/orestbida/cookieconsent@3.0.1/dist/cookieconsent.css https://cpauth.icos-cp.eu/ https://creativecommons.org/licenses/
```

### `https://raw.githubusercontent.com/openclimatedata/global-carbon-budget/main/data/global-carbon-budget.csv` → **404**

```
1 lignes
404: Not Found
…
404: Not Found
```

### `https://api.github.com/repos/openclimatedata/global-carbon-budget/contents/data` → **200**

```
1 lignes
[{"name":"global-carbon-budget-2018-fossil-emissions.csv","path":"data/global-carbon-budget-2018-fossil-emissions.csv","sha":"4c67aa46be862c91fac4d3a6c56cb7d19cca82c6","size":6951,"url":"https://api.github.com/repos/openclimatedata/global-carbon-budget/contents/data/global-carbon-budget-2018-fossil-
…
[{"name":"global-carbon-budget-2018-fossil-emissions.csv","path":"data/global-carbon-budget-2018-fossil-emissions.csv","sha":"4c67aa46be862c91fac4d3a6c56cb7d19cca82c6","size":6951,"url":"https://api.github.com/repos/openclimatedata/global-carbon-budget/contents/data/global-carbon-budget-2018-fossil-
```

## Température de la troposphère (satellites MSU)

### `https://www.nsstc.uah.edu/data/msu/v6.1/tlt/uahncdc_lt_6.1.txt` → **200**

```
585 lignes
 Year Mo Globe  Land Ocean   NH   Land Ocean   SH   Land Ocean Trpcs  Land Ocean NoExt  Land Ocean SoExt  Land Ocean NoPol  Land Ocean SoPol  Land Ocean USA48 USA49  AUST CANADA
 1978 12 -0.48 -0.52 -0.46 -0.44 -0.47 -0.42 -0.52 -0.62 -0.49 -0.60 -0.62 -0.59 -0.37 -0.45 -0.30 -0.46 -0.55 -0.44 -0.39 -0.68 -0.06 -0.45 -0.37 -0.49 -1.29 -1.15 -1.30 -0.95
 1979  1 -0.47 -0.64 -0.41 -0.64 -0.86 -0.50 -0.31 -0.13 -0.34 -0.47 -0.54 -0.45 -0.73 -0.93 -0.54 -0.22  0.12 -0.29 -0.46 -0.95  0.10 -0.15 -0.15 -0.16 -3.22 -2.42  0.92 -0.32
 1979  2 -0.43 -0.56 -0.38 -0.47 -0.57 -0.41 -0.39 -0.53 -0.36 -0.36 -0.25 -0.39 -0.54 -0.67 -0.42 -0.41 -0.70 -0.36 -2.00 -2.30 -1.66 -0.80 -1.25 -0.58 -1.76 -1.84 -0.30 -3.99
 1979  3 -0.38 -0.52 -0.33 -0.46 -0.51 -0.44 -0.30 -0.53 -0.25 -0.36 -0.43 -0.34 -0.53 -0.54 -0.52 -0.26 -0.59 -0.21 -0.56 -0.47 -0.65 -0.52 -1.25 -0.18 -0.70 -0.39  0.22  0.37
 1979  4 -0.40 -0.57 -0.34 -0.47 -0.62 -0.37 -0.34 -0.46 -0.31 -0.35 -0.37 -0.34 -0.54 -0.72 -0.38 -0.33 -0.44 -0.31 -0.84 -0.81 -0.87 -0.26  0.26 -0.51 -0.73 -0.46 -1.12 -0.35
 1979  5 -0.39 -0.56 -0.33 -0.52 -0.54 -0.51 -0.27 -0.62 -0.19 -0.46 -0.55 -0.43 -0.54 -0.52 -0.55 -0.18 -0.70 -0.09 -0.76 -0.55 -1.00  0.05 -0.43  0.27 -0.82 -0.75 -1.10 -0.55
 1979  6 -0.39 -0.61 -0.31 -0.50 -0.61 -0.43 -0.29 -0.62 -0.22 -0.37 -0.50 -0.33 -0.55 -0.63 -0.48 -0.27 -0.74 -0.19 -0.76 -1.14 -0.32 -0.98 -1.62 -0.67 -0.62 -0.67 -0.56 -1.24
 1979  7 -0.31 -0.57 -0.21 -0.21 -0.33 -0.14 -0.41 -1.11 -0.26 -0.41 -0.56 -0.37 -0.15 -0.33  0.01 -0.37 -1.35 -0.20 -0.20 -0.38  0.01 -0.95 -2.18 -0.37 -0.15 -0.09 -1.16  0.46
 1979  8 -0.40 -0.54 -0.35 -0.34 -0.37 -0.32 -0.46 -0.91 -0.36 -0.37 -0.35 -0.38 -0.36 -0.43 -0.30 -0.47 -1.17 -0.34 -0.26 -0.35 -0.15 -1.00 -1.68 -0.69 -0.74 -0.36 -1.06 -0.85
 1979  9 -0.32 -0.44 -0.28 -0.33 -0.31 -0.34 -0.32 -0.73 -0.23 -0.35 -0.42 -0.33 -0.33 -0.29 -0.36 -0.29 -0.95 -0.17 -0.17 -0.02 -0.35 -0.11 -0.65  0.15  0.61  0.68 -0.77  0.02
 1979 10 -0.17 -0.32 -0.11 -0.15 -0.26 -0.07 -0.19 -0.45 -0.14 -0.19 -0.23 -0.18 -0.15 -0.27 -0.05 -0.16 -0.63 -0.08 -0.22 -0.34 -0.09 -0.30 -0.97  0.02  0.24  0.38 -0.36  0.34
…
  NOTE:  3/13 More accurate grid weighting for USA48
  NOTE:  3/13 Alaska added in USA49, Australia added
  GL 90S-90N, NH 0-90N, SH 90S-0, TRPCS 20S-20N
  NoExt 20N-90N, SoExt 90S-20S, NoPol 60N-90N, SoPol 90S-60S
```

### `https://data.remss.com/msu/graphics/TLT_v40/time_series/RSS_TS_channel_TLT_Global_Land_And_Sea_v04_0.txt` → **200**

```
593 lignes
Channel = TLT
Region  = Global
Latitude Range =  70.0S to  82.5N
year  mon  TLT Anomaly (K)
------------------------------------------
1978   1  -99.9000
1978   2  -99.9000
1978   3  -99.9000
1978   4  -99.9000
1978   5  -99.9000
1978   6  -99.9000
1978   7  -99.9000
…
2026   9    1.1890
2026  10  -99.9000
2026  11  -99.9000
2026  12  -99.9000
```

## Déséquilibre énergétique (CERES EBAF)

### `https://ceres.larc.nasa.gov/data/` → **200**

```
HTML, 6750528 caractères ; liens : # #main-content #top /data/documentation/#FLASHFluxGridded /data/documentation/#cldtyphist /data/documentation/#crs /data/documentation/#crs1deg /data/documentation/#ebaf /data/documentation/#flash-ssf /data/documentation/#fluxbycldtyp /data/documentation/#ssf /dat
```

### `https://opendap.larc.nasa.gov/opendap/CERES/EBAF/Edition4.2.1/contents.html` → **403**

```
HTML, 919 caractères ; liens : 
```

## Aérosols (CAMS, Atmosphere Data Store)

### cams-global-reanalysis-eac4-monthly (description)

→ **200**

```
variable : {'type': 'array', 'items': {'enum': ['2m_dewpoint_temperature', '2m_temperature', 'black_carbon_aerosol_optical_depth_550nm', 'carbon_monoxide', 'charnock', 'dust_aerosol_0.03-0.55um_mixing_ratio', 'dust_aerosol_0.55-0.9um_mixing_ratio', 'dust_aerosol_0.9-20um_mixing_ratio', 'dust_aerosol_optical_de
pressure_level : {'type': 'array', 'items': {'enum': ['1', '10', '100', '1000', '150', '2', '20', '200', '250', '3', '30', '300', '400', '5', '50', '500', '600', '7', '70', '700', '800', '850', '900', '925', '950'], 'type': 'string'}}
model_level : {'type': 'array', 'items': {'enum': ['60'], 'type': 'string'}}
year : {'type': 'array', 'items': {'enum': ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'], 'type': 'string'}}
month : {'type': 'array', 'items': {'enum': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'], 'type': 'string'}}
product_type : {'type': 'array', 'items': {'enum': ['monthly_mean', 'monthly_mean_by_hour_of_day'], 'type': 'string'}}
time : {'type': 'array', 'items': {'enum': ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'], 'type': 'string'}}
data_format : {'enum': ['grib', 'netcdf_zip'], 'type': 'string', 'default': 'grib'}
area : {'maxItems': 4, 'minItems': 4, 'type': 'array', 'default': [90, -180, -90, 180], 'items': {'type': 'number'}}
```

### soumission minimale (AOD 550 nm, janvier 2020)

→ **403**

```
{"type":"permission denied","title":"user didn't accept all required site policies","status":403,"detail":"Missing policies are: Terms of use of the Copernicus Atmosphere Data Store (rev. 13) - https://ads.atmosphere.copernicus.eu/licences/terms-of-use-ads, Data protection and privacy statement (rev. 1) - https://ads.atmosphere.copernicus.eu/licences/ads-data-protection-privacy-statement","instance":"https://ads.atmosphere.copernicus.eu/api/retrieve/v1/processes/cams-global-reanalysis-eac4-monthly/execution","trace_id":"3dca73aa-14cd-4f61-83e6-c51fbde75c2b"}
```
