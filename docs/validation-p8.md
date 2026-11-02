# Validation P8 — analyse

Résultats automatiques : `docs/validation-p8-resultats.md`. Relecture indépendante : `docs/relecture-p8.md`.
Critères M1-M7 validés par Grég le 02/11/2026, avant toute rédaction.

## Bilan

**Critères** : M1 à M7 conformes. Seul M7 reste « en attente » de la P7, comme le critère le permet.

**Affirmations** : 79 au total, dont :

| Type | Nombre |
|---|---|
| Signal | 31 |
| Absence de signal | 16 |
| Comparaison | 8 |
| Accélération | 2 |
| Information | 6 |
| Contexte externe | 4 |
| Lacune | 12 |

S'y ajoutent 5 lacunes tirées de la couverture.

## Ce que le calcul a apporté

**Accélération**
- **Niveau marin mondial** : 0,076 mm/an² sur 1993-2024 (p < 0,001). Sur 1993-2017, la valeur est de 0,067 mm/an², dans la fourchette [0,059 ; 0,109]. Ce chiffre reste sous les valeurs de Nerem et al. (0,084 corrigé, 0,097 brut). Son intervalle est large (0,006 à 0,128), parce que la série est annuelle et non corrigée.
- **Température mondiale** : pas d'accélération détectée au seuil de 5 % (HadCRUT5 p = 0,07 ; Berkeley p = 0,09). L'estimation centrale va dans ce sens, mais ne l'établit pas.
- **CO₂** : accélération significative.
- **Méthane** et **France** : pas d'accélération détectée.
- **Gironde** : terme quadratique significatif (p = 0,02). Le test ne distingue pas une accélération d'un réchauffement concentré après la rupture de 1988.

**Comparaisons sur 1959-2021**
- La Gironde (+0,33 °C par décennie) et la France (+0,34) se réchauffent plus vite que la moyenne mondiale (+0,18). Les intervalles sont disjoints.
- Le contraste entre terres et océan, selon les chiffres du GIEC, n'explique qu'une partie de cet écart (un rapport d'environ 1,5, contre 1,9 observé). L'étude ne peut pas trancher, faute d'une moyenne des seules terres.

**FWI**
- Dans ERA5, la décennie 1940-1949 dépasse 2016-2025.
- La hausse depuis 1976 est établie. Un record actuel ne l'est pas.

## Corrections tracées après calcul

- **Règle S3** : la phrase « un écart est attendu et ne dit rien de propre à la région » était fausse. Elle a été corrigée sur relecture (voir `phases.md`).
- **TM Gironde** : l'accélération est calculée sur 1953-2022, et non sur 1953-2024. Ce choix a été fait avant calcul : les années 2023-2024 ne sont pas homogénéisées.

## Reste à faire

- Ajouter la section exploratoire quand le relevé des blocages de la P7 sera complet.
