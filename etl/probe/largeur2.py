"""Sonde « largeur d'abord », lot 2 : vent, pression, humidité, mer, altitude, ouragans, catastrophes naturelles.

Aucun résultat climatique : formats, couverture et disponibilité constatés avant d'écrire les lecteurs.
Usage : python -m etl.probe.largeur2   → écrit docs/sonde-largeur2.md
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import re
import sys
import urllib.parse
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone

from etl.context import RAW_DIR, ROOT
from etl.sources import meteofrance_quot as quot

OUT = ROOT / "docs" / "sonde-largeur2.md"
UA = {"User-Agent": "projet-evolution-climat (sonde)"}


def get(url: str, limit: int = 200_000_000, timeout: int = 300) -> tuple[int | str, bytes]:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return r.status, r.read(limit)
    except urllib.error.HTTPError as exc:
        return exc.code, b""
    except Exception as exc:  # noqa: BLE001
        return f"erreur : {type(exc).__name__} {exc}"[:200], b""


def block(md: list[str], title: str, url: str, status, lines: list[str]) -> None:
    md += ["", f"### {title}", "", f"`{url}` → **{status}**", "", "```", *lines[:40], "```"]


def daily_wind(md: list[str]) -> None:
    """Colonnes du fichier quotidien et couverture des rafales (FXI) et du vent moyen (FFM) par poste."""
    md += ["", "## 1. Vent dans le quotidien Météo-France (département 33)"]
    res = quot.resources("33", RAW_DIR)
    md += ["", "Fichiers : " + ", ".join(r["title"] for r in res)]
    years: dict[str, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    names: dict[str, str] = {}
    header_seen = None
    for r in res:
        rows = quot._rows(quot.fetch(r, RAW_DIR))
        header = [h.strip() for h in next(rows)]
        header_seen = header
        idx = {h: i for i, h in enumerate(header)}
        cols = [c for c in ("FXI", "FXY", "FFM", "FXI3S") if c in idx]
        for row in rows:
            if len(row) < len(header):
                continue
            p = row[idx["NUM_POSTE"]].strip()
            names.setdefault(p, row[idx["NOM_USUEL"]].strip())
            y = row[idx["AAAAMMJJ"]][:4]
            for c in cols:
                if row[idx[c]].strip():
                    years[p][c][y] += 1
    md += ["", "Colonnes : " + ", ".join(header_seen or [])]
    md += ["", "| Poste | Nom | Années FXI ≥ 330 j | Plage FXI | Années FFM ≥ 330 j | Années FXI3S ≥ 330 j |", "|---|---|---|---|---|---|"]
    rows_out = []
    for p, cs in years.items():
        full = {c: sorted(int(y) for y, n in cs[c].items() if n >= 330) for c in cs}
        fxi = full.get("FXI", [])
        if len(fxi) >= 20 or len(full.get("FXI3S", [])) >= 20:
            rows_out.append((len(fxi), p, names[p], fxi, full))
    for n, p, name, fxi, full in sorted(rows_out, reverse=True)[:20]:
        md.append(f"| {p} | {name} | {n} | {fxi[0] if fxi else '—'}-{fxi[-1] if fxi else '—'} | "
                  f"{len(full.get('FFM', []))} | {len(full.get('FXI3S', []))} |")


def openmeteo(md: list[str]) -> None:
    md += ["", "## 2. ERA5 via Open-Meteo (Bordeaux-Mérignac) : variables quotidiennes disponibles"]
    q = urllib.parse.urlencode({"latitude": "44.831", "longitude": "-0.691", "start_date": "1940-01-01", "end_date": "1940-01-05",
                                "daily": "pressure_msl_mean,relative_humidity_2m_mean,wind_speed_10m_max,wind_gusts_10m_max,"
                                         "precipitation_sum,shortwave_radiation_sum",
                                "models": "era5", "timezone": "Europe/Paris"})
    url = f"https://archive-api.open-meteo.com/v1/archive?{q}"
    st, data = get(url)
    block(md, "Open-Meteo archive, 1940", url, st, data.decode("utf-8", "replace")[:1500].splitlines())


def sst(md: list[str]) -> None:
    md += ["", "## 3. Température de la mer"]
    for title, url in [
        ("NOAA Climate at a Glance — océan mondial, annuel",
         "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/ocean/tavg/land_ocean/12/12/1850-2025/data.csv"),
        ("NOAA Climate at a Glance — océan mondial, annuel (autre forme)",
         "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/ocean/12/12/1850-2025/data.csv"),
        ("ERDDAP OISST v2.1 mensuel, point golfe de Gascogne (45 N, 2 W)",
         "https://coastwatch.pfeg.noaa.gov/erddap/griddap/ncdcOisst21Agg_LonPM180.csv?sst%5B(2024-01-16):1:(2024-01-16)%5D%5B(0.0)%5D%5B(45.125)%5D%5B(-1.875)%5D"),
        ("HadSST4 — page des données", "https://www.metoffice.gov.uk/hadobs/hadsst4/data/download.html"),
    ]:
        st, data = get(url, limit=5_000_000)
        text = data.decode("utf-8", "replace")
        if "<html" in text[:3000].lower():
            lines = ["[page HTML] liens :"] + sorted(set(re.findall(r'href="([^"]+\.(?:csv|txt|zip|nc))"', text)))[:25]
        else:
            lines = text.splitlines()[:15]
        block(md, title, url, st, lines)


def igra(md: list[str]) -> None:
    md += ["", "## 4. Radiosondages IGRA (Bordeaux-Mérignac, FRM00007510)"]
    for title, url in [("Liste des stations IGRA", "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/doc/igra2-station-list.txt"),
                       ("Répertoire monthly-por", "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/monthly-por/"),
                       ("Répertoire data-por", "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/data-por/")]:
        st, data = get(url, limit=20_000_000)
        text = data.decode("utf-8", "replace")
        if title.startswith("Liste"):
            lines = [ln for ln in text.splitlines() if "07510" in ln or "BORDEAUX" in ln.upper()][:10]
        else:
            lines = sorted(set(re.findall(r'href="([^"]+)"', text)))[:30]
            lines = [ln for ln in lines if "FRM" in ln or "mly" in ln or "temp" in ln][:30] or lines[:30]
        block(md, title, url, st, lines)
    url = "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/data-por/FRM00007510-data.txt.zip"
    st, data = get(url)
    lines = [f"[{len(data) / 1e6:.1f} Mo]"]
    if data:
        try:
            z = zipfile.ZipFile(io.BytesIO(data))
            n = z.namelist()[0]
            with z.open(n) as f:
                head = [next(f).decode("ascii", "replace").rstrip() for _ in range(25)]
            lines += [n] + head
        except Exception as exc:  # noqa: BLE001
            lines.append(f"illisible : {exc}")
    block(md, "IGRA data-por, Mérignac", url, st, lines)


def hurricanes(md: list[str]) -> None:
    md += ["", "## 5. IBTrACS Atlantique Nord : colonnes utiles"]
    url = "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.NA.list.v04r01.csv"
    st, data = get(url)
    rows = list(csv.reader(io.StringIO(data.decode("utf-8", "replace"))))
    header = rows[0] if rows else []
    keep = [h for h in header if h in ("SID", "SEASON", "NAME", "ISO_TIME", "NATURE", "USA_WIND", "WMO_WIND", "USA_SSHS", "TRACK_TYPE")]
    seasons = Counter(r[1] for r in rows[2:] if len(r) > 1)
    lines = [f"{len(data) / 1e6:.1f} Mo, {len(rows)} lignes", "Colonnes retenues : " + ", ".join(keep),
             f"Saisons : {min(seasons)}-{max(seasons)}", "NATURE : " + str(Counter(r[header.index('NATURE')] for r in rows[2:])),
             "TRACK_TYPE : " + str(Counter(r[header.index('TRACK_TYPE')] for r in rows[2:]))]
    block(md, "IBTrACS NA", url, st, lines)


def catnat(md: list[str]) -> None:
    md += ["", "## 6. Catastrophes naturelles : base GASPAR (data.gouv.fr)"]
    url = "https://www.data.gouv.fr/api/1/datasets/?q=gaspar%20catnat&page_size=5"
    st, data = get(url)
    lines = []
    if data:
        for d in json.loads(data).get("data", []):
            lines.append(f"{d['title']} — {d['page']}")
            for r in d.get("resources", [])[:8]:
                lines.append(f"    {r['title']} | {r.get('format')} | {r.get('filesize')} | {r['url']}")
    block(md, "Recherche GASPAR", url, st, lines)


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde « largeur d'abord », lot 2 (généré)", "",
          f"Généré par `python -m etl.probe.largeur2` le {now}. Aucun calcul : formats et couverture constatés."]
    for step in (daily_wind, openmeteo, sst, igra, hurricanes, catnat):
        try:
            step(md)
        except Exception as exc:  # noqa: BLE001
            md += ["", f"**{step.__name__} : échec — {type(exc).__name__} {exc}**"]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
