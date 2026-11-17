"""Source : EN4.2.2 (Met Office Hadley Centre), température et salinité 0-700 m sur deux zones de l'Atlantique Nord (P9).

Choix fixés le 17/11/2026 avant tout calcul (docs/phases.md, P9 ; sonde docs/sonde-p9.md et docs/sonde-p9b.md) :
- **Zones** : grilles publiées par Caesar et al. (2018) (PIK) : gyre subpolaire `sg_grid.txt` (744 mailles de 1°)
  et région du Gulf Stream `gulfstream_grid.txt` (199 mailles). Centres des mailles en x,5° ; la grille EN4 est
  centrée sur les degrés entiers : chaque maille de Caesar couvre un quart de 4 mailles EN4. Le poids d'une maille
  EN4 est la part de sa surface couverte par la zone (0 à 1), multipliée par le cosinus de la latitude.
- **Couche 0-700 m** : niveaux EN4 pondérés par leur épaisseur (`depth_bnds`), coupée à 700 m.
- **Moyenne** : moyenne pondérée volume (surface × épaisseur) des valeurs présentes (mailles de terre exclues).
- Température en °C (EN4 la donne en kelvins), salinité sans unité (échelle pratique).
- Poids des observations (`temperature_observation_weights`, `salinity_observation_weights`) moyennés de la même façon :
  ils servent au critère N7 (année de début de la tendance), fixé avant toute lecture des températures et salinités.
Analyses `g10` (corrections XBT de Gouretski et Reseghetti, 2010), version la plus citée.
Licence : Non Commercial Government Licence v2 (Met Office) ; citation Good et al. (2013).

Sortie : data/sources/en4/en4-zones.csv (une ligne par mois et par zone) et une copie des deux grilles de Caesar.
Usage : python -m etl.sources.en4 [--years 1900-2026]
"""

from __future__ import annotations

import csv
import io
import os
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

import numpy as np

from etl.context import ROOT

OUT_DIR = ROOT / "data" / "sources" / "en4"
OUT = OUT_DIR / "en4-zones.csv"
LIST_URL = "https://www.metoffice.gov.uk/hadobs/en4/EN.4.2.2.analyses.g10.download-list.txt"
PIK = "https://www.pik-potsdam.de/~caesar/AMOC_slowdown/"
ZONES = {"gulf-stream": "gulfstream_grid.txt", "gyre-subpolaire": "sg_grid.txt"}
BOTTOM = 700.0
UA = {"User-Agent": "projet-evolution-climat (releve EN4 ; github.com/gregfs21-blip/projet-evolution-climat)"}
FIELDS = ["annee", "mois", "zone", "temperature_0_700", "salinite_0_700", "poids_obs_temperature", "poids_obs_salinite"]


def fetch(url: str, tries: int = 3) -> bytes:
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
                return r.read()
        except Exception:  # noqa: BLE001
            if k == tries - 1:
                raise
            time.sleep(20 * (k + 1))
    return b""


def read_grid(text: str) -> list[tuple[float, float]]:
    """Centres (lat, lon) des mailles de 1° d'un fichier de Caesar ; lignes de commentaire « # » ignorées."""
    cells = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 2 and not line.lstrip().startswith("#"):
            cells.append((float(parts[0]), float(parts[1])))
    return cells


def zone_weights(cells, lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    """Part (0 à 1) de chaque maille EN4 (centrée sur des degrés entiers) couverte par la zone, × cos(latitude).

    Une maille de Caesar centrée en (φ, λ) = (n + 0,5, m + 0,5) couvre un quart des mailles EN4 centrées en
    (n, m), (n + 1, m), (n, m + 1), (n + 1, m + 1). Longitudes EN4 en degrés est de 1 à 360."""
    frac = np.zeros((len(lat), len(lon)))
    ilat = {round(float(v), 3): i for i, v in enumerate(lat)}
    ilon = {round(float(v) % 360, 3): j for j, v in enumerate(lon)}
    for la, lo in cells:
        for dla in (-0.5, 0.5):
            for dlo in (-0.5, 0.5):
                i = ilat.get(round(la + dla, 3))
                j = ilon.get(round((lo + dlo) % 360, 3))
                if i is not None and j is not None:
                    frac[i, j] += 0.25
    return np.minimum(frac, 1.0) * np.cos(np.radians(lat))[:, None]


def layer_thickness(bounds: np.ndarray, bottom: float = BOTTOM) -> np.ndarray:
    """Épaisseur de chaque niveau comprise entre la surface et `bottom` (m) ; 0 pour les niveaux plus profonds."""
    top, bot = bounds[:, 0], np.minimum(bounds[:, 1], bottom)
    return np.clip(bot - top, 0.0, None)


def weighted_mean(field: np.ndarray, w2d: np.ndarray, dz: np.ndarray) -> float:
    """Moyenne pondérée volume d'un champ (niveau, lat, lon) ; valeurs absentes (NaN) exclues."""
    w = dz[:, None, None] * w2d[None, :, :]
    ok = np.isfinite(field) & (w > 0)
    tot = w[ok].sum()
    return float((field[ok] * w[ok]).sum() / tot) if tot > 0 else float("nan")


def month_rows(path: Path, weights: dict[str, np.ndarray] | None):
    """Lignes d'un fichier mensuel EN4. Les poids de zone sont calculés au premier fichier (grille fixe)."""
    import netCDF4

    with netCDF4.Dataset(path) as ds:
        lat, lon = np.asarray(ds["lat"][:], float), np.asarray(ds["lon"][:], float)
        dz = layer_thickness(np.asarray(ds["depth_bnds"][:], float))
        nlev = int(np.count_nonzero(dz))
        if weights is None:
            weights = {z: zone_weights(c, lat, lon) for z, c in GRIDS.items()}
        t = ds["time"]
        date = netCDF4.num2date(t[0], t.units)
        rows = []
        for zone, w2d in weights.items():
            ii = np.where(w2d.any(axis=1))[0]
            jj = np.where(w2d.any(axis=0))[0]
            sl = (0, slice(0, nlev), slice(ii.min(), ii.max() + 1), slice(jj.min(), jj.max() + 1))
            sub_w = w2d[ii.min():ii.max() + 1, jj.min():jj.max() + 1]
            vals = {}
            for name in ("temperature", "salinity", "temperature_observation_weights", "salinity_observation_weights"):
                a = np.ma.filled(ds[name][sl].astype(float), np.nan)
                vals[name] = weighted_mean(a, sub_w, dz[:nlev])
            rows.append({"annee": date.year, "mois": date.month, "zone": zone,
                         "temperature_0_700": round(vals["temperature"] - 273.15, 4),
                         "salinite_0_700": round(vals["salinity"], 4),
                         "poids_obs_temperature": round(vals["temperature_observation_weights"], 4),
                         "poids_obs_salinite": round(vals["salinity_observation_weights"], 4)})
    return rows, weights


GRIDS: dict[str, list[tuple[float, float]]] = {}


def load_grids() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for zone, name in ZONES.items():
        text = fetch(PIK + name).decode("latin-1")
        (OUT_DIR / name).write_text(text, encoding="utf-8")
        GRIDS[zone] = read_grid(text)
        print(f"zone {zone} : {len(GRIDS[zone])} mailles", flush=True)


def existing() -> dict[tuple[int, int, str], dict]:
    if not OUT.exists():
        return {}
    with OUT.open(encoding="utf-8") as f:
        return {(int(r["annee"]), int(r["mois"]), r["zone"]): r for r in csv.DictReader(f)}


def write(rows: dict) -> None:
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for key in sorted(rows):
            w.writerow({k: rows[key][k] for k in FIELDS})


def main(argv: list[str]) -> int:
    years = None
    if "--years" in argv:
        a, b = argv[argv.index("--years") + 1].split("-")
        years = range(int(a), int(b) + 1)
    load_grids()
    urls = fetch(LIST_URL).decode().split()
    rows = existing()
    done = {y for (y, _m, _z) in rows if sum(1 for k in rows if k[0] == y) == 24}
    weights = None
    budget = float(os.environ.get("EN4_MAX_SECONDS", "19000"))
    t0 = time.time()
    tmp = OUT_DIR / "_en4.nc"
    for url in urls:
        year = int(url.rsplit(".", 2)[-2])
        if (years and year not in years) or year in done:
            continue
        if time.time() - t0 > budget:
            print("budget de temps atteint", flush=True)
            break
        blob = fetch(url.replace("http://", "https://"))
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            for name in sorted(z.namelist()):
                tmp.write_bytes(z.read(name))
                new, weights = month_rows(tmp, weights)
                for r in new:
                    rows[(r["annee"], r["mois"], r["zone"])] = r
        tmp.unlink(missing_ok=True)
        write(rows)
        print(f"{year} : {sum(1 for k in rows if k[0] == year)} lignes ({time.time() - t0:.0f} s)", flush=True)
    write(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))


# ---------------------------------------------------------------- lecture par l'ETL (P9)

PAGE = "https://www.metoffice.gov.uk/hadobs/en4/"
LICENSE = "Non Commercial Government Licence v2 (Met Office), citation Good et al. (2013)"
SOURCE_NAME = "Met Office Hadley Centre — EN4.2.2, analyses objectives mensuelles (corrections g10)"
N7_WEIGHT = 0.5
MIN_MONTHS = 10
COLUMNS = {"temperature": ("temperature_0_700", "poids_obs_temperature"),
           "salinite": ("salinite_0_700", "poids_obs_salinite")}


def load_zone(zone: str, quantity: str) -> tuple[dict[int, float], dict[int, float]]:
    """Moyennes annuelles (année gardée si au moins 10 mois, N2) de la grandeur et du poids moyen des observations."""
    col, wcol = COLUMNS[quantity]
    vals: dict[int, list[float]] = {}
    wts: dict[int, list[float]] = {}
    with OUT.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["zone"] == zone and r[col] not in ("", "nan"):
                vals.setdefault(int(r["annee"]), []).append(float(r[col]))
                wts.setdefault(int(r["annee"]), []).append(float(r[wcol]))
    keep = [y for y, v in vals.items() if len(v) >= MIN_MONTHS]
    return ({y: sum(vals[y]) / len(vals[y]) for y in keep}, {y: sum(wts[y]) / len(wts[y]) for y in keep})


def n7_start(weights: dict[int, float], threshold: float = N7_WEIGHT) -> int | None:
    """Critère N7 : première année à partir de laquelle le poids moyen des observations reste ≥ `threshold`."""
    ys = sorted(weights)
    for i, y in enumerate(ys):
        if all(weights[k] >= threshold for k in ys[i:]):
            return y
    return None
