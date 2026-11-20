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
# P10.4b (D-AV, D-AX) : température de la mer sur le même domaine, ERSST v5 (sonde docs/sonde-p10e.md)
ERSST_URL = "https://downloads.psl.noaa.gov/Datasets/noaa.ersst.v5/sst.mnmean.nc"
ERSST_PAGE = "https://psl.noaa.gov/data/gridded/data.noaa.ersst.v5.html"
ERSST_NAME = "NOAA NCEI — ERSST v5, température de surface de la mer, grille de 2° (via NOAA PSL)"
ERSST_LICENSE = "Domaine public (NOAA)"
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


def nearest_ersst(lat: float, lon: float) -> tuple[int, int]:
    """Indice de la maille ERSST v5 (2°, latitudes 88 → −88, longitudes 0 → 358) la plus proche d'un centre RSS (x,5°)."""
    i = int(round((88.0 - lat) / 2.0))
    j = int(round((lon % 360.0) / 2.0)) % 180
    return min(max(i, 0), 88), j


def extract_common(rss_path: Path, ersst_path: Path) -> tuple[list[dict], dict]:
    """P10.4b : masque commun (masque constant RSS ∩ maille ERSST la plus proche valide tous les mois), moyennes
    mensuelles pondérées par l'aire de la vapeur d'eau et de la température de la mer sur ce masque."""
    import netCDF4
    import numpy as np
    with netCDF4.Dataset(rss_path) as ds:
        lat = np.asarray(ds.variables["latitude"][:], float)
        lon = np.asarray(ds.variables["longitude"][:], float)
        t = np.asarray(ds.variables["time"][:], float)
        band = np.abs(lat) <= LAT_MAX
        w = np.ma.filled(ds.variables[VAR][band, :, :].astype(float), np.nan)
    w[(w < 0) | (w > 100)] = np.nan
    lat_b = lat[band]
    rss_mask = np.all(np.isfinite(w), axis=2)
    months = [month_of(x) for x in t]
    with netCDF4.Dataset(ersst_path) as ds:
        tv = ds.variables["time"]
        dates = netCDF4.num2date(tv[:], tv.units, only_use_cftime_datetimes=False, only_use_python_datetimes=True)
        index = {f"{d.year}-{d.month:02d}": k for k, d in enumerate(dates)}
        missing = [m for m in months if m not in index]
        if missing:
            raise ValueError(f"ERSST : mois absents {missing[:3]}")
        if np.asarray(ds.variables["lat"][:2], float).tolist() != [88.0, 86.0] or float(ds.variables["lon"][1]) != 2.0:
            raise ValueError("ERSST : grille inattendue (88 → −88, 0 → 358 attendue)")
        ks = [index[m] for m in months]
        sst = np.ma.filled(ds.variables["sst"][ks[0]:ks[-1] + 1, :, :].astype(float), np.nan)   # (temps, lat, lon)
    if sst.shape[0] != len(months):
        raise ValueError("ERSST : mois non consécutifs")
    sst[np.abs(sst) > 100] = np.nan
    ii, jj = np.nonzero(rss_mask)
    pairs = [nearest_ersst(lat_b[i], lon[j]) for i, j in zip(ii, jj)]
    pi = np.array([p[0] for p in pairs])
    pj = np.array([p[1] for p in pairs])
    sst_cells = sst[:, pi, pj]                                         # (temps, mailles)
    ok = np.all(np.isfinite(sst_cells), axis=0)
    area_all = np.cos(np.deg2rad(lat_b))[:, None] * np.ones(rss_mask.shape)
    wts = np.cos(np.deg2rad(lat_b[ii[ok]]))
    tpw_cells = w[ii[ok], jj[ok], :]                                   # (mailles, temps)
    rows = [{"month": m,
             "tpw_kgm2": round(float(np.sum(tpw_cells[:, k] * wts) / wts.sum()), 4),
             "sst_c": round(float(np.sum(sst_cells[k, ok] * wts) / wts.sum()), 4)} for k, m in enumerate(months)]
    meta = {"common_cells": int(ok.sum()), "common_area_fraction": round(float(wts.sum() / area_all.sum()), 4),
            "rss_cells_dropped": int((~ok).sum())}
    return rows, meta


def _modified(url: str) -> str:
    with urllib.request.urlopen(urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA}), timeout=60) as r:
        return r.headers.get("Last-Modified", "")


def _download(url: str, path: Path) -> None:
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=600) as r, \
            path.open("wb") as f:
        while chunk := r.read(1 << 22):
            f.write(chunk)


def collect(out_dir: Path = OUT_DIR) -> str:
    out_dir.mkdir(parents=True, exist_ok=True)
    meta_path = out_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    name = latest()
    # Les fichiers gardent leur nom pendant l'année : on compare aussi leur date de modification.
    modified, ersst_modified = _modified(DIR_URL + name), _modified(ERSST_URL)
    fresh = meta.get("file") == name and meta.get("modified") == modified and (out_dir / "tpw.csv").exists()
    fresh_common = (fresh and meta.get("ersst_modified") == ersst_modified and (out_dir / "tpw-sst-common.csv").exists())
    if fresh and fresh_common:
        return f"RSS vapeur : à jour ({name})"
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        _download(DIR_URL + name, path)
        rows, info = extract(path)
        epath = Path(tmp) / "ersst.nc"
        _download(ERSST_URL, epath)
        common, cinfo = extract_common(path, epath)
    with (out_dir / "tpw.csv").open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["month", "tpw_kgm2"])
        wr.writeheader()
        wr.writerows(rows)
    with (out_dir / "tpw-sst-common.csv").open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["month", "tpw_kgm2", "sst_c"])
        wr.writeheader()
        wr.writerows(common)
    meta = {"file": name, "modified": modified, "rows": len(rows), **info, "ersst_modified": ersst_modified, **cinfo,
            "collected": datetime.now(timezone.utc).isoformat()}
    meta_path.write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    return (f"RSS vapeur : relevé {name}, {len(rows)} mois, masque {info['mask_area_fraction']:.1%} de la bande ; "
            f"domaine commun avec ERSST {cinfo['common_area_fraction']:.1%}")


def load_common(out_dir: Path = OUT_DIR) -> dict[str, tuple[float, float]]:
    with (out_dir / "tpw-sst-common.csv").open(encoding="utf-8") as f:
        return {r["month"]: (float(r["tpw_kgm2"]), float(r["sst_c"])) for r in csv.DictReader(f)}


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
