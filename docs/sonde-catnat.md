# Sonde « largeur d'abord », lot 2 (généré)

Généré par `python -m etl.probe.largeur2` le 25/10/2026 08:30 UTC. Aucun calcul : formats et couverture constatés.

## 6. Catastrophes naturelles : base GASPAR (data.gouv.fr)

### GASPAR (ministère), ressource CSV

`https://www.data.gouv.fr/api/1/datasets/r/d6fb9e18-b66b-499c-8284-46a3595579cc` → **200**

```
[8.1 Mo, début : b'PK\x03\x04']
archive : azi_gaspar_2026-10-05.csv (3.7 Mo), catnat_gaspar_2026-10-05.csv (41.5 Mo), ddrm_risq_gaspar_2026-10-05.csv (9.1 Mo), dicrim_gaspar_2026-10-05.csv (0.4 Mo), pprm_gaspar_2026-10-05.csv (0.3 Mo), pprn_gaspar_2026-10-05.csv (15.5 Mo), pprt_gaspar_2026-10-05.csv (0.9 Mo), tim_gaspar_2026-10-05.csv (0.7 Mo)
lu : catnat_gaspar_2026-10-05.csv
247141 lignes
id_gaspar;code_commune;libelle_commune;num_risque_jo;lib_risque_jo;date_debut;date_fin;date_signature_arrete;date_publication_jo;date_modification
INTE9900627A;33436;Saint-Magne;CMV;Chocs Mécaniques liés à l'action des Vagues;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
INTE9900627A;37100;Ã‰peignÃ©-les-Bois;MVT;Mouvement de Terrain;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
INTE9900627A;31247;Labarthe-RiviÃ¨re;MVT;Mouvement de Terrain;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
INTE9900627A;18187;PrÃ©veranges;MVT;Mouvement de Terrain;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
INTE1228647A;16384;Touvérac;SEC;Sécheresse;2011-04-01 02:00:00;2011-06-30 02:00:00;2012-07-11 02:00:00;2012-07-17 02:00:00;2022-05-24 02:00:00.000
INTE9900627A;59627;Villers-Sire-Nicole;MVT;Mouvement de Terrain;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
INTE9900627A;10054;Bourdenay;MVT;Mouvement de Terrain;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
lignes avec un code commune 33xxx : 7816
INTE9900627A;33436;Saint-Magne;CMV;Chocs Mécaniques liés à l'action des Vagues;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
IOME2308745A;33285;Mombrier;SEC;Sécheresse;2022-10-01 12:00:00;2022-12-31 12:00:00;2023-04-03 12:00:00;2023-05-03 12:00:00;2023-05-04 10:59:28.790
INTE9900627A;33242;Les LÃ¨ves-et-Thoumeyragues;MVT;Mouvement de Terrain;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
INTE9900627A;33398;Saint-ExupÃ©ry;ICB;Inondations et/ou Coulées de Boue;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
INTE9900627A;33372;Saint-Antoine-du-Queyret;CMV;Chocs Mécaniques liés à l'action des Vagues;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
IOME2308745A;33272;Marsas;SEC;Sécheresse;2022-10-01 12:00:00;2022-12-31 12:00:00;2023-04-03 12:00:00;2023-05-03 12:00:00;2023-05-04 10:59:28.790
INTE9900627A;33049;Beychac-et-Caillau;ICB;Inondations et/ou Coulées de Boue;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
INTE9900627A;33451;Saint-Michel-de-Fronsac;CMV;Chocs Mécaniques liés à l'action des Vagues;1999-12-25 12:00:00;1999-12-29 12:00:00;1999-12-29 12:00:00;1999-12-30 12:00:00;2022-05-24 11:17:06.954
IOCE0902322A;33406;Saint-GenÃ¨s-de-Castillon;ICB;Inondations et/ou Coulées de Boue;2009-01-24 12:00:00;2009-01-27 12:00:00;2009-01-28 12:00:00;2009-01-29 12:00:00;2022-05-24 11:39:20.861
IOCE0902322A;33187;Gironde-sur-Dropt;ICB;Inondations et/ou Coulées de Boue;2009-01-24 12:00:00;2009-01-27 12:00:00;2009-01-28 12:00:00;2009-01-29 12:00:00;2022-05-24 11:39:20.861
INTE9900488A;33114;Cavignac;ICB;Inondations et/ou Coulées de Boue;1999-07-29 02:00:00;1999-07-29 02:00:00;1999-11-29 01:00:00;1999-12-04 01:00:00;2022-05-23 02:00:00.000
BUDD8750068A;33119;Cenon;ICB;Inondations et/ou Coulées de Boue;1987-07-06 02:00:00;1987-07-06 02:00:00;1987-09-27 02:00:00;1987-10-09 01:00:00;2022-05-20 02:00:00.000
```

### Arrêtés CatNat par commune (TACCT, dérivé de GASPAR)

`https://www.data.gouv.fr/api/1/datasets/r/b3d02000-5f25-4967-a210-a4051dd620a1` → **200**

```
[52.6 Mo, début : b'7912']
260601 lignes
7912;04054;Châteauredon;200067437;Communauté d'agglomération Provence-Alpes-Agglomération;04;Alpes-de-Haute-Provence;93;;;;;Sécheresse;2017-07-01 00:00:00.000;2017-09-30 00:00:00.000;2018-06-27 00:00:00.000
7913;04054;Châteauredon;200067437;Communauté d'agglomération Provence-Alpes-Agglomération;04;Alpes-de-Haute-Provence;93;;;;;Sécheresse;2023-03-31 02:00:00.000;2023-06-29 02:00:00.000;2024-09-23 02:00:00.000
7914;04055;Chaudon-Norante;200068625;Communauté de communes Alpes-Provence-Verdon - Sources de Lumière;04;Alpes-de-Haute-Provence;93;;;;;Inondations;1996-01-11 00:00:00.000;1996-01-12 00:00:00.000;1996-06-17 00:00:00.000
7915;04055;Chaudon-Norante;200068625;Communauté de communes Alpes-Provence-Verdon - Sources de Lumière;04;Alpes-de-Haute-Provence;93;;;;;Inondations;2012-05-26 00:00:00.000;2012-05-26 00:00:00.000;2012-10-18 00:00:00.000
7916;04055;Chaudon-Norante;200068625;Communauté de communes Alpes-Provence-Verdon - Sources de Lumière;04;Alpes-de-Haute-Provence;93;;;;;Inondations;1994-11-04 00:00:00.000;1994-11-06 00:00:00.000;1994-11-21 00:00:00.000
7917;04057;Clamensane;200068765;Communauté de communes du Sisteronais-Buëch;04;Alpes-de-Haute-Provence;93;;;;;Inondations;1994-11-04 00:00:00.000;1994-11-06 00:00:00.000;1994-11-21 00:00:00.000
7918;04058;Claret;200067825;Communauté d'agglomération Gap-Tallard-Durance;04;Alpes-de-Haute-Provence;93;;;;;Inondations;2008-05-29 00:00:00.000;2008-05-31 00:00:00.000;2008-06-26 00:00:00.000
7919;04058;Claret;200067825;Communauté d'agglomération Gap-Tallard-Durance;04;Alpes-de-Haute-Provence;93;;;;;Inondations;2019-12-01 00:00:00.000;2019-12-02 00:00:00.000;2019-12-12 00:00:00.000
lignes avec un code commune 33xxx : 8217
89926;33075;Bruges;243300316;Bordeaux Métropole;33;Gironde;75;;;;;Sécheresse;2005-01-01 00:00:00.000;2005-03-31 00:00:00.000;2008-02-20 00:00:00.000
89630;33063;Bordeaux;243300316;Bordeaux Métropole;33;Gironde;75;;;;;Inondations;1983-06-24 00:00:00.000;1983-06-24 00:00:00.000;1983-10-05 00:00:00.000
89631;33063;Bordeaux;243300316;Bordeaux Métropole;33;Gironde;75;;;;;Inondations;1983-07-04 00:00:00.000;1983-07-04 00:00:00.000;1983-10-05 00:00:00.000
89632;33063;Bordeaux;243300316;Bordeaux Métropole;33;Gironde;75;;;;;Sécheresse;1996-02-07 00:00:00.000;1996-02-08 00:00:00.000;1996-04-03 00:00:00.000
89633;33063;Bordeaux;243300316;Bordeaux Métropole;33;Gironde;75;;;;;Sécheresse;2002-01-01 00:00:00.000;2002-12-31 00:00:00.000;2003-04-30 00:00:00.000
89634;33063;Bordeaux;243300316;Bordeaux Métropole;33;Gironde;75;;;;;Inondations;2018-05-26 00:00:00.000;2018-05-26 00:00:00.000;2018-10-04 00:00:00.000
89635;33063;Bordeaux;243300316;Bordeaux Métropole;33;Gironde;75;;;;;Sécheresse;2005-01-01 00:00:00.000;2005-03-31 00:00:00.000;2008-02-20 00:00:00.000
89636;33063;Bordeaux;243300316;Bordeaux Métropole;33;Gironde;75;;;;;Sécheresse;2005-01-01 00:00:00.000;2005-03-31 00:00:00.000;2008-02-20 00:00:00.000
96672;33545;Vertheuil;200069995;Communauté de communes Médoc Cœur de Presqu'île;33;Gironde;75;;;FR8000055;PNR Medoc;Sécheresse;2003-07-01 00:00:00.000;2003-09-30 00:00:00.000;2006-06-16 00:00:00.000
96673;33545;Vertheuil;200069995;Communauté de communes Médoc Cœur de Presqu'île;33;Gironde;75;;;FR8000055;PNR Medoc;Inondations;1999-12-25 00:00:00.000;1999-12-29 00:00:00.000;1999-12-29 00:00:00.000
96663;33545;Vertheuil;200069995;Communauté de communes Médoc Cœur de Presqu'île;33;Gironde;75;;;FR8000055;PNR Medoc;Cyclones / Tempêtes;1982-11-06 00:00:00.000;1982-11-10 00:00:00.000;1982-11-30 00:00:00.000
89658;33063;Bordeaux;243300316;Bordeaux Métropole;33;Gironde;75;;;;;Inondations;2011-08-02 00:00:00.000;2011-08-02 00:00:00.000;2011-11-28 00:00:00.000
```
