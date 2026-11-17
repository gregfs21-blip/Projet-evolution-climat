"""Sources de P10.1 : forçages radiatifs effectifs de l'IGCC 2025, indice Niño 3.4 long (HadISST1.1), ONI mensuel.

Formats constatés par la sonde du 17/11/2026 (docs/sonde-p10.md), pas supposés. Téléchargement et cache par
etl.sources.globaux.fetch : en cas d'échec réseau, le cache est réutilisé ; sans cache, erreur.

- ERF : `ClimateIndicator/data`, étiquette **v2026.06.02** (IGCC 2025), figée. Une nouvelle édition de l'IGCC change
  les forçages ET les références R-O1 à R-O3 : la changer est une décision consignée dans docs/phases.md.
- Niño 3.4 : NOAA PSL, HadISST1.1, anomalies par rapport à 1981-2010, mensuel depuis 1870 (−99.99 = absent).
- ONI : NOAA CPC, saisons glissantes de 3 mois (contrôle O2 et sous-période O8 c).
"""

from __future__ import annotations

from pathlib import Path

from etl.sources import globaux as G

TAG = "v2026.06.02"
REPO = f"https://raw.githubusercontent.com/ClimateIndicator/data/{TAG}/data"
PAGE = "https://doi.org/10.5281/zenodo.20499280"
NINO_URL = "https://psl.noaa.gov/data/timeseries/month/data/nino34.long.anom.data"
NINO_PAGE = "https://psl.noaa.gov/data/timeseries/month/Nino34/"


def _src(sid: str, name: str, url: str, page: str, license_: str, unit: str) -> G.Source:
    return G.Source(sid, name, url, page, license_, unit, parse=lambda _t: {})


ERF = {
    level: _src(f"igcc-erf-{level}", f"IGCC 2025 — forçages radiatifs effectifs ({level})",
                f"{REPO}/effective_radiative_forcing/ERF_{level}_aggregates.csv", PAGE, "CC BY 4.0 (Forster et al., 2026)",
                "W/m²")
    for level in ("best", "p05", "p95")
}
NINO = _src("nino34-hadisst", "NOAA PSL — Niño 3.4, HadISST1.1, anomalies mensuelles", NINO_URL, NINO_PAGE,
            "Domaine public (NOAA) ; HadISST © Crown copyright, Met Office, usage non commercial", "°C")

# Colonnes attendues (sonde du 17/11/2026) ; une colonne absente arrête le calcul.
ERF_COLUMNS = ("anthro", "volcanic", "solar", "total")


def parse_erf(text: str) -> dict[int, dict[str, float]]:
    """CSV « time,timebound_lower,timebound_upper,… » : une ligne par année (time = année + 0,5)."""
    lines = [ln for ln in text.lstrip("﻿").splitlines() if ln.strip()]
    header = [h.strip() for h in lines[0].split(",")]
    missing = [c for c in ("time", "timebound_lower", "timebound_upper", *ERF_COLUMNS) if c not in header]
    if missing:
        raise ValueError(f"ERF : colonnes absentes {missing} (en-tête : {header})")
    out: dict[int, dict[str, float]] = {}
    for ln in lines[1:]:
        parts = [p.strip() for p in ln.split(",")]
        row = dict(zip(header, parts))
        year = int(float(row["timebound_lower"]))
        if int(float(row["timebound_upper"])) != year + 1 or abs(float(row["time"]) - (year + 0.5)) > 1e-6:
            raise ValueError(f"ERF : ligne non annuelle ({ln[:60]})")
        if year in out:
            raise ValueError(f"ERF : année {year} en double")
        out[year] = {c: float(row[c]) for c in ERF_COLUMNS}
    years = sorted(out)
    if years != list(range(years[0], years[-1] + 1)):
        raise ValueError("ERF : années non consécutives")
    return out


def parse_psl_monthly(text: str) -> dict[tuple[int, int], float]:
    """Format standard PSL : « début fin » puis une ligne par année (13 champs) ; −99.99 = absent."""
    lines = text.splitlines()
    first, last = (int(x) for x in lines[0].split()[:2])
    out: dict[tuple[int, int], float] = {}
    for ln in lines[1:]:
        parts = ln.split()
        if len(parts) != 13 or not parts[0].isdigit():
            continue
        y = int(parts[0])
        if not first <= y <= last:
            raise ValueError(f"Niño 3.4 : année {y} hors de l'en-tête {first}-{last}")
        for m, v in enumerate(parts[1:], start=1):
            x = float(v)
            if x > -99:
                out[(y, m)] = x
    if not out:
        raise ValueError("Niño 3.4 : aucune valeur lue")
    return out


ONI_SEASONS = ("DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ")


def parse_oni_monthly(text: str) -> dict[tuple[int, int], float]:
    """ONI (CPC) : « SEAS YR TOTAL ANOM » ; chaque saison est rattachée à son mois central (DJF → janvier)."""
    out: dict[tuple[int, int], float] = {}
    for ln in text.splitlines()[1:]:
        parts = ln.split()
        if len(parts) == 4 and parts[1].isdigit() and parts[0] in ONI_SEASONS:
            out[(int(parts[1]), ONI_SEASONS.index(parts[0]) + 1)] = float(parts[3])
    if not out:
        raise ValueError("ONI : aucune valeur lue")
    return out


def load_erf(raw_dir: Path, level: str = "best") -> dict[int, dict[str, float]]:
    return parse_erf(G.fetch(ERF[level], raw_dir))


def load_nino(raw_dir: Path) -> dict[tuple[int, int], float]:
    return parse_psl_monthly(G.fetch(NINO, raw_dir))


def load_oni_monthly(raw_dir: Path) -> dict[tuple[int, int], float]:
    return parse_oni_monthly(G.fetch(G.SOURCES["oni"], raw_dir))
