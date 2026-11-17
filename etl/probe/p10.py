"""Sonde P10 (démonstration de l'évolution du climat) : données de la régression multiple (P10.1).

1. Forçages radiatifs effectifs (ERF) de l'Indicators of Global Climate Change 2025 (Forster et al., 2026) :
   dépôt ClimateIndicator/data (étiquette v2026.06.02, archivée sur Zenodo, doi 10.5281/zenodo.20499280) et dépôt
   ClimateIndicator/forcing-timeseries. Fichiers, colonnes, première et dernière années.
2. Réchauffement attribué publié par l'IGCC 2025 (fichier de la référence, s'il existe dans le dépôt).
3. Indice Niño 3.4 long (HadISST1.1, NOAA PSL), valeurs absolues et anomalies, depuis 1870.
Aucune régression, aucun indicateur calculé. Usage : python -m etl.probe.p10   → docs/sonde-p10.md
"""

from __future__ import annotations

import io
import json
import re
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-p10.md"
UA = {"User-Agent": "projet-evolution-climat (sonde P10 ; github.com/gregfs21-blip/projet-evolution-climat)"}
TAG = "v2026.06.02"
REPO = "ClimateIndicator/data"
ZENODO = "https://zenodo.org/records/20499280/files/ClimateIndicator/data-v2026.06.02.zip?download=1"


def get(url: str, limit: int = 200_000_000):
    """(statut, URL finale, octets). Les redirections sont suivies ; aucune erreur ne remonte."""
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, r.geturl(), r.read(limit)
    except urllib.error.HTTPError as exc:
        return exc.code, url, exc.read()[:2000]
    except Exception as exc:  # noqa: BLE001
        return f"erreur : {type(exc).__name__} {exc}", url, b""


def show_text(name: str, data: bytes, head: int = 6, tail: int = 4) -> list[str]:
    lines = data.decode("utf-8", "replace").splitlines()
    out = [f"{name} : {len(lines)} lignes, {len(data)} o ; début :"]
    out += [f"  {x[:400]}" for x in lines[:head]]
    out.append("fin :")
    out += [f"  {x[:400]}" for x in lines[-tail:]]
    return out


def show_csv(name: str, data: bytes) -> list[str]:
    """En-tête complet (une colonne par ligne), années extrêmes, et valeurs de quelques colonnes clés."""
    lines = [ln for ln in data.decode("utf-8", "replace").splitlines() if ln.strip()]
    out = show_text(name, data)
    if not lines:
        return out
    header = [h.strip() for h in lines[0].split(",")]
    out.append(f"colonnes ({len(header)}) :")
    out += [f"  [{i}] {h}" for i, h in enumerate(header)]
    rows = [ln.split(",") for ln in lines[1:]]
    keys = [h for h in header if re.search(r"anthro|natural|volcan|solar|total|co2|aerosol", h, re.I)]
    for y in ("1750", "1850", "1900", "1991", "2000", "2015", "2020", "2023", "2024", "2025"):
        r = next((r for r in rows if r and r[0].split(".")[0].strip() == y), None)
        if r:
            vals = ", ".join(f"{k}={r[header.index(k)].strip()}" for k in keys if header.index(k) < len(r))
            out.append(f"  {y} : {vals}")
    return out


def github_listing() -> list[str]:
    out = []
    for path in ("", "data"):
        url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={TAG}"
        st, _, data = get(url, limit=5_000_000)
        out.append(f"GET {url} → {st}")
        if st == 200:
            try:
                for e in json.loads(data):
                    out.append(f"  {e['type']:4} {e['path']}")
            except Exception as exc:  # noqa: BLE001
                out.append(f"  lecture : {exc}")
    return out


def igcc_files() -> list[str]:
    out = []
    # Arborescence complète de l'étiquette (API Git trees), pour retrouver les fichiers ERF et d'attribution.
    url = f"https://api.github.com/repos/{REPO}/git/trees/{TAG}?recursive=1"
    st, _, data = get(url, limit=20_000_000)
    out.append(f"GET {url} → {st}")
    paths: list[str] = []
    if st == 200:
        try:
            paths = [e["path"] for e in json.loads(data).get("tree", []) if e.get("type") == "blob"]
        except Exception as exc:  # noqa: BLE001
            out.append(f"  lecture : {exc}")
    keep = [p for p in paths if re.search(r"forcing|ERF|attribut|warming|GMST|temperature", p, re.I)]
    out.append(f"{len(paths)} fichiers, dont {len(keep)} retenus (forçage, attribution, température) :")
    out += [f"  {p}" for p in keep]
    for p in keep:
        if p.lower().endswith(".csv") and re.search(r"ERF_best_aggregates|attribut|warming", p, re.I):
            raw = f"https://raw.githubusercontent.com/{REPO}/{TAG}/{p}"
            st, _, data = get(raw)
            out.append("")
            out.append(f"GET {raw} → {st}")
            if st == 200:
                out += show_csv(p, data)
        elif p.lower().endswith((".yml", ".yaml")) and re.search(r"ERF_best_aggregates|attribut", p, re.I):
            raw = f"https://raw.githubusercontent.com/{REPO}/{TAG}/{p}"
            st, _, data = get(raw, limit=200_000)
            out.append("")
            out.append(f"GET {raw} → {st}")
            if st == 200:
                out += show_text(p, data, head=60, tail=0)
    return out


def zenodo() -> list[str]:
    st, final, data = get(ZENODO)
    out = [f"GET {ZENODO} → {st} (URL finale : {final}, {len(data)} o)"]
    if st == 200 and data:
        try:
            z = zipfile.ZipFile(io.BytesIO(data))
            names = z.namelist()
            out.append(f"{len(names)} fichiers dans l'archive, dont :")
            out += [f"  {n}" for n in names if re.search(r"forcing|ERF|attribut|warming", n, re.I)]
        except Exception as exc:  # noqa: BLE001
            out.append(f"  lecture : {exc}")
    return out


def forcing_repo() -> list[str]:
    out = []
    for year in ("2025", "2024"):
        url = f"https://raw.githubusercontent.com/ClimateIndicator/forcing-timeseries/main/output/ERF_best_aggregates_1750-{year}.csv"
        st, _, data = get(url)
        out.append(f"GET {url} → {st}")
        if st == 200:
            out += show_csv(f"forcing-timeseries ERF_best_aggregates_1750-{year}.csv", data)
            break
    return out


def nino34() -> list[str]:
    out = []
    for url in ("https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/nino34.long.data",
                "https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/nino34.long.anom.data",
                "https://psl.noaa.gov/data/timeseries/month/data/nino34.long.data",
                "https://psl.noaa.gov/data/timeseries/month/data/nino34.long.anom.data"):
        st, final, data = get(url, limit=5_000_000)
        out.append(f"GET {url} → {st} (URL finale : {final})")
        if st == 200 and data:
            out += show_text(url.rsplit("/", 1)[-1], data, head=4, tail=8)
            rows = [r.split() for r in data.decode("utf-8", "replace").splitlines()]
            years = [r for r in rows if len(r) == 13 and r[0].isdigit()]
            if years:
                full = [r for r in years if all(float(v) > -90 for v in r[1:])]
                out.append(f"lignes annuelles à 13 champs : {len(years)} ({years[0][0]} → {years[-1][0]}), "
                           f"années complètes : {len(full)} ({full[0][0] if full else '-'} → {full[-1][0] if full else '-'})")
        out.append("")
    return out


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P10 — régression multiple : forçages et ENSO (généré)", "",
          f"Généré par `python -m etl.probe.p10` le {now}. Aucune régression, aucun indicateur calculé."]
    for title, fn in ((f"1. Dépôt {REPO} ({TAG}) : racine", github_listing),
                      ("2. IGCC 2025 : forçages et réchauffement attribué", igcc_files),
                      ("3. Archive Zenodo de l'IGCC 2025", zenodo),
                      ("4. Dépôt ClimateIndicator/forcing-timeseries (repli)", forcing_repo),
                      ("5. Niño 3.4 HadISST1.1 (NOAA PSL)", nino34)):
        try:
            body = fn()
        except Exception as exc:  # noqa: BLE001
            body = [f"échec : {type(exc).__name__} {exc}"]
        md += ["", f"## {title}", "", "```", *body, "```"]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
