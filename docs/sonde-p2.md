# Sonde P2 — inventaire des données (généré)

Généré par `python -m etl.probe.p2` le 23/10/2026 14:57 UTC. Aucun résultat climatique n'est calculé ici :
la sonde recense ce qui existe pour fixer les critères de P2 **avant** tout calcul.

## 1. LSH — autres paramètres que TN/TX

Archives trouvées (listage du dépôt) : SH_IN_metropole.zip, SH_RR_Outremer.zip, SH_RR_metropole.zip, SH_TN_Outremer.zip, SH_TN_metropole.zip, SH_TX_Outremer.zip, SH_TX_metropole.zip.

### IN — Gironde (1 séries)

| Poste | Nom | Période homogénéisée | Premier | Dernier | Mois | Part homogénéisée | AMD | Ruptures |
|---|---|---|---|---|---|---|---|---|
| 33281001 | Bordeaux-Mérignac | 1931-2014 | 1931-01 | 2014-12 | 1008 | 100% | 0.06 | 2 |

Indications d'unité relevées dans les en-têtes : DONNEES MENSUELLES HOMOGENEISEES de IN : Cumul mensuel des durées d'insolation (en heures 

### RR — Gironde (9 séries)

| Poste | Nom | Période homogénéisée | Premier | Dernier | Mois | Part homogénéisée | AMD | Ruptures |
|---|---|---|---|---|---|---|---|---|
| 33063001 | Bordeaux-Paulin | 1953-2017 | 1953-01 | 2024-12 | 864 | 90% | 0.08 | 0 |
| 33203001 | Hourtin | 1954-2017 | 1954-01 | 2021-12 | 816 | 94% | 0.09 | 1 |
| 33484001 | St-Symphorien | 1950-2017 | 1950-01 | 2024-12 | 900 | 91% | 0.09 | 3 |
| 33042001 | Belin-Beliet | 1950-2017 | 1950-01 | 2024-12 | 900 | 91% | 0.09 | 2 |
| 33095001 | Captieux | 1950-2017 | 1950-01 | 2024-12 | 900 | 91% | 0.09 | 1 |
| 33214002 | Lacanau | 1950-2017 | 1950-01 | 2024-12 | 900 | 91% | 0.08 | 0 |
| 33236002 | Cap-Ferret | 1950-2017 | 1950-01 | 2024-12 | 900 | 91% | 0.09 | 1 |
| 33504001 | Sauternes | 1950-2017 | 1950-01 | 2024-12 | 900 | 91% | 0.08 | 1 |
| 33529001 | Cazaux | 1950-2017 | 1950-01 | 2024-12 | 900 | 91% | 0.09 | 2 |

Indications d'unité relevées dans les en-têtes : DONNEES MENSUELLES HOMOGENEISEES de RR : Cumul mensuel des hauteurs de précipitation (en m

## 2. Données quotidiennes — département 33

624 ressources dans le jeu ; 6 pour le département.

| Fichier | Taille | Modifié | Variables lues | Remarque |
|---|---|---|---|---|
| QUOT_departement_33_periode_avant-1949_RR-T-Vent | 4.0 Mo | 2026-07-08 | TN, TX, RR |  |
| QUOT_departement_33_periode_avant-1949_autres-parametres | 0.1 Mo | 2026-07-08 | INST |  |
| QUOT_departement_33_periode_1950-2024_RR-T-Vent | 16.3 Mo | 2026-10-02 | TN, TX, RR |  |
| QUOT_departement_33_periode_1950-2024_autres-parametres | 7.6 Mo | 2026-10-02 | INST |  |
| QUOT_departement_33_periode_2025-2026_RR-T-Vent | 0.4 Mo | 2026-10-23 | TN, TX, RR |  |
| QUOT_departement_33_periode_2025-2026_autres-parametres | 0.2 Mo | 2026-10-23 | INST |  |

### 2a. Postes LSH de P1 : années complètes (≥ 90% des jours renseignés)

| Poste | Nom | TN | TX | RR | Insolation (INST) |
|---|---|---|---|---|---|
| 33063001 | Bordeaux-Paulin | 1953-2025 | 1953-2025 | 1879-1880, 1895-1910, 1921-1944, 1948-2025 | — |
| 33214002 | Lacanau | 1967-1997, 1999-2001, 2003-2017, 2019-2025 | 1967-1997, 1999-2001, 2003-2017, 2019-2025 | 1882-1910, 1921-1944, 1947-1960, 1962-1972, 1974-1977, 1980-1987, 1989-1997, 1999-2001, 2003-2017, 2019-2025 | — |
| 33236002 | Cap-Ferret | 1921-1937, 1949-2025 | 1921-1937, 1949-2025 | 1921-1937, 1947-1948, 1950-2025 | 1957-2017 |
| 33281001 | Bordeaux-Mérignac | 1927-1939, 1946-2025 | 1921-1922, 1924-1939, 1946-2025 | 1921-1922, 1924-1939, 1946-2025 | 1930-1939, 1949-2025 |
| 33504001 | Sauternes | 1897-2025 | 1897-2025 | 1897-2025 | — |
| 33529001 | Cazaux | 1922, 1924-1939, 1949-2025 | 1922, 1924, 1926-1939, 1949-2025 | 1924-1939, 1949-2025 | 1955-2013, 2015-2017 |
| 33550001 | Villenave-d'Ornon | 1924-1942, 1944-2025 | 1924-1942, 1944-2025 | 1924-2025 | — |

### 2b. Codes qualité aux postes LSH (toutes années, part des valeurs)

| Poste | Variable | Répartition des codes |
|---|---|---|
| Bordeaux-Paulin | TN | 1 : 91.6%, 9 : 8.4% |
| Bordeaux-Paulin | TX | 1 : 91.5%, 9 : 8.5%, 0 : 0.0% |
| Bordeaux-Paulin | RR | 1 : 98.4%, 9 : 1.6% |
| Lacanau | TN | 1 : 100.0% |
| Lacanau | TX | 1 : 100.0%, 0 : 0.0% |
| Lacanau | RR | 1 : 98.5%, 9 : 1.5% |
| Cap-Ferret | TN | 1 : 81.6%, 9 : 18.4% |
| Cap-Ferret | TX | 1 : 81.6%, 9 : 18.4% |
| Cap-Ferret | RR | 1 : 98.5%, 9 : 1.5% |
| Cap-Ferret | INST | 1 : 99.9%, 9 : 0.1% |
| Bordeaux-Mérignac | TN | 1 : 97.9%, 9 : 2.1%, 0 : 0.0% |
| Bordeaux-Mérignac | TX | 1 : 97.9%, 9 : 2.1%, 0 : 0.0% |
| Bordeaux-Mérignac | RR | 1 : 100.0% |
| Bordeaux-Mérignac | INST | 1 : 91.1%, 9 : 8.9%, 0 : 0.0% |
| Sauternes | TN | 1 : 100.0%, 9 : 0.0% |
| Sauternes | TX | 1 : 99.9%, 9 : 0.1% |
| Sauternes | RR | 1 : 95.0%, 9 : 5.0%, 0 : 0.0% |
| Cazaux | TN | 1 : 100.0%, 0 : 0.0% |
| Cazaux | TX | 1 : 100.0%, 0 : 0.0% |
| Cazaux | RR | 1 : 100.0%, 0 : 0.0% |
| Cazaux | INST | 1 : 100.0% |
| Villenave-d'Ornon | TN | 1 : 66.1%, 9 : 33.9% |
| Villenave-d'Ornon | TX | 1 : 66.1%, 9 : 33.9% |
| Villenave-d'Ornon | RR | 1 : 65.8%, 9 : 34.2% |

### 2c. Tous les postes du département avec au moins 50 années complètes en TX ou en RR

| Poste | Nom | Alt. | Années TX | Années TN | Années RR | Années INST | Plage TX |
|---|---|---|---|---|---|---|---|
| 33504001 | Sauternes | 65 | 129 | 129 | 129 | 0 | 1897-2025 |
| 33550001 | Villenave D'Ornon-Inrae | 25 | 101 | 101 | 102 | 0 | 1924-2025 |
| 33281001 | Bordeaux-Merignac | 47 | 98 | 93 | 98 | 87 | 1921-2025 |
| 33236002 | Cap-Ferret | 8 | 94 | 94 | 95 | 61 | 1921-2025 |
| 33529001 | Cazaux | 23 | 93 | 94 | 93 | 62 | 1922-2025 |
| 33167001 | Bordeaux_Observatoire | 74 | 75 | 75 | 74 | 0 | 1880-1955 |
| 33063001 | Bordeaux-Paulin | 10 | 73 | 73 | 120 | 0 | 1953-2025 |
| 33314005 | Pauillac | 26 | 64 | 64 | 64 | 21 | 1962-2025 |
| 33522001 | Talence | 15 | 60 | 61 | 65 | 0 | 1959-2020 |
| 33214002 | Lacanau | 16 | 56 | 56 | 124 | 0 | 1967-2025 |
| 33484002 | St-Symphorienj | 75 | 56 | 55 | 49 | 0 | 1955-2010 |
| 33095001 | Captieux | 96 | 52 | 49 | 132 | 0 | 1974-2025 |
| 33544001 | Le Verdon-Sur-M | 6 | 51 | 51 | 50 | 0 | 1959-2011 |
| 33138001 | Coutras | 21 | 50 | 50 | 51 | 0 | 1967-2017 |
| 33076001 | Budos | 24 | 48 | 48 | 117 | 0 | 1959-2006 |
| 33009001 | Arcachon | 4 | 47 | 47 | 51 | 1 | 1953-2000 |
| 33540001 | Vendays-Montalive | 6 | 42 | 42 | 53 | 0 | 1984-2025 |
| 33494001 | Salaunes | 50 | 40 | 39 | 63 | 0 | 1984-2025 |
| 33506001 | Sauveterre-De-G | 75 | 37 | 37 | 113 | 0 | 1978-2019 |
| 33242001 | Les Leves Thoum | 80 | 36 | 36 | 50 | 0 | 1984-2019 |
| 33541001 | Vensac David | 8 | 31 | 31 | 56 | 0 | 1984-2014 |
| 33240001 | Lesparre Medoc | 14 | 25 | 25 | 59 | 0 | 1985-2009 |
| 33011001 | Ares | 2 | 23 | 23 | 79 | 0 | 1883-1910 |
| 33417001 | Sainte-Helene Ecole | 43 | 23 | 22 | 58 | 0 | 1883-1910 |
| 33009004 | Arcachon Agglomeration - Cmd | 4 | 23 | 23 | 57 | 0 | 1888-1910 |
| 33473001 | St-Savin | 90 | 20 | 20 | 63 | 0 | 1994-2013 |
| 33042001 | Belin-Beliet | 36 | 17 | 17 | 139 | 0 | 1994-2025 |
| 33203001 | Hourtin | 17 | 16 | 16 | 62 | 0 | 2006-2021 |
| 33484001 | St-Symphorien | 54 | 4 | 4 | 75 | 0 | 2022-2025 |
| 33195001 | Grignols | 146 | 4 | 4 | 53 | 0 | 2022-2025 |
| 33122001 | Cestas Hermitage De Pierroton | 59 | 2 | 2 | 69 | 0 | 1954-1955 |
| 33203002 | Hourtin Phare | 17 | 0 | 0 | 65 | 0 | — |
| 33077001 | Cabanac Et Vill | 45 | 0 | 0 | 64 | 0 | — |
| 33114001 | Cavignac Agglomeration | 76 | 0 | 0 | 63 | 0 | — |
| 33544002 | Le Verdon-Sur-Mer-Cordouan | 58 | 0 | 0 | 63 | 0 | — |
| 33051001 | Biganos | 13 | 0 | 0 | 58 | 0 | — |
| 33373001 | Saint-Antoine-Sur-L'Isle Bourg | 20 | 0 | 0 | 56 | 0 | — |
| 33198001 | Guitres | 20 | 0 | 0 | 53 | 0 | — |
| 33366001 | Saint-Andre-De-Cubzac | 28 | 0 | 0 | 51 | 0 | — |
| 33529004 | La Teste-De-Buch-La Salie | 4 | 0 | 0 | 51 | 0 | — |
| 33424001 | St Laurent Medoc | 8 | 0 | 0 | 50 | 0 | — |

Postes distincts rencontrés dans les fichiers lus : 200.
