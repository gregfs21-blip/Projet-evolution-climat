"""Alerte de fraîcheur, exécutée après l'ETL mensuel (décision de Grég du 02/11/2026).

Deux questions, auxquelles personne ne pouvait répondre sans aller vérifier à la main :
- La période commune de comparaison entre échelles (etl/indicators/comparaison.py) peut-elle avancer ? Sa fin dépend de
  la dernière année homogénéisée de la Gironde et du globe, et du nombre de stations françaises couvrant toute la fenêtre.
- Des téléchargements ont-ils échoué ? Dans ce cas l'ETL réutilise l'ancien fichier, et la série peut rester ancienne
  sans que rien ne se voie.

Ce module n'écrit aucune donnée et ne change aucun chiffre : il ouvre une issue GitHub, déplacer la fenêtre reste une
décision consignée dans docs/phases.md.

    python -m etl.fraicheur --log etl.log --issues
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from etl.context import PROCESSED_DIR, make_context
from etl.indicators import comparaison as C
from etl.indicators import france as F
from etl.schema import Indicator
from etl.sources import meteofrance_lsh as lsh

log = logging.getLogger("fraicheur")

MIN_STATIONS = 220                      # taille du réseau actuel de la série France (1959-2021)
STALE_MARKER = "cache réutilisé"        # phrase commune des sources quand un téléchargement échoue
ISSUE_LIMIT = 60000                     # GitHub refuse les corps d'issue trop longs


@dataclass
class Report:
    current_end: int
    gironde_end: int
    monde_end: int
    stations: dict[int, int]            # fin de période possible → stations françaises couvrant toute la fenêtre
    possible_end: int | None
    stale: list[str] = field(default_factory=list)


def last_homogenized_year(ind: Indicator) -> int:
    quality = ind.series.quality or ["homogenized"] * len(ind.series.time)
    years = [int(t[:4]) for t, v, q in zip(ind.series.time, ind.series.value, quality) if v is not None and q != "raw"]
    if not years:
        raise ValueError(f"{ind.id} : aucune année homogénéisée")
    return max(years)


def possible_end(current_end: int, gironde_end: int, monde_end: int, stations: dict[int, int], minimum: int = MIN_STATIONS) -> int | None:
    """Fin de période la plus tardive que permettent les trois séries, ou None si la fenêtre ne peut pas avancer."""
    limit = min(gironde_end, monde_end)
    ok = [y for y, n in stations.items() if current_end < y <= limit and n >= minimum]
    return max(ok) if ok else None


def france_network_sizes(raw_dir: Path, start: int, ends: range) -> dict[int, int]:
    """Stations ayant TN et TX homogénéisés chaque année de `start` à la fin de période, pour chaque fin possible."""
    # L'archive vient d'être téléchargée par l'ETL : on ne la redemande que si elle manque (exécution partielle).
    tn, tx = ({s.station.id: s for s in lsh.load_department(v, "", raw_dir, download=not lsh.archive_path(v, raw_dir).exists())}
              for v in ("TN", "TX"))
    homogenized = []
    for p in tn.keys() & tx.keys():
        _, h_tn = F.station_annual("TN", tn[p], tx[p])
        _, h_tx = F.station_annual("TX", tn[p], tx[p])
        homogenized.append(h_tn & h_tx)
    return {end: sum(all(y in h for y in range(start, end + 1)) for h in homogenized) for end in ends}


def stale_downloads(log_text: str) -> list[str]:
    return sorted({line.strip() for line in log_text.splitlines() if STALE_MARKER in line})


def build_report(out_dir: Path, raw_dir: Path, log_text: str) -> Report:
    gironde = Indicator.model_validate_json((out_dir / "gironde" / "tm-annuelle-gironde.json").read_text(encoding="utf-8"))
    monde = Indicator.model_validate_json((out_dir / "monde" / "temperature-hadcrut5-monde.json").read_text(encoding="utf-8"))
    g_end, m_end = last_homogenized_year(gironde), last_homogenized_year(monde)
    current = C.WINDOW.end
    # Jusqu'à la plus récente des deux séries : le rapport montre aussi ce que la France permettrait au-delà de la limite.
    stations = france_network_sizes(raw_dir, C.WINDOW.start, range(current, max(g_end, m_end, current) + 1))
    return Report(current, g_end, m_end, stations, possible_end(current, g_end, m_end, stations), stale_downloads(log_text))


def summary(r: Report) -> str:
    rows = "\n".join(f"| {y} | {n} |" for y, n in sorted(r.stations.items()))
    return (
        f"Fenêtre actuelle : {C.WINDOW.start}-{r.current_end}. Dernière année homogénéisée : Gironde {r.gironde_end}, "
        f"globe {r.monde_end}. Seuil France : {MIN_STATIONS} stations.\n\n"
        f"| Fin de période ({C.WINDOW.start}-…) | Stations France (TN et TX) |\n|---|---|\n{rows}\n"
    )


def issues_for(r: Report) -> list[tuple[str, str]]:
    out = []
    if r.possible_end is not None:
        out.append((
            f"Période commune : extension possible jusqu'à {r.possible_end}",
            "Le contrôle mensuel indique que la comparaison entre échelles peut avancer. Aucun chiffre n'a changé.\n\n"
            + summary(r)
            + "\n**À décider :** déplacer la fenêtre, puis consigner la décision dans `docs/phases.md`.\n\n"
            "**Ce qu'il faudra modifier :** `WINDOW` dans `etl/indicators/comparaison.py` et `T_SPAN` dans "
            "`etl/indicators/france.py`. `T_SPAN` définit le réseau de stations de toute la série France : cela change "
            "aussi la tendance mise en avant de la France et sa carte départementale.",
        ))
    if r.stale:
        lines = "\n".join(f"- {s}" for s in r.stale)
        out.append((
            "ETL : téléchargements en échec, anciens fichiers réutilisés",
            "Ces sources n'ont pas pu être téléchargées lors du dernier ETL. Les séries concernées ont été calculées avec "
            f"l'ancien fichier et peuvent ne pas être à jour.\n\n{lines}\n\n"
            "Si le prochain ETL mensuel réussit, cette issue peut être fermée.",
        ))
    return out


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def open_issues(issues: list[tuple[str, str]]) -> list[str]:
    """Ouvre les issues manquantes. Une issue déjà ouverte avec le même titre n'est pas dupliquée : pas d'alerte chaque mois."""
    if not issues:
        return []
    existing = {i["title"] for i in json.loads(gh("issue", "list", "--state", "open", "--limit", "200", "--json", "title"))}
    created = []
    for title, body in issues:
        if title not in existing:
            gh("issue", "create", "--title", title, "--body", body[:ISSUE_LIMIT])
            created.append(title)
    return created


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--log", type=Path, help="Journal de l'ETL, pour y repérer les téléchargements en échec")
    parser.add_argument("--issues", action="store_true", help="Ouvre les issues GitHub (sinon, affiche seulement le rapport)")
    args = parser.parse_args(argv)

    log_text = args.log.read_text(encoding="utf-8", errors="replace") if args.log and args.log.exists() else ""
    report = build_report(PROCESSED_DIR, make_context().raw_dir, log_text)
    text = summary(report)
    log.info(text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write("## Fraîcheur\n\n" + text + (f"\nTéléchargements en échec : {len(report.stale)}\n" if report.stale else ""))
    issues = issues_for(report)
    log.info("Alertes : %s", [t for t, _ in issues] or "aucune")
    if args.issues:
        log.info("Issues ouvertes : %s", open_issues(issues) or "aucune")
    return 0


if __name__ == "__main__":
    sys.exit(main())
