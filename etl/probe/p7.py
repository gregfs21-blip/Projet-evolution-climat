"""Sonde P7 (exploratoire) : données pour les blocages atmosphériques et un indicateur indirect de la foudre.

1. ERA5 statistiques quotidiennes sur niveaux de pression (CDS `derived-era5-pressure-levels-daily-statistics`) :
   entrées permises, puis soumission non bloquante d'un mois de Z500 quotidien, Atlantique-Europe, grille 2,5°.
2. ERA5 moyennes mensuelles sur niveaux uniques : variables liées à la convection et à la foudre (CAPE, densité
   d'éclairs du modèle), puis soumission d'un mois sur la Gironde.
Aucun indicateur calculé. Usage : python -m etl.probe.p7   → docs/sonde-p7.md
"""

from __future__ import annotations

import io
import json
import os
import sys
import time
import urllib.request
import zipfile
from datetime import datetime, timezone

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-p7.md"
KEY = os.environ.get("CDSAPI_KEY", "")
API = "https://cds.climate.copernicus.eu/api/retrieve/v1"
HDR = {"PRIVATE-TOKEN": KEY, "Content-Type": "application/json", "User-Agent": "projet-evolution-climat (sonde)"}


def get(url, data=None, method=None, headers=None, limit=200_000_000):
    try:
        req = urllib.request.Request(url, headers=headers or HDR, data=data, method=method)
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read(limit)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()[:2000]
    except Exception as exc:  # noqa: BLE001
        return f"erreur : {type(exc).__name__} {exc}", b""


def enums(pid: str, keep=None) -> list[str]:
    st, data = get(f"{API}/processes/{pid}")
    out = [f"→ {st}"]
    try:
        for k, v in json.loads(data).get("inputs", {}).items():
            sch = v.get("schema", v)
            vals = sch.get("enum") or sch.get("items", {}).get("enum") or []
            if keep and k == "variable":
                vals = [x for x in vals if any(w in x for w in keep)]
            out.append(f"{k} : {len(vals)} valeurs : {vals[:40]}" if vals else f"{k} : {str(sch)[:200]}")
    except Exception as exc:  # noqa: BLE001
        out.append(f"{type(exc).__name__} {data[:300]!r}")
    return out


def submit_and_read(pid: str, inputs: dict, wait: int = 1500) -> list[str]:
    st, data = get(f"{API}/processes/{pid}/execution", data=json.dumps({"inputs": inputs}).encode(), method="POST")
    lines = [f"soumission → {st}", data.decode("utf-8", "replace").replace(KEY or "§§", "***")[:500]]
    try:
        job = json.loads(data)["jobID"]
    except Exception:  # noqa: BLE001
        return lines
    t0, status = time.time(), None
    while time.time() - t0 < wait:
        time.sleep(30)
        _, dj = get(f"{API}/jobs/{job}")
        status = json.loads(dj).get("status")
        if status in ("successful", "failed", "rejected", "dismissed"):
            break
    lines.append(f"état après {time.time() - t0:.0f} s : {status}")
    if status != "successful":
        return lines
    _, dr = get(f"{API}/jobs/{job}/results")
    href = json.loads(dr)["asset"]["value"]["href"]
    _, blob = get(href, headers={"PRIVATE-TOKEN": KEY})
    if blob[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(blob))
        lines.append("archive : " + ", ".join(f"{i.filename} ({i.file_size} o)" for i in z.infolist()))
        blob = z.read(z.namelist()[0])
    path = OUT.parent / "_p7.nc"
    path.write_bytes(blob)
    try:
        import netCDF4
        import numpy as np
        with netCDF4.Dataset(path) as ds:
            lines.append("dimensions : " + ", ".join(f"{k}={len(v)}" for k, v in ds.dimensions.items()))
            for name, var in ds.variables.items():
                lines.append(f"  {name} {var.dimensions} {var.shape} {getattr(var, 'units', '')} {getattr(var, 'long_name', '')}")
                if var.ndim >= 2:
                    a = np.ma.filled(var[:].astype(float), np.nan)
                    lines.append(f"    min {np.nanmin(a):.4g}, moyenne {np.nanmean(a):.4g}, max {np.nanmax(a):.4g}")
                elif var.ndim == 1 and len(var) <= 60:
                    lines.append(f"    {list(np.round(np.asarray(var[:], dtype=float), 3))[:60]}")
    finally:
        path.unlink(missing_ok=True)
    return lines


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P7 — blocages et foudre (généré)", "", f"Généré par `python -m etl.probe.p7` le {now}. Aucun indicateur calculé."]
    steps = [
        ("1. ERA5 quotidien, niveaux de pression : entrées", lambda: enums("derived-era5-pressure-levels-daily-statistics")),
        ("1 bis. Z500 quotidien, janvier 2020, 30-85° N, 60° O-60° E, 2,5°", lambda: submit_and_read(
            "derived-era5-pressure-levels-daily-statistics",
            {"product_type": "reanalysis", "variable": ["geopotential"], "pressure_level": ["500"], "year": "2020",
             "month": ["01"], "day": [f"{d:02d}" for d in range(1, 32)], "daily_statistic": "daily_mean",
             "time_zone": "utc+00:00", "frequency": "6_hourly", "area": [85, -60, 30, 60], "grid": ["2.5", "2.5"]})),
        ("2. ERA5 mensuel, niveaux uniques : variables convection et foudre",
         lambda: enums("reanalysis-era5-single-levels-monthly-means", keep=("lightning", "convective_available", "cape"))),
        ("2 bis. Densité d'éclairs et CAPE, juillet 2022, Gironde", lambda: submit_and_read(
            "reanalysis-era5-single-levels-monthly-means",
            {"product_type": ["monthly_averaged_reanalysis"], "variable": ["average_total_lightning_flash_density",
                                                                          "convective_available_potential_energy"],
             "year": ["2022"], "month": ["07"], "time": ["00:00"], "area": [45.6, -1.3, 44.2, 0.4],
             "data_format": "netcdf", "download_format": "unarchived"})),
    ]
    for title, fn in steps:
        try:
            lines = fn()
        except Exception as exc:  # noqa: BLE001
            lines = [f"échec : {type(exc).__name__} {exc}"]
        md += ["", f"## {title}", "", "```", *[str(x)[:500] for x in lines], "```"]
        OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
