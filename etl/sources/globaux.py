"""Sources « séries simples » : une valeur par an, publiée par un organisme de référence.

Chaque source déclare son URL, sa licence, son unité et son lecteur. Les formats sont ceux constatés par la sonde
du 23/10/2026 (docs/sonde-largeur.md), pas supposés. Téléchargement avec cache : en cas d'échec réseau, le cache est
réutilisé ; sans cache, erreur (on ne publie jamais une série inventée).

Toutes les séries sont rendues sous la même forme : {année: valeur}. Une valeur manquante n'est jamais complétée.
"""

from __future__ import annotations

import os
import re
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

UA = {"User-Agent": "projet-evolution-climat"}


@dataclass(frozen=True)
class Source:
    id: str
    name: str                 # organisme et produit
    url: str
    page: str                 # page de référence du jeu de données
    license: str
    unit: str
    parse: Callable[[str], dict[int, float]]
    drop_current_year: bool = False    # fichier annuel qui inclut l'année en cours, incomplète


def _num(s: str) -> float | None:
    s = s.strip()
    if s in ("", "***", "NaN", "nan") or s.startswith("-999"):
        return None
    return float(s)


def parse_gml(text: str) -> dict[int, float]:
    """NOAA GML, moyennes annuelles : lignes « # » de commentaire, en-tête « year,mean,unc »."""
    out = {}
    for line in text.splitlines():
        if line.startswith("#") or not line.strip() or line.lower().startswith("year"):
            continue
        parts = line.split(",")
        v = _num(parts[1])
        if v is not None:
            out[int(parts[0])] = v
    return out


def parse_gistemp(text: str) -> dict[int, float]:
    """GISTEMP v4 : titre, puis en-tête « Year,Jan,…,J-D,… » ; « *** » = manquant (année en cours)."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    i = next(k for k, ln in enumerate(lines) if ln.startswith("Year,"))
    col = lines[i].split(",").index("J-D")
    out = {}
    for ln in lines[i + 1:]:
        parts = ln.split(",")
        if not parts[0].strip().isdigit():
            continue
        v = _num(parts[col])
        if v is not None:
            out[int(parts[0])] = v
    return out


def parse_hadcrut5(text: str) -> dict[int, float]:
    """HadCRUT5, série globale annuelle : « Time,Anomaly (deg C),Lower…,Upper… »."""
    out = {}
    for ln in text.splitlines()[1:]:
        parts = ln.split(",")
        if len(parts) >= 2 and parts[0].strip().isdigit():
            v = _num(parts[1])
            if v is not None:
                out[int(parts[0])] = v
    return out


def parse_berkeley(text: str) -> dict[int, float]:
    """Berkeley Earth, résumé annuel : commentaires « % », puis « année anomalie incertitude … » séparés par des espaces."""
    out = {}
    for ln in text.splitlines():
        if ln.startswith("%") or not ln.strip():
            continue
        parts = ln.split()
        if len(parts) >= 2 and re.fullmatch(r"\d{4}", parts[0]):
            v = _num(parts[1])
            if v is not None:
                out[int(parts[0])] = v
    return out


def parse_oni(text: str) -> dict[int, float]:
    """ONI (NOAA CPC) : « SEAS YR TOTAL ANOM », 12 saisons glissantes par an. Moyenne annuelle des 12, années complètes."""
    by_year: dict[int, list[float]] = {}
    for ln in text.splitlines()[1:]:
        parts = ln.split()
        if len(parts) == 4 and parts[1].isdigit():
            by_year.setdefault(int(parts[1]), []).append(float(parts[3]))
    return {y: round(sum(v) / 12, 3) for y, v in by_year.items() if len(v) == 12}


def parse_nsidc(text: str) -> dict[int, float]:
    """NSIDC Sea Ice Index, fichier mensuel : « year, mo, source_dataset, region, extent, area » ; −9999 = manquant."""
    lines = text.splitlines()
    header = [h.strip() for h in lines[0].split(",")]
    col = header.index("extent")
    out = {}
    for ln in lines[1:]:
        parts = [p.strip() for p in ln.split(",")]
        if len(parts) > col and parts[0].isdigit():
            v = _num(parts[col])
            if v is not None:
                out[int(parts[0])] = v
    return out


def parse_ohc(text: str) -> dict[int, float]:
    """NOAA NCEI, contenu thermique : « YEAR WO WOse … », année au milieu (1955.500), 10²² J, océan mondial (WO)."""
    out = {}
    for ln in text.splitlines()[1:]:
        parts = ln.split()
        if len(parts) >= 2:
            try:
                out[int(float(parts[0]))] = float(parts[1])
            except ValueError:
                continue
    return out


def parse_psmsl(text: str) -> dict[int, float]:
    """PSMSL, moyennes annuelles RLR : « année; niveau (mm); indicateur; drapeau » ; −99999 = manquant.

    Le drapeau d'attention (4e champ, non « 000 ») signale une valeur douteuse : elle est écartée.
    """
    out = {}
    for ln in text.splitlines():
        parts = [p.strip() for p in ln.split(";")]
        if len(parts) < 2 or not parts[0].isdigit():
            continue
        v = _num(parts[1])
        flag = parts[3] if len(parts) > 3 else "000"
        if v is not None and flag in ("000", "0", ""):
            out[int(parts[0])] = v
    return out


PSMSL = "https://psmsl.org/data/obtaining/rlr.annual.data/{id}.rlrdata"
PSMSL_PAGE = "https://psmsl.org/data/obtaining/stations/{id}.php"

SOURCES: dict[str, Source] = {s.id: s for s in [
    Source("co2-mlo", "NOAA GML — CO₂ à Mauna Loa, moyennes annuelles", "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.csv",
           "https://gml.noaa.gov/ccgg/trends/", "Domaine public (NOAA), citation demandée", "ppm", parse_gml),
    Source("co2-gl", "NOAA GML — CO₂, moyenne globale annuelle (surface marine)", "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_gl.csv",
           "https://gml.noaa.gov/ccgg/trends/global.html", "Domaine public (NOAA), citation demandée", "ppm", parse_gml),
    Source("ch4-gl", "NOAA GML — CH₄, moyenne globale annuelle", "https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_annmean_gl.csv",
           "https://gml.noaa.gov/ccgg/trends_ch4/", "Domaine public (NOAA), citation demandée", "ppb", parse_gml),
    Source("n2o-gl", "NOAA GML — N₂O, moyenne globale annuelle", "https://gml.noaa.gov/webdata/ccgg/trends/n2o/n2o_annmean_gl.csv",
           "https://gml.noaa.gov/ccgg/trends_n2o/", "Domaine public (NOAA), citation demandée", "ppb", parse_gml),
    Source("gistemp", "NASA GISS — GISTEMP v4, température globale terre-océan", "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv",
           "https://data.giss.nasa.gov/gistemp/", "Domaine public (NASA)", "°C", parse_gistemp),
    Source("hadcrut5", "Met Office Hadley Centre / CRU — HadCRUT5, température globale",
           "https://www.metoffice.gov.uk/hadobs/hadcrut5/data/HadCRUT.5.0.2.0/analysis/diagnostics/HadCRUT.5.0.2.0.analysis.summary_series.global.annual.csv",
           "https://www.metoffice.gov.uk/hadobs/hadcrut5/", "Open Government Licence v3", "°C", parse_hadcrut5, drop_current_year=True),
    Source("berkeley", "Berkeley Earth — température globale terre-océan",
           "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_summary.txt",
           "https://berkeleyearth.org/data/", "CC BY 4.0", "°C", parse_berkeley, drop_current_year=True),
    Source("oni", "NOAA CPC — indice océanique El Niño (ONI)", "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt",
           "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php", "Domaine public (NOAA)", "°C", parse_oni),
    Source("nsidc-n09", "NSIDC — Sea Ice Index v4, banquise arctique en septembre",
           "https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/data/N_09_extent_v4.0.csv",
           "https://nsidc.org/data/g02135", "Libre, citation demandée (NSIDC)", "millions de km²", parse_nsidc),
    Source("nsidc-s02", "NSIDC — Sea Ice Index v4, banquise antarctique en février",
           "https://noaadata.apps.nsidc.org/NOAA/G02135/south/monthly/data/S_02_extent_v4.0.csv",
           "https://nsidc.org/data/g02135", "Libre, citation demandée (NSIDC)", "millions de km²", parse_nsidc),
    Source("ohc-700", "NOAA NCEI — contenu thermique de l'océan mondial, 0-700 m",
           "https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/yearly/h22-w0-700m.dat",
           "https://www.ncei.noaa.gov/access/global-ocean-heat-content/", "Domaine public (NOAA)", "10²² J", parse_ohc),
    Source("ohc-2000", "NOAA NCEI — contenu thermique de l'océan mondial, 0-2000 m",
           "https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/yearly/h22-w0-2000m.dat",
           "https://www.ncei.noaa.gov/access/global-ocean-heat-content/", "Domaine public (NOAA)", "10²² J", parse_ohc),
    *[Source(f"psmsl-{sid}", f"PSMSL — marégraphe de {name}, moyennes annuelles RLR", PSMSL.format(id=sid),
             PSMSL_PAGE.format(id=sid), "Libre, citation demandée (PSMSL)", "mm", parse_psmsl)
      for sid, name in (("1", "Brest"), ("459", "Le Verdon"), ("1918", "Arcachon-Eyrac"))],
]}


def _offline() -> bool:
    return os.environ.get("GLOBAUX_OFFLINE") == "1"


def fetch(src: Source, raw_dir: Path) -> str:
    path = raw_dir / "globaux" / f"{src.id}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not _offline():
        try:
            with urllib.request.urlopen(urllib.request.Request(src.url, headers=UA), timeout=180) as r:
                data = r.read()
            if b"<html" in data[:2000].lower():
                raise ValueError("page HTML reçue au lieu des données")
            path.write_bytes(data)
        except Exception as exc:  # noqa: BLE001
            if not path.exists():
                raise RuntimeError(f"{src.id} : téléchargement impossible et aucun cache : {exc}") from exc
    return path.read_text(encoding="utf-8", errors="replace")


def load(source_id: str, raw_dir: Path) -> dict[int, float]:
    src = SOURCES[source_id]
    series = src.parse(fetch(src, raw_dir))
    if src.drop_current_year:
        series.pop(datetime.now(timezone.utc).year, None)
    if len(series) < 10:
        raise ValueError(f"{source_id} : moins de 10 années lues, format probablement changé")
    return series
