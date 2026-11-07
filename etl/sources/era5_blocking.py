"""Source : Z500 quotidien ERA5 pour les blocages euro-atlantiques (P7 ; choix fixés le 31/10/2026 avant calcul).

Format constaté par la sonde du 31/10/2026 (docs/sonde-p7.md) : jeu `derived-era5-pressure-levels-daily-statistics`,
netCDF, `z` (m² s⁻²) de dimensions (valid_time, pressure_level, latitude, longitude), latitudes décroissantes de 85 à
30° N, longitudes de −60 à 60° E, pas de 2,5° ; `valid_time` en jours depuis le 1er janvier de l'année.

Changement du 01/11/2026, AVANT tout calcul : le jeu des statistiques quotidiennes est calculé à la demande et trop lent
(6 semestres relevés en 5 h 30, soit plusieurs semaines pour 86 ans). Grég a choisi de garder la **moyenne quotidienne
des 4 échéances de 6 h** (UTC) : elle est calculée ici à partir du jeu horaire `reanalysis-era5-pressure-levels`
(0, 6, 12 et 18 UTC), ce que fait le produit quotidien de Copernicus ; requêtes de 2 ans (8 champs par jour sur
2 ans restent sous la taille acceptée pour 10 ans à une échéance, docs/sonde-p7c.md).
Le relevé n'écrit, pour chaque jour, que :
- `blocked` : chaîne de 0 et de 1, une par longitude de −60 à 60° E (critère de Tibaldi et Molteni, 1990) ;
- `z500_sector` : Z500 moyen de 35-70° N, 30° O-30° E (m), pondéré par le cosinus de la latitude.
Fichiers : data/sources/era5-pl/blocking-AAAA.csv (2 ans à partir de AAAA), réunis dans blocking.csv quand tout est là.
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

DATASET = "reanalysis-era5-pressure-levels"
OLD_DATASET = "derived-era5-pressure-levels-daily-statistics"     # travaux encore en file : supprimés au relevé
PAGE = "https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels"
SOURCE_NAME = "ECMWF / Copernicus — ERA5 horaire sur niveaux de pression (Z500, moyenne quotidienne de 0, 6, 12 et 18 UTC)"
TIMES = ["00:00", "06:00", "12:00", "18:00"]
CHUNK = 2
OUT_DIR = cds.OUT_DIR
FIRST_YEAR = 1940
G0 = 9.80665
PHI = (80.0, 60.0, 40.0)        # φN, φ0, φS
DELTAS = (-5.0, 0.0, 5.0)
GHGN_MAX = -10.0                # m par degré de latitude
SECTOR_Z = (35.0, 70.0, -30.0, 30.0)
MAX_PENDING = 3


def names() -> list[str]:
    return [f"blocking-{y}" for y in range(FIRST_YEAR, cds.last_year() + 1, CHUNK)]


def years_of(name: str) -> list[str]:
    y0 = int(name.split("-")[1][:4])
    return [str(y) for y in range(y0, min(y0 + CHUNK, cds.last_year() + 1))]


def request(name: str) -> dict:
    return {"product_type": ["reanalysis"], "variable": ["geopotential"], "pressure_level": ["500"],
            "year": years_of(name), "month": [f"{m:02d}" for m in range(1, 13)],
            "day": [f"{d:02d}" for d in range(1, 32)], "time": TIMES, "area": [85, -60, 30, 60],
            "grid": ["2.5", "2.5"], "data_format": "netcdf", "download_format": "unarchived"}


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


def daily_mean(z: np.ndarray, valid_time: np.ndarray) -> tuple[list[str], np.ndarray]:
    """Moyenne par jour civil (UTC) des échéances présentes ; un jour n'est gardé que si ses 4 échéances existent."""
    days = [datetime.fromtimestamp(int(t), tz=timezone.utc).strftime("%Y-%m-%d") for t in valid_time]
    keep, out = [], []
    for d in sorted(set(days)):
        idx = [i for i, x in enumerate(days) if x == d]
        if len(idx) == len(TIMES):
            keep.append(d)
            out.append(z[idx].mean(axis=0))
    return keep, np.asarray(out)


def extract(arrays: dict[str, np.ndarray]) -> list[dict]:
    lat = np.asarray(arrays["latitude"], dtype=float)
    lon = np.asarray(arrays["longitude"], dtype=float)
    lon = np.where(lon > 180, lon - 360, lon)
    z = np.asarray(arrays["z"], dtype=float)
    if z.ndim == 4:
        z = z[:, 0]
    z = z / G0
    order = np.argsort(lon)
    lon, z = lon[order], z[:, :, order]
    days, zd = daily_mean(z, np.asarray(arrays["valid_time"]))
    rows = []
    for day, f in zip(days, zd):
        if not np.isfinite(f).all():
            continue
        b = blocked_longitudes(f, lat)
        rows.append({"day": day, "blocked": "".join("1" if x else "0" for x in b),
                     "z500_sector": round(sector_mean(f, lat, lon), 2)})
    return rows


# ---------------------------------------------------------------- relevé
#
# Mise à jour annuelle (décision de Grég du 07/11/2026) : le workflow « Blocages » tourne chaque 15 janvier. La
# dernière tranche de 2 ans peut n'avoir été relevée que pour sa première année : une tranche n'est tenue pour faite
# que si son fichier va jusqu'à la dernière année qu'elle doit couvrir.


def chunk_complete(name: str, out_dir: Path = OUT_DIR) -> bool:
    path = out_dir / f"{name}.csv"
    if not path.exists():
        return False
    last = None
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            last = row["day"]
    return last is not None and last >= f"{years_of(name)[-1]}-12-31"


def complete(out_dir: Path = OUT_DIR) -> bool:
    return all(chunk_complete(n, out_dir) for n in names()) and (out_dir / "blocking.csv").exists()


def merge(out_dir: Path = OUT_DIR) -> None:
    parts = [out_dir / f"{n}.csv" for n in names()]
    if not all(chunk_complete(n, out_dir) for n in names()):
        return
    rows = []
    for p in parts:
        with p.open(encoding="utf-8") as f:
            rows += list(csv.DictReader(f))
    cds._write_csv(out_dir / "blocking.csv", sorted(rows, key=lambda r: r["day"]))


def collect(out_dir: Path = OUT_DIR) -> list[str]:
    log = []
    all_jobs = cds._call("jobs?limit=100").get("jobs", [])
    for j in all_jobs:                      # anciens travaux (statistiques quotidiennes) : libèrent la file
        if j.get("processID") == OLD_DATASET and j.get("status") in ("accepted", "running"):
            try:
                cds._call(f"jobs/{j['jobID']}", "DELETE")
                log.append(f"ancien travail {j['jobID']} supprimé")
            except Exception as exc:  # noqa: BLE001
                log.append(f"suppression {j['jobID']} : {exc}")
    all_jobs = cds._call("jobs?limit=100").get("jobs", [])
    for j in all_jobs:                      # essai à 12 UTC seulement (abandonné) : libère la file
        if j.get("processID") == DATASET and j.get("status") in ("accepted", "running"):
            try:
                ids = cds._call(f"jobs/{j['jobID']}?request=true").get("metadata", {}).get("request", {}).get("ids", {})
                if [str(x) for x in ids.get("time", [])] != TIMES:
                    cds._call(f"jobs/{j['jobID']}", "DELETE")
                    log.append(f"travail à 12 UTC {j['jobID']} supprimé")
            except Exception as exc:  # noqa: BLE001
                log.append(f"suppression {j['jobID']} : {exc}")
    all_jobs = cds._call("jobs?limit=100").get("jobs", [])
    jobs = [j for j in all_jobs if j.get("processID") == DATASET]
    key_of = {}
    for j in jobs:
        if j.get("status") in ("accepted", "running", "successful"):
            try:
                ids = cds._call(f"jobs/{j['jobID']}?request=true").get("metadata", {}).get("request", {}).get("ids", {})
                key_of[j["jobID"]] = ([str(x) for x in ids.get("year", [])], [str(x) for x in ids.get("time", [])],
                                      [str(x) for x in ids.get("area", [])])
            except Exception:  # noqa: BLE001
                pass
    pending = [j for j in all_jobs if j.get("status") in ("accepted", "running")]
    m = cds.meta(out_dir)
    for name in names():
        if chunk_complete(name, out_dir) and name in m:
            continue
        req = request(name)
        key = (req["year"], req["time"], [str(x) for x in req["area"]])
        mine = [j for j in jobs if key_of.get(j["jobID"]) == key]
        done = sorted((j for j in mine if j["status"] == "successful"), key=lambda j: j.get("finished") or "")
        try:
            if done:
                job = done[-1]
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "r.nc"
                    cds._download(cds._call(f"jobs/{job['jobID']}/results")["asset"]["value"]["href"], path)
                    rows = extract(cds.read_nc(path))
                if len(rows) < 365 * len(req["year"]):
                    raise ValueError(f"{len(rows)} jours seulement")
                cds._write_csv(out_dir / f"{name}.csv", rows)
                m[name] = {"job": job["jobID"], "rows": len(rows), "collected": datetime.now(timezone.utc).isoformat()}
                log.append(f"{name} : relevé, {len(rows)} jours")
            elif any(j["status"] in ("accepted", "running") for j in mine):
                log.append(f"{name} : en file")
            elif len(pending) < MAX_PENDING:
                job = cds._call(f"processes/{DATASET}/execution", "POST", {"inputs": req})
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
        try:
            log = collect()
        except Exception as exc:  # noqa: BLE001 — panne passagère de Copernicus (HTTP 500 vu le 06/11/2026) : on réessaie
            log = [f"ÉCHEC de la lecture de la file : {type(exc).__name__} {str(exc)[:200]}"]
        done = sum(1 for n in names() if chunk_complete(n))
        print(f"[{(time.time() - t0) / 60:.0f} min] {done}/{len(names())} tranches de 2 ans ; " + " | ".join(x for x in log if "relevé" in x or "ÉCHEC" in x or "soumise" in x or "supprimé" in x), flush=True)
        if done == len(names()) or time.time() - t0 > limit:
            return 0
        time.sleep(120)


if __name__ == "__main__":
    sys.exit(main())
