"""Source : données climatologiques de base quotidiennes de Météo-France (data.gouv.fr).

Jeu « Données climatologiques de base - quotidiennes » (Licence Ouverte 2.0). Un fichier CSV compressé
par département et par période (avant 1949, 1950-<année-1>, <année>-<année+1>), séparateur « ; ».
Colonnes utilisées (constat de la sonde du 23/10/2026) : NUM_POSTE, AAAAMMJJ, TN, QTN, TX, QTX, RR, QRR.
Q* est le code qualité de la valeur (1 : validée ; 9 : à confirmer dans la notice Météo-France).

Ces données ne sont PAS homogénéisées : un déplacement ou un changement d'instrument décale toute la
série. Elles ne servent aux tendances qu'après correction ou contrôle (etl/indicators/extremes.py).

La liste des fichiers est découverte par l'API data.gouv.fr (les noms changent avec les années) et
conservée dans le cache, avec les fichiers : en cas d'échec réseau, le cache est réutilisé.
"""

from __future__ import annotations

import csv
import gzip
import json
import logging
import os
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path

DATASET = "6569b51ae64326786e4e8e1a"
DATASET_URL = f"https://www.data.gouv.fr/datasets/{DATASET}"
API = f"https://www.data.gouv.fr/api/2/datasets/{DATASET}/resources/?page={{page}}&page_size=100&type=main"
SOURCE_NAME = "Météo-France — données climatologiques de base quotidiennes"
LICENSE = "Licence Ouverte 2.0 (Etalab)"
UA = {"User-Agent": "projet-evolution-climat"}

log = logging.getLogger("etl.quot")


@dataclass(frozen=True)
class Daily:
    value: float
    quality: str      # code qualité Météo-France tel quel ("1", "9", "0"…), "" si absent


def _offline() -> bool:
    return os.environ.get("QUOT_OFFLINE") == "1"


def _get(url: str, timeout: int = 300) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def _dir(raw_dir: Path) -> Path:
    d = raw_dir / "quot"
    d.mkdir(parents=True, exist_ok=True)
    return d


def is_department_file(title: str, department: str, kind: str = "RR-T-Vent") -> bool:
    """`kind` : « RR-T-Vent » (pluie, températures, vent) ou « autres-parametres » (pression, humidité…)."""
    return f"departement_{department}_" in title and kind in title


def resources(department: str, raw_dir: Path, kind: str = "RR-T-Vent") -> list[dict]:
    """Fichiers du département (« RR-T-Vent » ou « autres-parametres ») : découverts par l'API, ou lus en cache."""
    index = _dir(raw_dir) / (f"index-{department}.json" if kind == "RR-T-Vent" else f"index-{department}-{kind}.json")
    if not _offline():
        try:
            out, page = [], 1
            while True:
                data = json.loads(_get(API.format(page=page), timeout=60))
                items = data.get("data", [])
                out += [{"title": r["title"], "url": r["url"]} for r in items if is_department_file(r.get("title", ""), department, kind)]
                if not data.get("next_page") or not items:
                    break
                page += 1
            if not out:
                raise RuntimeError(f"aucun fichier quotidien pour le département {department}")
            index.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
            return out
        except Exception as exc:  # noqa: BLE001
            if not index.exists():
                raise RuntimeError(f"liste des fichiers quotidiens indisponible et aucun cache : {exc}") from exc
            log.warning("quotidien : API indisponible (%s), liste en cache réutilisée", exc)
    return json.loads(index.read_text(encoding="utf-8"))


def fetch(res: dict, raw_dir: Path) -> Path:
    name = re.sub(r"[^\w.\-]", "_", Path(res["url"]).name or res["title"])
    path = _dir(raw_dir) / name
    if _offline():
        if not path.exists():
            raise RuntimeError(f"mode hors ligne : {name} absent du cache")
        return path
    try:
        data = _get(res["url"])
        if name.endswith(".gz") and data[:2] != b"\x1f\x8b":
            raise ValueError("réponse qui n'est pas une archive gzip")
        path.write_bytes(data)
        log.info("quotidien : %s, %d octets", name, len(data))
    except Exception as exc:  # noqa: BLE001
        if not path.exists():
            raise RuntimeError(f"téléchargement de {name} impossible et aucun cache : {exc}") from exc
        log.warning("quotidien : %s non téléchargé (%s), cache réutilisé", name, exc)
    return path


def _rows(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", errors="replace", newline="") as f:
        yield from csv.reader(f, delimiter=";")


def load(department: str, postes: set[str], variables: tuple[str, ...], raw_dir: Path,
         kind: str = "RR-T-Vent") -> dict[str, dict[str, dict[str, Daily]]]:
    """poste → variable → date ISO (AAAA-MM-JJ) → valeur et code qualité. Jours absents : clé absente."""
    out: dict[str, dict[str, dict[str, Daily]]] = {p: {v: {} for v in variables} for p in postes}
    for res in resources(department, raw_dir, kind):
        rows = _rows(fetch(res, raw_dir))
        header = [h.strip() for h in next(rows)]
        idx = {h: i for i, h in enumerate(header)}
        missing = {"NUM_POSTE", "AAAAMMJJ", *variables} - idx.keys()
        if missing:
            raise ValueError(f"{res['title']} : colonnes absentes {sorted(missing)}")
        q = {v: idx.get(f"Q{v}") for v in variables}
        for row in rows:
            if len(row) < len(header):
                continue
            poste = row[idx["NUM_POSTE"]].strip()
            if poste not in out:
                continue
            d = row[idx["AAAAMMJJ"]].strip()
            if len(d) != 8:
                continue
            day = f"{d[:4]}-{d[4:6]}-{d[6:]}"
            for v in variables:
                raw = row[idx[v]].strip()
                if raw == "":
                    continue
                series = out[poste][v]
                if day in series:
                    raise ValueError(f"{res['title']} : jour dupliqué {poste} {day} {v}")
                series[day] = Daily(float(raw), row[q[v]].strip() if q[v] is not None else "")
    return out


def meta(department: str, postes: set[str], raw_dir: Path) -> dict[str, tuple[str, float, float, float]]:
    """Nom, latitude, longitude et altitude des postes, lus dans le fichier le plus récent du département."""
    res = sorted(resources(department, raw_dir), key=lambda r: r["title"])[-1]
    rows = _rows(fetch(res, raw_dir))
    header = [h.strip() for h in next(rows)]
    idx = {h: i for i, h in enumerate(header)}
    out: dict[str, tuple[str, float, float, float]] = {}
    for row in rows:
        p = row[idx["NUM_POSTE"]].strip() if len(row) >= len(header) else ""
        if p in postes and p not in out:
            out[p] = (row[idx["NOM_USUEL"]].strip(), float(row[idx["LAT"]]), float(row[idx["LON"]]), float(row[idx["ALTI"]]))
    return out
