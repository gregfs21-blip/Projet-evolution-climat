"""Sonde P6 (monde) : sources des paramètres mondiaux encore absents. Aucun indicateur calculé.

Niveau marin mondial, acidification, ozone, puits de carbone, température de la troposphère (satellites),
déséquilibre énergétique (CERES), aérosols (CAMS, Atmosphere Data Store). Pour chaque candidat : statut HTTP,
taille, premières et dernières lignes. Aucune tendance.
Usage : python -m etl.probe.p6   → docs/sonde-p6.md
"""

from __future__ import annotations

import io
import json
import os
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-p6.md"
UA = {"User-Agent": "projet-evolution-climat (sonde)"}
KEY = os.environ.get("CDSAPI_KEY", "")

CANDIDATES = {
    "Niveau marin mondial (altimétrie)": [
        "https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_gbl_free_ref_90.csv",
        "https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_gbl_free_all_66.csv",
        "https://sealevel.colorado.edu/files/2023_rel2/gmsl_2023rel2_seasons_rmvd.txt",
        "https://sealevel.colorado.edu/files/2024_rel1/gmsl_2024rel1_seasons_rmvd.txt",
        "https://www.cmar.csiro.au/sealevel/downloads/church_white_gmsl_2011_up.zip",
        "https://podaac-opendap.jpl.nasa.gov/opendap/allData/merged_alt/L2/TP_J1_OSTM/global_mean_sea_level/",
    ],
    "Acidification (station HOT, Hawaï)": [
        "https://hahana.soest.hawaii.edu/hot/hotco2/HOT_surface_CO2.txt",
    ],
    "Ozone (NASA Ozone Watch)": [
        "https://ozonewatch.gsfc.nasa.gov/statistics/annual_data.txt",
    ],
    "Puits de carbone (Global Carbon Budget)": [
        "https://globalcarbonbudgetdata.org/downloads/latest-data/Global_Carbon_Budget_2025_v1.0.xlsx",
        "https://globalcarbonbudgetdata.org/downloads/latest-data/Global_Carbon_Budget_2025_v1.0.csv",
        "https://data.icos-cp.eu/objects/26QlKAL0-2D7QhMZ62n1R9PW",
        "https://raw.githubusercontent.com/openclimatedata/global-carbon-budget/main/data/global-carbon-budget.csv",
        "https://api.github.com/repos/openclimatedata/global-carbon-budget/contents/data",
    ],
    "Température de la troposphère (satellites MSU)": [
        "https://www.nsstc.uah.edu/data/msu/v6.1/tlt/uahncdc_lt_6.1.txt",
        "https://data.remss.com/msu/graphics/TLT_v40/time_series/RSS_TS_channel_TLT_Global_Land_And_Sea_v04_0.txt",
    ],
    "Déséquilibre énergétique (CERES EBAF)": [
        "https://ceres.larc.nasa.gov/data/",
        "https://opendap.larc.nasa.gov/opendap/CERES/EBAF/Edition4.2.1/contents.html",
    ],
}


def get(url: str, headers: dict | None = None, data: bytes | None = None, method: str | None = None, limit: int = 60_000_000):
    try:
        req = urllib.request.Request(url, headers={**UA, **(headers or {})}, data=data, method=method)
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read(limit), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()[:2000], ""
    except Exception as exc:  # noqa: BLE001
        return f"erreur : {type(exc).__name__} {str(exc)[:200]}", b"", ""


def describe(data: bytes, ctype: str) -> list[str]:
    if data[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(data))
        out = ["archive : " + ", ".join(f"{i.filename} ({i.file_size} o)" for i in z.infolist()[:15])]
        try:
            import openpyxl
            wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
            for ws in wb.worksheets[:12]:
                rows = list(ws.iter_rows(max_row=40, values_only=True))
                out.append(f"— feuille « {ws.title} » ({ws.max_row} lignes)")
                out += [str([c for c in r if c is not None])[:220] for r in rows if any(c is not None for c in r)][:22]
        except Exception:  # noqa: BLE001
            pass
        return out
    text = data.decode("utf-8", "replace")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if "html" in ctype or text.lstrip().startswith("<"):
        import re
        links = sorted(set(re.findall(r'href="([^"]+)"', text)))
        return [f"HTML, {len(text)} caractères ; liens : " + " ".join(links[:40])]
    return [f"{len(lines)} lignes"] + lines[:12] + ["…"] + lines[-4:]


def ads(md: list[str]) -> None:
    """CAMS (Atmosphere Data Store) : description du jeu mensuel EAC4 et soumission minimale (licence ?)."""
    md += ["", "## Aérosols (CAMS, Atmosphere Data Store)"]
    api = "https://ads.atmosphere.copernicus.eu/api/retrieve/v1"
    hdr = {"PRIVATE-TOKEN": KEY, "Content-Type": "application/json"}
    for pid in ("cams-global-reanalysis-eac4-monthly",):
        st, data, _ = get(f"{api}/processes/{pid}", headers=hdr)
        try:
            inputs = json.loads(data).get("inputs", {})
            lines = [f"{k} : {str(v.get('schema', v))[:300]}" for k, v in inputs.items()]
        except Exception as exc:  # noqa: BLE001
            lines = [f"{type(exc).__name__} {data[:300]!r}"]
        md += ["", f"### {pid} (description)", "", f"→ **{st}**", "", "```", *lines[:20], "```"]
        body = {"inputs": {"variable": ["total_aerosol_optical_depth_550nm"], "year": ["2020"], "month": ["01"],
                           "product_type": ["monthly_mean"], "data_format": "netcdf"}}
        st, data, _ = get(f"{api}/processes/{pid}/execution", headers=hdr, data=json.dumps(body).encode(), method="POST")
        txt = data.decode("utf-8", "replace").replace(KEY or "§§", "***")[:800]
        md += ["", "### soumission minimale (AOD 550 nm, janvier 2020)", "", f"→ **{st}**", "", "```", txt, "```"]


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P6 — sources mondiales (généré)", "", f"Généré par `python -m etl.probe.p6` le {now}. Aucun indicateur calculé."]
    for title, urls in CANDIDATES.items():
        md += ["", f"## {title}"]
        for url in urls:
            st, data, ctype = get(url, headers={"Accept": "application/vnd.github+json"} if "api.github.com" in url else None)
            md += ["", f"### `{url}` → **{st}**", "", "```", *[x[:300] for x in describe(data, ctype)][:60], "```"]
            OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    try:
        ads(md)
    except Exception as exc:  # noqa: BLE001
        md += ["", f"**ADS : échec — {type(exc).__name__} {exc}**"]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
