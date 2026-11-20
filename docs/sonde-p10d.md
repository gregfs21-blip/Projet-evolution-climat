# Sonde P10.4 — cohérence physique : données disponibles (généré)

Produit le 20/11/2026 10:55 UTC par `etl/probe/p10d.py`. Inventaire seulement : aucune tendance, aucun rapport.

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
Statut : 200 ; 486 o

2 liens ; retenus (2) :
```
timeseries_slb_element_phase_2/
timeseries_slb_elements/
```

**IMBIE (bilan de masse des calottes), page de téléchargement** — https://imbie.org/data-downloads/
Statut : 404 ; 0 o

**NASA, GRACE / GRACE-FO, masse de l'océan (PO.DAAC)** — https://podaac.jpl.nasa.gov/dataset/OCEAN_MASS_TIME_SERIES_GRACE-FO_JPL_RL06.3_V4
Statut : erreur : URLError <urlopen error _ssl.c:994: The handshake operation timed out> ; 0 o

**NASA Vital Signs, masse des calottes (page)** — https://climate.nasa.gov/vital-signs/ice-sheets/
Statut : 200 ; 275524 o

227 liens ; retenus (9) :
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
```

## 4. Compléments (deuxième passage)

**RSS vapeur, répertoire mensuel (HTML brut)** — https://data.remss.com/vapor/monthly_1deg/
Statut : 200
```
<html><head><title>data.remss.com - /vapor/monthly_1deg/</title></head><body><H1>data.remss.com - /vapor/monthly_1deg/</H1><hr>

<pre><A HREF="/vapor/">[To Parent Directory]</A><br><br>  1/8/2018 10:26 PM        &lt;dir&gt; <A HREF="/vapor/monthly_1deg/error_realizations/">error_realizations</A><br> 1/16/2026 11:20 PM    118243415 <A HREF="/vapor/monthly_1deg/merged_vapor_1988-2025.nc">merged_vapor_1988-2025.nc</A><br> 1/17/2026 12:16 AM        &lt;dir&gt; <A HREF="/vapor/monthly_1deg/old_files/">old_files</A><br> 1/25/2017 11:39 PM        &lt;dir&gt; <A HREF="/vapor/monthly_1deg/read_routines/">read_routines</A><br></pre><hr><script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)})(window,document,'script','//www.google-analytics.com/analytics.js','ga'); ga('create', 'UA-43439200-2', 'remss.com'); ga('send', 'pageview'); </script></body></html>
```

**RSS vapeur, répertoire parent (HTML brut)** — https://data.remss.com/vapor/
Statut : 200
```
<html><head><title>data.remss.com - /vapor/</title></head><body><H1>data.remss.com - /vapor/</H1><hr>

<pre><A HREF="/">[To Parent Directory]</A><br><br> 1/17/2026 12:16 AM        &lt;dir&gt; <A HREF="/vapor/monthly_1deg/">monthly_1deg</A><br></pre><hr><script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)})(window,document,'script','//www.google-analytics.com/analytics.js','ga'); ga('create', 'UA-43439200-2', 'remss.com'); ga('send', 'pageview'); </script></body></html>
```

**HadISDH, page d'accueil (tous les liens)** — https://www.metoffice.gov.uk/hadobs/hadisdh/
Statut : 200 ; 34930 o

```
../css/styles.css
../index.html
HadISDH.extremes.1.2.0.2024f_update.pdf
HadISDH.land.4.6.1.2024f_update.pdf
HadISDH.marine.1.6.1.2024f_update.pdf
Willett2023_HadISDHextremes_part1.pdf
Willett2023_HadISDHextremes_part2.pdf
Willettetal2013a.pdf
Willettetal2014b_HadISDH.pdf
Willettetal2014b_HadISDHsupplementary.pdf
Willettetal2020_HadISDHmarine.pdf
Willettetal2020_HadISDHmarine_supplement.pdf
anomalymapmaterial_DPDBLEND.html
anomalymapmaterial_DPDLAND.html
anomalymapmaterial_DPDMARINE.html
anomalymapmaterial_RHBLEND.html
anomalymapmaterial_RHLAND.html
anomalymapmaterial_RHMARINE.html
anomalymapmaterial_TBLEND.html
anomalymapmaterial_TLAND.html
anomalymapmaterial_TMARINE.html
anomalymapmaterial_TdBLEND.html
anomalymapmaterial_TdLAND.html
anomalymapmaterial_TdMARINE.html
anomalymapmaterial_TwBLEND.html
anomalymapmaterial_TwLAND.html
anomalymapmaterial_TwMARINE.html
anomalymapmaterial_TwN10p.html
anomalymapmaterial_TwX.html
anomalymapmaterial_TwX90p.html
anomalymapmaterial_eBLEND.html
anomalymapmaterial_eLAND.html
anomalymapmaterial_eMARINE.html
anomalymapmaterial_qBLEND.html
anomalymapmaterial_qLAND.html
anomalymapmaterial_qMARINE.html
code.html
contact.html
downloadBLEND.html
downloadBLENDprovisional.html
downloadEXTREMES.html
downloadEXTREMESprovisional.html
downloadLAND.html
downloadLANDprovisional.html
downloadMARINE.html
downloadMARINEprovisional.html
generalmaterial100.html
generalmaterial200.html
homogenisation.html
http://catalogue.ceda.ac.uk/uuid/251474c7b09449d8b9e7aeaf1461858f
http://hadisdh.blogspot.co.uk/
http://http://noc.ac.uk/
http://icoads.noaa.gov
http://journals.ametsoc.org/doi/abs/10.1175/2011BAMS3015.1
http://ncei.noaa.gov/products/land-based-station/integrated-surface-database
http://onlinelibrary.wiley.com/doi/10.1002/joc.4775/abstract;jsessionid=B0CF9D6ED283EB9DA3D591EF526CCAFF.f03t04
http://www.cru.uea.ac.uk
http://www.metoffice.gov.uk
http://www.metoffice.gov.uk/
http://www.metoffice.gov.uk/about-us/contact
http://www.metoffice.gov.uk/climate-change/resources/hadley
http://www.metoffice.gov.uk/hadobs/hadisd
http://www.metoffice.gov.uk/research/people/kate-willett
http://www.ncei.noaa.gov
http://www.nersc.no
http://www.noaa.gov/
http://www.npl.co.uk
https://hadisdh.blogspot.com/2026/04/provisional-2025-update-from-hadisdh-land-extremes.html
https://twitter.com/metofficeHadOBS
https://www.ncei.noaa.gov/products/land-based-station/us-historical-climatology-network
licence_ogl.html
onlinematerialBLEND.html
onlinematerialEXTREMES.html
onlinematerialLAND.html
onlinematerialMARINE.html
sotcmaterial.html
trendmaterialBLEND.html
trendmaterialEXTREMES.html
trendmaterialLAND.html
trendmaterialMARINE.html
uncertainty.html
```

**NOAA NCEI 3M_HEAT_CONTENT/DATA/basin (tous les liens)** — https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/
Statut : 200 ; 5222 o

```
/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/
3month/
3month_fs/
3month_hs/
3month_ms/
3month_mt/
3month_sl/
ohc2000m_levitus_climdash_seasonal.csv
onemonth/
onemonth_basin.tar
pentad/
pentad_fs/
pentad_hs/
pentad_ms/
pentad_mt/
pentad_sl/
yearly/
yearly_fs/
yearly_hs/
yearly_ms/
yearly_mt/
yearly_sl/
```

**NOAA NCEI 3M_HEAT_CONTENT/DATA (tous les liens)** — https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/
Statut : 200 ; 4808 o

```
/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/
basin/
heat_1month/
heat_3month/
heat_pentads/
heat_year/
mt_3month/
mt_pentads/
mt_year/
sl_3month/
sl_pentads/
sl_year/
tanom_1month/
tanom_1monthF/
tanom_3month/
tanom_3monthF/
tanom_pentad/
tanom_pentadF/
tanom_year/
tanom_yearF/
```

**NOAA NCEI 3M_HEAT_CONTENT (tous les liens)** — https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/
Statut : 200 ; 2908 o

```
/data/oceans/woa/DATA_ANALYSIS/
DATA/
DATA_old/
FIGURES/
FIGURES_old/
GRAPHS/
NETCDF/
PDF/
TEST_DATA/
TEST_FIGURES/
heat_content/
```

**IMBIE, page d'accueil** — https://imbie.org/
Statut : 200 ; 74481 o

```
/about/
/science/
https://gmpg.org/xfn/11
https://imbie.org/
https://imbie.org/about/
https://imbie.org/comments/feed/
https://imbie.org/contact/
https://imbie.org/feed/
https://imbie.org/media/
https://imbie.org/participate/
https://imbie.org/science/
https://imbie.org/wp-content/uploads/2026/09/cropped-imbie-logo-512x512-1-180x180.png
https://imbie.org/wp-content/uploads/2026/09/cropped-imbie-logo-512x512-1-192x192.png
https://imbie.org/wp-content/uploads/2026/09/cropped-imbie-logo-512x512-1-32x32.png
https://imbie.org/wp-content/uploads/2026/10/IMBIE-Privacy-Notice.pdf
https://imbie.org/wp-json/
https://imbie.org/wp-json/wp/v2/pages/6
//fonts.googleapis.com
https://imbie.org/
```

**CEDA, ESA CCI Sea Level Budget Closure (autre hôte)** — https://data.ceda.ac.uk/neodc/esacci/sea_level_budget_closure/data
Statut : 200 ; 15780 o

```
/neodc
/neodc/esacci
/neodc/esacci/sea_level_budget_closure
/neodc/esacci/sea_level_budget_closure/data/timeseries_slb_element_phase_2
/neodc/esacci/sea_level_budget_closure/data/timeseries_slb_elements
/static/common/img/favicon.d61e624a1ae4.ico
/static/fwtheme_django/css/fw-custom.475feb7d8445.css
/timelines/neodc/esacci/sea_level_budget_closure/data
https://archive.ceda.ac.uk/
https://archive.ceda.ac.uk/about/
https://archive.ceda.ac.uk/tools
https://arrivals.ceda.ac.uk
https://artefacts.ceda.ac.uk/themes/orgtheme_ceda_serv/0.2/4/flatly/bootstrap.css
https://artefacts.ceda.ac.uk/themes/orgtheme_ceda_serv/0.2/_assets/css/custom.min.css
https://artefacts.ceda.ac.uk/themes/orgtheme_ceda_serv/0.2/_assets/css/org-custom.css
https://catalogue.ceda.ac.uk
https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.3.0/css/all.min.css
https://data.ceda.ac.uk
https://help.ceda.ac.uk/article/4639-privacy-and-cookies
https://help.ceda.ac.uk/article/4641-accessibility
https://help.ceda.ac.uk/article/4642-disclaimer
https://help.ceda.ac.uk/article/5100-archive-access-tokens
https://help.ceda.ac.uk/article/5191-downloading-multiple-files-with-wget
https://www.ceda.ac.uk
https://www.ceda.ac.uk/news/
https://www.ncas.ac.uk
https://www.nceo.ac.uk
https://www.stfc.ac.uk
```

**CSR, mascons GRACE RL06 (page)** — https://www2.csr.utexas.edu/grace/RL06_mascons.html
Statut : 200 ; 20513 o

```
assets/css/portal-v1.0.13.css
http://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_MASCONS_RL0603_GSU
http://onlinelibrary.wiley.com/doi/10.1002/2016JB013007/full
https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/gracefo/open/docs/TN-13_GEOC_CSR_RL0603.txt
https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/gracefo/open/docs/TN-14_C30_C20_GSFC_SLR.txt
https://doi.org/10.15781/cgq9-nh24
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE-FO_RL0603_Mascons_MasconC30-component.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE-FO_RL0603_Mascons_SLR-C30-component.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL0603_Mascons_GAC-component.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL0603_Mascons_GAD-component.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL0603_Mascons_GIA-component.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL0603_Mascons_GSU-component.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL0603_Mascons_MasconC20-component.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL0603_Mascons_SLR-C20-component.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL0603_Mascons_degree1-component.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL0603_mascons_mapping_file.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL06_Mascons_v02_LandMask.nc
https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL06_Mascons_v02_OceanMask.nc
https://dx.doi.org/10.1002/2016JB013007
https://grace.jpl.nasa.gov/data-analysis-tool
https://www.gracetws.com/
https://www2.csr.utexas.edu/grace/
https://www2.csr.utexas.edu/grace/(https://doi.org/10.1007/s00190-018-1128-0
https://www2.csr.utexas.edu/grace/RL06.html
https://www2.csr.utexas.edu/grace/RL0603_mascons.html
https://www2.csr.utexas.edu/grace/csr_mascon_placement/
```

**SEANOE, budget WCRP 2018 (doi 10.17882/54854)** — https://www.seanoe.org/data/00444/55547/
Statut : 200 ; 64995 o

```
/env-styles/env-styles.scss
/webclient/chunk-Bgmrn8l1.js
/webclient/chunk-C0dijbCo.js
/webclient/chunk-C0u7oI5X.js
/webclient/chunk-CcfaevXO.js
/webclient/chunk-Cye5YTRJ.js
/webclient/chunk-DcfbhjZy.js
/webclient/chunk-DqImu7HG.js
/webclient/chunk-DtIplyFi.js
/webclient/chunk-WJVqYS7P.js
/webclient/styles-R5KKTB27.css
assets/images/favicon.ico
http://crepe-seanoe-frontoffice-internet:8080/rss
https://fonts.gstatic.com
https://www.coretrustseal.org/wp-content/uploads/2019/11/IFREMER-SISMER.pdf
https://www.seanoe.org
https://www.seanoe.org/html/about.htm
https://www.seanoe.org/html/credit.htm
https://www.seanoe.org/html/mentionlegales.htm
https://www.seanoe.org/oai/
```

**Zenodo, Frederikse et al. 2020, budget du niveau marin 1900-2018 (fiche)** — https://zenodo.org/api/records/3862995
Statut : 200

Titre : data supplement of "The causes of sea-level rise since 1900"
```
GMSL_ensembles.nc 4355070 https://zenodo.org/api/records/3862995/files/GMSL_ensembles.nc/content
GrIS.nc 24849871 https://zenodo.org/api/records/3862995/files/GrIS.nc/content
README 2197 https://zenodo.org/api/records/3862995/files/README/content
region_info.xlsx 60194 https://zenodo.org/api/records/3862995/files/region_info.xlsx/content
steric.nc 12819425 https://zenodo.org/api/records/3862995/files/steric.nc/content
AIS.nc 22456092 https://zenodo.org/api/records/3862995/files/AIS.nc/content
glac.nc 33170590 https://zenodo.org/api/records/3862995/files/glac.nc/content
global_basin_timeseries.xlsx 271196 https://zenodo.org/api/records/3862995/files/global_basin_timeseries.xlsx/content
tws.nc 25496893 https://zenodo.org/api/records/3862995/files/tws.nc/content
total.nc 46911247 https://zenodo.org/api/records/3862995/files/total.nc/content
```

## 5. Troisième passage

**RSS vapeur, monthly_1deg** — https://data.remss.com/vapor/monthly_1deg/
Statut : 200 ; 0 liens retenus
```
```

**NOAA NCEI, niveau thermostérique annuel (yearly_sl)** — https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/yearly_sl/
Statut : 200 ; 4 liens retenus
```
a-mm-w0-2000m.dat
a-mm-w0-700m.dat
tsl2000m_levitus_climdash_yearly.csv
tsl_levitus_climdash_yearly.csv
```

Fichier https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/yearly_sl/a-mm-w0-2000m.dat : 200 ; 1254 o

```
    YEAR      WO    WOse      NH    NHse      SH    SHse
2005.500  14.538   0.918  20.363   0.703  10.451   1.263
2006.500  16.881   0.413  22.012   1.065  13.281   0.603
2007.500  16.691   0.558  22.498   0.987  12.617   0.880
2008.500  17.683   0.472  24.206   1.308  13.107   0.481
2009.500  18.156   0.685  22.163   0.260  15.345   1.181
2010.500  19.235   0.471  23.284   0.325  16.394   0.829
2011.500  19.180   0.550  19.903   0.506  18.673   0.847
…
2022.500  35.408   0.183  39.321   0.740  32.662   0.538
2023.500  37.306   0.519  39.425   1.004  35.819   0.747
2024.500  38.401   0.327  45.128   0.765  33.680   0.908
2025.500  40.622   0.490  50.584   0.962  33.631   0.244
```

**NOAA NCEI, niveau thermostérique pentadaire (pentad_sl)** — https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/pentad_sl/
Statut : 200 ; 2 liens retenus
```
pent_a-mm-w0-2000m.dat
pent_a-mm-w0-700m.dat
```

Fichier https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/pentad_sl/pent_a-mm-w0-2000m.dat : 200 ; 3876 o

```
    YEAR      WO    WOse      NH    NHse      SH    SHse
  1957.5  -9.802   2.447  -8.721   2.720 -10.560   2.255
  1958.5  -7.705   2.358  -5.227   2.447  -9.443   2.296
  1959.5  -8.455   2.351  -5.982   2.333 -10.190   2.363
  1960.5  -4.492   2.154  -3.178   2.099  -5.414   2.193
  1961.5  -3.849   2.029  -4.315   2.000  -3.522   2.050
  1962.5  -3.527   1.960  -4.849   1.790  -2.599   2.080
  1963.5  -5.404   2.019  -5.941   1.853  -5.027   2.135
…
  2020.5  31.584   0.219  37.110   0.262  27.707   0.189
  2021.5  34.130   0.226  40.067   0.270  29.963   0.194
  2022.5  35.449   0.229  41.453   0.277  31.236   0.195
  2023.5  37.351   0.232  44.090   0.282  32.621   0.197
```

**HadISDH, téléchargement marin** — https://www.metoffice.gov.uk/hadobs/hadisdh/downloadMARINE.html
Statut : 200 ; 1 liens retenus
```
data/HadISDH.marineq.1.6.1.2024f_BClocalSHIP5by5both_anoms9120.nc
```

**HadISDH, téléchargement combiné** — https://www.metoffice.gov.uk/hadobs/hadisdh/downloadBLEND.html
Statut : 200 ; 1 liens retenus
```
data/HadISDH.blendq.1.5.1.2024f_FLATgridHOMBClocalSHIPboth5by5_anoms9120.nc
```

**CEDA SLBC_cci, phase 2** — https://data.ceda.ac.uk/neodc/esacci/sea_level_budget_closure/data/timeseries_slb_element_phase_2
Statut : 200 ; 0 liens retenus
```
```

**NASA CMR, collections « GRACE ocean mass »** — https://cmr.earthdata.nasa.gov/search/collections.json?keyword=GRACE%20ocean%20mass&page_size=20
Statut : 200
```
HOMAGE_GGFO_L4_GOMA_Monthly_v01 | 1.0 | GRACE/GRACE-FO Level-4 Monthly Global Ocean Mass Anomaly version 01 from NASA MEaSUREs HOMaGE project | 2002-04-17-
OCEAN_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4 | RL06.3Mv04 | Tellus Level-4 Ocean Mass Anomaly Time Series from JPL GRACE/GRACE-FO Mascon CRI Filtered Release 06.3 version | 2002-04-01-
TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4 | RL06.3Mv04 | JPL GRACE and GRACE-FO Mascon Ocean, Ice, and Hydrology Equivalent Water Height Coastal Resolution Improvement | 2002-04-04-
ANTARCTICA_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4 | RL06.3Mv04 | Tellus Level-4 Antarctica Mass Anomaly Time Series from JPL GRACE/GRACE-FO Mascon CRI Filtered Release 06.3 ve | 2002-04-01-
TELLUS_GRAC-GRFO_MASCON_GRID_RL06.3_V4 | RL06.3Mv04 | JPL GRACE and GRACE-FO Mascon Ocean, Ice, and Hydrology Equivalent Water Height JPL Release 06.3 Version 04 | 2002-04-04-
TELLUS_GRFO_L3_CSR_RL06.3_OCN_v04 | RL06.3v04 | CSR TELLUS GRACE-FO Level-3 Monthly Ocean Bottom Pressure Anomaly Release 6.3 version 04 | 2018-05-22-
GREENLAND_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4 | RL06.3Mv04 | Tellus Level-4 Greenland Mass Anomaly Time Series from JPL GRACE/GRACE-FO Mascon CRI Filtered Release 06.3 ver | 2002-04-01-
HOMAGE_GGFO_MSC_CRI_SALGRD_v01 | 1.0 | GRACE/GRACE-FO Level-4 Monthly Gravitational-Rotational-Deformation version 01 from NASA MEaSUREs HOMaGE | 2002-04-16-
HOMAGE_STERIC_OHC_TIME_SERIES_v01 | 1.0 | HOMAGE Monthly Time series of global average steric height anomalies and ocean heat content estimates from gri | 1978-01-15-
GRC-GFO_GRIDDED_AOD1B_JPL_1-DEG_RL06.3 | RL06.3 | JPL GRACE/GRACE-FO Gridded-AOD1B Water-Equivalent-Thickness Surface-Mass Anomaly RL06.3 dataset for Tellus Lev | 2002-04-04-
GRC-GFO_GRIDDED_AOD1B_JPL_MASCON_RL06.3 | RL06.3 | JPL GRACE/GRACE-FO Gridded-AOD1B Water-Equivalent-Thickness Surface-Mass Anomaly RL06.3 dataset for Tellus Lev | 2002-04-04-
TELLUS_GRFO_L3_GFZ_RL06.3_OCN_v04 | RL06.3v04 | GFZ TELLUS GRACE-FO Level-3 Monthly Ocean Bottom Pressure Anomaly Release 6.3 version 04 | 2018-05-22-
TELLUS_GRFO_L3_JPL_RL06.3_OCN_v04 | RL06.3v04 | JPL TELLUS GRACE-FO Level-3 Monthly Ocean Bottom Pressure Anomaly Release 6.3 version 04 | 2018-05-22-
GGP-SG-CORMIN | Not provided | GGP - Corrected Minute Data | 1997-07-01-
AAS_4318_GIA_model_output | 1 | GIA model output for bedrock displacement at geodetic GPS sites in the Casey-Davis region of East Antarctica | 2015-07-01-2020-06-30
JPL_RECON_GMSL | 1.0 | Reconstructed Global Mean Sea Level 1900-2018 | 1900-01-01-2018-12-31
AAS_4355_Mulder_etal_2019 | 1 | Zircon, monazite and feldspar datasets from Indo- and Australo-Antarctica | 2016-01-01-2018-12-30
GRACE-A.and.GRACE-B.Level1B.Level1Bcombined.Level2 | 5.0 | GRACE-A and GRACE-B Level 1B,  Level 1B combined and Level 2 Data Products | 2002-04-01-2017-10-27
TELLUS_GRAC_L3_CSR_RL06_OCN_v04 | RL06v04 | CSR TELLUS GRACE Level-3 Monthly Ocean Bottom Pressure Anomaly Release 6.0 version 04 | 2002-04-04-2017-10-25
TELLUS_GRAC_L3_GFZ_RL06_OCN_v04 | RL06v04 | GFZ TELLUS GRACE Level-3 Monthly Ocean Bottom Pressure Anomaly Release 6.0 version 04 | 2002-04-04-2017-10-25
```

Jeton Earthdata présent dans l'environnement : oui

## 6. Quatrième passage

**RSS vapeur, tous les liens de monthly_1deg**
```
/vapor/
/vapor/monthly_1deg/error_realizations/
/vapor/monthly_1deg/merged_vapor_1988-2025.nc
/vapor/monthly_1deg/old_files/
/vapor/monthly_1deg/read_routines/
```

Fichier https://data.remss.com/vapor/monthly_1deg/merged_vapor_1988-2025.nc : 200 ; 30000000 o

**CMR, OCEAN_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4**
Statut : 200
```
ocean_mass_200204_202609 2002-04-01T00:00:00.000Z 2026-09-30T23:59:59.000Z
https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-protected/OCEAN_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4/ocean_mass_200204_202609.txt
https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-public/OCEAN_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4/ocean_mass_200204_202609.txt.md5
https://archive.podaac.earthdata.nasa.gov/s3credentials
https://cmr.earthdata.nasa.gov/virtual-directory/collections/C3206302778-POCLOUD
https://search.earthdata.nasa.gov/search/granules?p=C3206302778-POCLOUD
https://github.com/podaac/data-subscriber
```
Téléchargement avec jeton : échec HTTPError HTTP Error 400: Bad Request

**CMR, GREENLAND_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4**
Statut : 200
```
greenland_mass_200204_202609 2002-04-01T00:00:00.000Z 2026-09-30T23:59:59.000Z
https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-protected/GREENLAND_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4/greenland_mass_200204_202609.txt
https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-public/GREENLAND_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4/greenland_mass_200204_202609.txt.md5
https://archive.podaac.earthdata.nasa.gov/s3credentials
https://cmr.earthdata.nasa.gov/virtual-directory/collections/C3206299308-POCLOUD
https://search.earthdata.nasa.gov/search/granules?p=C3206299308-POCLOUD
https://github.com/podaac/data-subscriber
```
Téléchargement avec jeton : échec HTTPError HTTP Error 400: Bad Request

**CMR, ANTARCTICA_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4**
Statut : 200
```
antarctica_mass_200204_202609 2002-04-01T00:00:00.000Z 2026-09-30T23:59:59.000Z
https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-protected/ANTARCTICA_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4/antarctica_mass_200204_202609.txt
https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-public/ANTARCTICA_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4/antarctica_mass_200204_202609.txt.md5
https://archive.podaac.earthdata.nasa.gov/s3credentials
https://cmr.earthdata.nasa.gov/virtual-directory/collections/C3206284786-POCLOUD
https://search.earthdata.nasa.gov/search/granules?p=C3206284786-POCLOUD
https://github.com/podaac/data-subscriber
```
Téléchargement avec jeton : échec HTTPError HTTP Error 400: Bad Request

**HadISDH marin, q** — https://www.metoffice.gov.uk/hadobs/hadisdh/data/HadISDH.marineq.1.6.1.2024f_BClocalSHIP5by5both_anoms9120.nc
Statut : 200 ; 30000000 o
lecture : OSError [Errno -101] NetCDF: HDF error: '/tmp/tmp4ltvghh_.nc'

