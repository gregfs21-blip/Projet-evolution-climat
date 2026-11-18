# Validation P10.1 — résultats automatiques

Fichier généré par `python -m etl.validation.p10` à chaque exécution de l'ETL. Ne pas éditer à la main. Critères : `docs/phases.md` (P10).

**Tous les critères comptant pour la clôture sont satisfaits.**

| Critère | Résultat | Mesure |
|---|---|---|
| O1 exhaustivité | ✅ conforme | 3 jeux sur 3 : HadCRUT5 1871-2025, GISTEMP v4 1880-2025, Berkeley Earth 1871-2024 |
| O2 données d'entrée | ✅ conforme | écart maximal anthropique + volcanique + solaire − total : 0,0000 W/m² (seuil 0,01) ; aucun mois ENSO manquant sur les périodes ; corrélation indice ENSO / ONI 1951-2025 : r = 0,991 (seuil 0,95) |
| O3 détection | ✅ conforme | HadCRUT5 ✓ βₐ = 0,466 °C par W/m², p < 0,001 | GISTEMP v4 ✓ βₐ = 0,447 °C par W/m², p < 0,001 | Berkeley Earth ✓ βₐ = 0,485 °C par W/m², p < 0,001 |
| O4 attribution | ✅ conforme | HadCRUT5 ✓ 2010-2019 : 1,06 °C [0,95 ; 1,17], référence [0,9 ; 1,3] ; 2016-2025 : 1,25 °C [1,12 ; 1,38], référence [1,0 ; 1,5] | GISTEMP v4 ✓ 2010-2019 : 1,02 °C [0,91 ; 1,12], référence [0,9 ; 1,3] ; 2016-2025 : 1,20 °C [1,07 ; 1,32], référence [1,0 ; 1,5] | Berkeley Earth ✓ 2010-2019 : 1,11 °C [0,99 ; 1,22], référence [0,9 ; 1,3] ; 2016-2025 : 1,30 °C [1,16 ; 1,44], référence [1,0 ; 1,5] |
| O5 part naturelle | ✅ conforme | HadCRUT5 ✓ 2010-2019 : +0,035 °C ; 2016-2025 : +0,033 °C | GISTEMP v4 ✓ 2010-2019 : +0,035 °C ; 2016-2025 : +0,033 °C | Berkeley Earth ✓ 2010-2019 : +0,036 °C ; 2016-2025 : +0,032 °C |
| O6 plausibilité physique | ✅ conforme | HadCRUT5 ✓ réponse transitoire 1,83 °C ; βₑ = 0,117 (p < 0,001) ; βᵥ = 0,136 (p < 0,001) ; βₛ = 0,168 (p = 0,496, sans exigence) | GISTEMP v4 ✓ réponse transitoire 1,76 °C ; βₑ = 0,110 (p < 0,001) ; βᵥ = 0,133 (p < 0,001) ; βₛ = 0,186 (p = 0,433, sans exigence) | Berkeley Earth ✓ réponse transitoire 1,91 °C ; βₑ = 0,119 (p < 0,001) ; βᵥ = 0,138 (p < 0,001) ; βₛ = 0,116 (p = 0,658, sans exigence) |
| O7 résidus | ✅ conforme | HadCRUT5 ✓ tendance des résidus : p = 0,317 (Hamed-Rao) ; ρ = 0,71 | GISTEMP v4 ✓ tendance des résidus : p = 0,326 (Hamed-Rao) ; ρ = 0,70 | Berkeley Earth ✓ tendance des résidus : p = 0,177 (Hamed-Rao) ; ρ = 0,70 |
| O8 robustesse | ☑ écart accepté par Grég le 18/11/2026 (D-AI) : seule la variante « forçage anthropique à 5 % » sort de la fourchette, l'estimateur AR(1) y dégénère (docs/validation-p10.md) | HadCRUT5 ✗ réchauffement attribué 2016-2025 de 0,22 à 1,26 °C sur 12 variantes ; hors fourchette : Forçage anthropique à 5 % | GISTEMP v4 ✗ réchauffement attribué 2016-2025 de 0,09 à 1,22 °C sur 12 variantes ; hors fourchette : Forçage anthropique à 5 % | Berkeley Earth ✗ réchauffement attribué 2016-2025 de 0,09 à 1,32 °C sur 12 variantes ; hors fourchette : Forçage anthropique à 5 % |
| D-AH cohérence de la synthèse | ✅ conforme | analyses publiées : p10.1 ; la synthèse (limite-attribution, limite-projections) en tient compte |
| O9 technique | ℹ️ information | Tests, contrat et construction de l'onglet vérifiés par la CI (ci.yml), hors de ce module, comme pour les phases précédentes. |
| Confiance (règle D-AG) | ℹ️ information | moyenne — Détection établie (O3), mais critère non conforme, d'où la confiance « moyenne » (règle D-AG) : O8 (robustesse) : réchauffement attribué hors de [1,0 ; 1,5] °C pour HadCRUT5 « Forçage anthropique à 5 % » 0,22 °C, GISTEMP v4 « Forçage anthropique à 5 % » 0,09 °C, Berkeley Earth « Forçage anthropique à 5 % » 0,09 °C. Analyse de l'écart : docs/validation-p10.md. |
