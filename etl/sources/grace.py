"""Source : masse de l'océan mondial, GRACE et GRACE-FO, solution mascons JPL RL06.3Mv4 (NASA PO.DAAC).

Accès constaté par la sonde du 20/11/2026 (docs/sonde-p10d.md, sixième passage) : le fichier texte
« ocean_mass_AAAAMM_AAAAMM.txt » de la collection OCEAN_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4 se télécharge par
le catalogue CMR avec le jeton NASA Earthdata (secret EARTHDATA_TOKEN, jamais affiché). Le jeton n'est transmis
qu'aux hôtes Earthdata : la redirection vers le stockage (CloudFront) se fait sans en-tête d'autorisation.

Le fichier donne, en mm de niveau marin, l'anomalie mensuelle de masse de l'océan par rapport à avril 2002, corrigée de
l'ajustement isostatique glaciaire (ICE6G-D) et de la masse de l'atmosphère, son incertitude (1 σ) et la même série
désaisonnalisée par JPL. Le relevé (workflow « Copernicus ») l'extrait dans data/sources/grace/ocean-mass.csv ;
l'ETL ne lit que ce CSV. Les mois sans mesure (trou GRACE / GRACE-FO de juillet 2017 à mai 2018, mois isolés) restent
absents : rien n'est complété.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from etl.context import ROOT

OUT_DIR = ROOT / "data" / "sources" / "grace"
SHORT_NAME = "OCEAN_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4"
CMR = f"https://cmr.earthdata.nasa.gov/search/granules.json?short_name={SHORT_NAME}&page_size=10&sort_key=-start_date"
PAGE = "https://podaac.jpl.nasa.gov/dataset/OCEAN_MASS_TELLUS_MASCON_CRI_TIME_SERIES_RL06.3_V4"
SOURCE_NAME = "NASA JPL — GRACE et GRACE-FO, mascons RL06.3Mv4, masse de l'océan mondial (Wiese et al., 2022)"
LICENSE = "Domaine public (NASA), citation demandée"
UA = "projet-evolution-climat"
FIELDS = ["time", "mass_mm", "sigma_mm", "deseasoned_mm"]
TRIES, WAIT = 4, 30      # essais et pause croissante (s)


class _EarthdataOnly(urllib.request.HTTPRedirectHandler):
    """Suit les redirections ; le jeton n'est remis qu'aux hôtes *.earthdata.nasa.gov."""

    def __init__(self, token: str):
        self.token = token
        self.chain: list[str] = []      # hôtes successifs, pour le diagnostic (jamais le jeton)

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        self.chain.append(f"{code} → {urllib.parse.urlparse(newurl).hostname}")
        if new is not None:
            new.remove_header("Authorization")
            new.unredirected_hdrs.pop("Authorization", None)
            host = urllib.parse.urlparse(newurl).hostname or ""
            if host.endswith("earthdata.nasa.gov"):
                new.add_unredirected_header("Authorization", f"Bearer {self.token}")
        return new


def latest() -> tuple[str, str]:
    with urllib.request.urlopen(urllib.request.Request(CMR, headers={"User-Agent": UA}), timeout=60) as r:
        entries = json.loads(r.read())["feed"]["entry"]
    for g in entries:
        for lk in g.get("links", []):
            href = lk.get("href", "")
            if href.startswith("https://") and href.endswith(".txt") and "ocean_mass" in href and "data#" in lk.get("rel", ""):
                return g["title"], href
    raise RuntimeError("GRACE : aucun fichier ocean_mass dans le catalogue CMR")


def parse(text: str) -> list[dict]:
    """Lignes après « Header_End » : temps décimal, masse, incertitude, masse désaisonnalisée (mm)."""
    rows, body = [], False
    for ln in text.splitlines():
        if ln.startswith("HDR Header_End"):
            body = True
            continue
        if not body or not ln.strip():
            continue
        c = ln.split()
        if len(c) != 4:
            raise ValueError(f"GRACE : ligne inattendue « {ln[:60]} »")
        rows.append(dict(zip(FIELDS, (float(c[0]), float(c[1]), float(c[2]), float(c[3])))))
    if len(rows) < 100:
        raise ValueError(f"GRACE : {len(rows)} mois lus, format probablement changé")
    return rows


def collect(out_dir: Path = OUT_DIR) -> str:
    token = os.environ.get("EARTHDATA_TOKEN", "")
    if not token:
        return "EARTHDATA_TOKEN absent : rien à faire"
    out_dir.mkdir(parents=True, exist_ok=True)
    meta_path = out_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    title, href = latest()
    if meta.get("granule") == title and (out_dir / "ocean-mass.csv").exists():
        return f"GRACE : à jour ({title})"
    errors = []
    for attempt in range(TRIES):          # PO.DAAC répond parfois 403 ou 504 de façon passagère
        handler = _EarthdataOnly(token)
        opener = urllib.request.build_opener(handler)
        req = urllib.request.Request(href, headers={"User-Agent": UA})
        req.add_unredirected_header("Authorization", f"Bearer {token}")
        try:
            with opener.open(req, timeout=120) as r:
                text = r.read().decode("utf-8", errors="replace")
            break
        except urllib.error.HTTPError as exc:
            errors.append(f"{exc.code} sur {urllib.parse.urlparse(exc.url or href).hostname} (redirections : "
                          f"{' ; '.join(handler.chain) or 'aucune'})")
            if attempt + 1 < TRIES:
                time.sleep(WAIT * (attempt + 1))
    else:
        raise RuntimeError(f"fichier {urllib.parse.urlparse(href).path.rsplit('/', 1)[-1]}, {TRIES} essais : "
                           + " ; ".join(errors))
    if errors:
        print(f"GRACE : réussi après {len(errors)} échec(s) : {' ; '.join(errors)}", flush=True)
    rows = parse(text)
    with (out_dir / "ocean-mass.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    trend = next((ln.split(":", 1)[1].strip() for ln in text.splitlines() if ln.startswith("HDR Ocean Mass Trend")), None)
    meta = {"granule": title, "rows": len(rows), "published_trend": trend,
            "collected": datetime.now(timezone.utc).isoformat()}
    meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return f"GRACE : relevé {title}, {len(rows)} mois"


def load(out_dir: Path = OUT_DIR) -> list[dict]:
    with (out_dir / "ocean-mass.csv").open(encoding="utf-8") as f:
        return [{k: float(v) for k, v in r.items()} for r in csv.DictReader(f)]


def main() -> int:
    try:
        print(collect(), flush=True)
    except Exception as exc:  # noqa: BLE001
        msg = f"GRACE : ÉCHEC {type(exc).__name__} {str(exc)[:300]}"
        print(msg)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(f"::error title=GRACE::{msg}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
