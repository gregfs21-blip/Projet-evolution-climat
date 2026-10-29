"""Source : indice forêt-météo (FWI) du CEMS/EFFIS calculé sur ERA5 (Copernicus Early Warning Data Store).

Format constaté par la sonde du 29/10/2026 (docs/sonde-p4c.md) : netCDF, dimensions `valid_time` (secondes depuis
1970, un pas par jour), `latitude`, `longitude` (0-360°) ; variable `fwinx` (FWI du système canadien). Requête de
juillet 2022 sur la boîte Gironde traitée en moins de 3 minutes.

Choix fixés le 29/10/2026, avant tout calcul (docs/phases.md, P4) :
- jeu `cems-fire-historical-v1`, réanalyse, données consolidées, version 4.1, grille 0,25° ;
- boîte demandée 44,2-45,6° N, 1,3° O-0,4° E ; la colonne la plus à l'ouest (centres à 1,3° O, surtout en mer) est
  écartée : 36 mailles de centres 44,2-45,45° N, 1,05° O-0,2° E ;
- moyenne quotidienne pondérée par le cosinus de la latitude des mailles valides ; saison de juin à septembre ;
- requêtes par tranches de 10 ans (juin-septembre), relevées par le workflow « Copernicus » comme les séries ERA5.

L'ETL ne lit que le CSV produit (data/sources/era5-pl/fwi-gironde.csv) : aucun appel réseau.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from etl.sources import cds_era5 as cds

API = "https://ewds.climate.copernicus.eu/api"
DATASET = "cems-fire-historical-v1"
PAGE = "https://ewds.climate.copernicus.eu/datasets/cems-fire-historical-v1"
SOURCE_NAME = "Copernicus CEMS / EFFIS — indices de danger d'incendie historiques sur ERA5 (Early Warning Data Store)"
LICENSE = "CC BY 4.0 (Copernicus)"
OUT_DIR = cds.OUT_DIR
AREA = [45.6, -1.3, 44.2, 0.4]
WEST_EDGE = -1.2                   # mailles de centre à l'ouest : écartées (en mer)
FIRST_YEAR = 1940
CHUNK = 10
MONTHS = ["06", "07", "08", "09"]
SEASON_DAYS = 122
MAX_PENDING = 3


def names() -> list[str]:
    return [f"fwi-gironde-{y}" for y in range(FIRST_YEAR, cds.last_year() + 1, CHUNK)]


def requests() -> dict[str, dict]:
    out = {}
    for name in names():
        y0 = int(name[-4:])
        out[name] = {"product_type": ["reanalysis"], "variable": ["fire_weather_index"],
                     "dataset_type": ["consolidated_dataset"], "system_version": ["4_1"],
                     "year": [str(y) for y in range(y0, min(y0 + CHUNK, cds.last_year() + 1))], "month": MONTHS,
                     "day": [f"{d:02d}" for d in range(1, 32)], "grid": ["0.25/0.25"], "data_format": "netcdf",
                     "area": AREA}
    return out


# ---------------------------------------------------------------- extraction (pure, testée)


def extract_daily(arrays: dict[str, np.ndarray]) -> list[dict]:
    lat = np.asarray(arrays["latitude"], dtype=float)
    lon = np.asarray(arrays["longitude"], dtype=float)
    lon = np.where(lon > 180, lon - 360, lon)
    keep = lon > WEST_EDGE
    w = np.cos(np.radians(lat))[:, None] * np.ones((1, len(lon)))
    w = w[:, keep]
    rows = []
    for i, t in enumerate(np.asarray(arrays["valid_time"], dtype=np.int64)):
        day = datetime.fromtimestamp(int(t), tz=timezone.utc).strftime("%Y-%m-%d")
        f = np.asarray(arrays["fwinx"][i], dtype=float)[:, keep]
        ok = np.isfinite(f)
        if not ok.any():
            continue
        rows.append({"day": day, "fwi": round(float((f[ok] * w[ok]).sum() / w[ok].sum()), 3), "cells": int(ok.sum())})
    return rows


def read_nc(path: Path) -> dict[str, np.ndarray]:
    import netCDF4
    with netCDF4.Dataset(path) as ds:
        return {k: np.ma.filled(ds.variables[k][:].astype(float), np.nan) if k == "fwinx" else ds.variables[k][:]
                for k in ("valid_time", "latitude", "longitude", "fwinx")}


def merge(out_dir: Path = OUT_DIR) -> None:
    parts = [out_dir / f"{n}.csv" for n in names()]
    if not all(p.exists() for p in parts):
        return
    import csv
    rows = []
    for p in parts:
        with p.open(encoding="utf-8") as f:
            rows += list(csv.DictReader(f))
    rows = sorted({r["day"]: r for r in rows}.values(), key=lambda r: r["day"])
    cds._write_csv(out_dir / "fwi-gironde.csv", rows)


def load(out_dir: Path = OUT_DIR) -> dict[str, float]:
    import csv
    with (out_dir / "fwi-gironde.csv").open(encoding="utf-8") as f:
        return {r["day"]: float(r["fwi"]) for r in csv.DictReader(f)}


# ---------------------------------------------------------------- relevé et soumission


def _call(path: str, method: str = "GET", body: dict | None = None) -> dict:
    req = urllib.request.Request(f"{API}/retrieve/v1/{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"PRIVATE-TOKEN": os.environ.get("CDSAPI_KEY", ""),
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} : {exc.read()[:400].decode('utf-8', 'replace')}") from exc


def _same(a: dict, b: dict) -> bool:
    norm = lambda d, k: [str(x) for x in d.get(k, [])]  # noqa: E731
    return all(norm(a, k) == norm(b, k) for k in ("variable", "year", "month", "area"))


def collect(out_dir: Path = OUT_DIR) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    log: list[str] = []
    jobs = [j for j in _call("jobs?limit=100").get("jobs", []) if j.get("processID", DATASET) == DATASET]
    details = {}
    for j in jobs:
        if j.get("status") in ("accepted", "running", "successful"):
            try:
                details[j["jobID"]] = _call(f"jobs/{j['jobID']}?request=true").get("metadata", {}).get("request", {}).get("ids", {})
            except Exception:  # noqa: BLE001
                details[j["jobID"]] = {}
    pending = [j for j in jobs if j.get("status") in ("accepted", "running")]
    m = cds.meta(out_dir)
    for name, req in requests().items():
        try:
            mine = [j for j in jobs if j["jobID"] in details and _same(details[j["jobID"]], req)]
            done = sorted((j for j in mine if j["status"] == "successful"), key=lambda j: j.get("finished") or "")
            if done:
                job = done[-1]
                if m.get(name, {}).get("job") == job["jobID"]:
                    log.append(f"{name} : à jour (travail {job['jobID']})")
                    continue
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "r.nc"
                    cds._download(_call(f"jobs/{job['jobID']}/results")["asset"]["value"]["href"], path)
                    rows = extract_daily(read_nc(path))
                cds._write_csv(out_dir / f"{name}.csv", rows)
                m[name] = {"job": job["jobID"], "finished": job.get("finished"), "rows": len(rows),
                           "years": [req["year"][0], req["year"][-1]], "collected": datetime.now(timezone.utc).isoformat()}
                log.append(f"{name} : relevé, {len(rows)} jours (travail {job['jobID']})")
            elif any(j["status"] in ("accepted", "running") for j in mine):
                log.append(f"{name} : en file chez Copernicus")
            elif len(pending) >= MAX_PENDING:
                log.append(f"{name} : non soumise, {len(pending)} requêtes déjà en attente")
            else:
                job = _call(f"processes/{DATASET}/execution", "POST", {"inputs": req})
                pending.append(job)
                log.append(f"{name} : soumise (travail {job.get('jobID')})")
        except Exception as exc:  # noqa: BLE001 — une requête en échec ne bloque pas les autres
            msg = f"{name} : ÉCHEC {type(exc).__name__} {str(exc)[:400]}"
            log.append(msg)
            if os.environ.get("GITHUB_ACTIONS") == "true":
                print(f"::error title=EWDS {name}::{msg}", flush=True)
    (out_dir / "meta.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    merge(out_dir)
    return log


def main() -> int:
    if not os.environ.get("CDSAPI_KEY"):
        print("CDSAPI_KEY absente : rien à faire")
        return 1
    t0 = time.time()
    while True:
        log = collect()
        print("\n".join(log), flush=True)
        busy = [x for x in log if "soumise (" in x or "en file" in x or "non soumise" in x]
        if not busy or time.time() - t0 > 25 * 60:
            return 0
        time.sleep(60)


if __name__ == "__main__":
    sys.exit(main())
