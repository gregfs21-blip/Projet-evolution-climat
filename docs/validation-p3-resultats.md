# Validation P3 — résultats automatiques

Fichier généré par `python -m etl.validation.p3` à chaque exécution de l'ETL. Ne pas éditer à la main. Critères : `docs/phases.md` (P3).

**Au moins un critère comptant pour la clôture n'est pas satisfait.**

| Critère | Résultat | Mesure |
|---|---|---|
| H1 exhaustivité | ✅ conforme | 7 indicateurs sur 7 |
| H2 complétude | ℹ️ information | Appliquée par le code : mois ETCCDI et années de 12 mois (stations), années complètes (ERA5, altimétrie). |
| H3 brut ≠ homogénéisé | ✅ conforme | Les mesures de station ne portent aucune tendance publiée ; elles servent au seul contrôle H5. |
| H4 validation externe (R8, SST du golfe) | ✅ conforme | attendu [+0,21 ; +0,31] °C/déc. sur 1982-2014 ; mesuré : 0.2184 |
| H5 contrôle croisé (pression) | ✅ conforme | Bordeaux-Mérignac : 1971-2025 : écart moyen -0.35, pente +0.024/déc. (p = 0.419) : conforme ; Cazaux : 1950-1990 : écart moyen -0.77, pente +0.051/déc. (p = 0.439) : conforme |
| H5 contrôle croisé (humidite) | ❌ non conforme | Bordeaux-Mérignac : 1981-2025 : écart moyen -0.81, pente +0.637/déc. (p = 0.005) : NON conforme ; Cazaux : 15 années communes seulement |
| H6 cohérence entre stations | ✅ conforme | pression : même comportement ; humidite : même comportement |
| H7 plausibilité | ✅ conforme | Bornes contrôlées à la construction (un dépassement empêche la publication). |
| Vent : ERA5 et mesure (information) | ℹ️ information | corrélation interannuelle des jours de vent fort, ERA5 contre rafales mesurées à Mérignac (≥ 16 m/s, brutes) : r = 0.58 sur 75 ans |
| H8 technique | ℹ️ information | Tests, CI et contrat vérifiés par les workflows. |
