"""Source : radiosondages IGRA v2 (NOAA NCEI), fichier « data-por » d'une station.

Format constaté par la sonde du 25/10/2026 (docs/sonde-largeur2.md) et décrit par la documentation IGRA v2 :
- en-tête de sondage : « #ID ANNÉE MOIS JOUR HEURE HEURE_LANCEMENT NB_NIVEAUX SOURCES LAT LON » ;
- niveau, colonnes fixes : type (1-2), temps écoulé (4-8), pression en Pa (10-15) et drapeau (16),
  géopotentiel en m (17-21) et drapeau (22), température en dixièmes de °C (23-27) et drapeau (28) ;
  −9999 = manquant, −8888 = retiré par le contrôle qualité ; drapeau « A » ou « B » = contrôle climatologique passé,
  blanc = non contrôlé.

Données BRUTES : aucune homogénéisation (changements de sondes, d'horaires et de corrections de rayonnement).
"""

from __future__ import annotations

import io
import os
import urllib.request
import zipfile
from pathlib import Path

URL = "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/data-por/{id}-data.txt.zip"
PAGE = "https://www.ncei.noaa.gov/products/weather-balloon/integrated-global-radiosonde-archive"
SOURCE_NAME = "NOAA NCEI — IGRA v2, radiosondages"
LICENSE = "Domaine public (NOAA)"
UA = {"User-Agent": "projet-evolution-climat"}
FLAGS_OK = (" ", "A", "B")


def fetch(station: str, raw_dir: Path) -> Path:
    path = raw_dir / "igra" / f"{station}-data.txt.zip"
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.environ.get("IGRA_OFFLINE") != "1":
        try:
            with urllib.request.urlopen(urllib.request.Request(URL.format(id=station), headers=UA), timeout=600) as r:
                data = r.read()
            zipfile.ZipFile(io.BytesIO(data)).testzip()
            path.write_bytes(data)
        except Exception as exc:  # noqa: BLE001
            if not path.exists():
                raise RuntimeError(f"IGRA {station} : téléchargement impossible et aucun cache : {exc}") from exc
    return path


def _int(s: str) -> int | None:
    s = s.strip()
    if not s or s in ("-9999", "-8888"):
        return None
    return int(s)


def parse(lines, levels: tuple[int, ...], hour: int) -> dict[int, dict[str, dict[tuple[int, int], list[float]]]]:
    """niveau (hPa) → « temp » (°C) ou « gph » (m) → (année, mois) → valeurs des sondages de l'heure nominale `hour`."""
    pa = {lvl * 100: lvl for lvl in levels}
    out: dict[int, dict[str, dict[tuple[int, int], list[float]]]] = {lvl: {"temp": {}, "gph": {}} for lvl in levels}
    keep = False
    ym = (0, 0)
    for ln in lines:
        if ln.startswith("#"):
            parts = ln.split()
            keep = len(parts) >= 5 and parts[4].isdigit() and int(parts[4]) == hour
            ym = (int(parts[1]), int(parts[2])) if keep else ym
            continue
        if not keep or len(ln) < 28:
            continue
        p = _int(ln[9:15])
        if p not in pa or ln[15] not in FLAGS_OK:
            continue
        lvl = pa[p]
        t, z = _int(ln[22:27]), _int(ln[16:21])
        if t is not None and ln[27] in FLAGS_OK:
            out[lvl]["temp"].setdefault(ym, []).append(t / 10)
        if z is not None and ln[21] in FLAGS_OK:
            out[lvl]["gph"].setdefault(ym, []).append(float(z))
    return out


def load(station: str, levels: tuple[int, ...], hour: int, raw_dir: Path):
    with zipfile.ZipFile(fetch(station, raw_dir)) as z:
        with z.open(z.namelist()[0]) as f:
            return parse((ln.decode("ascii", "replace").rstrip("\n") for ln in f), levels, hour)
