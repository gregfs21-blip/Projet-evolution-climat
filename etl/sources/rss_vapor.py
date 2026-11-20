"""Source : vapeur d'eau intégrée sur les océans, RSS V7 « merged vapor », cartes mensuelles à 1° (Remote Sensing Systems).

Accès constaté par la sonde du 20/11/2026 (docs/sonde-p10d.md) : fichier netCDF libre
« merged_vapor_1988-AAAA.nc » (environ 118 Mo) dans https://data.remss.com/vapor/monthly_1deg/ ; variable
`merged_vapor` (latitude 180, longitude 360, temps), kg/m², temps en années décimales (milieu du mois). Les mailles
continentales et englacées sont absentes.

Choix du cadrage P10.4 (D-AS, 20/11/2026) : masque **constant**, mailles de 60° S à 60° N valides tous les mois du
fichier ; moyenne mensuelle pondérée par l'aire (cos φ) sur ce masque. Le relevé (workflow « Copernicus ») écrit
data/sources/rss-vapor/tpw.csv et la part de la bande 60° S-60° N couverte par le masque (critère C1) dans meta.json.
L'ETL ne lit que ces fichiers.
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from etl.context import ROOT

OUT_DIR = ROOT / "data" / "sources" / "rss-vapor"
DIR_URL = "https://data.remss.com/vapor/monthly_1deg/"
PAGE = "https://www.remss.com/measurements/atmospheric-water-vapor/"
SOURCE_NAME = "Remote Sensing Systems — RSS V7, vapeur d'eau intégrée sur les océans (SSM/I, SSMIS, AMSR, WindSat)"
LICENSE = "CC BY 4.0 (RSS)"
VAR = "merged_vapor"
LAT_MAX = 60.0
UA = "projet-evolution-climat"


def latest() -> str:
    with urllib.request.urlopen(urllib.request.Request(DIR_URL, headers={"User-Agent": UA}), timeout=60) as r:
        html = r.read().decode("utf-8", errors="replace")
    names = sorted(set(re.findall(r"merged_vapor_1988-(\d{4})\.nc", html)))
    if not names:
        raise RuntimeError("RSS vapeur : aucun fichier merged_vapor_1988-AAAA.nc dans le répertoire")
    return f"merged_vapor_1988-{names[-1]}.nc"


def month_of(t: float) -> str:
    """Année décimale au milieu du mois (1988.0417 = janvier 1988) → « AAAA-MM »."""
    y = int(t)
    m = int(round((t - y) * 12 - 0.5)) + 1
    if not 1 <= m <= 12:
        raise ValueError(f"RSS vapeur : temps {t} hors d'un milieu de mois")
    return f"{y}-{m:02d}"


def extract(path: Path) -> tuple[list[dict], dict]:
    import netCDF4
    import numpy as np
    with netCDF4.Dataset(path) as ds:
        v = ds.variables[VAR]
        if v.dimensions != ("latitude", "longitude", "time"):
            raise ValueError(f"RSS vapeur : dimensions inattendues {v.dimensions}")
        lat = np.asarray(ds.variables["latitude"][:], float)
        t = np.asarray(ds.variables["time"][:], float)
        band = np.abs(lat) <= LAT_MAX
        w = np.ma.filled(v[band, :, :].astype(float), np.nan)        # (lat, lon, temps)
    w[(w < 0) | (w > 100)] = np.nan
    mask = np.all(np.isfinite(w), axis=2)                           # valide tous les mois
    area = np.cos(np.deg2rad(lat[band]))[:, None] * np.ones(mask.shape)
    fraction = float(area[mask].sum() / area.sum())
    wts = area[mask]
    months = [month_of(x) for x in t]
    if len(set(months)) != len(months):
        raise ValueError("RSS vapeur : mois en double")
    rows = [{"month": m, "tpw_kgm2": round(float(np.sum(w[:, :, i][mask] * wts) / wts.sum()), 4)}
            for i, m in enumerate(months)]
    meta = {"mask_cells": int(mask.sum()), "mask_area_fraction": round(fraction, 4), "lat_max": LAT_MAX}
    return rows, meta


def collect(out_dir: Path = OUT_DIR) -> str:
    out_dir.mkdir(parents=True, exist_ok=True)
    meta_path = out_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    name = latest()
    # Le fichier garde son nom pendant l'année : on compare aussi sa date de modification.
    with urllib.request.urlopen(urllib.request.Request(DIR_URL + name, method="HEAD", headers={"User-Agent": UA}),
                                timeout=60) as r:
        modified = r.headers.get("Last-Modified", "")
    if meta.get("file") == name and meta.get("modified") == modified and (out_dir / "tpw.csv").exists():
        return f"RSS vapeur : à jour ({name})"
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        with urllib.request.urlopen(urllib.request.Request(DIR_URL + name, headers={"User-Agent": UA}), timeout=300) as r, \
                path.open("wb") as f:
            while chunk := r.read(1 << 22):
                f.write(chunk)
        rows, info = extract(path)
    with (out_dir / "tpw.csv").open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["month", "tpw_kgm2"])
        wr.writeheader()
        wr.writerows(rows)
    meta = {"file": name, "modified": modified, "rows": len(rows), **info,
            "collected": datetime.now(timezone.utc).isoformat()}
    meta_path.write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    return f"RSS vapeur : relevé {name}, {len(rows)} mois, masque {info['mask_area_fraction']:.1%} de la bande"


def load(out_dir: Path = OUT_DIR) -> tuple[dict[str, float], dict]:
    with (out_dir / "tpw.csv").open(encoding="utf-8") as f:
        rows = {r["month"]: float(r["tpw_kgm2"]) for r in csv.DictReader(f)}
    return rows, json.loads((out_dir / "meta.json").read_text(encoding="utf-8"))


def main() -> int:
    try:
        print(collect(), flush=True)
    except Exception as exc:  # noqa: BLE001
        msg = f"RSS vapeur : ÉCHEC {type(exc).__name__} {str(exc)[:300]}"
        print(msg)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(f"::error title=RSS vapeur::{msg}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
