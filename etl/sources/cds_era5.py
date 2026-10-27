"""Source : ERA5, moyennes mensuelles sur niveaux de pression (Copernicus Climate Data Store).

Format constaté par la sonde du 26/10/2026 (docs/sonde-cds.md) : netCDF4 (HDF5), dimensions
`valid_time` (secondes depuis 1970), `pressure_level` (hPa), `latitude`, `longitude` ; variables `t` (K),
`z` (géopotentiel, m² s⁻²) et `u` (vent zonal, m s⁻¹).

Le CDS traite une requête en plusieurs heures (file de 3 à 7 h constatée les 25-26/10/2026) et refuse au-delà de
trois requêtes en attente par utilisateur. D'où deux temps, sans jamais attendre :
1. `collect()` (workflow « Copernicus », quotidien) : relève les travaux aboutis, en extrait de petites séries
   (CSV de quelques centaines de ko) commitées dans `data/sources/era5-pl/`, et soumet les requêtes manquantes ;
2. l'ETL ne lit que ces CSV : aucun appel réseau, aucune attente.

La clé vient de la variable d'environnement CDSAPI_KEY (secret du dépôt) et n'est jamais écrite nulle part.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

from etl.context import ROOT

API = os.environ.get("CDSAPI_URL", "https://cds.climate.copernicus.eu/api")
DATASET = "reanalysis-era5-pressure-levels-monthly-means"
PAGE = "https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels-monthly-means"
SOURCE_NAME = "ECMWF / Copernicus — ERA5, moyennes mensuelles sur niveaux de pression (Climate Data Store)"
LICENSE = "Licence d'utilisation des produits Copernicus (CC BY 4.0)"
OUT_DIR = ROOT / "data" / "sources" / "era5-pl"
G0 = 9.80665                       # m s⁻² : géopotentiel → altitude géopotentielle
FIRST_YEAR = 1940
MAX_PENDING = 3                    # au-delà, le CDS rejette (constaté le 26/10/2026)
MAX_MB = 500

BASE = {"product_type": ["monthly_averaged_reanalysis"], "time": ["00:00"], "data_format": "netcdf",
        "download_format": "unarchived"}
BORDEAUX = (44.75, -0.75)          # maille ERA5 0,25° la plus proche de Bordeaux-Mérignac (44,83° N ; 0,69° O)
JET_BOX = [70.0, -60.0, 20.0, 0.0]  # N, O, S, E : Atlantique Nord, 60° O-0°, 20-70° N


def last_year() -> int:
    return datetime.now(timezone.utc).year - 1


SINGLE = "reanalysis-era5-single-levels-monthly-means"
SST_BOXES = {                       # N, O, S, E — fixées le 27/10/2026 (P3), avant tout calcul
    "sst-large-gironde": [46.0, -3.0, 44.0, -1.0],     # au large de la Gironde
    "sst-golfe-gascogne": [48.0, -10.0, 43.5, -1.0],   # golfe entier, pour la référence R8
}


ALTI = "satellite-sea-level-global"
ALTI_BOX = [46.5, -3.0, 44.0, -1.0]   # au large de la Gironde, 0,25° (P3, 27/10/2026)
ALTI_FIRST = 1993
ALTI_CHUNK = 4                        # années par requête : 33 ans d'un coup dépassent la limite de coût du CDS (27/10/2026)


def alti_names() -> list[str]:
    return [f"alti-gironde-{y}" for y in range(ALTI_FIRST, last_year() + 1, ALTI_CHUNK)]


def datasets() -> dict[str, str]:
    """Jeu de données CDS de chaque requête (par défaut : niveaux de pression)."""
    return {**{name: SINGLE for name in SST_BOXES}, **{name: ALTI for name in alti_names()}}


def requests() -> dict[str, dict]:
    years = [str(y) for y in range(FIRST_YEAR, last_year() + 1)]
    months = [f"{m:02d}" for m in range(1, 13)]
    sst = {name: {**BASE, "variable": ["sea_surface_temperature"], "year": years, "month": months, "area": box}
           for name, box in SST_BOXES.items()}
    alti = {name: {"variable": ["monthly_mean"],
                   "year": [str(y) for y in range(int(name[-4:]), min(int(name[-4:]) + ALTI_CHUNK, last_year() + 1))],
                   "month": months, "version": ["vdt2024"], "area": ALTI_BOX} for name in alti_names()}
    return {**sst, **alti,
        "bordeaux": {**BASE, "variable": ["temperature", "geopotential", "u_component_of_wind"],
                     "pressure_level": ["250", "500", "850"], "year": years, "month": months,
                     "area": [45.0, -1.0, 44.5, -0.5]},
        "atlantique-u250": {**BASE, "variable": ["u_component_of_wind"], "pressure_level": ["250"], "year": years,
                            "month": months, "area": JET_BOX, "grid": ["1.0", "1.0"]},
        # Vent zonal à 850 hPa, 0-60° O, 15-75° N (Woollings et al., 2010) : jet « des tempêtes », séparé du jet
        # subtropical. Demandé le 26/10/2026 après le constat que le profil à 250 hPa a deux maxima (voir phases.md) ;
        # indice retenu par Grég le 26/10/2026 (après la distribution à 250 hPa, avant tout calcul de tendance).
        "atlantique-u850": {**BASE, "variable": ["u_component_of_wind"], "pressure_level": ["850"], "year": years,
                            "month": months, "area": [75.0, -60.0, 15.0, 0.0], "grid": ["1.0", "1.0"]},
    }


# ---------------------------------------------------------------- extraction (pure, testable sans netCDF)


def months_of(valid_time: np.ndarray) -> list[str]:
    return [datetime.fromtimestamp(int(s), tz=timezone.utc).strftime("%Y-%m") for s in valid_time]


def _nearest(values: np.ndarray, target: float) -> int:
    return int(np.argmin(np.abs(np.asarray(values, dtype=float) - target)))


def extract_point(arrays: dict[str, np.ndarray], lat0: float, lon0: float) -> list[dict]:
    """Une ligne par mois et par niveau : t en °C, z en m (altitude géopotentielle), u en m/s, à la maille la plus proche."""
    i, j = _nearest(arrays["latitude"], lat0), _nearest(arrays["longitude"], lon0)
    rows = []
    for k, month in enumerate(months_of(arrays["valid_time"])):
        for li, lvl in enumerate(arrays["pressure_level"]):
            rows.append({"month": month, "level": int(lvl),
                         "t_c": round(float(arrays["t"][k, li, i, j]) - 273.15, 3),
                         "z_m": round(float(arrays["z"][k, li, i, j]) / G0, 1),
                         "u_ms": round(float(arrays["u"][k, li, i, j]), 3)})
    return rows


def extract_zonal(arrays: dict[str, np.ndarray]) -> list[dict]:
    """Vent zonal moyenné sur les longitudes de la boîte : une ligne par mois et par latitude."""
    u = np.asarray(arrays["u"], dtype=float)
    if u.ndim == 4:                       # (temps, niveau, lat, lon) : un seul niveau demandé
        u = u[:, 0]
    zonal = np.nanmean(u, axis=2)         # (temps, lat)
    rows = []
    for k, month in enumerate(months_of(arrays["valid_time"])):
        for li, lat in enumerate(arrays["latitude"]):
            rows.append({"month": month, "lat": round(float(lat), 2), "u_ms": round(float(zonal[k, li]), 3)})
    return rows


def read_nc(path: Path) -> dict[str, np.ndarray]:
    """Valeurs masquées (terre pour la SST) rendues en NaN, jamais en valeur de remplissage."""
    import netCDF4
    out = {}
    with netCDF4.Dataset(path) as ds:
        for name in ds.variables:
            if name in ("valid_time", "pressure_level", "latitude", "longitude"):
                out[name] = np.asarray(ds.variables[name][:])
            elif name in ("t", "z", "u", "sst"):
                out[name] = np.ma.filled(np.ma.asarray(ds.variables[name][:], dtype=float), np.nan)
    return out


def extract_alti(zip_path: Path) -> list[dict]:
    """Archive zip d'un fichier netCDF par mois (format constaté le 27/10/2026) : anomalie du niveau de la mer
    (sla, m) moyennée sur la zone, pondérée par cos(latitude), en mm."""
    import zipfile
    import netCDF4
    rows = []
    with zipfile.ZipFile(zip_path) as z, tempfile.TemporaryDirectory() as tmp:
        for name in sorted(z.namelist()):
            if not name.endswith(".nc"):
                continue
            path = Path(tmp) / "m.nc"
            path.write_bytes(z.read(name))
            with netCDF4.Dataset(path) as ds:
                sla = np.ma.filled(np.ma.asarray(ds.variables["sla"][:], dtype=float), np.nan)[0]
                lat = np.asarray(ds.variables["latitude"][:], dtype=float)
                days = float(ds.variables["time"][0])
            month = (datetime(1950, 1, 1) + timedelta(days=days)).strftime("%Y-%m")
            w = np.cos(np.radians(lat))[:, None] * np.ones(sla.shape[1])
            ok = np.isfinite(sla)
            if ok.sum():
                rows.append({"month": month, "sla_mm": round(float((sla[ok] * w[ok]).sum() / w[ok].sum()) * 1000, 2),
                             "cells": int(ok.sum())})
    return sorted(rows, key=lambda r: r["month"])


def load_alti(out_dir: Path = OUT_DIR) -> dict[str, float]:
    with (out_dir / "alti-gironde.csv").open(encoding="utf-8") as f:
        return {r["month"]: float(r["sla_mm"]) for r in csv.DictReader(f)}


def extract_area_mean(arrays: dict[str, np.ndarray], var: str = "sst") -> list[dict]:
    """Moyenne pondérée par cos(latitude) des mailles de mer, en °C ; une ligne par mois (mois sans maille : écarté)."""
    x = np.asarray(arrays[var], dtype=float)
    if x.ndim == 4:
        x = x[:, 0]
    w = np.cos(np.radians(np.asarray(arrays["latitude"], dtype=float)))[:, None] * np.ones(x.shape[2])
    rows = []
    for k, month in enumerate(months_of(arrays["valid_time"])):
        ok = np.isfinite(x[k])
        if ok.sum() == 0:
            continue
        rows.append({"month": month, "sst_c": round(float((x[k][ok] * w[ok]).sum() / w[ok].sum()) - 273.15, 3),
                     "cells": int(ok.sum())})
    return rows


# ---------------------------------------------------------------- lecture des CSV commités (utilisée par l'ETL)


def load_point(out_dir: Path = OUT_DIR) -> dict[int, dict[str, dict[str, float]]]:
    """niveau → grandeur (t_c, z_m, u_ms) → mois « AAAA-MM » → valeur."""
    out: dict[int, dict[str, dict[str, float]]] = {}
    with (out_dir / "bordeaux.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            lvl = out.setdefault(int(r["level"]), {"t_c": {}, "z_m": {}, "u_ms": {}})
            for k in lvl:
                lvl[k][r["month"]] = float(r[k])
    return out


def load_zonal(out_dir: Path = OUT_DIR, name: str = "atlantique-u850") -> dict[str, dict[float, float]]:
    """mois « AAAA-MM » → latitude → vent zonal moyen (m/s). Par défaut 850 hPa (indice retenu le 26/10/2026)."""
    out: dict[str, dict[float, float]] = {}
    with (out_dir / f"{name}.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["month"], {})[float(r["lat"])] = float(r["u_ms"])
    return out


def meta(out_dir: Path = OUT_DIR) -> dict:
    path = out_dir / "meta.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


# ---------------------------------------------------------------- relevé et soumission (workflow « Copernicus »)


def _call(path: str, method: str = "GET", body: dict | None = None) -> dict:
    req = urllib.request.Request(f"{API}/retrieve/v1/{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"PRIVATE-TOKEN": os.environ.get("CDSAPI_KEY", ""),
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as exc:          # motif du refus (licence, quota…) dans le journal
        raise RuntimeError(f"HTTP {exc.code} : {exc.read()[:400].decode('utf-8', 'replace')}") from exc


def _same(a: dict, b: dict) -> bool:
    keys = ("variable", "pressure_level", "year", "month", "area", "grid")
    norm = lambda d, k: [str(x) for x in d.get(k, [])]  # noqa: E731
    return all(norm(a, k) == norm(b, k) for k in keys)


def _download(href: str, path: Path, max_seconds: int = 900) -> None:
    t0 = time.time()
    req = urllib.request.Request(href, headers={"PRIVATE-TOKEN": os.environ.get("CDSAPI_KEY", "")})
    with urllib.request.urlopen(req, timeout=60) as r, path.open("wb") as f:
        total = r.headers.get("Content-Length")
        if total and int(total) > MAX_MB * 1e6:
            raise ValueError(f"résultat de {int(total) / 1e6:.0f} Mo, au-delà de {MAX_MB} Mo")
        while chunk := r.read(1 << 20):
            f.write(chunk)
            if time.time() - t0 > max_seconds:
                raise TimeoutError(f"téléchargement interrompu après {max_seconds} s")


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def collect(out_dir: Path = OUT_DIR) -> list[str]:
    """Relève les travaux aboutis, écrit les CSV, soumet ce qui manque. Renvoie un journal lisible."""
    out_dir.mkdir(parents=True, exist_ok=True)
    log: list[str] = []
    jobs = _call("jobs?limit=100").get("jobs", [])
    details = {}
    for j in jobs:
        if j.get("status") in ("accepted", "running", "successful"):
            try:
                details[j["jobID"]] = _call(f"jobs/{j['jobID']}?request=true").get("metadata", {}).get("request", {}).get("ids", {})
            except Exception:  # noqa: BLE001
                details[j["jobID"]] = {}
    pending = [j for j in jobs if j.get("status") in ("accepted", "running")]
    m = meta(out_dir)
    ds_of = datasets()
    for name, req in requests().items():
        try:
            log.append(_one(name, req, ds_of.get(name, DATASET), jobs, details, pending, m, out_dir))
        except Exception as exc:  # noqa: BLE001 — une requête en échec ne bloque pas les autres
            msg = f"{name} : ÉCHEC {type(exc).__name__} {str(exc)[:400]}"
            log.append(msg)
            if os.environ.get("GITHUB_ACTIONS") == "true":
                print(f"::error title=Copernicus {name}::{msg}", flush=True)
    (out_dir / "meta.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    merge_alti(out_dir)
    return log


def merge_alti(out_dir: Path = OUT_DIR) -> None:
    """Réunit les morceaux d'altimétrie relevés dans alti-gironde.csv (seulement si tous sont là : pas de trou)."""
    parts = [out_dir / f"{n}.csv" for n in alti_names()]
    if not all(p.exists() for p in parts):
        return
    rows = []
    for p in parts:
        with p.open(encoding="utf-8") as f:
            rows += list(csv.DictReader(f))
    rows = sorted({r["month"]: r for r in rows}.values(), key=lambda r: r["month"])
    _write_csv(out_dir / "alti-gironde.csv", rows)


def _one(name: str, req: dict, dataset: str, jobs: list, details: dict, pending: list, m: dict, out_dir: Path) -> str:
    mine = [j for j in jobs if j["jobID"] in details and j.get("processID", dataset) == dataset
            and _same(details[j["jobID"]], req)]
    done = sorted((j for j in mine if j["status"] == "successful"), key=lambda j: j.get("finished") or "")
    if done:
        job = done[-1]
        if m.get(name, {}).get("job") == job["jobID"]:
            return f"{name} : à jour (travail {job['jobID']})"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "r.nc"
            href = _call(f"jobs/{job['jobID']}/results")["asset"]["value"]["href"]
            _download(href, path)
            if name.startswith("alti-gironde"):
                rows = extract_alti(path)
            else:
                arrays = read_nc(path)
                rows = (extract_point(arrays, *BORDEAUX) if name == "bordeaux"
                        else extract_area_mean(arrays) if name in SST_BOXES else extract_zonal(arrays))
        _write_csv(out_dir / f"{name}.csv", rows)
        m[name] = {"job": job["jobID"], "finished": job.get("finished"), "rows": len(rows),
                   "years": [req["year"][0], req["year"][-1]], "collected": datetime.now(timezone.utc).isoformat()}
        return f"{name} : relevé, {len(rows)} lignes (travail {job['jobID']})"
    elif any(j["status"] in ("accepted", "running") for j in mine):
        return f"{name} : en file chez Copernicus"
    elif len(pending) >= MAX_PENDING:
        return f"{name} : non soumise, {len(pending)} requêtes déjà en attente"
    else:
        job = _call(f"processes/{dataset}/execution", "POST", {"inputs": req})
        pending.append(job)
        return f"{name} : soumise (travail {job.get('jobID')})"


def main() -> int:
    if not os.environ.get("CDSAPI_KEY"):
        print("CDSAPI_KEY absente : rien à faire")
        return 1
    # Plusieurs passages tant que des requêtes viennent d'être soumises ou attendent (l'altimétrie aboutit en
    # quelques dizaines de secondes) ; au plus 20 minutes, sans jamais dépendre de ce délai.
    t0 = time.time()
    while True:
        log = collect()
        print("\n".join(log), flush=True)
        busy = [x for x in log if "soumise (" in x or "en file" in x]
        if not busy or time.time() - t0 > 20 * 60:
            return 0
        time.sleep(90)


if __name__ == "__main__":
    sys.exit(main())


def load_sst(name: str, out_dir: Path = OUT_DIR) -> dict[str, float]:
    """mois « AAAA-MM » → SST moyenne de la boîte (°C)."""
    with (out_dir / f"{name}.csv").open(encoding="utf-8") as f:
        return {r["month"]: float(r["sst_c"]) for r in csv.DictReader(f)}
