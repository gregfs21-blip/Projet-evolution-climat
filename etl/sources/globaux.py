"""Sources « séries simples » : une valeur par an, publiée par un organisme de référence.

Chaque source déclare son URL, sa licence, son unité et son lecteur. Les formats sont ceux constatés par la sonde
du 23/10/2026 (docs/sonde-largeur.md), pas supposés. Téléchargement avec cache : en cas d'échec réseau, le cache est
réutilisé ; sans cache, erreur (on ne publie jamais une série inventée).

Toutes les séries sont rendues sous la même forme : {année: valeur}. Une valeur manquante n'est jamais complétée.
"""

from __future__ import annotations

import io
import os
import re
import zipfile
import urllib.request
from dataclasses import dataclass
from functools import partial
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
    cache: str | None = None           # fichier de cache partagé par plusieurs séries tirées du même fichier
    timeout: int = 180
    member: str | None = None          # archive zip : motif du nom du fichier à lire dans l'archive
    fetcher: Callable[["Source", Path], str] | None = None    # téléchargement particulier (ex. par morceaux)


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


def parse_cag(text: str) -> dict[int, float]:
    """NOAA NCEI « Climate at a Glance » : en-têtes « # », puis « Year,Departure from Average » (base 1901-2000)."""
    out = {}
    for ln in text.splitlines():
        if ln.startswith("#") or not ln[:4].isdigit():
            continue
        parts = ln.split(",")
        v = _num(parts[1])
        if v is not None:
            out[int(parts[0][:4])] = v
    return out


def parse_hadsst(text: str) -> dict[int, float]:
    """HadSST 4.2 série annuelle : une ligne d'en-tête, puis « année,anomalie,incertitudes… » (base 1961-1990)."""
    out = {}
    for ln in text.splitlines():
        parts = [p.strip() for p in ln.split(",")]
        if len(parts) >= 2 and re.fullmatch(r"\d{4}", parts[0]):
            v = _num(parts[1])
            if v is not None:
                out[int(parts[0])] = v
    return out


def parse_oisst_point(text: str) -> dict[int, float]:
    """ERDDAP, OISST v2.1 quotidien en un point : deux lignes d'en-tête (noms, unités), puis « temps,zlev,lat,lon,sst ».

    Moyenne annuelle des années dont au moins 360 jours sont présents ; aucune valeur n'est complétée.
    """
    days: dict[int, list[float]] = {}
    for ln in text.splitlines()[2:]:
        parts = ln.split(",")
        if len(parts) >= 5 and parts[0][:4].isdigit():
            v = _num(parts[4])
            if v is not None:
                days.setdefault(int(parts[0][:4]), []).append(v)
    return {y: round(sum(v) / len(v), 3) for y, v in days.items() if len(v) >= 360}


# OISST en un point : une requête ERDDAP par année (la série entière dépasse le délai du serveur, ETL du 25/10/2026).
# Les années passées sont définitives : une fois en cache, elles ne sont plus retéléchargées.
OISST_URL = ("https://coastwatch.pfeg.noaa.gov/erddap/griddap/ncdcOisst21Agg_LonPM180.csv?"
             "sst%5B({start}):1:({end})%5D%5B(0.0)%5D%5B(45.125)%5D%5B(-1.875)%5D")


def fetch_oisst_years(src: "Source", raw_dir: Path) -> str:
    folder = raw_dir / "globaux" / src.id
    folder.mkdir(parents=True, exist_ok=True)
    last = datetime.now(timezone.utc).year - 1
    parts = []
    for y in range(1981, last + 1):
        path = folder / f"{y}.csv"
        if not path.exists():
            if _offline():
                raise RuntimeError(f"{src.id} : année {y} absente du cache (mode hors ligne)")
            url = src.url.format(start=f"{y}-09-01" if y == 1981 else f"{y}-01-01", end=f"{y}-12-31")
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=src.timeout) as r:
                data = r.read()
            if not data.startswith(b"time,"):
                raise ValueError(f"{src.id} {y} : réponse inattendue {data[:200]!r}")
            path.write_bytes(data)
        parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


# --- IBTrACS (NOAA NCEI), Atlantique Nord : une ligne par point de trajectoire, deuxième ligne = unités.
IBTRACS_START = 1966    # ère satellitaire : avant, des ouragans de haute mer échappaient à l'observation (fixé avant calcul)


def _ibtracs_points(text: str):
    """Points des trajectoires principales : saison, identifiant, heure, vent max (kt), catégorie Saffir-Simpson."""
    import csv
    import io
    rows = csv.reader(io.StringIO(text))
    header = [h.strip() for h in next(rows)]
    next(rows)                                             # ligne des unités
    ix = {h: header.index(h) for h in ("SID", "SEASON", "ISO_TIME", "TRACK_TYPE", "USA_WIND", "USA_SSHS")}
    for r in rows:
        if len(r) < len(header) or r[ix["TRACK_TYPE"]].strip() not in ("main", "PROVISIONAL"):
            continue
        sshs, wind = r[ix["USA_SSHS"]].strip(), r[ix["USA_WIND"]].strip()
        yield (int(r[ix["SEASON"]]), r[ix["SID"]], r[ix["ISO_TIME"]].strip(),
               float(wind) if wind else None, int(sshs) if sshs.lstrip("-").isdigit() else None)


def parse_ibtracs_hurricanes(text: str) -> dict[int, float]:
    """Nombre d'ouragans par saison : systèmes ayant atteint au moins la catégorie 1 (USA_SSHS ≥ 1)."""
    seasons: dict[int, set[str]] = {}
    hurricanes: dict[int, set[str]] = {}
    for season, sid, _t, _w, sshs in _ibtracs_points(text):
        seasons.setdefault(season, set())
        if sshs is not None and sshs >= 1:
            hurricanes.setdefault(season, set()).add(sid)
    return {y: float(len(hurricanes.get(y, ()))) for y in seasons if y >= IBTRACS_START}


def parse_ibtracs_ace(text: str) -> dict[int, float]:
    """Énergie cumulée des cyclones (ACE) par saison, en 10⁴ kt² : somme des carrés du vent max aux heures
    synoptiques (00, 06, 12, 18 UTC) des points de tempête tropicale ou d'ouragan (USA_SSHS ≥ 0, vent ≥ 34 kt)."""
    out: dict[int, float] = {}
    for season, _sid, t, wind, sshs in _ibtracs_points(text):
        out.setdefault(season, 0.0)
        if wind is not None and sshs is not None and sshs >= 0 and t[11:16] in ("00:00", "06:00", "12:00", "18:00"):
            out[season] += wind * wind / 1e4
    return {y: round(v, 2) for y, v in out.items() if y >= IBTRACS_START}



# --- GASPAR (ministère de la Transition écologique), arrêtés de catastrophe naturelle.
# Fichier « catnat_gaspar_AAAA-MM-JJ.csv » de l'archive data.gouv.fr (sonde du 25/10/2026, docs/sonde-catnat.md) :
# « id_gaspar;code_commune;libelle_commune;num_risque_jo;lib_risque_jo;date_debut;date_fin;… », une ligne par
# arrêté × commune × péril. Encodage mêlé (libellés parfois mal convertis) : seuls codes et dates sont utilisés.
CATNAT_START = 1982           # loi du 13 juillet 1982 : création du régime
CATNAT_LAG = 2                # les deux dernières années d'événement sont exclues (reconnaissances encore à venir)


def parse_catnat(text: str, department: str | None = None, peril: str | None = None) -> dict[int, float]:
    """Reconnaissances (commune × arrêté × péril, doublons retirés) par année de DÉBUT de l'événement."""
    last = datetime.now(timezone.utc).year - 1 - CATNAT_LAG
    seen: set[tuple[str, str, str]] = set()
    out: dict[int, float] = {y: 0.0 for y in range(CATNAT_START, last + 1)}
    lines = text.splitlines()
    header = lines[0].lstrip("\ufeff").split(";")
    ix = {h: header.index(h) for h in ("id_gaspar", "code_commune", "num_risque_jo", "lib_risque_jo", "date_debut")}
    for ln in lines[1:]:
        parts = ln.split(";")
        if len(parts) < len(header):
            continue
        commune, start = parts[ix["code_commune"]].strip(), parts[ix["date_debut"]].strip()
        if department and not commune.startswith(department):
            continue
        if peril and peril not in parts[ix["lib_risque_jo"]].lower():
            continue
        if not start[:4].isdigit() or not CATNAT_START <= int(start[:4]) <= last:
            continue
        key = (parts[ix["id_gaspar"]].strip(), commune, parts[ix["num_risque_jo"]].strip())
        if key not in seen:
            seen.add(key)
            out[int(start[:4])] += 1
    return out


# --- Dates de vendanges : base européenne Daux et al. (2012), NOAA WDS Paleoclimatology (europe2012ghd.txt).
# Format constaté par la sonde du 28/10/2026 (docs/sonde-p4b.md) : tableaux à largeur fixe, une ligne d'en-tête
# « Year Als Auv … Bor … », valeurs en jours après le 31 août ALIGNÉES À DROITE sur la fin du code de colonne, case
# vide = année absente.


def parse_ghd(text: str, code: str = "Bor") -> dict[int, float]:
    lines = text.splitlines()
    out: dict[int, float] = {}
    for i, ln in enumerate(lines):
        if not (re.match(r"\s*[Yy]ear\s", ln) and re.search(rf"\b{re.escape(code)}\b", ln)):
            continue
        heads = [(m.group(0), m.start(), m.end()) for m in re.finditer(r"\S+", ln)]
        k = next(j for j, h in enumerate(heads) if h[0] == code)
        lo, hi = heads[k - 1][2], heads[k][2] + 1
        started = False
        for row in lines[i + 1:]:
            m = re.match(r"\s*(\d{4})\b", row)
            if not m:
                if started:
                    break
                continue
            started = True
            if "\t" in row:
                raise ValueError("dates de vendanges : tabulation inattendue, format changé")
            cell = row[lo:hi].strip()
            if cell:
                out[int(m.group(1))] = float(cell)
    return out


PSMSL = "https://psmsl.org/data/obtaining/rlr.annual.data/{id}.rlrdata"
PSMSL_PAGE = "https://psmsl.org/data/obtaining/stations/{id}.php"

_LAST = datetime.now(timezone.utc).year - 1    # dernière année complète

SOURCES: dict[str, Source] = {s.id: s for s in [
    *[Source(sid, "Ministère de la Transition écologique — base GASPAR, arrêtés de catastrophe naturelle",
             "https://www.data.gouv.fr/api/1/datasets/r/d6fb9e18-b66b-499c-8284-46a3595579cc",
             "https://www.data.gouv.fr/datasets/base-nationale-de-gestion-assistee-des-procedures-administratives-relatives-aux-risques-gaspar",
             "Licence Ouverte 2.0 (Etalab)", "reconnaissances", partial(parse_catnat, department=dep, peril=per),
             cache="gaspar-catnat", timeout=600, member=r"catnat_gaspar.*\.csv$")
      for sid, dep, per in (("catnat-gironde", "33", None), ("catnat-france", None, None),
                            ("catnat-secheresse-france", None, "cheresse"),
                            # P4, D-I (28/10/2026) : Gironde par péril, affichage seulement (critère I8)
                            ("catnat-inondation-gironde", "33", "inondation"),
                            ("catnat-secheresse-gironde", "33", "cheresse"),
                            ("catnat-vagues-gironde", "33", "vagues"))],
    Source("vendanges-bordeaux", "NOAA WDS Paleoclimatology — base européenne des dates de vendanges (Daux et al., 2012), Bordeaux",
           "https://www.ncei.noaa.gov/pub/data/paleo/historical/europe/europe2012ghd.txt",
           "https://www.ncei.noaa.gov/access/paleo-search/study/13194", "Domaine public (NOAA WDS)", "jours", parse_ghd),
    Source("sst-noaa", "NOAA NCEI — NOAAGlobalTemp, température de surface de l'océan mondial (Climate at a Glance)",
           f"https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/ocean/12/12/1850-{_LAST}/data.csv",
           "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series", "Domaine public (NOAA)", "°C", parse_cag),
    Source("hadsst", "Met Office Hadley Centre — HadSST 4.2, température de surface de la mer, moyenne mondiale",
           "https://www.metoffice.gov.uk/hadobs/hadsst4/data/data/HadSST.4.2.0.0_annual_GLOBE.csv",
           "https://www.metoffice.gov.uk/hadobs/hadsst4/", "Open Government Licence v3", "°C", parse_hadsst, drop_current_year=True),
    Source("oisst-gascogne", "NOAA — OISST v2.1 (analyse quotidienne satellite et in situ), via ERDDAP (NOAA CoastWatch)",
           OISST_URL, "https://www.ncei.noaa.gov/products/optimum-interpolation-sst", "Domaine public (NOAA)", "°C",
           parse_oisst_point, drop_current_year=True, timeout=300, fetcher=lambda src, raw: fetch_oisst_years(src, raw)),
    Source("ibtracs-ouragans", "NOAA NCEI — IBTrACS v04r01, Atlantique Nord",
           "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.NA.list.v04r01.csv",
           "https://www.ncei.noaa.gov/products/international-best-track-archive", "Domaine public (NOAA)", "ouragans",
           parse_ibtracs_hurricanes, drop_current_year=True, cache="ibtracs-na", timeout=600),
    Source("ibtracs-ace", "NOAA NCEI — IBTrACS v04r01, Atlantique Nord",
           "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.NA.list.v04r01.csv",
           "https://www.ncei.noaa.gov/products/international-best-track-archive", "Domaine public (NOAA)", "10⁴ kt²",
           parse_ibtracs_ace, drop_current_year=True, cache="ibtracs-na", timeout=600),
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


_FETCHED: set[str] = set()     # fichiers partagés déjà téléchargés pendant cette exécution


def fetch(src: Source, raw_dir: Path) -> str:
    if src.fetcher:
        return src.fetcher(src, raw_dir)
    key = src.cache or src.id
    path = raw_dir / "globaux" / f"{key}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not _offline() and key not in _FETCHED:
        try:
            with urllib.request.urlopen(urllib.request.Request(src.url, headers=UA), timeout=src.timeout) as r:
                data = r.read()
            if b"<html" in data[:2000].lower():
                raise ValueError("page HTML reçue au lieu des données")
            if src.member:
                z = zipfile.ZipFile(io.BytesIO(data))
                name = next((n for n in z.namelist() if re.search(src.member, n)), None)
                if name is None:
                    raise ValueError(f"aucun fichier « {src.member} » dans l'archive : {z.namelist()}")
                data = z.read(name)
            path.write_bytes(data)
            _FETCHED.add(key)
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
