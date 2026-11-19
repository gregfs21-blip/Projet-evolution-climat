"""Sonde P10.3 (amplification régionale : Gironde et France contre monde) : données disponibles, avant tout calcul.

1. Séries publiées sur le site qui serviraient à l'analyse : France (TM, TX, TN, composite LSH), Gironde (régional et
   postes), monde (GISTEMP, HadCRUT5, Berkeley) : période, années manquantes, années brutes.
2. Réseau France (postes LSH du composite P5) : pour 2019-2025, nombre de postes ayant 12 mois de TN et de TX, et
   combien sont homogénéisés (Q_HOM = 1) ; fin de la période homogénéisée et date de production des fichiers.
   Sert à décider si la série France peut être prolongée au-delà de 2021, et comment.
3. Postes de Gironde du composite régional : derniers mois disponibles dans les fichiers LSH.
4. Températures mondiales des terres émergées (contrôle « terres contre océans ») : CRUTEM5, Berkeley Earth (terres),
   NOAA (terres) : accessibilité, format, première et dernière années.
Aucun facteur d'amplification, aucune régression, aucune tendance. Usage : python -m etl.probe.p10c
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone

from etl.context import RAW_DIR, ROOT
from etl.indicators import france as F
from etl.sources import meteofrance_lsh as lsh

OUT = ROOT / "docs" / "sonde-p10c.md"
PROCESSED = ROOT / "data" / "processed"
UA = {"User-Agent": "projet-evolution-climat (sonde P10.3 ; github.com/gregfs21-blip/projet-evolution-climat)"}

PUBLISHED = [
    "france/tm-france", "france/tx-france", "france/tn-france",
    "gironde/tm-annuelle-gironde", "gironde/tx-annuelle-gironde", "gironde/tn-annuelle-gironde",
    "gironde/tm-annuelle-bordeaux-merignac", "gironde/tm-annuelle-cap-ferret", "gironde/tm-annuelle-cazaux",
    "gironde/tm-annuelle-villenave-d-ornon", "gironde/tm-annuelle-bordeaux-paulin",
    "monde/temperature-gistemp-monde", "monde/temperature-hadcrut5-monde", "monde/temperature-berkeley-monde",
]
GIRONDE_REGIONAL = ("33236002", "33281001", "33529001", "33550001")
LAND = [
    ("CRUTEM5 (Met Office / CRU), terres, moyenne mondiale annuelle",
     "https://www.metoffice.gov.uk/hadobs/crutem5/data/CRUTEM.5.0.2.0/diagnostics/"
     "CRUTEM.5.0.2.0.summary_series.global.annual.csv"),
    ("Berkeley Earth, terres (TAVG), résumé annuel",
     "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_summary.txt"),
    ("NOAA Climate at a Glance, terres, annuel",
     "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land/12/12/"
     "1850-2025/data.csv"),
    ("NASA GISTEMP v4, stations météorologiques seules (Ts)",
     "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts.csv"),
]


def get(url: str):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
            return r.status, r.read(20_000_000)
    except urllib.error.HTTPError as exc:
        return exc.code, b""
    except Exception as exc:  # noqa: BLE001
        return f"erreur : {type(exc).__name__} {exc}", b""


def published() -> list[str]:
    out = ["## 1. Séries publiées sur le site", "",
           "| Indicateur | Période | Valeurs | Années manquantes | Années brutes | Référence |", "|---|---|---|---|---|---|"]
    for p in PUBLISHED:
        f = PROCESSED / f"{p}.json"
        if not f.exists():
            out.append(f"| {p} | absent | | | | |")
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        s = d["series"]
        ys = [int(t[:4]) for t, v in zip(s["time"], s["value"]) if v is not None]
        q = s.get("quality") or ["?"] * len(s["time"])
        raw = [int(t[:4]) for t, k in zip(s["time"], q) if k == "raw"]
        miss = [y for y in range(ys[0], ys[-1] + 1) if y not in ys]
        ref = d.get("reference_period")
        ref_txt = f"{ref['start']}-{ref['end']}" if ref else "-"
        out.append(f"| {p} | {ys[0]}-{ys[-1]} | {len(ys)} | {', '.join(map(str, miss)) or 'aucune'} | "
                   f"{', '.join(map(str, raw)) or 'aucune'} | {ref_txt} |")
    return out + [""]


def france_network() -> list[str]:
    tn, tx = F._all("TN", str(RAW_DIR)), F._all("TX", str(RAW_DIR))
    net = F.t_network(str(RAW_DIR))
    out = ["## 2. Réseau France (composite P5, réseau constant 1959-2021)", "",
           f"Postes du réseau : {len(net)}.", "",
           "| Année | Postes avec 12 mois de TN et TX | dont homogénéisés (TN et TX) | Départements couverts |",
           "|---|---|---|---|"]
    for y in range(2019, 2026):
        full, hom, deps = 0, 0, set()
        for p in net:
            ks = [(y, m) for m in range(1, 13)]
            if all(k in tn[p].values and k in tx[p].values for k in ks):
                full += 1
                deps.add(F.department(p))
                if all(tn[p].homogenized.get(k) and tx[p].homogenized.get(k) for k in ks):
                    hom += 1
        out.append(f"| {y} | {full} | {hom} | {len(deps)} |")
    ends = Counter(min(tn[p].station.homogenized_period.end, tx[p].station.homogenized_period.end) for p in net)
    prod = Counter((tn[p].station.file_produced or "?")[:7] for p in net)
    last = Counter(max(k for k in tn[p].values) for p in net)
    out += ["", "Fin de la période homogénéisée (min TN, TX) : "
            + ", ".join(f"{k} : {v}" for k, v in sorted(ends.items())) + ".",
            "Production des fichiers TN : " + ", ".join(f"{k} : {v}" for k, v in sorted(prod.items())) + ".",
            "Dernier mois présent (TN) : " + ", ".join(f"{a}-{m:02d} : {v}" for (a, m), v in sorted(last.items())) + ".",
            ""]
    return out


def gironde() -> list[str]:
    out = ["## 3. Postes du composite Gironde (LSH)", "",
           "| Poste | Nom | TN homogénéisé | TX homogénéisé | Dernier mois TN | Dernier mois TX | Mois 2025 (TN/TX) |",
           "|---|---|---|---|---|---|---|"]
    tn = {s.station.id: s for s in lsh.load_department("TN", "33", RAW_DIR)}
    tx = {s.station.id: s for s in lsh.load_department("TX", "33", RAW_DIR)}
    for p in GIRONDE_REGIONAL:
        a, b = tn.get(p), tx.get(p)
        if not a or not b:
            out.append(f"| {p} | absent | | | | | |")
            continue
        la, lb = max(a.values), max(b.values)
        n25 = (sum(1 for k in a.values if k[0] == 2025), sum(1 for k in b.values if k[0] == 2025))
        out.append(f"| {p} | {a.station.name} | {a.station.homogenized_period.start}-{a.station.homogenized_period.end} | "
                   f"{b.station.homogenized_period.start}-{b.station.homogenized_period.end} | {la[0]}-{la[1]:02d} | "
                   f"{lb[0]}-{lb[1]:02d} | {n25[0]}/{n25[1]} |")
    return out + [""]


def land() -> list[str]:
    out = ["## 4. Températures mondiales des terres émergées", ""]
    for name, url in LAND:
        st, data = get(url)
        out += [f"### {name}", "", f"URL : {url}", f"Statut : {st} ; {len(data)} o", ""]
        if data:
            lines = data.decode("utf-8", "replace").splitlines()
            body = [x for x in lines if x.strip() and not x.lstrip().startswith(("%", "#"))]
            out += ["```"] + [x[:200] for x in lines[:5]] + ["…"] + [x[:200] for x in body[-4:]] + ["```", ""]
    return out


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P10.3 — amplification régionale : données disponibles (généré)", "",
          f"Produit le {now} par `etl/probe/p10c.py`. Inventaire seulement : aucun facteur, aucune régression.", ""]
    for part in (published, france_network, gironde, land):
        try:
            md += part()
        except Exception as exc:  # noqa: BLE001 — une section en échec ne masque pas les autres
            md += [f"Section {part.__name__} en échec : {type(exc).__name__} {exc}", ""]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
