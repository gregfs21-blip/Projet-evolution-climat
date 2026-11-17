"""Source : RAPID-MOCHA-WBTS, circulation de retournement atlantique (AMOC) à 26,5° N (P9).

Fichier déposé par Grég (décision D-AB du 17/11/2026) : data/sources/rapid/RAPID_transports_v*.nc, le plus récent.
Format constaté par la sonde (docs/sonde-p9d.md) : netCDF-4, mensuel (`time_1m`, jours depuis 1950-01-01, avril 2004 →
novembre 2024 pour v2024-2) ;
- `amoc_depth_1m` : débit de l'AMOC (Sv), « maximum de la fonction de courant moyenne » ;
- `stream_depth_1m` (time_1m, depth) : fonction de courant (Sv) sur 307 profondeurs de 0 à 5 995 m ;
- `heat_trans_1m` : transport de chaleur vers le nord (PW).
Choix fixés avant calcul (docs/phases.md, P9) : profondeur du maximum = profondeur où la fonction de courant mensuelle
est maximale ; moyennes annuelles des mois présents, année gardée si au moins 10 mois (N2).
Depuis la version v2023.1, le débit du détroit de Floride utilisé par RAPID est corrigé de la dérive séculaire du champ
géomagnétique (README RAPID v2023.1 ; Volkov et al., 2024).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from etl.context import ROOT

DIR = ROOT / "data" / "sources" / "rapid"
PAGE = "https://rapid.ac.uk/data/data-download"
LICENSE = "Données RAPID librement disponibles (NERC, NSF, NOAA), citation demandée ; archive BODC sous Open Government Licence v3"
MIN_MONTHS = 10


def path() -> Path:
    files = sorted(DIR.glob("RAPID_transports_v*.nc"))
    if not files:
        raise FileNotFoundError(f"aucun fichier RAPID_transports_v*.nc dans {DIR} (dépôt manuel, décision D-AB)")
    return files[-1]


def version() -> str:
    return path().stem.replace("RAPID_transports_", "")


def source_name() -> str:
    return f"RAPID-MOCHA-WBTS 26,5° N (NOC, NSF, NOAA, Université de Miami), version {version()}"


def depth_of_max(profile: np.ndarray, depth: np.ndarray) -> float:
    """Profondeur (m) où la fonction de courant est maximale ; NaN si le profil est vide."""
    p = np.asarray(profile, float)
    if not np.isfinite(p).any():
        return float("nan")
    return float(np.asarray(depth, float)[int(np.nanargmax(p))])


def annual(months: dict[str, float], min_months: int = MIN_MONTHS) -> tuple[dict[int, float], dict[int, int]]:
    """Moyennes annuelles des mois présents (clé « AAAA-MM ») ; années de moins de `min_months` mois écartées.
    Renvoie aussi le nombre de mois de chaque année (N2)."""
    per: dict[int, list[float]] = {}
    for m, v in months.items():
        if np.isfinite(v):
            per.setdefault(int(m[:4]), []).append(float(v))
    counts = {y: len(v) for y, v in per.items()}
    return {y: sum(v) / len(v) for y, v in per.items() if len(v) >= min_months}, counts


def load() -> dict[str, dict[str, float]]:
    """{"debit": {"AAAA-MM": Sv}, "profondeur": {…: m}, "chaleur": {…: PW}} lus dans le fichier le plus récent."""
    import netCDF4

    out: dict[str, dict[str, float]] = {"debit": {}, "profondeur": {}, "chaleur": {}}
    with netCDF4.Dataset(path()) as ds:
        t = ds["time_1m"]
        dates = netCDF4.num2date(t[:], t.units)
        depth = np.asarray(ds["depth"][:], float)
        amoc = np.ma.filled(ds["amoc_depth_1m"][:].astype(float), np.nan)
        heat = np.ma.filled(ds["heat_trans_1m"][:].astype(float), np.nan)
        stream = np.ma.filled(ds["stream_depth_1m"][:].astype(float), np.nan)
    for i, d in enumerate(dates):
        key = f"{d.year}-{d.month:02d}"
        out["debit"][key] = float(amoc[i])
        out["chaleur"][key] = float(heat[i])
        out["profondeur"][key] = depth_of_max(stream[i], depth)
    return out
