"""Source : épaisseur optique des aérosols, réanalyse CAMS EAC4 mensuelle (Copernicus Atmosphere Data Store).

Format constaté par la sonde du 31/10/2026 (docs/sonde-p6c.md) : archive zip contenant un netCDF, dimensions
`valid_time`, `latitude` (241, 0,75°), `longitude` (480) ; variable `aod550` (sans unité). Même compte ECMWF et même
clé que le CDS (secret CDSAPI_KEY). Une seule requête : 2003 à la dernière année complète, 12 mois, globe entier.

Choix fixés avant calcul (docs/phases.md, P6) : moyenne mondiale pondérée par le cosinus de la latitude, chaque mois ;
l'ETL fait la moyenne des 12 mois. Sortie : data/sources/era5-pl/aod-monde.csv.
"""

from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from etl.sources import cds_era5 as cds

API = "https://ads.atmosphere.copernicus.eu/api"
DATASET = "cams-global-reanalysis-eac4-monthly"
PAGE = "https://ads.atmosphere.copernicus.eu/datasets/cams-global-reanalysis-eac4-monthly"
SOURCE_NAME = "Copernicus CAMS — réanalyse EAC4 mensuelle, épaisseur optique des aérosols à 550 nm (Atmosphere Data Store)"
LICENSE = "Licence d'utilisation des produits Copernicus (CC BY 4.0)"
OUT_DIR = cds.OUT_DIR
NAME = "aod-monde"
FIRST_YEAR = 2003


def request() -> dict:
    return {"variable": ["total_aerosol_optical_depth_550nm"], "product_type": ["monthly_mean"],
            "year": [str(y) for y in range(FIRST_YEAR, cds.last_year() + 1)],
            "month": [f"{m:02d}" for m in range(1, 13)], "data_format": "netcdf_zip"}


def global_means(arrays: dict[str, np.ndarray]) -> list[dict]:
    lat = np.asarray(arrays["latitude"], dtype=float)
    w = np.cos(np.radians(lat))[:, None] * np.ones((1, len(arrays["longitude"])))
    rows = []
    for i, t in enumerate(np.asarray(arrays["valid_time"], dtype=np.int64)):
        f = np.asarray(arrays["aod550"][i], dtype=float)
        ok = np.isfinite(f)
        rows.append({"month": datetime.fromtimestamp(int(t), tz=timezone.utc).strftime("%Y-%m"),
                     "aod550": round(float((f[ok] * w[ok]).sum() / w[ok].sum()), 5)})
    return sorted(rows, key=lambda r: r["month"])


def extract_zip(path: Path) -> list[dict]:
    import netCDF4
    rows = []
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if not name.endswith(".nc"):
                continue
            with tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp) / "x.nc"
                p.write_bytes(z.read(name))
                with netCDF4.Dataset(p) as ds:
                    arrays = {k: (np.ma.filled(ds.variables[k][:].astype(float), np.nan) if k == "aod550" else ds.variables[k][:])
                              for k in ("valid_time", "latitude", "longitude", "aod550")}
                rows += global_means(arrays)
    return sorted({r["month"]: r for r in rows}.values(), key=lambda r: r["month"])


def _call(path: str, method: str = "GET", body: dict | None = None) -> dict:
    req = urllib.request.Request(f"{API}/retrieve/v1/{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"PRIVATE-TOKEN": os.environ.get("CDSAPI_KEY", ""), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} : {exc.read()[:400].decode('utf-8', 'replace')}") from exc


def collect(out_dir: Path = OUT_DIR) -> str:
    req = request()
    jobs = [j for j in _call("jobs?limit=50").get("jobs", []) if j.get("processID", DATASET) == DATASET]
    mine = []
    for j in jobs:
        if j.get("status") not in ("accepted", "running", "successful"):
            continue
        ids = _call(f"jobs/{j['jobID']}?request=true").get("metadata", {}).get("request", {}).get("ids", {})
        if [str(x) for x in ids.get("year", [])] == req["year"] and ids.get("variable") == req["variable"]:
            mine.append(j)
    m = cds.meta(out_dir)
    done = sorted((j for j in mine if j["status"] == "successful"), key=lambda j: j.get("finished") or "")
    if done:
        job = done[-1]
        if m.get(NAME, {}).get("job") == job["jobID"]:
            return f"{NAME} : à jour (travail {job['jobID']})"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "r.zip"
            cds._download(_call(f"jobs/{job['jobID']}/results")["asset"]["value"]["href"], path)
            rows = extract_zip(path)
        cds._write_csv(out_dir / f"{NAME}.csv", rows)
        m[NAME] = {"job": job["jobID"], "finished": job.get("finished"), "rows": len(rows),
                   "years": [req["year"][0], req["year"][-1]], "collected": datetime.now(timezone.utc).isoformat()}
        (out_dir / "meta.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        return f"{NAME} : relevé, {len(rows)} mois (travail {job['jobID']})"
    if mine:
        return f"{NAME} : en file chez Copernicus"
    job = _call(f"processes/{DATASET}/execution", "POST", {"inputs": req})
    return f"{NAME} : soumise (travail {job.get('jobID')})"


def load(out_dir: Path = OUT_DIR) -> dict[str, float]:
    import csv
    with (out_dir / f"{NAME}.csv").open(encoding="utf-8") as f:
        return {r["month"]: float(r["aod550"]) for r in csv.DictReader(f)}


def main() -> int:
    if not os.environ.get("CDSAPI_KEY"):
        print("CDSAPI_KEY absente : rien à faire")
        return 1
    t0 = time.time()
    while True:
        try:
            msg = collect()
        except Exception as exc:  # noqa: BLE001
            msg = f"{NAME} : ÉCHEC {type(exc).__name__} {str(exc)[:300]}"
            if os.environ.get("GITHUB_ACTIONS") == "true":
                print(f"::error title=CAMS::{msg}", flush=True)
            print(msg, flush=True)
            return 0
        print(msg, flush=True)
        if "soumise" not in msg and "en file" not in msg or time.time() - t0 > 20 * 60:
            return 0
        time.sleep(60)


if __name__ == "__main__":
    sys.exit(main())
