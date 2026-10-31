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


def ceres(md: list[str]) -> None:
    """CERES EBAF (NASA LaRC) par OPeNDAP, avec le jeton Earthdata : liste des fichiers, puis variable du flux net
    global au sommet de l'atmosphère (lecture ASCII d'une seule variable, quelques centaines de valeurs)."""
    import re
    tok = os.environ.get("EARTHDATA_TOKEN", "")
    md += ["", "## Déséquilibre énergétique (CERES EBAF, OPeNDAP avec jeton Earthdata)", "",
           f"jeton présent : {'oui' if tok else 'NON'}"]
    hdr = {"Authorization": f"Bearer {tok}"} if tok else {}
    for ed in ("Edition4.2.1", "Edition4.2"):
        base = f"https://opendap.larc.nasa.gov/opendap/CERES/EBAF/{ed}/"
        st, data, _ = get(base + "contents.html", headers=hdr)
        html = data.decode("utf-8", "replace")
        files = sorted(set(re.findall(r"(CERES_EBAF[^\"<>]*?\.nc)", html)))
        md += ["", f"### `{base}contents.html` → **{st}**", "", "```", f"{len(files)} fichiers : {files[:10]}",
               html[:300].replace(tok or "§§", "***") if not files else "", "```"]
        if not files:
            continue
        f = files[-1]
        for suffix in (".dds", ".ascii?gtoa_net_all_mon[0:1:5],time[0:1:5]"):
            st, data, _ = get(base + f + suffix, headers=hdr)
            md += ["", f"### `{f}{suffix}` → **{st}**", "", "```",
                   *data.decode("utf-8", "replace").replace(tok or "§§", "***").splitlines()[:40], "```"]
        break


def ads_result(md: list[str]) -> None:
    """CAMS EAC4 mensuel : soumission minimale et lecture du résultat (variables, dimensions)."""
    import time
    md += ["", "## Aérosols (CAMS EAC4 mensuel, Atmosphere Data Store)"]
    api = "https://ads.atmosphere.copernicus.eu/api/retrieve/v1"
    hdr = {"PRIVATE-TOKEN": KEY, "Content-Type": "application/json"}
    body = {"inputs": {"variable": ["total_aerosol_optical_depth_550nm"], "year": ["2020"], "month": ["01"],
                       "product_type": ["monthly_mean"], "data_format": "netcdf_zip"}}
    st, data, _ = get(f"{api}/processes/cams-global-reanalysis-eac4-monthly/execution", headers=hdr,
                      data=json.dumps(body).encode(), method="POST")
    lines = [data.decode("utf-8", "replace").replace(KEY or "§§", "***")[:600]]
    try:
        job = json.loads(data)["jobID"]
        t0, status = time.time(), None
        while time.time() - t0 < 1200:
            time.sleep(30)
            _, dj, _ = get(f"{api}/jobs/{job}", headers=hdr)
            status = json.loads(dj).get("status")
            if status in ("successful", "failed", "rejected", "dismissed"):
                break
        lines.append(f"état après {time.time() - t0:.0f} s : {status}")
        _, dr, _ = get(f"{api}/jobs/{job}/results", headers=hdr)
        res = json.loads(dr)
        href = res["asset"]["value"]["href"]
        _, blob, _ = get(href, headers={"PRIVATE-TOKEN": KEY}, limit=300_000_000)
        if blob[:2] == b"PK":
            z = zipfile.ZipFile(io.BytesIO(blob))
            lines.append("archive : " + ", ".join(f"{i.filename} ({i.file_size} o)" for i in z.infolist()))
            blob = z.read(z.namelist()[0])
        path = OUT.parent / "_aod.nc"
        path.write_bytes(blob)
        try:
            import netCDF4
            with netCDF4.Dataset(path) as ds:
                lines.append("dimensions : " + ", ".join(f"{k}={len(v)}" for k, v in ds.dimensions.items()))
                for name, var in ds.variables.items():
                    lines.append(f"  {name} {var.dimensions} {var.shape} {getattr(var, 'units', '')} {getattr(var, 'long_name', '')}")
        finally:
            path.unlink(missing_ok=True)
    except Exception as exc:  # noqa: BLE001
        lines.append(f"{type(exc).__name__} {exc}")
    md += ["", f"→ **{st}**", "", "```", *lines, "```"]


def ceres_cmr(md: list[str]) -> None:
    """CERES EBAF par le catalogue CMR de la NASA : collections, granules, liens de téléchargement (ASDC), taille ;
    essai d'accès avec le jeton Earthdata (en-tête seulement, puis premier mégaoctet)."""
    tok = os.environ.get("EARTHDATA_TOKEN", "")
    hdr = {"Authorization": f"Bearer {tok}"} if tok else {}
    md += ["", "## CERES EBAF par le catalogue CMR (NASA)"]
    st, data, _ = get("https://cmr.earthdata.nasa.gov/search/collections.json?keyword=CERES%20EBAF&page_size=20")
    links = []
    try:
        cols = json.loads(data)["feed"]["entry"]
        lines = [f"{c.get('short_name')} | {c.get('version_id')} | {c.get('id')} | {c.get('time_start', '')[:10]}-{(c.get('time_end') or '')[:10]}"
                 for c in cols]
    except Exception as exc:  # noqa: BLE001
        cols, lines = [], [f"{type(exc).__name__} {data[:300]!r}"]
    md += ["", f"### collections → **{st}**", "", "```", *lines, "```"]
    for c in cols:
        if "TOA" not in (c.get("short_name") or "") or "EBAF" not in (c.get("short_name") or ""):
            continue
        st, data, _ = get(f"https://cmr.earthdata.nasa.gov/search/granules.json?collection_concept_id={c['id']}&page_size=5&sort_key=-start_date")
        try:
            gr = json.loads(data)["feed"]["entry"]
            lines = []
            for g in gr:
                for lk in g.get("links", []):
                    if lk.get("href", "").startswith("http") and "data#" in lk.get("rel", ""):
                        links.append(lk["href"])
                        lines.append(f"{g.get('title')} | {g.get('granule_size')} Mo | {lk['href']}")
        except Exception as exc:  # noqa: BLE001
            lines = [f"{type(exc).__name__} {data[:300]!r}"]
        md += ["", f"### granules {c.get('short_name')} {c.get('version_id')} → **{st}**", "", "```", *lines[:10], "```"]
    for href in links[:2]:
        st, data, _ = get(href, headers={**hdr, "Range": "bytes=0-1000000"}, limit=1_100_000)
        md += ["", f"### accès `{href}` (premier Mo, jeton) → **{st}**", "", "```",
               f"{len(data)} octets ; début {data[:8]!r}", "```"]


CANDIDATES_2 = {
    "Puits de carbone : fichiers CSV openclimatedata (Global Carbon Budget 2025)": [
        "https://openclimatedata.github.io/global-carbon-budget/data/global-carbon-budget-2025-ocean-sink-gcb.csv",
        "https://openclimatedata.github.io/global-carbon-budget/data/global-carbon-budget-2025-terrestrial-sink-gcb.csv",
        "https://openclimatedata.github.io/global-carbon-budget/data/global-carbon-budget-2025-fossil-emissions.csv",
        "https://openclimatedata.github.io/global-carbon-budget/data/global-carbon-budget-2025-land-use-change-emissions-gcb.csv",
    ],
}
PASS = 4      # 4e passage (31/10/2026) : CERES par le catalogue CMR (OPeNDAP refusé depuis GitHub)


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P6 — sources mondiales (généré)", "", f"Généré par `python -m etl.probe.p6` le {now}. Aucun indicateur calculé."]
    global OUT
    if PASS in (3, 4):
        OUT = ROOT / "docs" / ("sonde-p6c.md" if PASS == 3 else "sonde-p6d.md")
        md[0] = "# Sonde P6 — accès CERES et CAMS (généré)"
        for step in ((ceres, ads_result) if PASS == 3 else (ceres_cmr,)):
            try:
                step(md)
            except Exception as exc:  # noqa: BLE001
                md += ["", f"**{step.__name__} : échec — {type(exc).__name__} {exc}**"]
            OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
        print(f"→ {OUT.relative_to(ROOT)}")
        return 0
    if PASS == 2:
        OUT = ROOT / "docs" / "sonde-p6b.md"
    for title, urls in (CANDIDATES_2 if PASS == 2 else CANDIDATES).items():
        md += ["", f"## {title}"]
        for url in urls:
            st, data, ctype = get(url, headers={"Accept": "application/vnd.github+json"} if "api.github.com" in url else None)
            md += ["", f"### `{url}` → **{st}**", "", "```", *[x[:300] for x in describe(data, ctype)][:60], "```"]
            OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    if PASS == 1:
        try:
            ads(md)
        except Exception as exc:  # noqa: BLE001
            md += ["", f"**ADS : échec — {type(exc).__name__} {exc}**"]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
