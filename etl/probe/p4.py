"""Sonde P4 (impacts Gironde) : sources, formats, couverture. Aucun indicateur calculé.

1. Dates de vendanges : base européenne Daux et al. 2012 (NOAA Paleo), colonne Bordeaux ; série Saint-Émilion de
   l'ONERC (INRAE, Bordeaux Sciences Agro), recherche d'un fichier ; entrepôt Recherche Data Gouv (INRAE).
2. Danger météorologique d'incendie : indices CEMS/EFFIS calculés sur ERA5 (Copernicus EWDS, cems-fire-historical-v1),
   description du jeu puis soumission non bloquante d'un mois sur la Gironde.
3. Feux de forêt observés : BDIFF (data.gouv.fr), ressources et format.
4. CatNat Gironde par péril (GASPAR) : décompte par péril et par décennie, sans tendance.
Usage : python -m etl.probe.p4   → docs/sonde-p4.md
"""

from __future__ import annotations

import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-p4.md"
UA = {"User-Agent": "projet-evolution-climat (sonde)"}
KEY = os.environ.get("CDSAPI_KEY", "")
EWDS = "https://ewds.climate.copernicus.eu/api/retrieve/v1"
GIRONDE = [45.6, -1.3, 44.2, 0.4]          # N, O, S, E


def get(url: str, limit: int = 300_000_000, timeout: int = 300, headers: dict | None = None, data: bytes | None = None,
        method: str | None = None):
    try:
        req = urllib.request.Request(url, headers={**UA, **(headers or {})}, data=data, method=method)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(limit)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()[:3000]
    except Exception as exc:  # noqa: BLE001
        return f"erreur : {type(exc).__name__} {exc}"[:300], b""


def hide(text: str) -> str:
    return text.replace(KEY, "***") if KEY else text


def block(md, title, url, st, lines):
    md += ["", f"### {title}", "", f"`{url[:300]}` → **{st}**", "", "```", *[hide(str(x))[:500] for x in lines[:80]], "```"]


# ---------------------------------------------------------------- 1. vendanges

def ghd(md):
    md += ["", "## 1. Dates de vendanges"]
    url = "https://www.ncei.noaa.gov/pub/data/paleo/historical/europe/europe2012ghd.txt"
    st, data = get(url, timeout=120)
    text = data.decode("latin-1", "replace")
    lines = text.splitlines()
    out = [f"{len(lines)} lignes"]
    out += [ln for ln in lines if re.search(r"Bordeaux|Bor\b|Gaillac|days after|Missing|Part ", ln)][:25]
    # Tables : une ligne d'en-tête commençant par « Year » (ou « year ») suivie de codes à trois lettres.
    for i, ln in enumerate(lines):
        if re.match(r"\s*[Yy]ear\s", ln) and "Bor" in ln.split():
            head = ln.split()
            col = head.index("Bor")
            years = []
            for row in lines[i + 1:]:
                if not re.match(r"\s*\d{4}\b", row):
                    if years:
                        break
                    continue
                # colonnes séparées par tabulation dans le fichier d'origine
                cells = row.split("\t") if "\t" in row else row.split()
                if len(cells) > col and cells[col].strip() not in ("", "NaN"):
                    try:
                        years.append((int(cells[0]), float(cells[col])))
                    except ValueError:
                        pass
            out.append(f"en-tête ligne {i} : {' '.join(head[:20])}")
            out.append(f"colonne Bor : {len(years)} valeurs, {years[:3]} … {years[-5:]}")
            recent = [y for y, _ in years if y >= 1950]
            out.append(f"depuis 1950 : {len(recent)} années ; trous : "
                       f"{sorted(set(range(1950, (recent or [1950])[-1] + 1)) - set(recent))[:30]}")
            break
    block(md, "Base Daux et al. 2012 (NOAA Paleo), colonne Bordeaux", url, st, out)

    for url in ("https://www.ecologie.gouv.fr/politiques-publiques/impacts-du-changement-climatique-agriculture-foret",
                "https://www.ecologie.gouv.fr/impacts-du-changement-climatique-agriculture-et-foret"):
        st, data = get(url, timeout=120)
        html = data.decode("utf-8", "replace")
        found = sorted(set(re.findall(r"""(?:href|src|data-src)=["']([^"']+)["']""", html)))
        keep = [u for u in found if re.search(r"\.(xlsx?|csv|ods|json)(\?|$)|datawrapper|highcharts|flourish|"
                                            r"iframe|vendange|graph", u, re.I)]
        ctx = [m.group(0) for m in re.finditer(r".{0,200}[Ss]aint-[ÉE]milion.{0,300}", html)][:4]
        scripts = re.findall(r"<script[^>]*>(.{0,4000}?)</script>", html, re.S)
        series = [s[:600] for s in scripts if re.search(r"vendange|Emilion|series|data\s*:", s, re.I)][:3]
        block(md, "ONERC, page « agriculture et forêt » (série Saint-Émilion)", url, st,
              [f"{len(html)} caractères, {len(found)} liens"] + keep[:40] + ["— contexte —"] + ctx + ["— scripts —"] + series)
        if st == 200:
            break

    q = urllib.parse.quote("vendanges")
    url = f"https://entrepot.recherche.data.gouv.fr/api/search?q={q}&type=dataset&per_page=30"
    st, data = get(url, timeout=120)
    out = []
    try:
        for it in json.loads(data)["data"]["items"]:
            out.append(f"{it.get('global_id')} | {it.get('name')} | {it.get('published_at', '')[:10]}")
    except Exception as exc:  # noqa: BLE001
        out.append(f"{type(exc).__name__} {exc} {data[:300]!r}")
    block(md, "Recherche Data Gouv : jeux de données « vendanges »", url, st, out)

    url = ("https://entrepot.recherche.data.gouv.fr/api/datasets/:persistentId/?persistentId="
           + urllib.parse.quote("doi:10.15454/GYSGNR"))
    st, data = get(url, timeout=120)
    out = []
    try:
        v = json.loads(data)["data"]["latestVersion"]
        out += [f"{f['dataFile'].get('filename')} ({f['dataFile'].get('filesize')} o)" for f in v.get("files", [])]
    except Exception as exc:  # noqa: BLE001
        out.append(f"{type(exc).__name__} {exc}")
    block(md, "INRAE Colmar (indicateur ONERC Alsace), fichiers", url, st, out)


# ---------------------------------------------------------------- 2. danger météorologique d'incendie

def _enum(schema: dict) -> list:
    if not isinstance(schema, dict):
        return []
    for k in ("enum",):
        if k in schema:
            return schema[k]
    for k in ("items", "schema"):
        if k in schema:
            return _enum(schema[k])
    return []


def fire(md):
    md += ["", "## 2. Danger météorologique d'incendie (CEMS/EFFIS, ERA5, Copernicus EWDS)"]
    hdr = {"PRIVATE-TOKEN": KEY, "Content-Type": "application/json"}
    pid = "cems-fire-historical-v1"
    st, data = get(f"{EWDS}/processes/{pid}", headers=hdr, timeout=120)
    inputs, out = {}, []
    try:
        desc = json.loads(data)
        inputs = desc.get("inputs", {})
        for name, spec in inputs.items():
            vals = _enum(spec.get("schema", spec))
            out.append(f"{name} : {len(vals)} valeurs : {vals[:25]}")
    except Exception as exc:  # noqa: BLE001
        out.append(f"{type(exc).__name__} {exc} {data[:800]!r}")
    block(md, "Description du jeu (entrées et valeurs permises)", f"{EWDS}/processes/{pid}", st, out)

    def pick(name, *wanted, default=None):
        vals = _enum(inputs.get(name, {}).get("schema", inputs.get(name, {})))
        for w in wanted:
            for v in vals:
                if w in str(v):
                    return [v]
        return default if default is not None else vals[-1:]

    body = {"inputs": {
        "product_type": pick("product_type", "reanalysis", default=["reanalysis"]),
        "variable": pick("variable", "fire_weather_index", default=["fire_weather_index"]),
        "dataset_type": pick("dataset_type", "consolidated", default=["consolidated_dataset"]),
        "system_version": pick("system_version", "4_1", "4_0", default=["4_1"]),
        "year": ["2022"], "month": ["07"], "day": [f"{d:02d}" for d in range(1, 32)],
        "grid": pick("grid", "0.25", default=["0.25/0.25"]),
        "data_format": pick("data_format", "netcdf", default=["netcdf"])[0] if "data_format" in inputs else "netcdf",
        "area": GIRONDE,
    }}
    if "area" not in inputs:
        body["inputs"].pop("area")
    st, data = get(f"{EWDS}/processes/{pid}/execution", headers=hdr, data=json.dumps(body).encode(), method="POST",
                   timeout=120)
    lines = [f"requête : {json.dumps(body['inputs'])[:700]}", data.decode("utf-8", "replace")[:1500]]
    try:
        job = json.loads(data)["jobID"]
        t0, status = time.time(), None
        while time.time() - t0 < 1200:
            time.sleep(30)
            _, dj = get(f"{EWDS}/jobs/{job}", headers=hdr, timeout=60)
            status = json.loads(dj).get("status")
            if status in ("successful", "failed", "rejected", "dismissed"):
                break
        lines.append(f"état après {time.time() - t0:.0f} s : {status}")
        _, dr = get(f"{EWDS}/jobs/{job}/results", headers=hdr, timeout=60)
        res = json.loads(dr)
        if "asset" in res:
            href = res["asset"]["value"]["href"]
            lines.append(f"résultat : {res['asset']['value'].get('file:size')} octets, {href.rsplit('/', 1)[-1]}")
            _, blob = get(href, headers={"PRIVATE-TOKEN": KEY}, timeout=300, limit=300_000_000)
            if blob[:2] == b"PK":
                z = zipfile.ZipFile(io.BytesIO(blob))
                lines.append("archive : " + ", ".join(f"{i.filename} ({i.file_size} o)" for i in z.infolist()[:10]))
                blob = z.read(z.namelist()[0])
            path = OUT.parent / "_fwi.nc"
            path.write_bytes(blob)
            try:
                import netCDF4
                import numpy as np
                with netCDF4.Dataset(path) as ds:
                    lines.append("dimensions : " + ", ".join(f"{k}={len(v)}" for k, v in ds.dimensions.items()))
                    for name, var in ds.variables.items():
                        lines.append(f"  {name} {var.dimensions} {var.shape} {getattr(var, 'units', '')} "
                                     f"{getattr(var, 'long_name', '')}")
                        if var.ndim >= 3:
                            a = np.ma.filled(var[:].astype(float), np.nan)
                            lines.append(f"    min {np.nanmin(a):.1f}, moyenne {np.nanmean(a):.1f}, max {np.nanmax(a):.1f}, "
                                         f"mailles valides au 1er pas : {int(np.isfinite(a[0]).sum())}")
                        elif var.ndim == 1 and len(var) < 40:
                            lines.append(f"    {list(np.asarray(var[:]).round(3))}")
            except Exception as exc:  # noqa: BLE001
                lines.append(f"lecture netCDF : {type(exc).__name__} {exc}")
            finally:
                path.unlink(missing_ok=True)
        else:
            lines.append(json.dumps(res)[:1000])
    except Exception as exc:  # noqa: BLE001
        lines.append(f"{type(exc).__name__} {exc}")
    block(md, "Soumission : FWI quotidien, juillet 2022, boîte Gironde", f"{EWDS}/processes/{pid}/execution", st, lines)


# ---------------------------------------------------------------- 3. BDIFF

def bdiff(md):
    md += ["", "## 3. Feux de forêt observés (BDIFF)"]
    url = "https://www.data.gouv.fr/api/1/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff/"
    st, data = get(url, timeout=120)
    out, urls = [], []
    try:
        j = json.loads(data)
        out.append(f"{j.get('title')} | licence {j.get('license')} | maj {j.get('last_update', '')[:10]}")
        out.append((j.get("description") or "")[:900].replace("\n", " "))
        for r in j.get("resources", []):
            out.append(f"- {r.get('title')} | {r.get('format')} | {r.get('type')} | {r.get('url')}")
            urls.append(r.get("url"))
    except Exception as exc:  # noqa: BLE001
        out.append(f"{type(exc).__name__} {exc}")
    block(md, "Jeu data.gouv.fr", url, st, out)
    for u in [x for x in urls if x][:4]:
        st, data = get(u, timeout=120, limit=2_000_000)
        txt = data[:3000].decode("utf-8", "replace")
        block(md, "Ressource (début)", u, st, [f"{len(data)} octets lus"] + txt.splitlines()[:25])
    for u in ("https://bdiff.agriculture.gouv.fr/", "https://bdiff.agriculture.gouv.fr/incendies"):
        st, data = get(u, timeout=60)
        html = data.decode("utf-8", "replace")
        links = sorted(set(re.findall(r"""href=["']([^"']+)["']""", html)))
        block(md, "Site BDIFF", u, st, [f"{len(html)} caractères"] +
              [x for x in links if re.search(r"export|csv|telecharg|download|api", x, re.I)][:30])


# ---------------------------------------------------------------- 4. CatNat Gironde par péril

def catnat(md):
    md += ["", "## 4. CatNat Gironde par péril (GASPAR), décompte sans tendance"]
    url = "https://www.data.gouv.fr/api/1/datasets/r/d6fb9e18-b66b-499c-8284-46a3595579cc"
    st, data = get(url, timeout=600)
    out = []
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
        name = next(n for n in z.namelist() if re.match(r"catnat_gaspar.*\.csv$", n))
        text = z.read(name).decode("utf-8", "replace").splitlines()
        head = text[0].split(";")
        ix = {h: head.index(h) for h in ("id_gaspar", "code_commune", "num_risque_jo", "lib_risque_jo", "date_debut")}
        seen, per = set(), defaultdict(Counter)
        labels = {}
        for ln in text[1:]:
            p = ln.split(";")
            if len(p) < len(head) or not p[ix["code_commune"]].startswith("33"):
                continue
            k = (p[ix["id_gaspar"]], p[ix["code_commune"]], p[ix["num_risque_jo"]])
            if k in seen:
                continue
            seen.add(k)
            code = p[ix["num_risque_jo"]]
            labels[code] = p[ix["lib_risque_jo"]]
            y = int(p[ix["date_debut"]][:4])
            per[code][(y // 10) * 10] += 1
        out.append(f"{name} : {len(seen)} reconnaissances (arrêté × commune × péril) en Gironde")
        decades = sorted({d for c in per.values() for d in c})
        out.append("péril | " + " | ".join(str(d) for d in decades) + " | total")
        for code, c in sorted(per.items(), key=lambda kv: -sum(kv[1].values())):
            out.append(f"{code} {labels[code][:45]} | " + " | ".join(str(c.get(d, 0)) for d in decades)
                       + f" | {sum(c.values())}")
    except Exception as exc:  # noqa: BLE001
        out.append(f"{type(exc).__name__} {exc}")
    block(md, "Archive GASPAR", url, st, out)


STEPS = (ghd, fire, bdiff, catnat)


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P4 — impacts Gironde (généré)", "",
          f"Généré par `python -m etl.probe.p4` le {now}. Aucun indicateur calculé."]
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
