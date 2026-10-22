"""Données LSH synthétiques pour les tests : aucun accès réseau, résultats connus d'avance."""

from __future__ import annotations

import os
import zipfile
from pathlib import Path

import numpy as np

# poste, nom, première année, TN ?, TX ?, ruptures MF
STATIONS = [
    ("33000001", "STATION-A", 1953, True, True, "198712"),
    ("33000002", "STATION-B", 1953, True, True, "196612 199412"),
    ("33000003", "STATION-C", 1953, True, True, ""),
    ("33000004", "STATION-D", 1962, True, True, ""),   # série courte, comme Bordeaux-Paulin TX
]
SLOPE_PER_YEAR = 0.03       # tendance imposée : +0,30 °C/décennie
LAST_HOM, LAST = 2022, 2024


def lsh_text(var: str, poste: str, name: str, first: int, breaks: str, seed: int) -> str:
    rng = np.random.default_rng(seed)
    base = 8.0 if var == "TN" else 18.0
    lines = [
        f"# DONNEES MENSUELLES HOMOGENEISEES de {var} : test",
        f"# NUM_POSTE= {poste}",
        f"# NOM_USUEL= {name}",
        "# LATITUDE (°) = 44.8",
        "# LONGITUDE(°)= -0.6",
        "# ALTITUDE (m) = 20",
        "# ETAT DU POSTE (fermé avec date de fermeture AAAA-MM-JJ ou ouvert à la date de production du fichier le 13/03/2025) = ouvert",
        f"# NUM_SERIE= M{var}2{poste}",
        "# Amplitude minimale détectable de la série = 0.15",
        f"# Période homogénéisée : {first}01 {LAST_HOM}12",
        f"# Date(s) de rupture(s) d'homogénéité : {breaks}",
        "YYYYMM;VALEUR;Q_HOM",
    ]
    for y in range(first, LAST + 1):
        for m in range(1, 13):
            seasonal = 6 * np.sin((m - 4) / 12 * 2 * np.pi)
            v = base + seasonal + SLOPE_PER_YEAR * (y - 1953) + rng.normal(0, 0.3)
            lines.append(f"{y}{m:02d};{v:.1f};{1 if y <= LAST_HOM else 0}")
    return "\n".join(lines) + "\n"


def make_raw_dir(root: Path) -> Path:
    """Construit data/raw/lsh/SH_{TN,TX}_metropole.zip et active le mode hors ligne."""
    lsh_dir = root / "raw" / "lsh"
    lsh_dir.mkdir(parents=True)
    for var in ("TN", "TX"):
        with zipfile.ZipFile(lsh_dir / f"SH_{var}_metropole.zip", "w") as z:
            for i, (poste, name, first, tn, tx, breaks) in enumerate(STATIONS):
                if (var == "TN" and tn) or (var == "TX" and tx):
                    z.writestr(f"SH_M{var}2{poste}.csv", lsh_text(var, poste, name, first, breaks, seed=i * 10 + len(var)))
            z.writestr("SH_MTN201089001.csv", lsh_text(var, "01089001", "HORS-GIRONDE", 1953, "", 99))  # autre département
    os.environ["LSH_OFFLINE"] = "1"
    return root / "raw"
