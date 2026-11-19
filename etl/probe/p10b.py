"""Sonde P10.2 (valeurs extrêmes non stationnaires en Gironde) : données disponibles, avant tout ajustement.

Pour chaque poste de Gironde disposant d'une série LSH de TX (correction B de P2a possible) : années complètes,
années homogénéisées, dernière rupture corrigée par Météo-France, maximum annuel de TX (TXx) corrigé et brut avec sa
date, et maximum annuel de la moyenne de TX sur 3 jours (TX3x). Les valeurs sont écrites telles quelles dans
docs/sonde-p10b.md (tableau + bloc JSON) pour que le cadrage repose sur un constat. Aucun ajustement GEV, aucune
tendance. Usage : python -m etl.probe.p10b
"""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone

from etl.context import RAW_DIR, ROOT
from etl.indicators import extremes as X

OUT = ROOT / "docs" / "sonde-p10b.md"


def tx3(series: dict[str, float], year: int) -> float | None:
    """Maximum annuel de la moyenne de TX sur 3 jours consécutifs, sans trou."""
    best = None
    d = date(year, 1, 1)
    while d.year == year:
        keys = [(d + timedelta(days=k)).isoformat() for k in range(3)]
        if all(k in series for k in keys):
            v = sum(series[k] for k in keys) / 3
            best = v if best is None or v > best else best
        d += timedelta(days=1)
    return best


def station(sid: str) -> tuple[list[str], dict]:
    sd = X.station_daily("TX", sid, RAW_DIR)
    years = sorted(sd.year_status)
    hom = sd.hom_years()
    out = [f"### {sd.station.name} ({sid})", "",
           f"Années complètes : {len(years)} ({years[0] if years else '-'}-{years[-1] if years else '-'}) ; "
           f"homogénéisées (correction B) : {len(hom)} ({hom[0] if hom else '-'}-{hom[-1] if hom else '-'}) ; "
           f"plus longue suite homogénéisée : {X.longest_run(hom)[0] if hom else '-'}-"
           f"{X.longest_run(hom)[-1] if hom else '-'} ; dernier régime après rupture MF : {sd.last_break_regime}", "",
           "| Année | Statut | TXx corrigé | date | TXx brut | TX3x corrigé |", "|---|---|---|---|---|---|"]
    data = {}
    for y in years:
        src = sd.corrected if sd.year_status[y] == "homogenized" else sd.raw
        days = {d: v for d, v in src.items() if d.startswith(f"{y}-")}
        raw_days = {d: v for d, v in sd.raw.items() if d.startswith(f"{y}-")}
        dmax = max(days, key=days.get)
        t3 = tx3(src, y)
        data[y] = {"status": sd.year_status[y], "txx": round(days[dmax], 2), "date": dmax,
                   "txx_raw": round(max(raw_days.values()), 2), "tx3x": None if t3 is None else round(t3, 2)}
        out.append(f"| {y} | {sd.year_status[y]} | {days[dmax]:.1f} | {dmax} | {max(raw_days.values()):.1f} | "
                   f"{'' if t3 is None else f'{t3:.1f}'} |")
    return out, {"name": sd.station.name, "last_break_regime": sd.last_break_regime, "years": data}


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P10.2 — maxima annuels de TX en Gironde (généré)", "",
          f"Généré par `python -m etl.probe.p10b` le {now}. Aucun ajustement, aucune tendance.", ""]
    payload = {}
    for sid in X.stations_for("TX", RAW_DIR):
        try:
            lines, data = station(sid)
            payload[sid] = data
        except Exception as exc:  # noqa: BLE001
            lines = [f"### {sid}", "", f"échec : {type(exc).__name__} {exc}"]
        md += [*lines, ""]
    md += ["## Données brutes (JSON)", "", "```json", json.dumps(payload, ensure_ascii=False), "```", ""]
    OUT.write_text("\n".join(md), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
