# Sonde P7 — blocages et foudre (généré)

Généré par `python -m etl.probe.p7` le 31/10/2026 21:20 UTC. Aucun indicateur calculé.

## 1. ERA5 quotidien, niveaux de pression : entrées

```
→ 200
product_type : 3 valeurs : ['reanalysis', 'ensemble_mean', 'ensemble_members']
variable : 16 valeurs : ['divergence', 'fraction_of_cloud_cover', 'geopotential', 'ozone_mass_mixing_ratio', 'potential_vorticity', 'relative_humidity', 'specific_cloud_ice_water_content', 'specific_cloud_liquid_water_content', 'specific_humidity', 'specific_rain_water_content', 'specific_snow_water_content', 'temperature', 'u_component_of_wind', 'v_component_of_wind', 'vertical_velocity', 'vorticity']
year : 87 valeurs : ['1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949', '1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979']
month : 12 valeurs : ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
day : 31 valeurs : ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
pressure_level : 37 valeurs : ['1', '10', '100', '1000', '125', '150', '175', '2', '20', '200', '225', '250', '3', '30', '300', '350', '400', '450', '5', '50', '500', '550', '600', '650', '7', '70', '700', '750', '775', '800', '825', '850', '875', '900', '925', '950', '975']
daily_statistic : 3 valeurs : ['daily_mean', 'daily_maximum', 'daily_minimum']
time_zone : 27 valeurs : ['utc+00:00', 'utc+01:00', 'utc+02:00', 'utc+03:00', 'utc+04:00', 'utc+05:00', 'utc+06:00', 'utc+07:00', 'utc+08:00', 'utc+09:00', 'utc+10:00', 'utc+11:00', 'utc+12:00', 'utc+13:00', 'utc+14:00', 'utc-01:00', 'utc-02:00', 'utc-03:00', 'utc-04:00', 'utc-05:00', 'utc-06:00', 'utc-07:00', 'utc-08:00', 'utc-09:00', 'utc-10:00', 'utc-11:00', 'utc-12:00']
frequency : 3 valeurs : ['1_hourly', '3_hourly', '6_hourly']
area : {'maxItems': 4, 'minItems': 4, 'type': 'array', 'default': [90, -180, -90, 180], 'items': {'type': 'number'}}
```

## 1 bis. Z500 quotidien, janvier 2020, 30-85° N, 60° O-60° E, 2,5°

```
soumission → 201
{"processID":"derived-era5-pressure-levels-daily-statistics","type":"process","jobID":"a08e7e8e-258b-4233-8ecc-8804fc6bcfec","status":"accepted","created":"2026-10-31T21:20:31.745741","updated":"2026-10-31T21:20:31.745741","links":[{"href":"https://cds.climate.copernicus.eu/api/retrieve/v1/processes/derived-era5-pressure-levels-daily-statistics/execution","rel":"self"},{"href":"https://cds.climate.copernicus.eu/api/retrieve/v1/jobs/a08e7e8e-258b-4233-8ecc-8804fc6bcfec","rel":"monitor","type":"ap
état après 336 s : successful
dimensions : valid_time=31, pressure_level=1, latitude=23, longitude=49
  z ('valid_time', 'pressure_level', 'latitude', 'longitude') (31, 1, 23, 49) m**2 s**-2 Geopotential
    min 4.485e+04, moyenne 5.229e+04, max 5.827e+04
  number () () 1 ensemble member numerical id
  pressure_level ('pressure_level',) (1,) hPa pressure
    [np.float64(500.0)]
  latitude ('latitude',) (23,) degrees_north latitude
    [np.float64(85.0), np.float64(82.5), np.float64(80.0), np.float64(77.5), np.float64(75.0), np.float64(72.5), np.float64(70.0), np.float64(67.5), np.float64(65.0), np.float64(62.5), np.float64(60.0), np.float64(57.5), np.float64(55.0), np.float64(52.5), np.float64(50.0), np.float64(47.5), np.float64(45.0), np.float64(42.5), np.float64(40.0), np.float64(37.5), np.float64(35.0), np.float64(32.5), np.float64(30.0)]
  longitude ('longitude',) (49,) degrees_east longitude
    [np.float64(-60.0), np.float64(-57.5), np.float64(-55.0), np.float64(-52.5), np.float64(-50.0), np.float64(-47.5), np.float64(-45.0), np.float64(-42.5), np.float64(-40.0), np.float64(-37.5), np.float64(-35.0), np.float64(-32.5), np.float64(-30.0), np.float64(-27.5), np.float64(-25.0), np.float64(-22.5), np.float64(-20.0), np.float64(-17.5), np.float64(-15.0), np.float64(-12.5), np.float64(-10.0), np.float64(-7.5), np.float64(-5.0), np.float64(-2.5), np.float64(0.0), np.float64(2.5), np.float
  valid_time ('valid_time',) (31,) days since 2020-01-01 00:00:00 time
    [np.float64(0.0), np.float64(1.0), np.float64(2.0), np.float64(3.0), np.float64(4.0), np.float64(5.0), np.float64(6.0), np.float64(7.0), np.float64(8.0), np.float64(9.0), np.float64(10.0), np.float64(11.0), np.float64(12.0), np.float64(13.0), np.float64(14.0), np.float64(15.0), np.float64(16.0), np.float64(17.0), np.float64(18.0), np.float64(19.0), np.float64(20.0), np.float64(21.0), np.float64(22.0), np.float64(23.0), np.float64(24.0), np.float64(25.0), np.float64(26.0), np.float64(27.0), n
```

## 2. ERA5 mensuel, niveaux uniques : variables convection et foudre

```
→ 200
product_type : 4 valeurs : ['monthly_averaged_ensemble_members', 'monthly_averaged_ensemble_members_by_hour_of_day', 'monthly_averaged_reanalysis', 'monthly_averaged_reanalysis_by_hour_of_day']
variable : 1 valeurs : ['convective_available_potential_energy']
year : 87 valeurs : ['1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949', '1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979']
month : 12 valeurs : ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
time : 24 valeurs : ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
area : {'maxItems': 4, 'minItems': 4, 'type': 'array', 'default': [90, -180, -90, 180], 'items': {'type': 'number'}}
data_format : 2 valeurs : ['grib', 'netcdf']
download_format : 2 valeurs : ['zip', 'unarchived']
```

## 2 bis. Densité d'éclairs et CAPE, juillet 2022, Gironde

```
soumission → 201
{"processID":"reanalysis-era5-single-levels-monthly-means","type":"process","jobID":"953881e7-5376-4958-b1ad-66d0f9e96ace","status":"accepted","created":"2026-10-31T21:26:11.988283","updated":"2026-10-31T21:26:11.988283","links":[{"href":"https://cds.climate.copernicus.eu/api/retrieve/v1/processes/reanalysis-era5-single-levels-monthly-means/execution","rel":"self"},{"href":"https://cds.climate.copernicus.eu/api/retrieve/v1/jobs/953881e7-5376-4958-b1ad-66d0f9e96ace","rel":"monitor","type":"applic
état après 825 s : failed
```
