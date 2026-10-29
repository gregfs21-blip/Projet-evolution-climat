"""Sonde P5 (France) : inventaire des Longues Séries Homogénéisées de la métropole. Aucun indicateur calculé.

Pour chaque paramètre (TN, TX, RR, IN) : nombre de séries, départements couverts, période homogénéisée déclarée,
premières et dernières années dont les 12 mois sont homogénéisés, et nombre de stations à réseau constant sur
quelques fenêtres candidates. Aucune tendance, aucune moyenne de température.
Usage : python -m etl.probe.p5   → docs/sonde-p5.md
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import datetime, timezone

from etl.context import RAW_DIR, ROOT
from etl.sources import meteofrance_lsh as lsh

OUT = ROOT / "docs" / "sonde-p5.md"
WINDOWS = [(1901, 2022), (1931, 2022), (1951, 2022), (1959, 2021), (1961, 2022), (1961, 2020)]


def full_years(s: lsh.LshSeries) -> set[int]:
    years = {y for y, _ in s.values}
    return {y for y in years if all(s.homogenized.get((y, m)) for m in range(1, 13))}


def inventory(md: list[str], var: str) -> dict[str, set[int]]:
    md += ["", f"## {var}"]
    try:
        series = lsh.load_department(var, "", RAW_DIR)
    except Exception as exc:  # noqa: BLE001
        md += ["", f"**échec : {type(exc).__name__} {exc}**"]
        return {}
    full = {s.station.id: full_years(s) for s in series}
    deps = Counter(s.station.id[:2] for s in series)
    ends = Counter(max(f) if f else None for f in full.values())
    starts = Counter((min(f) // 10) * 10 if f else None for f in full.values())
    md += ["", f"- {len(series)} séries, {len(deps)} départements (2 premiers chiffres du poste)",
           f"- dernière année entièrement homogénéisée : {sorted(ends.items(), key=lambda kv: (kv[0] is None, kv[0]))}",
           f"- décennie de la première année homogénéisée : {sorted(starts.items(), key=lambda kv: (kv[0] is None, kv[0]))}",
           f"- départements sans série : {sorted(set(f'{d:02d}' for d in range(1, 96) if d != 20) - set(deps))}"]
    for a, b in WINDOWS:
        n = sum(1 for f in full.values() if all(y in f for y in range(a, b + 1)))
        md.append(f"- réseau constant {a}-{b} (12 mois homogénéisés chaque année) : {n} stations")
    md += ["", "| poste | nom | alt. | période déclarée | années complètes homogénéisées |", "|---|---|---|---|---|"]
    for s in series:
        f = full[s.station.id]
        hp = s.station.homogenized_period
        md.append(f"| {s.station.id} | {s.station.name} | {s.station.altitude:.0f} | {hp.start}-{hp.end} | "
                  f"{(str(min(f)) + '-' + str(max(f)) + f' ({len(f)})') if f else '—'} |")
    return full


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P5 — Longues Séries Homogénéisées de la métropole (généré)", "",
          f"Généré par `python -m etl.probe.p5` le {now}. Inventaire seulement : aucune valeur de température ni "
          "tendance n'est calculée."]
    full = {}
    for var in ("TN", "TX", "RR", "IN"):
        full[var] = inventory(md, var)
        OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    both = set(full.get("TN", {})) & set(full.get("TX", {}))
    md += ["", "## TN et TX à la fois", "", f"- {len(both)} postes ont les deux séries"]
    for a, b in WINDOWS:
        n = sum(1 for p in both if all(y in full["TN"][p] and y in full["TX"][p] for y in range(a, b + 1)))
        md.append(f"- réseau constant {a}-{b}, TN et TX : {n} stations")
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
