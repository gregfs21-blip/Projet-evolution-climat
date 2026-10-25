"""Sonde Copernicus Climate Data Store (ERA5 niveaux de pression, moyennes mensuelles).

Vérifie l'accès (compte, clé, licence acceptée), le délai de file d'attente et le format réel des fichiers AVANT
d'écrire le lecteur. Aucun résultat climatique. La clé vient du secret GitHub CDSAPI_KEY : jamais affichée.
Usage : python -m etl.probe.cds   → écrit docs/sonde-cds.md
"""

from __future__ import annotations

import os
import sys
import tempfile
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-cds.md"
DATASET = "reanalysis-era5-pressure-levels-monthly-means"
BASE = {"product_type": ["monthly_averaged_reanalysis"], "time": ["00:00"], "data_format": "netcdf",
        "download_format": "unarchived"}

REQUESTS = [
    ("1. Point de Bordeaux, 3 variables × 3 niveaux, janvier 2024",
     {"variable": ["temperature", "geopotential", "u_component_of_wind"], "pressure_level": ["250", "500", "850"],
      "year": ["2024"], "month": ["01"], "area": [45.0, -1.0, 44.5, -0.5]}),
    ("2. Atlantique Nord (60° O-0°, 20-70° N), vent zonal 250 hPa, grille 1°, janvier 2024",
     {"variable": ["u_component_of_wind"], "pressure_level": ["250"], "year": ["2024"], "month": ["01"],
      "area": [70.0, -60.0, 20.0, 0.0], "grid": ["1.0", "1.0"]}),
    ("3. Globe, température 850 hPa, grille 2,5°, 12 mois de 2024",
     {"variable": ["temperature"], "pressure_level": ["850"], "year": ["2024"],
      "month": [f"{m:02d}" for m in range(1, 13)], "grid": ["2.5", "2.5"]}),
    ("4. Point de Bordeaux, température 850 hPa, 1940-2025 (série complète : délai réel de la file)",
     {"variable": ["temperature"], "pressure_level": ["850"], "year": [str(y) for y in range(1940, 2026)],
      "month": [f"{m:02d}" for m in range(1, 13)], "area": [45.0, -1.0, 44.5, -0.5]}),
]


def describe(path: Path) -> list[str]:
    data = path.read_bytes()
    lines = [f"{len(data) / 1e3:.0f} ko, début {data[:8]!r}"]
    try:
        import netCDF4
        with netCDF4.Dataset(path) as ds:
            lines.append("dimensions : " + ", ".join(f"{k}={len(v)}" for k, v in ds.dimensions.items()))
            for name, var in ds.variables.items():
                attrs = {a: getattr(var, a) for a in ("units", "long_name") if a in var.ncattrs()}
                head = var[:].ravel()[:4].tolist() if var.size else []
                lines.append(f"  {name} {var.dimensions} {var.shape} {attrs} : {head}")
    except Exception as exc:  # noqa: BLE001
        lines.append(f"lecture netCDF impossible : {type(exc).__name__} {exc}")
    return lines


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde Copernicus CDS — ERA5 niveaux de pression, moyennes mensuelles (généré)", "",
          f"Généré par `python -m etl.probe.cds` le {now}. Aucun calcul : accès, délais et format constatés.", "",
          f"Jeu de données : `{DATASET}`.", "",
          f"Clé présente dans l'environnement : **{'oui' if os.environ.get('CDSAPI_KEY') else 'NON'}** (jamais affichée)."]
    try:
        import cdsapi
        client = cdsapi.Client(url=os.environ.get("CDSAPI_URL", "https://cds.climate.copernicus.eu/api"),
                               key=os.environ.get("CDSAPI_KEY"), quiet=True, progress=False, timeout=600)
    except Exception as exc:  # noqa: BLE001
        md += ["", f"**Client cdsapi indisponible : {type(exc).__name__} {exc}**"]
        client = None
    if client:
        with tempfile.TemporaryDirectory() as tmp:
            for i, (title, req) in enumerate(REQUESTS):
                path = Path(tmp) / f"r{i}.nc"
                t0 = time.time()
                try:
                    client.retrieve(DATASET, {**BASE, **req}, str(path))
                    lines = [f"OK en {time.time() - t0:.0f} s"] + describe(path)
                except Exception as exc:  # noqa: BLE001
                    msg = str(exc).replace(os.environ.get("CDSAPI_KEY") or "§§", "***")
                    lines = [f"ÉCHEC après {time.time() - t0:.0f} s : {type(exc).__name__}", msg[:1500],
                             traceback.format_exc().splitlines()[-1][:300]]
                md += ["", f"### {title}", "", "```", *lines, "```"]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
