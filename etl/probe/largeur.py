"""Sonde « largeur d'abord » : accessibilité et format réel des sources candidates, AVANT d'écrire leurs lecteurs.

Aucun résultat climatique n'est calculé. Pour chaque source : statut HTTP, taille, type, et premières lignes (ou
liste des fichiers d'une archive). Le rapport sert à écrire les lecteurs sur le format constaté, pas supposé.

Usage : python -m etl.probe.largeur   → écrit docs/sonde-largeur.md
"""

from __future__ import annotations

import gzip
import io
import re
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-largeur.md"
UA = {"User-Agent": "projet-evolution-climat (sonde)"}
MAX_BYTES = 40_000_000
HEAD = 14

# (identifiant, paramètre du projet, URL)
SOURCES = [
    ("co2-mlo", "GES — CO₂ Mauna Loa annuel", "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.csv"),
    ("co2-gl", "GES — CO₂ global annuel", "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_gl.csv"),
    ("ch4-gl", "GES — CH₄ global annuel", "https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_annmean_gl.csv"),
    ("n2o-gl", "GES — N₂O global annuel", "https://gml.noaa.gov/webdata/ccgg/trends/n2o/n2o_annmean_gl.csv"),
    ("gistemp", "Température globale — NASA GISTEMP v4", "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"),
    ("hadcrut5", "Température globale — HadCRUT5",
     "https://www.metoffice.gov.uk/hadobs/hadcrut5/data/HadCRUT.5.0.2.0/analysis/diagnostics/HadCRUT.5.0.2.0.analysis.summary_series.global.annual.csv"),
    ("berkeley", "Température globale — Berkeley Earth",
     "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_summary.txt"),
    ("hadsst4", "Température de la mer — HadSST4 global annuel",
     "https://www.metoffice.gov.uk/hadobs/hadsst4/data/csv/HadSST.4.0.1.0_annual_GLOBE.csv"),
    ("oni", "El Niño — indice ONI (NOAA CPC)", "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"),
    ("nsidc-n09-v3", "Fonte des glaces — banquise arctique de septembre (v3)",
     "https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/data/N_09_extent_v3.0.csv"),
    ("nsidc-n09-v4", "Fonte des glaces — banquise arctique de septembre (v4)",
     "https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/data/N_09_extent_v4.0.csv"),
    ("nsidc-s02-v4", "Fonte des glaces — banquise antarctique de février (v4)",
     "https://noaadata.apps.nsidc.org/NOAA/G02135/south/monthly/data/S_02_extent_v4.0.csv"),
    ("ohc-700", "Contenu thermique des océans 0-700 m (NOAA NCEI)",
     "https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/yearly/h22-w0-700m.dat"),
    ("ohc-2000", "Contenu thermique des océans 0-2000 m (NOAA NCEI)",
     "https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/yearly/h22-w0-2000m.dat"),
    ("gmsl-star", "Niveau des océans — altimétrie (NOAA STAR)",
     "https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_gbl_free_txj1j2_90.csv"),
    ("gmsl-csiro", "Niveau des océans — reconstruction CSIRO (Church & White)",
     "https://www.cmar.csiro.au/sealevel/downloads/church_white_gmsl_2011_up.zip"),
    ("psmsl-list", "Niveau des océans — liste des marégraphes PSMSL (annuel RLR)",
     "https://psmsl.org/data/obtaining/rlr.annual.data/filelist.txt"),
    ("ozone-hole", "Couche d'ozone — trou antarctique (NASA Ozone Watch)",
     "https://ozonewatch.gsfc.nasa.gov/meteorology/annual_data.txt"),
    ("ibtracs-na", "Ouragans — IBTrACS Atlantique Nord (NOAA)",
     "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.NA.list.v04r01.csv"),
    ("igra-merignac", "Température en altitude — radiosondages Mérignac, dérivés (IGRA)",
     "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/derived-por/FRM00007510-drvd.txt.zip"),
    ("gcb", "Puits de carbone — Global Carbon Budget (liste des fichiers)",
     "https://globalcarbonbudgetdata.org/latest-data.html"),
    ("ceres", "Déséquilibre énergétique — CERES EBAF (page d'accès)", "https://ceres.larc.nasa.gov/data/"),
]


def get(url: str) -> tuple[int | str, bytes, str]:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read(MAX_BYTES), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        return exc.code, b"", ""
    except Exception as exc:  # noqa: BLE001
        return f"erreur : {type(exc).__name__} {exc}"[:160], b"", ""


def head(data: bytes, url: str) -> list[str]:
    if url.endswith(".zip"):
        try:
            z = zipfile.ZipFile(io.BytesIO(data))
            names = z.namelist()
            first = z.read(names[0]).decode("utf-8", errors="replace").splitlines()[:HEAD] if names else []
            return [f"[archive : {len(names)} fichier(s) : {', '.join(names[:6])}]"] + first
        except Exception as exc:  # noqa: BLE001
            return [f"[archive illisible : {exc}]"]
    if url.endswith(".gz"):
        data = gzip.decompress(data)
    text = data.decode("utf-8", errors="replace")
    if "<html" in text[:2000].lower():
        links = sorted(set(re.findall(r'href="([^"]+\.(?:csv|txt|xlsx|nc|zip))"', text)))[:20]
        return ["[page HTML] liens de données trouvés :"] + links
    return text.splitlines()[:HEAD]


def psmsl_france(data: bytes) -> list[str]:
    """Marégraphes français de la façade atlantique dans la liste PSMSL."""
    lines = data.decode("utf-8", errors="replace").splitlines()
    keep = [ln for ln in lines if re.search(r"(?i)verdon|arcachon|eyrac|bordeaux|brest|saint-nazaire|st\.? nazaire|socoa|"
                                            r"boucau|la rochelle|pallice|royan|cordouan", ln)]
    return keep[:30]


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde « largeur d'abord » — sources candidates (généré)", "",
          f"Généré par `python -m etl.probe.largeur` le {now}. Aucun calcul : accessibilité et format constaté.", "",
          "| Source | Paramètre | Statut | Taille | Type |", "|---|---|---|---|---|"]
    details = []
    for sid, what, url in SOURCES:
        status, data, ctype = get(url)
        md.append(f"| `{sid}` | {what} | {status} | {len(data) / 1e3:.0f} ko | {ctype[:40]} |")
        details += ["", f"### `{sid}` — {what}", "", url, "", "```"]
        if data:
            details += head(data, url)
            if sid == "psmsl-list":
                details += ["", "[stations façade atlantique française]"] + psmsl_france(data)
        else:
            details.append("(aucune donnée)")
        details.append("```")
    OUT.write_text("\n".join(md + details) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
