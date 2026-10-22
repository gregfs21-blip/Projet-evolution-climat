"""Source : Longues Séries Homogénéisées (LSH) de Météo-France.

Jeu publié sur data.gouv.fr (Licence Ouverte 2.0). Une archive zip par paramètre
(TN, TX, RR, IN) pour la métropole ; un fichier CSV par série dans l'archive.

Format d'un fichier (constaté le 22/10/2026) :
    # ... en-tête de métadonnées, lignes commençant par '#'
    YYYYMM;VALEUR;Q_HOM
    195301;-1.5;1
Q_HOM = 1 : valeur homogénéisée ; Q_HOM = 0 : prolongation par des données
mensuelles brutes, non homogénéisées. Ces dernières ne doivent servir ni aux
tendances ni aux normales.
"""

from __future__ import annotations

import io
import logging
import re
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from etl.schema import Period, Station

BASE_URL = "https://meteofrance.s3.sbg.io.cloud.ovh.net/data/synchro_ftp/REF_CC/LSH/"
DATASET_URL = "https://www.data.gouv.fr/datasets/6569b2c4f1937611d4c8b1a3"
LICENSE = "Licence Ouverte 2.0 (Etalab)"
SOURCE_NAME = "Météo-France — Longues Séries Homogénéisées (LSH)"

log = logging.getLogger("etl.lsh")


@dataclass(frozen=True)
class LshSeries:
    variable: str                      # "TN" ou "TX"
    station: Station
    values: dict[tuple[int, int], float] = field(repr=False)        # (année, mois) -> °C
    homogenized: dict[tuple[int, int], bool] = field(repr=False)    # (année, mois) -> Q_HOM == 1

    @property
    def series_id(self) -> str:
        return self.station.series_id or ""


def archive_path(variable: str, raw_dir: Path) -> Path:
    return raw_dir / "lsh" / f"SH_{variable}_metropole.zip"


def fetch_archive(variable: str, raw_dir: Path, timeout: int = 120) -> Path:
    """Télécharge l'archive du paramètre. En cas d'échec réseau, réutilise le cache s'il existe."""
    path = archive_path(variable, raw_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    url = f"{BASE_URL}SH_{variable}_metropole.zip"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "projet-evolution-climat"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
        zipfile.ZipFile(io.BytesIO(data)).testzip()  # archive corrompue → exception
        path.write_bytes(data)
        log.info("LSH %s : %d octets téléchargés", variable, len(data))
    except Exception as exc:  # noqa: BLE001
        if not path.exists():
            raise RuntimeError(f"téléchargement LSH {variable} impossible et aucun cache : {exc}") from exc
        log.warning("LSH %s : téléchargement impossible (%s), cache réutilisé", variable, exc)
    return path


_META = {
    "num_poste": re.compile(r"NUM_POSTE=\s*(\S+)"),
    "nom": re.compile(r"NOM_USUEL=\s*(.+?)\s*$"),
    "lat": re.compile(r"LATITUDE \(°\)\s*=\s*([-\d.]+)"),
    "lon": re.compile(r"LONGITUDE\(°\)\s*=\s*([-\d.]+)"),
    "alt": re.compile(r"ALTITUDE \(m\)\s*=\s*([-\d.]+)"),
    "serie": re.compile(r"NUM_SERIE=\s*(\S+)"),
    "amd": re.compile(r"Amplitude minimale détectable de la série\s*=\s*([-\d.]+)"),
    "periode": re.compile(r"Période homogénéisée\s*:\s*(\d{6})\s+(\d{6})"),
    "ruptures": re.compile(r"Date\(s\) de rupture\(s\) d'homogénéité\s*:\s*(.*)$"),
    "produit": re.compile(r"date de production du fichier le (\d{2}/\d{2}/\d{4})"),
}


def parse_file(text: str, variable: str) -> LshSeries:
    meta: dict[str, re.Match] = {}
    values: dict[tuple[int, int], float] = {}
    hom: dict[tuple[int, int], bool] = {}
    header_seen = False

    for line in text.splitlines():
        if line.startswith("#"):
            for key, rx in _META.items():
                if key not in meta and (m := rx.search(line)):
                    meta[key] = m
            continue
        if line.startswith("YYYYMM"):
            header_seen = True
            continue
        if not line.strip():
            continue
        ym, val, q = line.split(";")[:3]
        key = (int(ym[:4]), int(ym[4:6]))
        if key in values:
            raise ValueError(f"mois dupliqué {ym}")
        if val.strip() == "":
            continue  # mois manquant : on ne complète jamais
        values[key] = float(val)
        hom[key] = q.strip() == "1"

    missing = {"num_poste", "nom", "lat", "lon", "alt", "serie", "periode"} - meta.keys()
    if missing or not header_seen:
        raise ValueError(f"fichier LSH incomplet, métadonnées manquantes : {sorted(missing)}")

    p0, p1 = meta["periode"].group(1), meta["periode"].group(2)
    breaks_raw = meta["ruptures"].group(1).split() if "ruptures" in meta else []
    station = Station(
        id=meta["num_poste"].group(1),
        name=meta["nom"].group(1).title(),
        latitude=float(meta["lat"].group(1)),
        longitude=float(meta["lon"].group(1)),
        altitude=float(meta["alt"].group(1)),
        series_id=meta["serie"].group(1),
        homogenized_period=Period(start=int(p0[:4]), end=int(p1[:4])),
        min_detectable_amplitude=float(meta["amd"].group(1)) if "amd" in meta else None,
        homogenization_breaks=[f"{b[:4]}-{b[4:6]}" for b in breaks_raw if re.fullmatch(r"\d{6}", b)],
        file_produced=meta["produit"].group(1) if "produit" in meta else None,
    )
    return LshSeries(variable=variable, station=station, values=values, homogenized=hom)


def load_department(variable: str, department: str, raw_dir: Path, download: bool = True) -> list[LshSeries]:
    """Toutes les séries d'un département pour un paramètre, triées par identifiant de poste."""
    path = fetch_archive(variable, raw_dir) if download else archive_path(variable, raw_dir)
    out = []
    with zipfile.ZipFile(path) as z:
        for name in sorted(z.namelist()):
            # Nom : SH_M{VAR}{indice}{poste sur 8 chiffres}.csv ; le poste commence par le département.
            m = re.fullmatch(rf"SH_M{variable}\d(\d{{8}})\.csv", Path(name).name)
            if not m or not m.group(1).startswith(department):
                continue
            out.append(parse_file(z.read(name).decode("utf-8"), variable))
    out.sort(key=lambda s: s.station.id)
    return out
