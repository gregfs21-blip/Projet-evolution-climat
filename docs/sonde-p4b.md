# Sonde P4 — impacts Gironde (généré)

Généré par `python -m etl.probe.p4` le 28/10/2026 18:19 UTC. Aucun indicateur calculé.

## 1. Dates de vendanges

Second passage : la première lecture découpait les lignes aux blancs et décalait les colonnes.

### Base Daux et al. 2012 (NOAA Paleo), colonne Bordeaux

`https://www.ncei.noaa.gov/pub/data/paleo/historical/europe/europe2012ghd.txt` → **200**

```
2118 lignes
lignes brutes (repr) :
'Year              Als                  Auv                  Aux                  Bea                  Bor                  Bur                 Cha1                 Cha2                  Gai'
'1354                                                                                                                      15.3'
'1355                                                                                                                      13.4'
'Year            Germany         High Loire Valley      Ile de France            Jura               Languedoc        Low Loire Valley        Luxembourg          Maritime alps       Northern Italy'
'1354              Ger                  HLV                  IdF                  Jur                  Lan                  LLV                  Lux                  Mar                  NIt'
'1355'
'1976             21.7                                                            6.0                 11.7                  8.8                                       1.0'
'2003              8.0                                                                                -4.3                 -10.1                                     -4.0'
'2006                                                                                                 16.1                 16.0                                      16.0'
'1976                                                       28.0                 29.0                 24.9                 39.0'
'2003                                                                                                 20.8                 34.4'
'2006                                                                                                 20.4                 24.0'
table ligne 137 : colonnes ['Year', 'Als', 'Auv', 'Aux', 'Bea', 'Bor', 'Bur', 'Cha1', 'Cha2', 'Gai'] ; Bor entre les caractères 84 et 123
cellules illisibles (lecture à largeur fixe) : 325
colonne Bor : 265 valeurs, [1354] à [1976]
1800s : 
1810s : 
1820s : 1822:-5.8
1830s : 
1840s : 
1850s : 
1860s : 
1870s : 
1880s : 
1890s : 
1900s : 
1910s : 1910:36.4, 1917:16.1
1920s : 
1930s : 
1940s : 
1950s : 
1960s : 
1970s : 1976:11.7
1980s : 
1990s : 
2000s : 
années manquantes 1900-2006 : [1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1911, 1912, 1913, 1914, 1915, 1916, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1977, 1978, 1979, 1980, 1
```

### ONERC, page « agriculture et forêt » (série Saint-Émilion)

`https://www.ecologie.gouv.fr/politiques-publiques/impacts-du-changement-climatique-agriculture-foret` → **200**

```
102155 caractères, 103 liens
/sites/default/files/styles/default_mobile/public/images/19_Graph_indicateur_date_vendanges_Saint-Emilion.png?itok=HLn-yxaI
/sites/default/files/styles/default_mobile/public/images/21_Visuel_1_Graph_indicateur_Dates_recolte_ble_Mirecourt.png?itok=m4kK2B80
/sites/default/files/styles/default_mobile/public/images/21_Visuel_2_Graph_indicateur_Dates_recolte_ble_Breteniere.png?itok=RDUfWhR6
/sites/default/files/styles/default_mobile/public/images/21_Visuel_3_Graph_indicateur_Dates_recolte_ble_Auzeville.png?itok=tRSCspi9
/sites/default/files/styles/default_mobile/public/images/22_Graph_indicateur_dates_d%C3%A9bu_vendanges_C%C3%B4tes_d_Rh%C3%B4ne_m%C3%A9ridionales.png?itok=DILKfX2V
/sites/default/files/styles/default_mobile/public/images/23_Graph_indicateur_date_floraison_vendanges_en_Champagne.png?itok=tecxbMum
/sites/default/files/styles/default_mobile/public/images/Onerc_Date%20des%20vendanges_1901_2016.png?itok=7x5hqSnk
— contexte —
dernières années (95 jours d'écart en 1951-1961 contre 86 en 2015-2025).&nbsp;</p></div><div class="paragraph paragraph--type--accordion-group paragraph--view-mode--default"><h2 > Date de vendanges à Saint-Emilion (Gironde)</h2><div class="paragraph paragraph--type--accordion-group paragraph--view-mode--default fr-accordions-group" data-component-id="customer:accordion_group" data-fr-group="false"><div class="paragraph paragraph--type--accordion-element paragraph--view-mode--default"> <section d
ion"><h3 class="fr-accordion__title"> <button class="fr-accordion__btn" aria-expanded="false" aria-controls="accordion-587886023" type="button"> Définition de l&#039;indicateur de date de vendanges à Saint-Emilion (Gironde) </button></h3><div class="fr-collapse" id="accordion-587886023"><p>Cet indicateur rend compte de la date de début des vendanges dans une propriété de l’appellation Saint-Émilion depuis 1900.</p></div> </section></div><div class="paragraph paragraph--type--accordion-element pa
dion__title"> <button class="fr-accordion__btn" aria-expanded="false" aria-controls="accordion-265263275" type="button"> Responsable et origine des données de l&#039;indicateur de date de vendanges à Saint-Emilion (Gironde) </button></h3><div class="fr-collapse" id="accordion-265263275"><p>Responsable de l’indicateur&nbsp;: Pr. Cornelis (Kees) VAN&nbsp;LEEUWEN, INRAE et Bordeaux Sciences Agro</p><p>Organisme propriétaire des données&nbsp;: INRAE et Bordeaux Sciences Agro</p><p>Date de dernière a
dion"><h3 class="fr-accordion__title"> <button class="fr-accordion__btn" aria-expanded="false" aria-controls="accordion-221818234" type="button"> Fiabilité de l&#039;indicateur de date de vendanges à Saint-Emilion (Gironde) </button></h3><div class="fr-collapse" id="accordion-221818234"><p>La date des vendanges est un indicateur pertinent du régime thermique de l’année. La phénologie de la vigne est corrélée à la somme des températures moyennes journalières supérieures à 10&nbsp;°C. En effet, la
— scripts —
```

### Recherche Data Gouv : jeux de données « vendanges »

`https://entrepot.recherche.data.gouv.fr/api/search?q=vendanges&type=dataset&per_page=30` → **200**

```
```

### INRAE Colmar (indicateur ONERC Alsace), fichiers

`https://entrepot.recherche.data.gouv.fr/api/datasets/:persistentId/?persistentId=doi%3A10.15454/GYSGNR` → **200**

```
ReadMe_PhenoRiesling_INRA_Bergheim_2024.rtf (10693 o)
RieslingPhenology_Bergheim_68_1958_2026.tab (5753 o)
```
