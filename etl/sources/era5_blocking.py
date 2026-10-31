"""Source : Z500 quotidien ERA5 pour les blocages euro-atlantiques (P7 ; choix fixés le 31/10/2026 avant calcul).

Format constaté par la sonde du 31/10/2026 (docs/sonde-p7.md) : jeu `derived-era5-pressure-levels-daily-statistics`,
netCDF, `z` (m² s⁻²) de dimensions (valid_time, pressure_level, latitude, longitude), latitudes décroissantes de 85 à
30° N, longitudes de −60 à 60° E, pas de 2,5° ; `valid_time` en jours depuis le 1er janvier de l'année.

Une requête par année. Le relevé n'écrit, pour chaque jour, que :
- `blocked` : chaîne de 0 et de 1, une par longitude de −60 à 60° E (critère de Tibaldi et Molteni, 1990) ;
- `z500_sector` : Z500 moyen de 35-70° N, 30° O-30° E (m), pondéré par le cosinus de la latitude.
Fichiers : data/sources/era5-pl/blocking-AAAA.csv, réunis dans blocking.csv quand toutes les années sont là.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

from etl.sources import cds_era5 as cds

DATASET = "derived-era5-pressure-levels-daily-statistics"
PAGE = "https://cds.climate.copernicus.eu/datasets/derived-era5-pressure-levels-daily-statistics"
SOURCE_NAME = "ECMWF / Copernicus — ERA5, statistiques quotidiennes sur niveaux de pression (Z500)"
OUT_DIR = cds.OUT_DIR
FIRST_YEAR = 1940
G0 = 9.80665
PHI = (80.0, 60.0, 40.0)        # φN, φ0, φS
DELTAS = (-5.0, 0.0, 5.0)
GHGN_MAX = -10.0                # m par degré de latitude
SECTOR_Z = (35.0, 70.0, -30.0, 30.0)
MAX_PENDING = 3


def names() -> list[str]:
    return [f"blocking-{y}" for y in range(FIRST_YEAR, cds.last_year() + 1)]


def request(year: int) -> dict:
    return {"product_type": "reanalysis", "variable": ["geopotential"], "pressure_level": ["500"], "year": str(year),
            "month": [f"{m:02d}" for m in range(1, 13)], "day": [f"{d:02d}" for d in range(1, 32)],
            "daily_statistic": "daily_mean", "time_zone": "utc+00:00", "frequency": "6_hourly",
            "area": [85, -60, 30, 60], "grid": ["2.5", "2.5"]}


# ---------------------------------------------------------------- calculs purs (testés)


def blocked_longitudes(z: np.ndarray, lat: np.ndarray) -> np.ndarray:
    """z : (latitude, longitude) en mètres géopotentiels. Booléen par longitude (Tibaldi et Molteni, 1990)."""
    idx = {round(float(v), 2): i for i, v in enumerate(lat)}
    out = np.zeros(z.shape[1], dtype=bool)
    for d in DELTAS:
        n, o, s = (idx.get(round(p + d, 2)) for p in PHI)
        if None in (n, o, s):
            continue
        ghgs = (z[o] - z[s]) / (PHI[1] - PHI[2])
        ghgn = (z[n] - z[o]) / (PHI[0] - PHI[1])
        out |= (ghgs > 0) & (ghgn < GHGN_MAX)
    return out


def sector_mean(z: np.ndarray, lat: np.ndarray, lon: np.ndarray) -> float:
    s, n, w, e = SECTOR_Z
    mi = (lat >= s) & (lat <= n)
    mj = (lon >= w) & (lon <= e)
    sub = z[np.ix_(mi, mj)]
    wts = np.cos(np.radians(lat[mi]))[:, None] * np.ones((1, mj.sum()))
    return float((sub * wts).sum() / wts.sum())


def extract(arrays: dict[str, np.ndarray], year: int) -> list[dict]:
    lat = np.asarray(arrays["latitude"], dtype=float)
    lon = np.asarray(arrays["longitude"], dtype=float)
    lon = np.where(lon > 180, lon - 360, lon)
    z = np.asarray(arrays["z"], dtype=float)
    if z.ndim == 4:
        z = z[:, 0]
    z = z / G0
    order = np.argsort(lon)
    lon, z = lon[order], z[:, :, order]
    rows = []
    for k, t in enumerate(np.asarray(arrays["valid_time"], dtype=float)):
        day = (datetime(year, 1, 1, tzinfo=timezone.utc) + timedelta(days=float(t))).strftime("%Y-%m-%d")
        if not np.isfinite(z[k]).all():
            continue
        b = blocked_longitudes(z[k], lat)
        rows.append({"day": day, "blocked": "".join("1" if x else "0" for x in b),
                     "z500_sector": round(sector_mean(z[k], lat, lon), 2)})
    return rows


# ---------------------------------------------------------------- relevé


def merge(out_dir: Path = OUT_DIR) -> None:
    parts = [out_dir / f"{n}.csv" for n in names()]
    if not all(p.exists() for p in parts):
        return
    rows = []
    for p in parts:
        with p.open(encoding="utf-8") as f:
            rows += list(csv.DictReader(f))
    cds._write_csv(out_dir / "blocking.csv", sorted(rows, key=lambda r: r["day"]))


def collect(out_dir: Path = OUT_DIR) -> list[str]:
    log = []
    jobs = [j for j in cds._call("jobs?limit=100").get("jobs", []) if j.get("processID") == DATASET]
    years_of = {}
    for j in jobs:
        if j.get("status") in ("accepted", "running", "successful"):
            try:
                ids = cds._call(f"jobs/{j['jobID']}?request=true").get("metadata", {}).get("request", {}).get("ids", {})
                y = ids.get("year")
                years_of[j["jobID"]] = str(y[0] if isinstance(y, list) else y)
            except Exception:  # noqa: BLE001
                pass
    pending = [j for j in cds._call("jobs?limit=100").get("jobs", []) if j.get("status") in ("accepted", "running")]
    m = cds.meta(out_dir)
    for name in names():
        year = int(name[-4:])
        if (out_dir / f"{name}.csv").exists() and name in m:
            continue
        mine = [j for j in jobs if years_of.get(j["jobID"]) == str(year)]
        done = sorted((j for j in mine if j["status"] == "successful"), key=lambda j: j.get("finished") or "")
        try:
            if done:
                job = done[-1]
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "r.nc"
                    cds._download(cds._call(f"jobs/{job['jobID']}/results")["asset"]["value"]["href"], path)
                    rows = extract(cds.read_nc(path), year)
                if len(rows) < 365:
                    raise ValueError(f"{len(rows)} jours seulement")
                cds._write_csv(out_dir / f"{name}.csv", rows)
                m[name] = {"job": job["jobID"], "rows": len(rows), "collected": datetime.now(timezone.utc).isoformat()}
                log.append(f"{name} : relevé, {len(rows)} jours")
            elif any(j["status"] in ("accepted", "running") for j in mine):
                log.append(f"{name} : en file")
            elif len(pending) < MAX_PENDING:
                job = cds._call(f"processes/{DATASET}/execution", "POST", {"inputs": request(year)})
                pending.append(job)
                log.append(f"{name} : soumise (travail {job.get('jobID')})")
        except Exception as exc:  # noqa: BLE001
            msg = f"{name} : ÉCHEC {type(exc).__name__} {str(exc)[:300]}"
            log.append(msg)
            if os.environ.get("GITHUB_ACTIONS") == "true":
                print(f"::error title=Blocages {name}::{msg}", flush=True)
    (out_dir / "meta.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    merge(out_dir)
    return log


def load(out_dir: Path = OUT_DIR) -> list[dict]:
    with (out_dir / "blocking.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    """Boucle jusqu'à 5 h 30 : garde 3 requêtes en file, relève et commite au fil de l'eau (fait par le workflow)."""
    if not os.environ.get("CDSAPI_KEY"):
        print("CDSAPI_KEY absente : rien à faire")
        return 1
    limit = float(os.environ.get("BLOCKING_MAX_SECONDS", 5.5 * 3600))
    t0 = time.time()
    while True:
        log = collect()
        done = sum(1 for n in names() if (OUT_DIR / f"{n}.csv").exists())
        print(f"[{(time.time() - t0) / 60:.0f} min] {done}/{len(names())} années ; " + " | ".join(x for x in log if "relevé" in x or "ÉCHEC" in x or "soumise" in x), flush=True)
        if done == len(names()) or time.time() - t0 > limit:
            return 0
        time.sleep(120)


if __name__ == "__main__":
    sys.exit(main())
