"""Sonde P10.4b : température de la mer sur le domaine de la vapeur d'eau RSS (inventaire, aucun calcul).

Après le calcul officiel de P10.4 (écart C2), Grég a demandé un recadrage (D-AV, 20/11/2026) : comparer la vapeur
d'eau à la température de la mer **du même domaine**. Cette sonde vérifie quelles grilles de température de la mer
sont téléchargeables et si leur grille coïncide avec celle de RSS (1°). Elle n'estime aucune pente.
Usage : python -m etl.probe.p10e   → docs/sonde-p10e.md
"""

from __future__ import annotations

import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-p10e.md"
UA = {"User-Agent": "projet-evolution-climat"}
FILES = (
    ("OISST v2, 1°, mensuel (NOAA PSL)", "https://downloads.psl.noaa.gov/Datasets/noaa.oisst.v2/sst.mnmean.nc"),
    ("OISST v2, masque terre-mer 1° (NOAA PSL)", "https://downloads.psl.noaa.gov/Datasets/noaa.oisst.v2/lsmask.nc"),
    ("ERSST v5, 2°, mensuel (NOAA PSL)", "https://downloads.psl.noaa.gov/Datasets/noaa.ersst.v5/sst.mnmean.nc"),
    ("HadSST 4.2, 5°, mensuel, médiane (Met Office)",
     "https://www.metoffice.gov.uk/hadobs/hadsst4/data/netcdf/HadSST.4.2.0.0_median.nc"),
    ("RSS vapeur d'eau, 1° (grille de référence)", "https://data.remss.com/vapor/monthly_1deg/merged_vapor_1988-2025.nc"),
)
PAGES = ("https://psl.noaa.gov/data/gridded/data.noaa.oisst.v2.html",
         "https://psl.noaa.gov/data/gridded/data.noaa.ersst.v5.html")


def describe(path: Path) -> list[str]:
    import netCDF4
    import numpy as np
    out = []
    with netCDF4.Dataset(path) as ds:
        for name, v in ds.variables.items():
            out.append(f"{name} {v.dimensions} {v.shape} {getattr(v, 'units', '')} {getattr(v, 'long_name', '')}"[:200])
        for key in ("lat", "latitude"):
            if key in ds.variables:
                a = np.asarray(ds.variables[key][:], float)
                out.append(f"{key} : premier {a[0]}, dernier {a[-1]}, pas {a[1] - a[0]}, n = {len(a)}")
        for key in ("lon", "longitude"):
            if key in ds.variables:
                a = np.asarray(ds.variables[key][:], float)
                out.append(f"{key} : premier {a[0]}, dernier {a[-1]}, pas {a[1] - a[0]}, n = {len(a)}")
        if "time" in ds.variables:
            t = ds.variables["time"]
            out.append(f"time : unités « {getattr(t, 'units', '')} », premier {float(t[0])}, dernier {float(t[-1])}, n = {len(t)}")
        for a in ("title", "source", "references", "dataset_title", "comment"):
            if hasattr(ds, a):
                out.append(f"attribut {a} = {str(getattr(ds, a))[:200]}")
    return out


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P10.4b — température de la mer sur le domaine de la vapeur d'eau (généré)", "",
          f"Produit le {now} par `etl/probe/p10e.py`. Inventaire seulement : aucune pente, aucun rapport.", ""]
    for label, url in FILES:
        md.append(f"## {label}\n\n{url}\n")
        try:
            with tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp) / "f.nc"
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r, p.open("wb") as f:
                    modified = r.headers.get("Last-Modified")
                    while chunk := r.read(1 << 22):
                        f.write(chunk)
                md += [f"Statut : 200 ; {p.stat().st_size} o ; modifié {modified}", "", "```", *describe(p), "```", ""]
        except Exception as exc:  # noqa: BLE001
            md += [f"Statut : échec {type(exc).__name__} {str(exc)[:200]}", ""]
    for page in PAGES:
        try:
            with urllib.request.urlopen(urllib.request.Request(page, headers=UA), timeout=60) as r:
                html = r.read().decode("utf-8", "replace")
            import re
            text = re.sub(r"<[^>]+>", " ", html)
            text = re.sub(r"\s+", " ", text)
            keep = [m.group(0) for m in re.finditer(r"[^.]{0,160}(?:[Tt]emporal|[Cc]overage|[Rr]etire|[Dd]iscontinu|[Ss]patial)[^.]{0,160}\.", text)][:8]
            md += [f"**Page** {page} : 200", "", *[f"> {k.strip()}" for k in keep], ""]
        except Exception as exc:  # noqa: BLE001
            md += [f"**Page** {page} : échec {type(exc).__name__} {str(exc)[:200]}", ""]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
