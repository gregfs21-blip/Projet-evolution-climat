# Sonde P4 — impacts Gironde (généré)

Généré par `python -m etl.probe.p4` le 29/10/2026 12:28 UTC. Aucun indicateur calculé.

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

`https://ewds.climate.copernicus.eu/api/retrieve/v1/processes/cems-fire-historical-v1/execution` → **201**

```
requête : {"product_type": ["reanalysis"], "variable": ["fire_weather_index"], "dataset_type": ["consolidated_dataset"], "system_version": ["4_1"], "year": ["2022"], "month": ["07"], "day": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"], "grid": ["0.25/0.25"], "data_format": "netcdf", "area": [45.6, -1.3, 44.2, 0.4]}
{"processID":"cems-fire-historical-v1","type":"process","jobID":"3e88fe03-b66f-45d6-8c3e-e284852f60ee","status":"accepted","created":"2026-10-29T12:28:37.833547","updated":"2026-10-29T12:28:37.833547","links":[{"href":"https://ewds.climate.copernicus.eu/api/retrieve/v1/processes/cems-fire-historical-v1/execution","rel":"self"},{"href":"https://ewds.climate.copernicus.eu/api/retrieve/v1/jobs/3e88fe03-b66f-45d6-8c3e-e284852f60ee","rel":"monitor","type":"application/json","title":"job status info"}
état après 157 s : successful
résultat : 28840 octets, 52c38f9bb71f864a09cb9477b84bb372.nc
dimensions : valid_time=31, latitude=6, longitude=7
  valid_time ('valid_time',) (31,) seconds since 1970-01-01 initial time of forecast
    [np.int64(1656633600), np.int64(1656720000), np.int64(1656806400), np.int64(1656892800), np.int64(1656979200), np.int64(1657065600), np.int64(1657152000), np.int64(1657238400), np.int64(1657324800), np.int64(1657411200), np.int64(1657497600), np.int64(1657584000), np.int64(1657670400), np.int64(1657756800), np.int64(1657843200), np.int64(1657929600), np.int64(1658016000), np.int64(1658102400), np.int64(1658188800), np.int64(1658275200), np.int64(1658361600), np.int64(1658448000), np.int64(16
  surface () () 1 original GRIB coordinate for key: level(surface)
  latitude ('latitude',) (6,) degrees_north latitude
    [np.float64(45.45), np.float64(45.2), np.float64(44.95), np.float64(44.7), np.float64(44.45), np.float64(44.2)]
  longitude ('longitude',) (7,) degrees_east longitude
    [np.float64(0.2), np.float64(358.7), np.float64(358.95), np.float64(359.2), np.float64(359.45), np.float64(359.7), np.float64(359.95)]
  fwinx ('valid_time', 'latitude', 'longitude') (31, 6, 7) Numeric Forest fire weather index (as defined by the Canadian Forest Service)
    min 0.1, moyenne 22.8, max 80.2, mailles valides au 1er pas : 42
```
