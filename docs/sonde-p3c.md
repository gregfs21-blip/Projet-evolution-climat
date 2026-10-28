# Sonde P3 — atmosphère et littoral Gironde (généré)

Généré par `python -m etl.probe.p3` le 27/10/2026 21:10 UTC. Aucun indicateur calculé.

## 6. Altimétrie satellite (CDS satellite-sea-level-global)

### mensuel, janvier 2020, avec zone

`…/processes/satellite-sea-level-global/execution` → **201**

```
{"processID":"satellite-sea-level-global","type":"process","jobID":"ad06a9d5-ea6d-46ff-a823-ab51fe8627d6","status":"accepted","created":"2026-10-27T21:10:11.327102","updated":"2026-10-27T21:10:11.327102","links":[{"href":"https://cds.climate.copernicus.eu/api/retrieve/v1/processes/satellite-sea-level-global/execution","rel":"self"},{"href":"https://cds.climate.copernicus.eu/api/retrieve/v1/jobs/ad
état après 32 s : successful
résultat : 55904 octets, 54ce62ea219bd76db4855cd9e1dc4f24.zip
archive : dt_global_twosat_phy_l4_202001_vDT2024-M01.area-subset.46.5.-1.0.44.0.-3.0.nc (55642 o)
dimensions : time=1, nv=2, latitude=10, longitude=8
  crs () ()  
  climatology_bnds ('time', 'nv') (1, 2)  
  lat_bnds ('latitude', 'nv') (10, 2)  
  lon_bnds ('longitude', 'nv') (8, 2)  
  sla ('time', 'latitude', 'longitude') (1, 10, 8) m Averaged Sea Level Anomalies 2020/01
  eke ('time', 'latitude', 'longitude') (1, 10, 8) cm2/s2 Averaged Eddy Kinetic Energy 2020/01
  time ('time',) (1,) days since 1950-01-01 00:00:00 Time
  latitude ('latitude',) (10,) degrees_north Latitude
  longitude ('longitude',) (8,) degrees_east Longitude
  nv ('nv',) (2,) 1 Number of cell vertices
```
