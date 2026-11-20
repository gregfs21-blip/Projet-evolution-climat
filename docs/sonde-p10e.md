# Sonde P10.4b — température de la mer sur le domaine de la vapeur d'eau (généré)

Produit le 20/11/2026 12:28 UTC par `etl/probe/p10e.py`. Inventaire seulement : aucune pente, aucun rapport.

## OISST v2, 1°, mensuel (NOAA PSL)

https://downloads.psl.noaa.gov/Datasets/noaa.oisst.v2/sst.mnmean.nc

Statut : 200 ; 64038940 o ; modifié Tue, 07 Feb 2023 06:00:15 GMT

```
lat ('lat',) (180,) degrees_north Latitude
lon ('lon',) (360,) degrees_east Longitude
sst ('time', 'lat', 'lon') (494, 180, 360) degC Monthly Mean of Sea Surface Temperature
time ('time',) (494,) days since 1800-1-1 00:00:00 Time
time_bnds ('time', 'nbnds') (494, 2)  Time Boundaries
lat : premier 89.5, dernier -89.5, pas -1.0, n = 180
lon : premier 0.5, dernier 359.5, pas 1.0, n = 360
time : unités « days since 1800-1-1 00:00:00 », premier 66443.0, dernier 81449.0, n = 494
attribut title = NOAA Optimum Interpolation (OI) SST V2
attribut source = NCEP Climate Modeling Branch
attribut dataset_title = NOAA Optimum Interpolation (OI) SST V2
```

## OISST v2, masque terre-mer 1° (NOAA PSL)

https://downloads.psl.noaa.gov/Datasets/noaa.oisst.v2/lsmask.nc

Statut : 200 ; 133700 o ; modifié Tue, 14 Apr 2020 15:56:21 GMT

```
lat ('lat',) (180,) degrees_north Latitude
lon ('lon',) (360,) degrees_east Longitude
time ('time',) (1,) days since 1800-1-1 00:00:0.0 Time
mask ('time', 'lat', 'lon') (1, 180, 360) none Land Sea Mask
lat : premier 89.5, dernier -89.5, pas -1.0, n = 180
lon : premier 0.5, dernier 359.5, pas 1.0, n = 360
time : unités « days since 1800-1-1 00:00:0.0 », premier 66410.0, dernier 66410.0, n = 1
attribut title = NOAA Optimum Interpolation (OI) SST V2
attribut source = NCEP Climate Modeling Branch
attribut dataset_title = NOAA Optimum Interpolation (OI) SST V2
```

## ERSST v5, 2°, mensuel (NOAA PSL)

https://downloads.psl.noaa.gov/Datasets/noaa.ersst.v5/sst.mnmean.nc

Statut : 200 ; 162376295 o ; modifié Tue, 03 Nov 2026 23:23:39 GMT

```
lat ('lat',) (89,) degrees_north Latitude
lon ('lon',) (180,) degrees_east Longitude
time_bnds ('time', 'nbnds') (2074, 2)  Time Boundaries
time ('time',) (2074,) days since 1800-1-1 00:00:00 Time
sst ('time', 'lat', 'lon') (2074, 89, 180) degC Monthly Means of Sea Surface Temperature
lat : premier 88.0, dernier -88.0, pas -2.0, n = 89
lon : premier 0.0, dernier 358.0, pas 2.0, n = 180
time : unités « days since 1800-1-1 00:00:00 », premier 19723.0, dernier 82818.0, n = 2074
attribut title = NOAA ERSSTv5 (in situ only)
attribut source = In situ data: ICOADS R3.0 before 2015, NCEP in situ GTS from 2016 to present, and Argo SST from 1999 to present. Ice data: HadISST2 ice before 2015, and NCEP ice after 2015
attribut dataset_title = NOAA Extended Reconstructed SST V5
attribut comment = SSTs were observed by conventional thermometers in Buckets (insulated or un-insulated canvas and wooded buckets), Engine Room Intakers, or floats and drifters
```

## HadSST 4.2, 5°, mensuel, médiane (Met Office)

https://www.metoffice.gov.uk/hadobs/hadsst4/data/netcdf/HadSST.4.2.0.0_median.nc

Statut : échec HTTPError HTTP Error 404: Not Found

## RSS vapeur d'eau, 1° (grille de référence)

https://data.remss.com/vapor/monthly_1deg/merged_vapor_1988-2025.nc

Statut : 200 ; 118243415 o ; modifié Fri, 16 Jan 2026 23:20:25 GMT

```
merged_vapor ('latitude', 'longitude', 'time') (180, 360, 456) kg/m^2 
satellites_used ('time', 'sats') (456, 12)  
latitude ('latitude',) (180,) degrees_north latitude
longitude ('longitude',) (360,) degrees_east longitude
time ('time',) (456,) fractional year time
clim_time ('clim_time',) (12,) month climatology month
sats ('sats',) (12,)  satellite number
latitude : premier -89.5, dernier 89.5, pas 1.0, n = 180
longitude : premier -179.5, dernier 179.5, pas 1.0, n = 360
time : unités « fractional year », premier 1988.0416666666667, dernier 2025.958333333299, n = 456
```

**Page** https://psl.noaa.gov/data/gridded/data.noaa.oisst.v2.html : 200


**Page** https://psl.noaa.gov/data/gridded/data.noaa.ersst.v5.html : 200


