# Sonde P3 — atmosphère et littoral Gironde (généré)

Généré par `python -m etl.probe.p3` le 27/10/2026 20:59 UTC. Aucun indicateur calculé.

## 1. Quotidien Météo-France, autres paramètres (Gironde)

Fichiers du département 33 :

- QUOT_departement_33_periode_avant-1949_RR-T-Vent
- QUOT_departement_33_periode_avant-1949_autres-parametres
- QUOT_departement_33_periode_1950-2024_RR-T-Vent
- QUOT_departement_33_periode_1950-2024_autres-parametres
- QUOT_departement_33_periode_2025-2026_RR-T-Vent
- QUOT_departement_33_periode_2025-2026_autres-parametres

### QUOT_departement_33_periode_avant-1949_autres-parametres

`https://meteofrance.s3.sbg.io.cloud.ovh.net/data/synchro_ftp/BASE/QUOT/Q_33_avant-1949_autres-parametres.csv.gz` → **200**

```
colonnes : NUM_POSTE, NOM_USUEL, LAT, LON, ALTI, AAAAMMJJ, DHUMEC, QDHUMEC, PMERM, QPMERM, PMERMIN, QPMERMIN, INST, QINST, GLOT, QGLOT, DIFT, QDIFT, DIRT, QDIRT, INFRART, QINFRART, UV, QUV, UV_INDICEX, QUV_INDICEX, SIGMA, QSIGMA, UN, QUN, HUN, QHUN, UX, QUX, HUX, QHUX, UM, QUM, DHUMI40, QDHUMI40, DHUMI80, QDHUMI80, TSVM, QTSVM, ETPMON, QETPMON, ETPGRILLE, QETPGRILLE, ECOULEMENTM, QECOULEMENTM, HNE
```

### QUOT_departement_33_periode_1950-2024_autres-parametres

`https://meteofrance.s3.sbg.io.cloud.ovh.net/data/synchro_ftp/BASE/QUOT/Q_33_previous-1950-2024_autres-parametres.csv.gz` → **200**

```
colonnes : NUM_POSTE, NOM_USUEL, LAT, LON, ALTI, AAAAMMJJ, DHUMEC, QDHUMEC, PMERM, QPMERM, PMERMIN, QPMERMIN, INST, QINST, GLOT, QGLOT, DIFT, QDIFT, DIRT, QDIRT, INFRART, QINFRART, UV, QUV, UV_INDICEX, QUV_INDICEX, SIGMA, QSIGMA, UN, QUN, HUN, QHUN, UX, QUX, HUX, QHUX, UM, QUM, DHUMI40, QDHUMI40, DHUMI80, QDHUMI80, TSVM, QTSVM, ETPMON, QETPMON, ETPGRILLE, QETPGRILLE, ECOULEMENTM, QECOULEMENTM, HNE
33281001 BORDEAUX-MERIGNAC : PMERM 75 ans (1950-2024) ; UM 75 ans (1950-2024) ; UN 69 ans (1950-2024) ; UX 75 ans (1950-2024) ; TSVM 69 ans (1950-2024) ; INST 75 ans (1950-2024) ; GLOT 47 ans (1978-2024) ; PMERMIN 17 ans (2008-2024)
33529001 CAZAUX : PMERM 75 ans (1950-2024) ; UM 75 ans (1950-2024) ; UN 75 ans (1950-2024) ; UX 75 ans (1950-2024) ; TSVM 75 ans (1950-2024) ; INST 62 ans (1955-2017) ; PMERMIN 15 ans (2008-2024)
33236002 CAP-FERRET : UN 43 ans (1972-2019) ; UX 48 ans (1972-2019) ; TSVM 63 ans (1951-2019) ; PMERM 65 ans (1951-2019) ; INST 61 ans (1957-2017) ; UM 26 ans (1994-2019) ; PMERMIN 11 ans (2009-2019)
33042005 BELIN BELIET : UN 18 ans (2007-2024) ; UX 18 ans (2007-2024) ; TSVM 18 ans (2007-2024) ; UM 18 ans (2007-2024) ; INST 17 ans (2007-2024) ; GLOT 17 ans (2007-2024)
33080001 CADAUJAC-INRAE : UN 33 ans (1988-2024) ; UX 32 ans (1988-2024) ; TSVM 31 ans (1993-2024) ; GLOT 34 ans (1991-2024) ; UM 23 ans (1996-2024) ; DHUMEC 2 ans (2005-2007)
33116001 CAZATS : UN 22 ans (2003-2024) ; UX 22 ans (2003-2024) ; TSVM 22 ans (2003-2024) ; UM 22 ans (2003-2024)
33122003 PIERROTON-INRAE : UM 20 ans (2004-2024) ; UN 21 ans (2004-2024) ; UX 21 ans (2004-2024) ; TSVM 21 ans (2004-2024) ; GLOT 21 ans (2004-2024)
33234002 LATRESNE-INRAE : UN 22 ans (1987-2012) ; UX 23 ans (1987-2012) ; TSVM 22 ans (1987-2012) ; GLOT 20 ans (1987-2012) ; UM 16 ans (1995-2012) ; DHUMEC 3 ans (2005-2007)
33314003 PAUILLAC-SUD : UN 19 ans (1993-2012) ; UX 19 ans (1993-2012) ; TSVM 19 ans (1993-2012) ; GLOT 2 ans (1987-1988) ; UM 15 ans (1993-2012) ; DHUMEC 7 ans (2005-2012)
33314005 PAUILLAC : UN 63 ans (1962-2024) ; UX 63 ans (1962-2024) ; TSVM 63 ans (1962-2024) ; UM 20 ans (2005-2024) ; GLOT 20 ans (2005-2024) ; INST 20 ans (2005-2024)
33394002 ST EMILION : GLOT 20 ans (2005-2024) ; UM 18 ans (2007-2024) ; UN 18 ans (2007-2024) ; UX 18 ans (2007-2024) ; TSVM 18 ans (2007-2024) ; INST 18 ans (2007-2024)
33415001 ST GERVAIS : UM 24 ans (1996-2024) ; UN 28 ans (1996-2024) ; UX 28 ans (1996-2024) ; TSVM 28 ans (1996-2024)
33445001 ST-MARTIN-DU-BO : UM 11 ans (1995-2005) ; UN 12 ans (1995-2006) ; UX 12 ans (1995-2006) ; TSVM 12 ans (1995-2006)
33473001 ST-SAVIN : UM 17 ans (1994-2010) ; UN 17 ans (1994-2010) ; UX 17 ans (1994-2010) ; TSVM 17 ans (1994-2010)
33482001 ST SULPICE DE POMMIERS : UN 22 ans (2003-2024) ; UX 22 ans (2003-2024) ; TSVM 22 ans (2003-2024) ; UM 22 ans (2003-2024)
33504001 SAUTERNES : UN 23 ans (1993-2015) ; UX 23 ans (1993-2015) ; TSVM 24 ans (1992-2015) ; GLOT 22 ans (1993-2015) ; UM 21 ans (1992-2015) ; DHUMEC 11 ans (2005-2015)
33540001 VENDAYS-MONTALIVE : UN 22 ans (1996-2024) ; UX 22 ans (1996-2024) ; TSVM 22 ans (1996-2024) ; UM 21 ans (1996-2024)
33550001 VILLENAVE D'ORNON-INRAE : UM 21 ans (2004-2024) ; TSVM 21 ans (2004-2024) ; UN 21 ans (2004-2024) ; UX 21 ans (2004-2024) ; GLOT 21 ans (2004-2024)
```

### QUOT_departement_33_periode_2025-2026_autres-parametres

`https://meteofrance.s3.sbg.io.cloud.ovh.net/data/synchro_ftp/BASE/QUOT/Q_33_latest-2025-2026_autres-parametres.csv.gz` → **200**

```
colonnes : NUM_POSTE, NOM_USUEL, LAT, LON, ALTI, AAAAMMJJ, DHUMEC, QDHUMEC, PMERM, QPMERM, PMERMIN, QPMERMIN, INST, QINST, GLOT, QGLOT, DIFT, QDIFT, DIRT, QDIRT, INFRART, QINFRART, UV, QUV, UV_INDICEX, QUV_INDICEX, SIGMA, QSIGMA, UN, QUN, HUN, QHUN, UX, QUX, HUX, QHUX, UM, QUM, DHUMI40, QDHUMI40, DHUMI80, QDHUMI80, TSVM, QTSVM, ETPMON, QETPMON, ETPGRILLE, QETPGRILLE, ECOULEMENTM, QECOULEMENTM, HNE
```

## 2. Température de la mer au large de la Gironde

### OISST (ERDDAP CoastWatch), une année

`https://coastwatch.pfeg.noaa.gov/erddap/griddap/ncdcOisst21Agg_LonPM180.csv?sst%5B(2024-01-01):1:(2024-12-31)%5D%5B(0.0)%5D%5B(45.125)%5D%5B(-1.875)%5D` → **erreur : URLError <urlopen error [Errno 101] Network is unreachable>**

```
0 lignes
```

### ERA5 single levels, moyennes mensuelles : soumission de la SST 1940-2025, boîte 44-46° N, 3-1° O

`…/processes/reanalysis-era5-single-levels-monthly-means/execution` → **201**

```
{"processID":"reanalysis-era5-single-levels-monthly-means","type":"process","jobID":"1d19e0d6-69b3-4179-bd5b-e4da0b172cfa","status":"accepted","created":"2026-10-27T21:01:50.967938","updated":"2026-10-27T21:01:50.967938","links":[{"href":"https://cds.climate.copernicus.eu/api/retrieve/v1/processes/reanalysis-era5-single-levels-monthly-means/execution","rel":"self"},{"href":"https://cds.climate.cop
```

## 3. Mouvements verticaux du sol (SONEL, GNSS, solution ULR7a)

### Description du jeu de données

`https://erddap.ioc-sealevelmonitoring.org/erddap/info/sonel_vlm_gnss_ulr7a/index.csv` → **200**

```
variable,stationid,,String,
variable,time,,double,
attribute,time,units,String,seconds since 1970-01-01T00:00:00Z
variable,par,,float,
attribute,par,units,String,mm
```

### Stations GNSS entre 43 et 47,5° N, 3,5° O et 0,5° E

`https://erddap.ioc-sealevelmonitoring.org/erddap/tabledap/sonel_vlm_gnss_ulr7a.csv` → **200**

```
stationid,time,par
,UTC,mm
filtrage impossible : 
…noms :
ferr00fra,2005-05-28T11:54:57Z,0.04
ferr00fra,2005-05-29T11:34:04Z,0.51
ferr00fra,2005-05-30T12:05:45Z,0.27
ferr00fra,2005-05-31T11:44:52Z,0.82
ferr00fra,2005-06-01T12:16:33Z,0.74
ferr00fra,2005-06-02T11:55:40Z,1.19
ferr00fra,2005-06-03T11:34:47Z,0.51
ferr00fra,2005-06-04T12:06:28Z,0.75
ferr00fra,2005-06-05T11:45:35Z,0.67
ferr00fra,2005-06-06T12:17:16Z,0.93
ferr00fra,2005-06-07T11:56:23Z,1.19
ferr00fra,2005-06-08T11:35:31Z,1.14
ferr00fra,2005-06-09T12:07:11Z,1.18
ferr00fra,2005-06-10T11:46:19Z,0.92
ferr00fra,2005-06-11T12:18:00Z,0.65
ferr00fra,2005-06-13T11:36:14Z,1.6
ferr00fra,2005-06-14T12:07:55Z,1.17
ferr00fra,2005-06-15T11:47:02Z,0.66
ferr00fra,2005-06-16T12:18:43Z,0.98
ferr00fra,2005-06-17T11:57:50Z,1.76
```

## 4. Marégraphes PSMSL de la façade (annuels RLR et metric)

### Liste RLR (façade atlantique sud)

`https://psmsl.org/data/obtaining/rlr.annual.data/filelist.txt` → **200**

```
  457;  47.270000;   -2.200000; ST. NAZAIRE                             ; 190; 111; N
  459;  45.550000;   -1.066667; LE VERDON                               ; 190; 131; N
  466;  46.158478;   -1.220736; LA ROCHELLE-LA PALLICE                  ; 190; 121; N
  469;  43.395239;   -1.681623; ST JEAN DE LUZ (SOCOA)                  ; 190; 141; N
  856;  40.893333;  -73.781667; NEW ROCHELLE                            ; 960; 143; N
 1747;  46.497501;   -1.793730; LES SABLES D OLONNE                     ; 190; 116; N
 1801;  43.527302;   -1.514830; BOUCAU                                  ; 190; 139; N
 1918;  44.665001;   -1.163550; ARCACHON-EYRAC                          ; 190; 140; N
 2236;  46.007353;   -1.174333; ILE D'AIX                               ; 190; 123; N
```
- 457 RLR (200) : 54 années valeur, 54 sans drapeau, 1965-2024
- 457 metric (404) : 0 années valeur, 0 sans drapeau
- 459 RLR (200) : 6 années valeur, 6 sans drapeau, 1942-1977
- 459 metric (404) : 0 années valeur, 0 sans drapeau
- 466 RLR (200) : 32 années valeur, 32 sans drapeau, 1942-2023
- 466 metric (404) : 0 années valeur, 0 sans drapeau
- 469 RLR (200) : 37 années valeur, 37 sans drapeau, 1966-2023
- 469 metric (404) : 0 années valeur, 0 sans drapeau
- 856 RLR (200) : 21 années valeur, 21 sans drapeau, 1958-1981
- 856 metric (404) : 0 années valeur, 0 sans drapeau
- 1747 RLR (200) : 33 années valeur, 33 sans drapeau, 1990-2024
- 1747 metric (404) : 0 années valeur, 0 sans drapeau
- 1801 RLR (200) : 45 années valeur, 45 sans drapeau, 1969-2024
- 1801 metric (404) : 0 années valeur, 0 sans drapeau
- 1918 RLR (200) : 19 années valeur, 19 sans drapeau, 2002-2024
- 1918 metric (404) : 0 années valeur, 0 sans drapeau
- 2236 RLR (200) : 6 années valeur, 6 sans drapeau, 2014-2022
- 2236 metric (404) : 0 années valeur, 0 sans drapeau
