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


# ---------------------------------------------------------------- quotidien (P2a)

DAILY_BIAS = {"33000001": (1988, 0.8)}   # station A : valeurs brutes trop chaudes de 0,8 °C avant 1988 (rupture 1987-12)
DAILY_GAP = ("33000003", 1970, 3, 4)      # station C : 4 jours absents en mars 1970 → année manquante (E2)
DAILY_Q9 = ("33000002", 2000)             # station B : code qualité 9 sur toute l'année 2000


def make_daily_dir(raw_dir: Path) -> None:
    """Fichier quotidien synthétique du département 33, cohérent avec les LSH de make_raw_dir.

    Chaque jour = valeur mensuelle LSH + biais brut éventuel + motif journalier de moyenne nulle sur le mois :
    la correction B doit donc retrouver exactement la LSH, et le biais de la station A doit disparaître.
    """
    import calendar
    import gzip
    import json

    from etl.sources import meteofrance_lsh as lsh

    monthly = {var: {s.station.id: s for s in lsh.load_department(var, "33", raw_dir, download=False)} for var in ("TN", "TX")}
    rng = np.random.default_rng(42)
    lines = ["NUM_POSTE;NOM_USUEL;LAT;LON;ALTI;AAAAMMJJ;RR;QRR;TN;QTN;TX;QTX"]
    for poste, name, first, *_ in STATIONS:
        for y in range(first, LAST + 1):
            for m in range(1, 13):
                n = calendar.monthrange(y, m)[1]
                shape = 5 * np.sin(np.arange(n) / n * 2 * np.pi * 2) + rng.normal(0, 2, n)
                shape -= shape.mean()
                vals = {}
                for var in ("TN", "TX"):
                    s = monthly[var].get(poste)
                    if s is None or (y, m) not in s.values:
                        vals[var] = [""] * n
                        continue
                    bias = DAILY_BIAS.get(poste, (0, 0.0))
                    b = bias[1] if y < bias[0] else 0.0
                    vals[var] = [f"{s.values[(y, m)] + b + v:.1f}" for v in shape]
                for d in range(n):
                    if (poste, y, m) == DAILY_GAP[:3] and d < DAILY_GAP[3]:
                        continue
                    q = "9" if (poste, y) == DAILY_Q9 else "1"
                    lines.append(f"{poste};{name};44.8;-0.6;20;{y}{m:02d}{d + 1:02d};0.0;1;{vals['TN'][d]};{q};{vals['TX'][d]};{q}")
    qdir = raw_dir / "quot"
    qdir.mkdir(parents=True, exist_ok=True)
    (qdir / "Q_33_test_RR-T-Vent.csv.gz").write_bytes(gzip.compress("\n".join(lines).encode("utf-8")))
    (qdir / "index-33.json").write_text(json.dumps([{"title": "QUOT_departement_33_periode_test_RR-T-Vent",
                                                     "url": "https://example.invalid/Q_33_test_RR-T-Vent.csv.gz"}]))
    os.environ["QUOT_OFFLINE"] = "1"
