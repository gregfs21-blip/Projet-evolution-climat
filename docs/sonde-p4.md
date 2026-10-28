# Sonde P4 — impacts Gironde (généré)

Généré par `python -m etl.probe.p4` le 28/10/2026 18:16 UTC. Aucun indicateur calculé.

## 1. Dates de vendanges

### Base Daux et al. 2012 (NOAA Paleo), colonne Bordeaux

`https://www.ncei.noaa.gov/pub/data/paleo/historical/europe/europe2012ghd.txt` → **200**

```
2118 lignes
the number of days after 31 August. 
Bordeaux                          45.18      -0.75
Gaillac- South-West               43.9        1.9
                Alsace              Auvergne          Auxerre-Avalon    Beaujolais and Maconn      Bordeaux             Burgundy            Champagne 1          Champagne 2      Gaillac- South-West
Year              Als                  Auv                  Aux                  Bea                  Bor                  Bur                 Cha1                 Cha2                  Gai
en-tête ligne 137 : Year Als Auv Aux Bea Bor Bur Cha1 Cha2 Gai
colonne Bor : 154 valeurs, [(1756, 38.0), (1764, 27.0), (1765, 40.0)] … [(1972, 42.0), (1973, 28.0), (1974, 28.0), (1975, 30.5), (1976, 1.0)]
depuis 1950 : 27 années ; trous : []
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

## 2. Danger météorologique d'incendie (CEMS/EFFIS, ERA5, Copernicus EWDS)

### Description du jeu (entrées et valeurs permises)

`https://ewds.climate.copernicus.eu/api/retrieve/v1/processes/cems-fire-historical-v1` → **200**

```
product_type : 2 valeurs : ['reanalysis', 'ensemble_members']
variable : 14 valeurs : ['build_up_index', 'burning_index', 'drought_code', 'drought_factor', 'duff_moisture_code', 'energy_release_component', 'fine_fuel_moisture_code', 'fire_daily_severity_rating', 'fire_danger_index', 'fire_weather_index', 'ignition_component', 'initial_fire_spread_index', 'keetch_byram_drought_index', 'spread_component']
dataset_type : 2 valeurs : ['consolidated_dataset', 'intermediate_dataset']
system_version : 1 valeurs : ['4_1']
year : 87 valeurs : ['1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949', '1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960', '1961', '1962', '1963', '1964']
month : 12 valeurs : ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
day : 31 valeurs : ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25']
grid : 3 valeurs : ['0.5/0.5', '0.25/0.25', 'original_grid']
data_format : 2 valeurs : ['grib', 'netcdf']
area : 0 valeurs : []
```

### Soumission : FWI quotidien, juillet 2022, boîte Gironde

`https://ewds.climate.copernicus.eu/api/retrieve/v1/processes/cems-fire-historical-v1/execution` → **403**

```
requête : {"product_type": ["reanalysis"], "variable": ["fire_weather_index"], "dataset_type": ["consolidated_dataset"], "system_version": ["4_1"], "year": ["2022"], "month": ["07"], "day": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"], "grid": ["0.25/0.25"], "data_format": "netcdf", "area": [45.6, -1.3, 44.2, 0.4]}
{"type":"permission denied","title":"user didn't accept all required site policies","status":403,"detail":"Missing policies are: Terms of use of the CEMS Early Warning Data Store (rev. 11) - https://ewds.climate.copernicus.eu/licences/terms-of-use-cems","instance":"https://ewds.climate.copernicus.eu/api/retrieve/v1/processes/cems-fire-historical-v1/execution","trace_id":"188facb5-cbd7-4395-8abd-8da00316f41f"}
KeyError 'jobID'
```

## 3. Feux de forêt observés (BDIFF)

### Jeu data.gouv.fr

`https://www.data.gouv.fr/api/1/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff/` → **200**

```
Base de Données sur les Incendies de Forêts en France (BDIFF) | licence lov2 | maj 2025-12-13
La base de données sur les incendies de forêt (BDIFF) est une application internet chargée de centraliser les données sur les incendies de forêt sur le territoire français depuis 2006 et de mettre l'ensemble de cette information à disposition du public et des services de l'État.  L'application diffusée sur le portail, permet à tout utilisateur intéressé, de consulter des données nationales, sur les feux de forêt jusqu'à l'année antérieure à l’année en cours et ce, agrégées à la commune.   ![entr
- Portail BDIFF | api | other | https://bdiff.agriculture.gouv.fr/
```

### Ressource (début)

`https://bdiff.agriculture.gouv.fr/` → **erreur : URLError <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1010)>**

```
0 octets lus
```

### Site BDIFF

`https://bdiff.agriculture.gouv.fr/` → **erreur : URLError <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1010)>**

```
0 caractères
```

### Site BDIFF

`https://bdiff.agriculture.gouv.fr/incendies` → **erreur : URLError <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1010)>**

```
0 caractères
```

## 4. CatNat Gironde par péril (GASPAR), décompte sans tendance

### Archive GASPAR

`https://www.data.gouv.fr/api/1/datasets/r/d6fb9e18-b66b-499c-8284-46a3595579cc` → **200**

```
catnat_gaspar_2026-10-05.csv : 7676 reconnaissances (arrêté × commune × péril) en Gironde
péril | 1980 | 1990 | 2000 | 2010 | 2020 | total
ICB Inondations et/ou Coulées de Boue | 1253 | 865 | 646 | 195 | 320 | 3279
SEC Sécheresse | 152 | 158 | 586 | 523 | 347 | 1766
CMV Chocs Mécaniques liés à l'action des Vagues | 0 | 570 | 537 | 32 | 10 | 1149
TMP Tempête | 721 | 0 | 0 | 0 | 0 | 721
MVT Mouvement de Terrain | 14 | 543 | 4 | 17 | 10 | 588
GRL Grêle | 146 | 0 | 0 | 0 | 0 | 146
IRN Inondations Remontée Nappe | 0 | 0 | 1 | 6 | 6 | 13
GLT Glissement de Terrain | 0 | 11 | 0 | 0 | 0 | 11
ECB Eboulement et/ou Chute de Blocs | 0 | 3 | 0 | 0 | 0 | 3
```
