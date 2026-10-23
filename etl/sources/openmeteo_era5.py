"""Source : réanalyse ERA5 (ECMWF / Copernicus) via l'API archive d'Open-Meteo.

`models=era5` force la seule réanalyse ERA5 (maille 0,25°), sans le mélange de modèles
« best match » d'Open-Meteo, inadapté à l'étude de tendances. Les valeurs quotidiennes
sont des agrégats sur 24 h des valeurs horaires, dans le fuseau demandé.

Licence : données ERA5 sous licence Copernicus (CC BY 4.0), service Open-Meteo gratuit
pour un usage non commercial. Mention : « Generated using Copernicus Climate Change
Service information » ; Hersbach et al. (2020), The ERA5 global reanalysis.
"""

from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path

API = "https://archive-api.open-meteo.com/v1/archive"
SOURCE_NAME = "ERA5 (ECMWF / Copernicus) via Open-Meteo"
LICENSE = "CC BY 4.0 (Copernicus) ; Open-Meteo, usage non commercial"
VARIABLES = ("temperature_2m_max", "temperature_2m_min")

log = logging.getLogger("etl.era5")


@dataclass(frozen=True)
class Era5Daily:
    requested: tuple[float, float]
    cell_lat: float
    cell_lon: float
    elevation: float
    tmax: dict[date, float]
    tmin: dict[date, float]


def cache_path(raw_dir: Path, lat: float, lon: float, start: str, end: str) -> Path:
    return raw_dir / "era5" / f"era5_{lat:.3f}_{lon:.3f}_{start}_{end}.json"


def _download(lat: float, lon: float, start: str, end: str, timeout: int) -> dict:
    query = urllib.parse.urlencode({
        "latitude": f"{lat:.3f}",
        "longitude": f"{lon:.3f}",
        "start_date": start,
        "end_date": end,
        "daily": ",".join(VARIABLES),
        "models": "era5",
        "timezone": "Europe/Paris",
    })
    req = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": "projet-evolution-climat"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def fetch_daily(lat: float, lon: float, start: str, end: str, raw_dir: Path, download: bool = True,
                timeout: int = 180) -> Era5Daily:
    path = cache_path(raw_dir, lat, lon, start, end)
    path.parent.mkdir(parents=True, exist_ok=True)
    if download:
        try:
            payload = _download(lat, lon, start, end, timeout)
            if "daily" not in payload:
                raise RuntimeError(f"réponse Open-Meteo sans données quotidiennes : {str(payload)[:300]}")
            path.write_text(json.dumps(payload), encoding="utf-8")
            log.info("ERA5 %.3f,%.3f %s→%s téléchargé", lat, lon, start, end)
        except Exception as exc:  # noqa: BLE001
            if not path.exists():
                raise RuntimeError(f"ERA5 indisponible et aucun cache : {exc}") from exc
            log.warning("ERA5 : téléchargement impossible (%s), cache réutilisé", exc)
    return parse(json.loads(path.read_text(encoding="utf-8")), (lat, lon))


def _column(daily: dict, name: str) -> list:
    # Un seul modèle demandé : clé simple ; plusieurs modèles : clé suffixée par le modèle.
    for key in (name, f"{name}_era5"):
        if key in daily:
            return daily[key]
    raise KeyError(f"variable {name} absente de la réponse ERA5")


def parse(payload: dict, requested: tuple[float, float]) -> Era5Daily:
    daily = payload["daily"]
    days = [date.fromisoformat(t) for t in daily["time"]]
    tmax, tmin = _column(daily, "temperature_2m_max"), _column(daily, "temperature_2m_min")
    if not (len(days) == len(tmax) == len(tmin)):
        raise ValueError("réponse ERA5 incohérente : colonnes de longueurs différentes")
    return Era5Daily(
        requested=requested,
        cell_lat=float(payload["latitude"]),
        cell_lon=float(payload["longitude"]),
        elevation=float(payload.get("elevation", float("nan"))),
        tmax={d: float(v) for d, v in zip(days, tmax) if v is not None},   # valeur nulle : jour manquant
        tmin={d: float(v) for d, v in zip(days, tmin) if v is not None},
    )


def monthly_means(data: Era5Daily) -> dict[str, dict[tuple[int, int], float]]:
    """TN, TX et TM mensuelles. Un mois n'est calculé que si tous ses jours sont présents."""
    by_month: dict[tuple[int, int], list[date]] = {}
    for d in data.tmax.keys() | data.tmin.keys():
        by_month.setdefault((d.year, d.month), []).append(d)
    out: dict[str, dict[tuple[int, int], float]] = {"TN": {}, "TX": {}, "TM": {}}
    for (y, m), days in by_month.items():
        n_days = (date(y + (m == 12), m % 12 + 1, 1) - date(y, m, 1)).days
        complete = [d for d in days if d in data.tmax and d in data.tmin]
        if len(complete) != n_days:
            continue
        tn = sum(data.tmin[d] for d in complete) / n_days
        tx = sum(data.tmax[d] for d in complete) / n_days
        out["TN"][(y, m)], out["TX"][(y, m)], out["TM"][(y, m)] = tn, tx, (tn + tx) / 2
    return out
