"""Sonde P3 (atmosphère et littoral Gironde) : sources, formats, couverture. Aucun indicateur calculé.

1. Quotidien Météo-France « autres paramètres » (Gironde) : pression et humidité mesurées, pour un contrôle croisé
   avec ERA5 ; 2. température de la mer : OISST (ERDDAP) de nouveau, et ERA5 single levels (CDS, soumission non
   bloquante) ; 3. mouvements verticaux du sol (SONEL, GNSS ULR7a) ; 4. marégraphes PSMSL de la façade
   (RLR et « metric ») autour de la Gironde.
Usage : python -m etl.probe.p3   → docs/sonde-p3.md
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-p3.md"
UA = {"User-Agent": "projet-evolution-climat (sonde)"}


def get(url: str, limit: int = 300_000_000, timeout: int = 300, headers: dict | None = None, data: bytes | None = None,
        method: str | None = None):
    try:
        req = urllib.request.Request(url, headers={**UA, **(headers or {})}, data=data, method=method)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(limit)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()[:2000]
    except Exception as exc:  # noqa: BLE001
        return f"erreur : {type(exc).__name__} {exc}"[:300], b""


def block(md, title, url, st, lines):
    md += ["", f"### {title}", "", f"`{url[:300]}` → **{st}**", "", "```", *[str(x)[:400] for x in lines[:60]], "```"]


def quot_other(md):
    md += ["", "## 1. Quotidien Météo-France, autres paramètres (Gironde)"]
    api = "https://www.data.gouv.fr/api/2/datasets/6569b51ae64326786e4e8e1a/resources/?page={p}&page_size=100&type=main"
    titles, p = [], 1
    while True:
        st, data = get(api.format(p=p), timeout=60)
        if not data:
            break
        j = json.loads(data)
        items = j.get("data", [])
        titles += [(r["title"], r["url"]) for r in items if "departement_33" in r.get("title", "")]
        if not j.get("next_page") or not items:
            break
        p += 1
    md += ["", "Fichiers du département 33 :", "", *[f"- {t}" for t, _ in titles]]
    for t, u in [x for x in titles if "autres" in x[0].lower()]:
        st, data = get(u)
        if u.endswith(".gz") or data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        text = data.decode("utf-8", "replace")
        rows = csv.reader(io.StringIO(text), delimiter=";")
        header = [h.strip() for h in next(rows)]
        idx = {h: i for i, h in enumerate(header)}
        cols = [c for c in ("PMERM", "PMERMIN", "UM", "UN", "UX", "TSVM", "INST", "GLOT", "DHUMEC") if c in idx]
        years: dict[str, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
        names = {}
        for r in rows:
            if len(r) < len(header):
                continue
            ps = r[idx["NUM_POSTE"]].strip()
            names.setdefault(ps, r[idx["NOM_USUEL"]].strip())
            y = r[idx["AAAAMMJJ"]][:4]
            for c in cols:
                if r[idx[c]].strip():
                    years[ps][c][y] += 1
        lines = ["colonnes : " + ", ".join(header)]
        for ps, cs in sorted(years.items(), key=lambda kv: -sum(1 for n in kv[1].get("PMERM", {}).values() if n >= 330)):
            full = {c: sorted(int(y) for y, n in cs[c].items() if n >= 330) for c in cs}
            if len(full.get("PMERM", [])) >= 10 or len(full.get("UM", [])) >= 10:
                lines.append(f"{ps} {names[ps]} : " + " ; ".join(
                    f"{c} {len(v)} ans ({v[0]}-{v[-1]})" for c, v in full.items() if v))
        block(md, t, u, st, lines)


def sst(md):
    md += ["", "## 2. Température de la mer au large de la Gironde"]
    url = ("https://coastwatch.pfeg.noaa.gov/erddap/griddap/ncdcOisst21Agg_LonPM180.csv?"
           "sst%5B(2024-01-01):1:(2024-12-31)%5D%5B(0.0)%5D%5B(45.125)%5D%5B(-1.875)%5D")
    st, data = get(url, timeout=600)
    lines = data.decode("utf-8", "replace").splitlines()
    block(md, "OISST (ERDDAP CoastWatch), une année", url, st, [f"{len(lines)} lignes"] + lines[:4] + lines[-2:])
    key = os.environ.get("CDSAPI_KEY", "")
    api = "https://cds.climate.copernicus.eu/api/retrieve/v1"
    body = {"inputs": {"product_type": ["monthly_averaged_reanalysis"], "variable": ["sea_surface_temperature"],
                       "year": [str(y) for y in range(1940, 2026)], "month": [f"{m:02d}" for m in range(1, 13)],
                       "time": ["00:00"], "area": [46.0, -3.0, 44.0, -1.0], "data_format": "netcdf",
                       "download_format": "unarchived"}}
    st, data = get(f"{api}/processes/reanalysis-era5-single-levels-monthly-means/execution", headers={
        "PRIVATE-TOKEN": key, "Content-Type": "application/json"}, data=json.dumps(body).encode(), method="POST", timeout=60)
    block(md, "ERA5 single levels, moyennes mensuelles : soumission de la SST 1940-2025, boîte 44-46° N, 3-1° O",
          "…/processes/reanalysis-era5-single-levels-monthly-means/execution", st,
          [data.decode("utf-8", "replace").replace(key or "§§", "***")[:1500]])


def sonel(md):
    md += ["", "## 3. Mouvements verticaux du sol (SONEL, GNSS, solution ULR7a)"]
    info = "https://erddap.ioc-sealevelmonitoring.org/erddap/info/sonel_vlm_gnss_ulr7a/index.csv"
    st, data = get(info, timeout=120)
    lines = data.decode("utf-8", "replace").splitlines()
    block(md, "Description du jeu de données", info, st, [ln for ln in lines if ln.startswith("variable") or "units" in ln][:40])
    url = "https://erddap.ioc-sealevelmonitoring.org/erddap/tabledap/sonel_vlm_gnss_ulr7a.csv"
    st, data = get(url, timeout=120)
    text = data.decode("utf-8", "replace").splitlines()
    head = text[:2]
    keep = [ln for ln in text[2:] if re.search(r"(?i)arca|ferr|verd|cap|grave|bord|roch|socoa|lr|bayo|pall|brest", ln)]
    near = []
    try:
        rd = list(csv.reader(text))
        h = rd[0]
        la = next(i for i, c in enumerate(h) if c.lower().startswith("lat"))
        lo = next(i for i, c in enumerate(h) if c.lower().startswith("lon"))
        near = [",".join(r) for r in rd[2:] if r and 43.0 <= float(r[la]) <= 47.5 and -3.5 <= float(r[lo]) <= 0.5]
    except Exception as exc:  # noqa: BLE001
        near = [f"filtrage impossible : {exc}"]
    block(md, "Stations GNSS entre 43 et 47,5° N, 3,5° O et 0,5° E", url, st, head + near + ["…noms :"] + keep[:20])


def psmsl(md):
    md += ["", "## 4. Marégraphes PSMSL de la façade (annuels RLR et metric)"]
    st, data = get("https://psmsl.org/data/obtaining/rlr.annual.data/filelist.txt", timeout=120)
    lines = data.decode("utf-8", "replace").splitlines()
    fac = [ln for ln in lines if re.search(r"(?i)verdon|arcachon|eyrac|grave|rochelle|pallice|socoa|boucau|bayonne|"
                                             r"st\.? ?nazaire|saint-nazaire|port-tudy|les sables|royan|ile d'aix|port-bloc", ln)]
    block(md, "Liste RLR (façade atlantique sud)", "https://psmsl.org/data/obtaining/rlr.annual.data/filelist.txt", st, fac)
    for sid in [ln.split(";")[0].strip() for ln in fac][:10]:
        for kind, base in (("RLR", "https://psmsl.org/data/obtaining/rlr.annual.data/{}.rlrdata"),
                           ("metric", "https://psmsl.org/data/obtaining/met.annual.data/{}.metdata")):
            st, data = get(base.format(sid), timeout=60)
            yrs = []
            for ln in data.decode("utf-8", "replace").splitlines():
                parts = [x.strip() for x in ln.split(";")]
                if len(parts) >= 4 and parts[0].isdigit() and not parts[1].startswith("-99999"):
                    yrs.append((int(parts[0]), parts[3]))
            ok = [y for y, f in yrs if f in ("000", "0")]
            md.append(f"- {sid} {kind} ({st}) : {len(yrs)} années valeur, {len(ok)} sans drapeau"
                      + (f", {ok[0]}-{ok[-1]}" if ok else ""))


def sonel_ids(md):
    md += ["", "## 3b. SONEL : stations françaises et couverture"]
    url = "https://erddap.ioc-sealevelmonitoring.org/erddap/tabledap/sonel_vlm_gnss_ulr7a.csv?stationid&distinct()"
    st, data = get(url, timeout=120)
    ids = [ln for ln in data.decode("utf-8", "replace").splitlines()[2:] if ln.endswith("fra")]
    block(md, "Identifiants de stations (France)", url, st, [", ".join(ids)])
    for sid in [i for i in ids if re.match(r"(?i)(ferr|arca|verd|roya|lroc|lrch|bayo|boca|boua|snaz|socb|sabl|aixi|bisc|brst|soul|cfer|capf)", i)]:
        u = ("https://erddap.ioc-sealevelmonitoring.org/erddap/tabledap/sonel_vlm_gnss_ulr7a.csv?time,par&stationid=%22"
             + sid + "%22")
        st, data = get(u, timeout=120)
        rows = data.decode("utf-8", "replace").splitlines()[2:]
        md.append(f"- {sid} : {len(rows)} jours, {rows[0][:10] if rows else '—'} → {rows[-1][:10] if rows else '—'}")


def cds_jobs(md):
    md += ["", "## 5. Travaux CDS en cours"]
    key = os.environ.get("CDSAPI_KEY", "")
    st, data = get("https://cds.climate.copernicus.eu/api/retrieve/v1/jobs?limit=10", headers={"PRIVATE-TOKEN": key}, timeout=60)
    try:
        lines = [f"{j['jobID']} {j.get('processID')} {j['status']} créé {j.get('created')}" for j in json.loads(data)["jobs"]]
    except Exception:  # noqa: BLE001
        lines = [data[:500]]
    block(md, "Travaux", "jobs", st, lines)


STEPS = (sonel_ids, cds_jobs)   # 2e passage (27/10) : les étapes 1 à 4 ont été constatées au 1er passage
OUT = ROOT / "docs" / "sonde-p3b.md"


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P3 — atmosphère et littoral Gironde (généré)", "",
          f"Généré par `python -m etl.probe.p3` le {now}. Aucun indicateur calculé."]
    for step in STEPS:
        try:
            step(md)
        except Exception as exc:  # noqa: BLE001
            md += ["", f"**{step.__name__} : échec — {type(exc).__name__} {exc}**"]
        OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
