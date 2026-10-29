# Sonde P4 — impacts Gironde (généré)

Généré par `python -m etl.probe.p4` le 29/10/2026 12:20 UTC. Aucun indicateur calculé.

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
{"type":"permission denied","title":"user didn't accept all required site policies","status":403,"detail":"Missing policies are: Terms of use of the CEMS Early Warning Data Store (rev. 11) - https://ewds.climate.copernicus.eu/licences/terms-of-use-cems","instance":"https://ewds.climate.copernicus.eu/api/retrieve/v1/processes/cems-fire-historical-v1/execution","trace_id":"b0dd4a5d-01fe-4660-a439-42bdb4e0ab3f"}
KeyError 'jobID'
```
