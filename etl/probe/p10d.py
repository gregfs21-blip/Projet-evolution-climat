"""Sonde P10.4 (cohérence physique) : données disponibles, avant tout calcul.

Trois contrôles prévus au cadrage de P10 : vapeur d'eau contre température (Clausius-Clapeyron), bilan du niveau marin,
troposphère contre stratosphère ; plus, à proposer, déséquilibre énergétique contre contenu thermique de l'océan.
Pour chaque source candidate : accessibilité, format, première et dernière lignes, liste des fichiers d'un répertoire.
Aucune tendance, aucun rapport, aucune régression. Usage : python -m etl.probe.p10d
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-p10d.md"
PROCESSED = ROOT / "data" / "processed"
UA = {"User-Agent": "projet-evolution-climat (sonde P10.4 ; github.com/gregfs21-blip/projet-evolution-climat)"}

FILES = {
    "Stratosphère": [
        ("RSS 4.0, basse stratosphère (TLS), moyenne mondiale",
         "https://data.remss.com/msu/graphics/TLS_v40/time_series/RSS_TS_channel_TLS_Global_Land_And_Sea_v04_0.txt"),
        ("UAH 6.1, basse stratosphère (LS)", "https://www.nsstc.uah.edu/data/msu/v6.1/tls/uahncdc_ls_6.1.txt"),
        ("RSS 4.0, moyenne troposphère (TMT), information",
         "https://data.remss.com/msu/graphics/TMT_v40/time_series/RSS_TS_channel_TMT_Global_Land_And_Sea_v04_0.txt"),
    ],
}
LISTINGS = {
    "Vapeur d'eau": [
        ("RSS, vapeur d'eau intégrée sur les océans (répertoire)", "https://data.remss.com/vapor/monthly_1deg/"),
        ("RSS, vapeur d'eau (répertoire parent)", "https://data.remss.com/vapor/"),
        ("HadISDH (Met Office), humidité de surface : page d'accueil", "https://www.metoffice.gov.uk/hadobs/hadisdh/"),
    ],
    "Niveau marin : dilatation thermique": [
        ("NOAA NCEI, contenu thermique et niveau thermostérique, annuel (répertoire)",
         "https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/yearly/"),
        ("NOAA NCEI, idem, pentadaire (répertoire)",
         "https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/pentad/"),
        ("NOAA NCEI, idem (répertoire parent)",
         "https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/"),
    ],
    "Niveau marin : masse (glaciers, calottes, eaux continentales)": [
        ("ESA CCI Sea Level Budget Closure (CEDA, répertoire)",
         "https://dap.ceda.ac.uk/neodc/esacci/sea_level_budget_closure/data/"),
        ("IMBIE (bilan de masse des calottes), page de téléchargement", "https://imbie.org/data-downloads/"),
        ("NASA, GRACE / GRACE-FO, masse de l'océan (PO.DAAC)",
         "https://podaac.jpl.nasa.gov/dataset/OCEAN_MASS_TIME_SERIES_GRACE-FO_JPL_RL06.3_V4"),
        ("NASA Vital Signs, masse des calottes (page)", "https://climate.nasa.gov/vital-signs/ice-sheets/"),
    ],
}
PUBLISHED = ["niveau-mer-monde", "ohc-700-monde", "ohc-2000-monde", "desequilibre-energetique-monde",
             "tlt-rss-monde", "tlt-uah-monde", "sst-hadsst-monde", "temperature-hadcrut5-monde"]


def get(url: str):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
            return r.status, r.read(30_000_000)
    except urllib.error.HTTPError as exc:
        return exc.code, b""
    except Exception as exc:  # noqa: BLE001
        return f"erreur : {type(exc).__name__} {exc}", b""


def head_tail(data: bytes) -> list[str]:
    lines = data.decode("utf-8", "replace").splitlines()
    body = [x for x in lines if x.strip()]
    return ["```"] + [x[:200] for x in lines[:8]] + ["…"] + [x[:200] for x in body[-4:]] + ["```", ""]


def links(data: bytes, base: str) -> list[str]:
    html = data.decode("utf-8", "replace")
    found = sorted(set(re.findall(r'href="([^"#?]+)"', html)))
    keep = [h for h in found if not h.startswith(("javascript:", "mailto:")) and h not in ("../", "/")]
    return keep


def published() -> list[str]:
    out = ["## 1. Séries déjà publiées sur le site", "", "| Indicateur | Fréquence | Période | Valeurs | Unité | Source |",
           "|---|---|---|---|---|---|"]
    for p in PUBLISHED:
        d = json.loads((PROCESSED / "monde" / f"{p}.json").read_text(encoding="utf-8"))
        s = d["series"]
        t = [x for x, v in zip(s["time"], s["value"]) if v is not None]
        out.append(f"| {p} | {d['frequency']} | {t[0][:7]}-{t[-1][:7]} | {len(t)} | {d['unit']} | "
                   f"{d['provenance'].get('source_name', '')[:80]} |")
    return out + [""]


def files() -> list[str]:
    out = ["## 2. Fichiers candidats", ""]
    for group, items in FILES.items():
        out += [f"### {group}", ""]
        for name, url in items:
            st, data = get(url)
            out += [f"**{name}** — {url}", f"Statut : {st} ; {len(data)} o", ""]
            if data:
                out += head_tail(data)
    return out


def listings() -> list[str]:
    out = ["## 3. Répertoires et pages candidats", ""]
    for group, items in LISTINGS.items():
        out += [f"### {group}", ""]
        for name, url in items:
            st, data = get(url)
            out += [f"**{name}** — {url}", f"Statut : {st} ; {len(data)} o", ""]
            if data:
                ls = links(data, url)
                interesting = [h for h in ls if re.search(r"(time_?series|_ts|ts_|annual|\.dat|\.csv|\.txt|\.nc|"
                                                          r"thermo|steric|mass|q|tsl|T-dC|h22|v\d)", h, re.I)]
                out += [f"{len(ls)} liens ; retenus ({len(interesting)}) :", "```"] + \
                       [h[:180] for h in interesting[:80]] + ["```", ""]
    return out


RAW_PAGES = [
    ("RSS vapeur, répertoire mensuel (HTML brut)", "https://data.remss.com/vapor/monthly_1deg/"),
    ("RSS vapeur, répertoire parent (HTML brut)", "https://data.remss.com/vapor/"),
]
ALL_LINKS = [
    ("HadISDH, page d'accueil (tous les liens)", "https://www.metoffice.gov.uk/hadobs/hadisdh/"),
    ("NOAA NCEI 3M_HEAT_CONTENT/DATA/basin (tous les liens)",
     "https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/"),
    ("NOAA NCEI 3M_HEAT_CONTENT/DATA (tous les liens)",
     "https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/"),
    ("NOAA NCEI 3M_HEAT_CONTENT (tous les liens)", "https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/"),
    ("IMBIE, page d'accueil", "https://imbie.org/"),
    ("CEDA, ESA CCI Sea Level Budget Closure (autre hôte)",
     "https://data.ceda.ac.uk/neodc/esacci/sea_level_budget_closure/data"),
    ("CSR, mascons GRACE RL06 (page)", "https://www2.csr.utexas.edu/grace/RL06_mascons.html"),
    ("SEANOE, budget WCRP 2018 (doi 10.17882/54854)", "https://www.seanoe.org/data/00444/55547/"),
]
API = [
    ("Zenodo, Frederikse et al. 2020, budget du niveau marin 1900-2018 (fiche)", "https://zenodo.org/api/records/3862995"),
]


def extra() -> list[str]:
    out = ["## 4. Compléments (deuxième passage)", ""]
    for name, url in RAW_PAGES:
        st, data = get(url)
        out += [f"**{name}** — {url}", f"Statut : {st}", "```", data.decode("utf-8", "replace")[:1500], "```", ""]
    for name, url in ALL_LINKS:
        st, data = get(url)
        out += [f"**{name}** — {url}", f"Statut : {st} ; {len(data)} o", ""]
        if data:
            ls = links(data, url) + sorted(set(re.findall(r"href='([^'#?]+)'", data.decode("utf-8", "replace"))))
            out += ["```"] + [h[:180] for h in ls[:120]] + ["```", ""]
    for name, url in API:
        st, data = get(url)
        out += [f"**{name}** — {url}", f"Statut : {st}", ""]
        if data:
            try:
                rec = json.loads(data)
                out += [f"Titre : {rec.get('metadata', {}).get('title')}", "```"] + \
                       [f"{f.get('key')} {f.get('size')} {f.get('links', {}).get('self')}" for f in rec.get("files", [])] + \
                       ["```", ""]
            except ValueError:
                out += ["(réponse non JSON)", ""]
    return out


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P10.4 — cohérence physique : données disponibles (généré)", "",
          f"Produit le {now} par `etl/probe/p10d.py`. Inventaire seulement : aucune tendance, aucun rapport.", ""]
    for part in (published, files, listings, extra):
        try:
            md += part()
        except Exception as exc:  # noqa: BLE001
            md += [f"Section {part.__name__} en échec : {type(exc).__name__} {exc}", ""]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
