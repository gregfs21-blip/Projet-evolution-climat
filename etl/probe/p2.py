"""Sonde de la phase 2 : inventaire des données disponibles, AVANT de fixer les critères.

Comme la sonde du 22/10/2026 pour P1, ce module ne calcule aucun résultat climatique (ni tendance,
ni comparaison entre sources) : il recense ce qui existe, sur quelles périodes, avec quelle complétude.
Les critères de clôture de P2 seront fixés à partir de ce constat, puis seulement les calculs lancés.

Deux sources :
1. LSH (séries mensuelles homogénéisées) : paramètres autres que TN/TX (précipitations, insolation…),
   séries de Gironde, période homogénéisée et métadonnées.
2. Données climatologiques de base quotidiennes (data.gouv.fr), département 33 : par poste et par an,
   complétude de TN, TX, RR et de l'insolation, et codes qualité.

Usage : python -m etl.probe.p2   → écrit docs/sonde-p2.md
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import logging
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from etl.context import RAW_DIR, ROOT
from etl.sources import meteofrance_lsh as lsh

log = logging.getLogger("etl.probe")
OUT = ROOT / "docs" / "sonde-p2.md"
DEPT = "33"
UA = {"User-Agent": "projet-evolution-climat (sonde P2)"}

DAILY_DATASET = "6569b51ae64326786e4e8e1a"   # « Données climatologiques de base - quotidiennes »
DAILY_API = f"https://www.data.gouv.fr/api/2/datasets/{DAILY_DATASET}/resources/?page={{page}}&page_size=100&type=main"
LSH_BUCKET = "https://meteofrance.s3.sbg.io.cloud.ovh.net/"
LSH_PREFIX = "data/synchro_ftp/REF_CC/LSH/"
LSH_CANDIDATES = ["RR", "IN", "INS", "INST", "TM", "FF"]   # paramètres à essayer si le listage échoue

# Postes LSH de Gironde (P1) : la sonde détaille leur couverture quotidienne.
P1_STATIONS = {
    "33063001": "Bordeaux-Paulin", "33214002": "Lacanau", "33236002": "Cap-Ferret",
    "33281001": "Bordeaux-Mérignac", "33504001": "Sauternes", "33529001": "Cazaux", "33550001": "Villenave-d'Ornon",
}
DAILY_VARS = ["TN", "TX", "RR", "INST"]
COMPLETE = 0.90   # année « complète » pour une variable : au moins 90 % des jours renseignés (seuil de description)


def http_get(url: str, timeout: int = 300) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def cached(url: str, name: str, raw_dir: Path) -> Path:
    path = raw_dir / "probe" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_bytes(http_get(url))
        log.info("téléchargé %s (%d octets)", name, path.stat().st_size)
    return path


# ---------------------------------------------------------------- 1. LSH


def lsh_archives() -> tuple[list[str], str]:
    """Archives LSH disponibles. Tente le listage du dépôt ; à défaut, essaie des noms candidats."""
    try:
        xml = http_get(f"{LSH_BUCKET}?prefix={LSH_PREFIX}&max-keys=1000", timeout=60)
        root = ET.fromstring(xml)
        keys = [el.text or "" for el in root.iter() if el.tag.endswith("Key")]
        names = sorted({Path(k).name for k in keys if k.endswith(".zip")})
        if names:
            return names, "listage du dépôt"
    except Exception as exc:  # noqa: BLE001
        log.warning("listage LSH impossible : %s", exc)
    found = []
    for p in LSH_CANDIDATES:
        name = f"SH_{p}_metropole.zip"
        try:
            req = urllib.request.Request(f"{LSH_BUCKET}{LSH_PREFIX}{name}", headers=UA, method="HEAD")
            urllib.request.urlopen(req, timeout=30)
            found.append(name)
        except Exception:  # noqa: BLE001
            pass
    return found, "noms candidats " + ", ".join(LSH_CANDIDATES)


def lsh_inventory(raw_dir: Path) -> tuple[list[str], dict[str, list[dict]], str]:
    archives, how = lsh_archives()
    out: dict[str, list[dict]] = {}
    for name in archives:
        m = re.fullmatch(r"SH_([A-Z]+)_metropole\.zip", name)
        if not m or m.group(1) in ("TN", "TX"):
            continue
        var = m.group(1)
        try:
            path = cached(f"{LSH_BUCKET}{LSH_PREFIX}{name}", name, raw_dir)
        except Exception as exc:  # noqa: BLE001
            out[var] = [{"error": f"téléchargement impossible : {exc}"}]
            continue
        rows = []
        with zipfile.ZipFile(path) as z:
            files = [n for n in z.namelist() if re.search(rf"{DEPT}\d{{6}}\.csv$", Path(n).name)]
            for n in sorted(files):
                text = z.read(n).decode("utf-8", errors="replace")
                try:
                    s = lsh.parse_file(text, var)
                except Exception as exc:  # noqa: BLE001
                    rows.append({"file": Path(n).name, "error": str(exc)})
                    continue
                months = sorted(s.values)
                n_hom = sum(s.homogenized.values())
                rows.append({
                    "file": Path(n).name,
                    "poste": s.station.id,
                    "nom": P1_STATIONS.get(s.station.id, s.station.name),
                    "periode_hom": f"{s.station.homogenized_period.start}-{s.station.homogenized_period.end}"
                    if s.station.homogenized_period else "—",
                    "premier": f"{months[0][0]}-{months[0][1]:02d}" if months else "—",
                    "dernier": f"{months[-1][0]}-{months[-1][1]:02d}" if months else "—",
                    "mois": len(months),
                    "part_hom": n_hom / len(months) if months else 0.0,
                    "amd": s.station.min_detectable_amplitude,
                    "ruptures": len(s.station.homogenization_breaks),
                    "unite": _unit_hint(text),
                })
        out[var] = rows
    return archives, out, how


def _unit_hint(text: str) -> str:
    for line in text.splitlines()[:30]:
        if line.startswith("#") and re.search(r"(?i)unit|mm|heure|°C|dixi", line):
            return line.lstrip("# ").strip()[:90]
    return "—"


# ---------------------------------------------------------------- 2. Quotidien


def daily_resources() -> list[dict]:
    res, page = [], 1
    while True:
        data = json.loads(http_get(DAILY_API.format(page=page), timeout=60))
        items = data.get("data", [])
        res += items
        if not data.get("next_page") or not items:
            break
        page += 1
    return res


def is_dept(title: str) -> bool:
    return bool(re.search(rf"(?:^|[_\-\s]){DEPT}(?:[_\-\s.]|$)", title)) or f"departement_{DEPT}_" in title


def read_daily(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=";")
        header = [h.strip() for h in next(reader)]
        yield header
        yield from reader


def daily_inventory(raw_dir: Path) -> dict:
    resources = daily_resources()
    mine = [r for r in resources if is_dept(r.get("title", ""))]
    stats: dict[str, dict] = defaultdict(lambda: {"nom": "", "lat": None, "lon": None, "alt": None,
                                                  "years": defaultdict(Counter), "quality": defaultdict(Counter)})
    files = []
    for r in mine:
        title, url = r.get("title", ""), r.get("url", "")
        files.append({"titre": title, "taille": r.get("filesize"), "modifie": (r.get("last_modified") or "")[:10], "url": url})
        if not re.search(r"(?i)RR-T-Vent|autres", title):
            continue
        try:
            path = cached(url, Path(url).name or f"{title}.csv.gz", raw_dir)
        except Exception as exc:  # noqa: BLE001
            files[-1]["erreur"] = str(exc)
            continue
        rows = read_daily(path)
        header = next(rows)
        idx = {h: i for i, h in enumerate(header)}
        files[-1]["colonnes"] = len(header)
        files[-1]["vars"] = [v for v in DAILY_VARS if v in idx]
        if "NUM_POSTE" not in idx or "AAAAMMJJ" not in idx:
            files[-1]["erreur"] = "colonnes NUM_POSTE / AAAAMMJJ absentes"
            continue
        present = [v for v in DAILY_VARS if v in idx]
        qcol = {v: idx.get(f"Q{v}") for v in present}
        for row in rows:
            if len(row) < len(header):
                continue
            poste, day = row[idx["NUM_POSTE"]].strip(), row[idx["AAAAMMJJ"]].strip()
            if len(day) != 8:
                continue
            st = stats[poste]
            if not st["nom"] and "NOM_USUEL" in idx:
                st["nom"] = row[idx["NOM_USUEL"]].strip()
                for k, col in (("lat", "LAT"), ("lon", "LON"), ("alt", "ALTI")):
                    if col in idx:
                        st[k] = row[idx[col]].strip()
            year = int(day[:4])
            for v in present:
                if row[idx[v]].strip() != "":
                    st["years"][year][v] += 1
                    q = qcol[v]
                    if q is not None:
                        st["quality"][v][row[q].strip() or "∅"] += 1
    return {"resources": files, "n_resources_total": len(resources), "stations": stats}


def days_in(year: int) -> int:
    return 366 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 365


def complete_years(st: dict, var: str) -> list[int]:
    return sorted(y for y, c in st["years"].items() if c[var] >= COMPLETE * days_in(y))


def runs(years: list[int]) -> str:
    """Années consécutives regroupées : [1950..1960, 1962] → « 1950-1960, 1962 »."""
    if not years:
        return "—"
    out, start, prev = [], years[0], years[0]
    for y in years[1:] + [None]:
        if y is not None and y == prev + 1:
            prev = y
            continue
        out.append(f"{start}-{prev}" if start != prev else f"{start}")
        if y is not None:
            start = prev = y
    return ", ".join(out)


# ---------------------------------------------------------------- rapport


def report(archives, lsh_rows, how, daily) -> str:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P2 — inventaire des données (généré)", "",
          f"Généré par `python -m etl.probe.p2` le {now}. Aucun résultat climatique n'est calculé ici :",
          "la sonde recense ce qui existe pour fixer les critères de P2 **avant** tout calcul.", "",
          "## 1. LSH — autres paramètres que TN/TX", "",
          f"Archives trouvées ({how}) : {', '.join(archives) or 'aucune'}.", ""]
    for var, rows in lsh_rows.items():
        md += [f"### {var} — Gironde ({len([r for r in rows if 'poste' in r])} séries)", ""]
        if not rows:
            md += ["Aucune série du département.", ""]
            continue
        md += ["| Poste | Nom | Période homogénéisée | Premier | Dernier | Mois | Part homogénéisée | AMD | Ruptures |",
               "|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            if "error" in r:
                md.append(f"| {r.get('file', '—')} | erreur : {r['error']} | | | | | | | |")
                continue
            md.append(f"| {r['poste']} | {r['nom']} | {r['periode_hom']} | {r['premier']} | {r['dernier']} | {r['mois']} | "
                      f"{r['part_hom']:.0%} | {r['amd'] if r['amd'] is not None else '—'} | {r['ruptures']} |")
        units = {r.get("unite") for r in rows if r.get("unite") and r.get("unite") != "—"}
        if units:
            md += ["", "Indications d'unité relevées dans les en-têtes : " + " / ".join(sorted(units)[:3])]
        md.append("")

    st = daily["stations"]
    md += ["## 2. Données quotidiennes — département 33", "",
           f"{daily['n_resources_total']} ressources dans le jeu ; {len(daily['resources'])} pour le département.", "",
           "| Fichier | Taille | Modifié | Variables lues | Remarque |", "|---|---|---|---|---|"]
    for f in daily["resources"]:
        size = f"{int(f['taille']) / 1e6:.1f} Mo" if f.get("taille") else "—"
        md.append(f"| {f['titre']} | {size} | {f['modifie']} | {', '.join(f.get('vars', [])) or '—'} | {f.get('erreur', '')} |")

    md += ["", f"### 2a. Postes LSH de P1 : années complètes (≥ {COMPLETE:.0%} des jours renseignés)", "",
           "| Poste | Nom | TN | TX | RR | Insolation (INST) |", "|---|---|---|---|---|---|"]
    for poste, name in P1_STATIONS.items():
        s = st.get(poste)
        if not s:
            md.append(f"| {poste} | {name} | absent | absent | absent | absent |")
            continue
        md.append(f"| {poste} | {name} | " + " | ".join(runs(complete_years(s, v)) for v in DAILY_VARS) + " |")

    md += ["", "### 2b. Codes qualité aux postes LSH (toutes années, part des valeurs)", "",
           "| Poste | Variable | Répartition des codes |", "|---|---|---|"]
    for poste, name in P1_STATIONS.items():
        s = st.get(poste)
        if not s:
            continue
        for v in DAILY_VARS:
            c = s["quality"].get(v)
            if not c:
                continue
            tot = sum(c.values())
            md.append(f"| {name} | {v} | " + ", ".join(f"{k} : {n / tot:.1%}" for k, n in c.most_common(5)) + " |")

    md += ["", f"### 2c. Tous les postes du département avec au moins 50 années complètes en TX ou en RR", "",
           "| Poste | Nom | Alt. | Années TX | Années TN | Années RR | Années INST | Plage TX |", "|---|---|---|---|---|---|---|---|"]
    rows = []
    for poste, s in st.items():
        n = {v: complete_years(s, v) for v in DAILY_VARS}
        if max(len(n["TX"]), len(n["RR"])) >= 50:
            rows.append((poste, s, n))
    for poste, s, n in sorted(rows, key=lambda r: (-len(r[2]["TX"]), -len(r[2]["RR"]))):
        rng = f"{n['TX'][0]}-{n['TX'][-1]}" if n["TX"] else "—"
        md.append(f"| {poste} | {s['nom'].title()} | {s['alt'] or '—'} | {len(n['TX'])} | {len(n['TN'])} | {len(n['RR'])} | "
                  f"{len(n['INST'])} | {rng} |")
    md += ["", f"Postes distincts rencontrés dans les fichiers lus : {len(st)}.", ""]
    return "\n".join(md)


def main(raw_dir: Path = RAW_DIR) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    archives, lsh_rows, how = lsh_inventory(raw_dir)
    daily = daily_inventory(raw_dir)
    OUT.write_text(report(archives, lsh_rows, how, daily), encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
