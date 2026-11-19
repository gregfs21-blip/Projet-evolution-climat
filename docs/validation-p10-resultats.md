# Validation P10 — résultats automatiques

Fichier généré par `python -m etl.validation.p10` à chaque exécution de l'ETL. Ne pas éditer à la main. Critères : `docs/phases.md` (P10).

**Au moins un critère comptant pour la clôture n'est pas satisfait.**

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
| D-AH cohérence de la synthèse | ❌ non conforme | analyses publiées que la synthèse ne prend pas en compte : p10.2 ; reformuler limite-attribution et limite-projections (etl/config/synthese.yaml), les faire relire (M6), puis compléter SYNTHESIS_COVERS |
| O9 technique | ℹ️ information | Tests, contrat et construction de l'onglet vérifiés par la CI (ci.yml), hors de ce module, comme pour les phases précédentes. |
| Confiance P10.1 (règle D-AG) | ℹ️ information | moyenne — Détection établie (O3), mais critère non conforme, d'où la confiance « moyenne » (règle D-AG) : O8 (robustesse) : réchauffement attribué hors de [1,0 ; 1,5] °C pour HadCRUT5 « Forçage anthropique à 5 % » 0,22 °C, GISTEMP v4 « Forçage anthropique à 5 % » 0,09 °C, Berkeley Earth « Forçage anthropique à 5 % » 0,09 °C. Analyse de l'écart : docs/validation-p10.md. |
| P10.2 X1 données | ✅ conforme | Bordeaux-Mérignac 1953-2025, 73 années, aucune manquante ; années brutes 2023, 2024, 2025 ; écart maximal |corrigé − brut| après la rupture de 2000 : 0,05 °C (seuil 0,1) |
| P10.2 X2 ajustement | ✅ conforme | ξ = −0,31 (bornes −0,5 et +0,2) ; Kolmogorov-Smirnov p = 0,73 (seuil 0,05) ; 0 tirage(s) bootstrap sans convergence sur 1000 |
| P10.2 X3 détection | ✅ conforme | α = 3,94 [2,39 ; 5,14] °C par °C ; rapport de vraisemblance p < 0,001 |
| P10.2 X4 plausibilité | ✅ conforme | intervalle de α [2,39 ; 5,14] contre la référence [2,5 ; 4,2] |
| P10.2 X5 robustesse | ✅ conforme | Covariable HadCRUT5 : α = 3,86, rapport de probabilité du record infini ✓ ; Années homogénéisées seules (1953-2022) : α = 3,64, rapport de probabilité du record infini ✓ ; Sans l'année 2025 : α = 3,73, rapport de probabilité du record infini ✓ ; Indice TX3x (moyenne de TX sur 3 jours) : α = 3,89, rapport de probabilité du record infini ✓ |
| P10.2 X6 cohérence régionale | ✅ conforme | Cap-Ferret 1953-2025 : α = 3,80 [2,39 ; 5,31] ✓ ; Cazaux 1953-2025 : α = 3,92 [2,64 ; 5,27] ✓ ; Villenave-d'Ornon 1953-2025 : α = 3,63 [1,98 ; 4,60] ✓ ; Bordeaux-Paulin 1962-2025 : α = 3,79 [2,06 ; 5,15] ✓ |
| P10.2 X7 technique | ℹ️ information | Tests (etl/tests/test_p10b.py), contrat et construction de l'onglet vérifiés par la CI. |
| Confiance P10.2 (règle D-AO) | ℹ️ information | elevee — Critères X1 à X6 conformes (règle D-AO). L'analyse relie les maxima au réchauffement mondial ; elle n'en attribue pas la cause. |
