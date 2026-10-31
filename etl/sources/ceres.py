"""Source : déséquilibre énergétique de la Terre, CERES EBAF-TOA Edition 4.2.1 (NASA LaRC, ASDC).

Accès constaté par la sonde du 31/10/2026 (docs/sonde-p6d.md) : OPeNDAP refusé depuis GitHub ; le granule unique
(« CERES_EBAF-TOA_Edition4.2.1_200003-AAAAMM.nc », environ 900 Mo, netCDF classique) se télécharge par le catalogue
CMR avec un jeton NASA Earthdata (secret EARTHDATA_TOKEN, jamais affiché).

Le relevé (workflow « Copernicus ») ne retélécharge le fichier que si le granule a changé ; il en extrait la série
mensuelle du flux net global (variable `gtoa_net_all_mon`, W/m²) dans data/sources/ceres/ebaf-toa.csv. L'ETL ne lit
que ce CSV.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import tempfile
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from etl.context import ROOT

OUT_DIR = ROOT / "data" / "sources" / "ceres"
CMR = ("https://cmr.earthdata.nasa.gov/search/granules.json?short_name=CERES_EBAF-TOA&version=Edition4.2.1"
       "&page_size=5&sort_key=-start_date")
VAR = "gtoa_net_all_mon"
PAGE = "https://ceres.larc.nasa.gov/data/#ebaftoa-level-3"
SOURCE_NAME = "NASA LaRC — CERES EBAF-TOA Edition 4.2.1 (flux radiatifs au sommet de l'atmosphère)"
LICENSE = "Domaine public (NASA)"


def latest() -> tuple[str, str]:
    with urllib.request.urlopen(urllib.request.Request(CMR, headers={"User-Agent": "projet-evolution-climat"}), timeout=60) as r:
        entries = json.loads(r.read())["feed"]["entry"]
    for g in entries:
        for lk in g.get("links", []):
            href = lk.get("href", "")
            if href.startswith("https://") and href.endswith(".nc") and "data#" in lk.get("rel", ""):
                return g["title"], href
    raise RuntimeError("CERES : aucun lien de téléchargement dans le catalogue CMR")


def months_from(time_values, units: str) -> list[str]:
    """Unités CF « days since AAAA-MM-JJ … » → « AAAA-MM »."""
    origin = datetime.fromisoformat(units.split("since")[1].strip().split()[0]).replace(tzinfo=timezone.utc)
    return [(origin + timedelta(days=float(t))).strftime("%Y-%m") for t in time_values]


def extract(path: Path) -> list[dict]:
    import netCDF4
    import numpy as np
    with netCDF4.Dataset(path) as ds:
        v = ds.variables[VAR]
        t = ds.variables["time"]
        months = months_from(np.asarray(t[:]), t.units)
        vals = np.ma.filled(v[:].astype(float), np.nan)
    return [{"month": m, "net_wm2": round(float(x), 4)} for m, x in zip(months, vals) if np.isfinite(x)]


def collect(out_dir: Path = OUT_DIR) -> str:
    token = os.environ.get("EARTHDATA_TOKEN", "")
    if not token:
        return "EARTHDATA_TOKEN absent : rien à faire"
    out_dir.mkdir(parents=True, exist_ok=True)
    meta_path = out_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    title, href = latest()
    if meta.get("granule") == title and (out_dir / "ebaf-toa.csv").exists():
        return f"CERES : à jour ({title})"
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "ebaf.nc"
        req = urllib.request.Request(href, headers={"Authorization": f"Bearer {token}", "User-Agent": "projet-evolution-climat"})
        with urllib.request.urlopen(req, timeout=120) as r, path.open("wb") as f:
            while chunk := r.read(1 << 22):
                f.write(chunk)
        rows = extract(path)
    with (out_dir / "ebaf-toa.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["month", "net_wm2"])
        w.writeheader()
        w.writerows(rows)
    meta = {"granule": title, "rows": len(rows), "collected": datetime.now(timezone.utc).isoformat()}
    meta_path.write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    return f"CERES : relevé {title}, {len(rows)} mois"


def load(out_dir: Path = OUT_DIR) -> dict[str, float]:
    with (out_dir / "ebaf-toa.csv").open(encoding="utf-8") as f:
        return {r["month"]: float(r["net_wm2"]) for r in csv.DictReader(f)}


def main() -> int:
    try:
        print(collect(), flush=True)
    except Exception as exc:  # noqa: BLE001
        msg = f"CERES : ÉCHEC {type(exc).__name__} {str(exc)[:300]}"
        print(msg)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(f"::error title=CERES::{msg}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
