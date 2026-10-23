# Sources de données

| Source | Usage | Accès | Licence | Phase |
|---|---|---|---|---|
| Météo-France — Longues Séries Homogénéisées (LSH) | TN, TX (P1, P2a) ; RR : 9 séries de Gironde homogénéisées jusqu'en 2017 ; IN : Mérignac seul, jusqu'en 2014 (P2b) | data.gouv.fr | Licence Ouverte 2.0 | P1, P2 |
| Météo-France — données climatologiques de base quotidiennes (jeu `6569b51ae64326786e4e8e1a`) | P2a : extrêmes (jours chauds, nuits tropicales, gel), corrigés mois par mois par les LSH — non homogénéisées à l'origine | data.gouv.fr (API, fichiers par département) | Licence Ouverte 2.0 | P2a |
| ERA5 via Open-Meteo (archive, `models=era5`) | P1 : recoupement des tendances de température (C4bis). P3 : vent, humidité, pression | API sans clé | CC BY 4.0 (Copernicus), Open-Meteo non commercial | P1, P3 |
| PSMSL | Niveau marin aux marégraphes | téléchargement | libre, citation requise | P3 |
| NOAA GML | CO₂, CH₄, N₂O | téléchargement | domaine public | P6 |
| HadCRUT5, GISTEMP, Berkeley Earth | Température globale (croisement) | téléchargement | variable selon source | P6 |
| NASA CERES | Déséquilibre énergétique | compte Earthdata | domaine public | P6 |
| Copernicus CDS (ERA5 niveaux de pression) | Jet stream, Z500 | compte + clé | CC BY 4.0 | P7 |

Les licences exactes sont reportées dans chaque JSON publié (`provenance.license`).
