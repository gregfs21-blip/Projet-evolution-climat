# Sonde P9 — Gulf Stream et AMOC (généré)

Généré par `python -m etl.probe.p9` le 17/11/2026 10:48 UTC. Aucun indicateur calculé.

## 1. Câble du détroit de Floride (NOAA AOML)

```
GET https://www.aoml.noaa.gov/phod/floridacurrent/data_access.php → erreur : URLError <urlopen error [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1011)> (URL finale : https://www.aoml.noaa.gov/phod/floridacurrent/data_access.php, 0 o)
liens retenus (0) :
mot « secular » : 0 occurrence(s)
mot « geomagnetic » : 0 occurrence(s)
mot « Volkov » : 0 occurrence(s)
mot « pressure » : 0 occurrence(s)
mot « 2023 » : 0 occurrence(s)
GET https://www.aoml.noaa.gov/phod/floridacurrent/FC_cable_transport_1982.dat → erreur : URLError <urlopen error [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1011)> (0 o)
GET https://www.aoml.noaa.gov/phod/floridacurrent/FC_cable_transport_1998.dat → erreur : URLError <urlopen error [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1011)> (0 o)
GET https://www.aoml.noaa.gov/phod/floridacurrent/FC_cable_transport_2000.dat → erreur : URLError <urlopen error [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1011)> (0 o)
GET https://www.aoml.noaa.gov/phod/floridacurrent/FC_cable_transport_2023.dat → erreur : URLError <urlopen error [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1011)> (0 o)
GET https://www.aoml.noaa.gov/phod/floridacurrent/FC_cable_transport_2024.dat → erreur : URLError <urlopen error [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1011)> (0 o)
GET https://www.aoml.noaa.gov/phod/floridacurrent/FC_cable_transport_2025.dat → erreur : URLError <urlopen error [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1011)> (0 o)
```

## 2. RAPID 26,5° N : accès

```
GET https://rapid.ac.uk/rapidmoc/rapid_data/datadl.php → 200 (URL finale : https://rapid.ac.uk/about-us/history, 31668 o)
liens retenus (1) :
  /data/data-download
mot « e-mail » : 0 occurrence(s)
mot « email » : 0 occurrence(s)
mot « version » : 0 occurrence(s)
mot « licen » : 0 occurrence(s)
GET https://rapid.ac.uk/data/data-download → 200 (URL finale : https://rapid.ac.uk/data/data-download, 45135 o)
liens retenus (12) :
  /data/data-download
  /sites/default/files/rapid_data/data/moc_transports_supporting_information_2026.pdf
  https://rapid.ac.uk/data/data-download
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/1a774e53-7383-2e9a-e053-6c86abc0d8c7/
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/223b34a3-2dc5-c945-e063-7086abc0f274
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/33826d6e-801c-b0a7-e063-7086abc0b9db&gt;Atlantic meridional overturning circulation observed by the RAPID-MOCHA-WBTS (RAPID-Meridional Overturning Circulation and Heatflux Array-Western Boundary Time Series) array at 26N from 2004 to 2023 (v2023.1)&lt;/a&gt;&nbsp;, British Oceanographic Data Centre - Natural Environment Research Council, UK. doi: 10.5285/223b34a3-2dc5-c945-e063-7086abc0f274
&lt;/p&gt;
&lt;p&gt;
    &lt;strong&gt;Version v2022.1&lt;/strong&gt;&lt;br&gt;
    Moat B.I.; Smeed D.A.; Rayner D.; Johns W.E.; Smith, R.; Volkov, D.; Baringer M. O.; and Collins, J. (2023).&nbsp;&lt;a href=
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/35784047-9b82-2160-e053-6c86abc0c91b/
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/5acfd143-1104-7b58-e053-6c86abc0d94b/
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/8cd7e7bb-9a20-05d8-e053-6c86abc012c2/
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/aa57e879-4cca-28b6-e053-6c86abc02de5/
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/cc1e34b3-3385-662b-e053-6c86abc03444
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/e91b10af-6f0a-7fa7-e053-6c86abc05a09
mot « e-mail » : 0 occurrence(s)
mot « email » : 6 occurrence(s)
  … Download data from the RAPID array To download the transports time series or vertical profile data sets, please enter your email-address below and select the checkboxes by the data sets you require. Email Required Datasets RAPID_gridded_v2024-2.nc …
  … To download the transports time series or vertical profile data sets, please enter your email-address below and select the checkboxes by the data sets you require. Email Required Datasets RAPID_gridded_v2024-2.nc RAPID_transports_v2024-2.nc RAPID_layers_v2024-2.nc …
  … sp;and the error estimates is given in&nbsp; README error file . Use the links in the Data section to view plots of the data and read about related data. To access the data we ask that you leave your email address so that we can notify you when updates to the timeseries become available and so that we can record the number of times the data is accessed. How to acknowledge data from the RAPID AMOC project: Data from RAPID AMOC monitoring project …
mot « version » : 13 occurrence(s)
  … Natural Environment Research Council, U.S. National&nbsp;Science Foundation (NSF) with support from NOAA. They are freely available from https://rapid.ac.uk/ ." Digital Object Identifier (doi) for version 2024-2 The full doi for this data set is: 10.5285/5c39bf4e-5140-5546-e063-7086abc027bc The citation that should be used in journals is: Moat B.I.; Petit T.; Smeed D.A.; Rayner D.; Johns W.E.; Smith, R.; Volkov, D.; Elipot S.; Baringer M. O. …
  … lux Array-Western Boundary Time Series) array at 26N from 2004 to 2024 (v2024-2). NERC EDS British Oceanographic Data Centre NOC. doi:10.5285/5c39bf4e-5140-5546-e063-7086abc027bc Previous releases Version v2024.1a Moat B.I.; Smeed D.A.; Rayner D.; Johns W.E.; Smith, R.; Volkov, D.; Elipot S.; Petit T.; Kajtar J.; Baringer M. O.; and Collins, J. (2026). Atlantic meridional overturning circulation observed by the RAPID-MOCHA-WBTS (RAPID-Meridi …
  … tern Boundary Time Series) array at 26N from 2004 to 2024 (v2024.1a), British Oceanographic Data Centre - Natural Environment Research Council, UK. doi: 10.5285/48d0bf43-0598-ceb2-e063-7086abc062f1 Version v2024.1 Moat B.I.; Smeed D.A.; Rayner D.; Johns W.E.; Smith, R.; Volkov, D.; Elipot S.; Petit T.; Kajtar J.; Baringer M. O.; and Collins, J. (2025). Atlantic meridional overturning circulation observed by the RAPID-MOCHA-WBTS (RAPID-Meridio …
mot « licen » : 0 occurrence(s)
GET https://rapid.ac.uk/node/10 → 200 (URL finale : https://rapid.ac.uk/node/10, 45124 o)
liens retenus (12) :
  /data/data-download
  /sites/default/files/rapid_data/data/moc_transports_supporting_information_2026.pdf
  https://rapid.ac.uk/data/data-download
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/1a774e53-7383-2e9a-e053-6c86abc0d8c7/
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/223b34a3-2dc5-c945-e063-7086abc0f274
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/33826d6e-801c-b0a7-e063-7086abc0b9db&gt;Atlantic meridional overturning circulation observed by the RAPID-MOCHA-WBTS (RAPID-Meridional Overturning Circulation and Heatflux Array-Western Boundary Time Series) array at 26N from 2004 to 2023 (v2023.1)&lt;/a&gt;&nbsp;, British Oceanographic Data Centre - Natural Environment Research Council, UK. doi: 10.5285/223b34a3-2dc5-c945-e063-7086abc0f274
&lt;/p&gt;
&lt;p&gt;
    &lt;strong&gt;Version v2022.1&lt;/strong&gt;&lt;br&gt;
    Moat B.I.; Smeed D.A.; Rayner D.; Johns W.E.; Smith, R.; Volkov, D.; Baringer M. O.; and Collins, J. (2023).&nbsp;&lt;a href=
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/35784047-9b82-2160-e053-6c86abc0c91b/
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/5acfd143-1104-7b58-e053-6c86abc0d94b/
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/8cd7e7bb-9a20-05d8-e053-6c86abc012c2/
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/aa57e879-4cca-28b6-e053-6c86abc02de5/
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/cc1e34b3-3385-662b-e053-6c86abc03444
  https://www.bodc.ac.uk/data/published_data_library/catalogue/10.5285/e91b10af-6f0a-7fa7-e053-6c86abc05a09
mot « e-mail » : 0 occurrence(s)
mot « email » : 6 occurrence(s)
  … Download data from the RAPID array To download the transports time series or vertical profile data sets, please enter your email-address below and select the checkboxes by the data sets you require. Email Required Datasets RAPID_gridded_v2024-2.nc …
  … To download the transports time series or vertical profile data sets, please enter your email-address below and select the checkboxes by the data sets you require. Email Required Datasets RAPID_gridded_v2024-2.nc RAPID_transports_v2024-2.nc RAPID_layers_v2024-2.nc …
  … sp;and the error estimates is given in&nbsp; README error file . Use the links in the Data section to view plots of the data and read about related data. To access the data we ask that you leave your email address so that we can notify you when updates to the timeseries become available and so that we can record the number of times the data is accessed. How to acknowledge data from the RAPID AMOC project: Data from RAPID AMOC monitoring project …
mot « version » : 13 occurrence(s)
  … Natural Environment Research Council, U.S. National&nbsp;Science Foundation (NSF) with support from NOAA. They are freely available from https://rapid.ac.uk/ ." Digital Object Identifier (doi) for version 2024-2 The full doi for this data set is: 10.5285/5c39bf4e-5140-5546-e063-7086abc027bc The citation that should be used in journals is: Moat B.I.; Petit T.; Smeed D.A.; Rayner D.; Johns W.E.; Smith, R.; Volkov, D.; Elipot S.; Baringer M. O. …
  … lux Array-Western Boundary Time Series) array at 26N from 2004 to 2024 (v2024-2). NERC EDS British Oceanographic Data Centre NOC. doi:10.5285/5c39bf4e-5140-5546-e063-7086abc027bc Previous releases Version v2024.1a Moat B.I.; Smeed D.A.; Rayner D.; Johns W.E.; Smith, R.; Volkov, D.; Elipot S.; Petit T.; Kajtar J.; Baringer M. O.; and Collins, J. (2026). Atlantic meridional overturning circulation observed by the RAPID-MOCHA-WBTS (RAPID-Meridi …
  … tern Boundary Time Series) array at 26N from 2004 to 2024 (v2024.1a), British Oceanographic Data Centre - Natural Environment Research Council, UK. doi: 10.5285/48d0bf43-0598-ceb2-e063-7086abc062f1 Version v2024.1 Moat B.I.; Smeed D.A.; Rayner D.; Johns W.E.; Smith, R.; Volkov, D.; Elipot S.; Petit T.; Kajtar J.; Baringer M. O.; and Collins, J. (2025). Atlantic meridional overturning circulation observed by the RAPID-MOCHA-WBTS (RAPID-Meridio …
mot « licen » : 0 occurrence(s)
GET https://doi.org/10.5285/223b34a32dc5c945e0637086abc0f274 → 404 (URL finale : https://doi.org/10.5285/223b34a32dc5c945e0637086abc0f274, 2000 o)
liens retenus (0) :
mot « 2004 » : 0 occurrence(s)
mot « licen » : 0 occurrence(s)
mot « download » : 0 occurrence(s)
```

## 3. Zones de Caesar et al. (2018)

```
GET https://www.pik-potsdam.de/~caesar/AMOC_slowdown/ → 200 (URL finale : https://www.pik-potsdam.de/~caesar/AMOC_slowdown/, 6604 o)
liens retenus (4) :
  gulfstream_grid.txt
  gulfstream_index_hadisst.txt
  sg_grid.txt
  sg_index_hadisst.txt
GET https://www.pik-potsdam.de/~caesar/AMOC_slowdown/sg_grid.txt → 200 (17165 o)
  745 lignes ; 3 premières : [['#', 'On', 'a', 'grid', 'from', '-90�S', 'to', '90�N', 'and', '-180�W', 'and', '180�E'], ['65.50', '-59.50'], ['65.50', '-58.50']]
  lecture numérique impossible : could not convert string to float: '#'
GET https://www.pik-potsdam.de/~caesar/AMOC_slowdown/gs_grid.txt → 404 (988 o)
```

## 4. EN4.2.2 : archives et contenu

```
GET https://www.metoffice.gov.uk/hadobs/en4/EN.4.2.2.analyses.g10.download-list.txt → 200 ; 127 archives
  première : http://www.metoffice.gov.uk/hadobs/en4/data/en4-2-1/EN.4.2.2/EN.4.2.2.analyses.g10.1900.zip
  dernière : http://www.metoffice.gov.uk/hadobs/en4/data/en4-2-1/EN.4.2.2.analyses.g10.2026.zip
GET https://www.metoffice.gov.uk/hadobs/en4/download-en4-2-2.html → 200 (URL finale : https://www.metoffice.gov.uk/hadobs/en4/download-en4-2-2.html, 165471 o)
liens retenus (9) :
  EN.4.2.2.analyses.c13.download-list.txt
  EN.4.2.2.analyses.c14.download-list.txt
  EN.4.2.2.analyses.g10.download-list.txt
  EN.4.2.2.analyses.l09.download-list.txt
  EN.4.2.2.profiles.c13.download-list.txt
  EN.4.2.2.profiles.c14.download-list.txt
  EN.4.2.2.profiles.g10.download-list.txt
  EN.4.2.2.profiles.l09.download-list.txt
  terms_and_conditions.html
mot « licen » : 1 occurrence(s)
  … r. The addition of Cowley et al (2013) XBT bias corrected data (paired with the Levitus et al (2009) MBT corrections) in the .c13. ensemble member. The addition of licence and reference attributes to all netCDF files to aid correct citations and use. The removal of data from eight TAO buoys between 2015 and 2016 after spurious salinity values were found by a user in EN.4.2.1. …
mot « non commercial » : 0 occurrence(s)
mot « Non-Commercial » : 0 occurrence(s)
GET https://www.metoffice.gov.uk/hadobs/en4/data/en4-2-1/EN.4.2.2.analyses.g10.2024.zip → 200 ; 313.8 Mo en 8 s
12 fichiers : EN.4.2.2.f.analysis.g10.202401.nc (63 Mo), EN.4.2.2.f.analysis.g10.202402.nc (63 Mo), EN.4.2.2.f.analysis.g10.202403.nc (63 Mo) …
dimensions : depth=42, lat=173, lon=360, time=1, bnds=2
  title : Temperature and salinity analysis
  licence : EN4 is distributed under the Non Commercial Government Licence: http://www.nationalarchives.gov.uk/doc/non-commercial-government-licence/version/2/. The data are available for non-commercial use with attribution to the data providers, please see the product website (see global attribute: references)
  references : Website and paper: https://www.metoffice.gov.uk/hadobs/en4/; Good, S. A., M. J. Martin and N. A. Rayner, 2013. EN4: quality controlled ocean temperature and salinity profiles and monthly objective analyses with uncertainty estimates, Journal of Geophysical Research: Oceans, 118, 6704-6716, doi:10.10
  history : 
  depth ('depth',) (42,) metres depth
    5.02 → 5350.27 ; [np.float64(5.0), np.float64(15.1), np.float64(25.2), np.float64(35.3), np.float64(45.4), np.float64(55.7), np.float64(66.0), np.float64(76.5), np.float64(87.3), np.float64(98.3), np.float64(109.8), np.float64(122.0), np.float64(135.0), np.float64(149.4), np.float64(165.7), np.float64(184.7), np.float64(207.4), np.float64(235.4), np.float64(270.5), np.float64(315.4), np.float64(373.0), np.float64(446.8), np.float64(540.5), np.float64(657.3), np.float64(799.5)]
  lat ('lat',) (173,) degrees_north latitude
    -83.00 → 89.00 ; 
  lon ('lon',) (360,) degrees_east longitude
    1.00 → 360.00 ; 
  temperature ('time', 'depth', 'lat', 'lon') (1, 42, 173, 360) kelvin temperature
    min 269.3, moyenne 280.8, max 304.3
  salinity ('time', 'depth', 'lat', 'lon') (1, 42, 173, 360) 1 salinity
    min 4.593, moyenne 34.66, max 40.79
  temperature_uncertainty ('time', 'depth', 'lat', 'lon') (1, 42, 173, 360) kelvin temperature error standard deviation
    min 0.0004578, moyenne 0.3851, max 3.743
  salinity_uncertainty ('time', 'depth', 'lat', 'lon') (1, 42, 173, 360) 1 salinity error standard deviation
    min 0.0006972, moyenne 0.0798, max 2.103
  temperature_observation_weights ('time', 'depth', 'lat', 'lon') (1, 42, 173, 360)  temperature observation weights
    min -6.104e-06, moyenne 0.7632, max 1.058
  salinity_observation_weights ('time', 'depth', 'lat', 'lon') (1, 42, 173, 360)  salinity observation weights
    min 2.563e-07, moyenne 0.7461, max 1.065
  time ('time',) (1,) days since 1800-01-01 00:00:00 
  time_bnds ('time', 'bnds') (1, 2)  
  depth_bnds ('depth', 'bnds') (42, 2)  
HEAD http://www.metoffice.gov.uk/hadobs/en4/data/en4-2-1/EN.4.2.2/EN.4.2.2.analyses.g10.1900.zip → 200 ; taille annoncée 254767872 o
```
