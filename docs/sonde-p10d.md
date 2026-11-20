# Sonde P10.4 — cohérence physique : données disponibles (généré)

Produit le 20/11/2026 10:42 UTC par `etl/probe/p10d.py`. Inventaire seulement : aucune tendance, aucun rapport.

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
Statut : 200 ; 275522 o

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

