# Validation P6 — analyse (rédigée à la main)

Résultats automatiques : `docs/validation-p6-resultats.md`. Critères : `docs/phases.md` (P6). Tous les critères
comptant pour la clôture sont satisfaits, sans écart accepté.

- **Niveau marin mondial** (NOAA STAR, 1993-2024) : + 3,1 mm/an ; + 3,5 mm/an sur 2006-2018, dans la fourchette du
  GIEC [3,2 ; 4,2] malgré l'absence de correction isostatique. Confiance « élevée ».
- **pH à ALOHA** (1989-2021) : − 0,018 par décennie ; − 0,0019 par an sur 1989-2007, la valeur publiée par Dore et al.
  2009. Confiance « élevée ».
- **Trou d'ozone** : + 16,6 millions de km² par décennie sur 1979-1994 ; − 1,35 depuis 2000, non significatif : la
  résorption attendue n'est pas encore établie statistiquement.
- **Puits de carbone** : océan + 0,35 et terres + 0,29 GtC/an par décennie depuis 1959 ; la part des émissions
  absorbée ne change pas significativement (+ 0,8 point par décennie) : les puits suivent les émissions sans en
  absorber une part croissante.
- **Troposphère** : UAH + 0,15, RSS + 0,23 °C par décennie (1979-2025) ; les deux suivent la surface (r = 0,94 et
  0,98, K5) mais divergent nettement sur la pente : incertitude structurelle des satellites.
- **Déséquilibre énergétique** (CERES, 2001-2025) : + 0,46 W/m² par décennie, significatif ; 1,84 W/m² en 2023.
  Pente 2006-2018 + 0,44, cohérente avec Loeb et al. 2021 (mêmes données : contrôle de lecture seulement).
- **Aérosols** (CAMS, 2003-2025) : − 0,003 par décennie (environ − 2 % par décennie), significatif ; réanalyse,
  série courte.

Décisions après calcul : aucune. Correctif d'implémentation tracé : en-tête « Net » du fichier des émissions du
changement d'usage des sols, constaté au premier calcul (le contrôle d'en-tête a bloqué, comme prévu).
