# Validation P6 — résultats automatiques

Fichier généré par `python -m etl.validation.p6` à chaque exécution de l'ETL. Ne pas éditer à la main. Critères : `docs/phases.md` (P6).

**Tous les critères comptant pour la clôture sont satisfaits.**

| Critère | Résultat | Mesure |
|---|---|---|
| K1 exhaustivité | ✅ conforme | 8 indicateurs sur 8 |
| K2 complétude | ℹ️ information | Appliquée par les lecteurs : 12 mois (niveau marin, troposphère), au moins 6 campagnes par an (pH). |
| K3 produits publiés | ✅ conforme | Séries reprises sans modification, unités contrôlées ; aucune série brute de station. |
| K4 validation externe (R11, R12) | ✅ conforme | niveau-mer-monde : mesuré +3,5409 mm/an, attendu [+3,2000 ; +4,2000] ; ph-ocean-hot : mesuré -0,0019 pH/an, attendu [-0,0023 ; -0,0015] |
| K5 contrôle croisé surface / troposphère | ✅ conforme | HadCRUT5 / UAH : r = 0,940 sur 47 ans ; HadCRUT5 / RSS : r = 0,984 sur 47 ans ; seuil 0,8 |
| K6 cohérence UAH / RSS | ✅ conforme | UAH +0,148 ; RSS +0,229 °C/déc. (1979-2025) ; écart +0,081 |
| K7 plausibilité | ✅ conforme | Bornes contrôlées à la construction pour les 8 indicateurs publiés. |
| K8 technique | ℹ️ information | Tests, CI et contrat vérifiés par les workflows. |
