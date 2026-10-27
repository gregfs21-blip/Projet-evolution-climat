"""Sonde P2b : disponibilité des données (aucun indice climatique calculé).

Pour chaque série LSH RR de Gironde : années quotidiennes complètes (ETCCDI), années entièrement corrigeables par
la méthode B′, rupture la plus récente, appartenance possible au composite 1961-2017 ; pour l'ETP et le SPEI :
couverture homogénéisée TN, TX, RR des trois postes. Sert à écrire le registre (F1) avant tout calcul d'indice.
Usage : python -m etl.probe.p2b   → docs/sonde-p2b.md
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone

from etl.context import RAW_DIR, ROOT
from etl.indicators import eau as E
from etl.indicators import pluie as P

OUT = ROOT / "docs" / "sonde-p2b.md"


def main() -> int:
    raw = str(RAW_DIR)
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P2b — disponibilité des données (généré)", "",
          f"Généré par `python -m etl.probe.p2b` le {now}. Aucun indice calculé.", "",
          "## Pluie quotidienne et correction B′", "",
          "| Poste | Nom | Années ETCCDI | Années corrigeables | Première-dernière corrigeable | Dernière rupture (régime) | Complet 1961-2017 | Facteurs B′ (min / médiane / max) |",
          "|---|---|---|---|---|---|---|---|"]
    ok, excluded = P.eligible(raw)
    for poste in sorted(P._lsh(raw)):
        rd = P.rain_daily(poste, raw)
        hom = sorted(rd.hom())
        full = all(rd.status.get(y) == "homogenized" for y in range(1961, 2018))
        f = sorted(rd.factors.values())
        fs = f"{f[0]:.2f} / {f[len(f) // 2]:.2f} / {f[-1]:.2f}" if f else "—"
        md.append(f"| {poste} | {rd.station.name} | {len(rd.status)} | {len(hom)} | "
                  f"{(str(hom[0]) + '-' + str(hom[-1])) if hom else '—'} | {rd.last_break_regime or '—'} | "
                  f"{'oui' if full else 'non'} | {fs} |")
    md += ["", "Postes retenus (F1) : " + ", ".join(ok), "",
           "Exclus : " + ("; ".join(f"{k} ({v})" for k, v in excluded.items()) or "aucun"), "",
           "## ETP et SPEI : couverture homogénéisée", ""]
    for poste in E.POSTES:
        try:
            etp, eh, _p, d, dh, st = E.station_water(poste, raw)
            ye = sorted({y for (y, m), h in eh.items() if h})
            yd = sorted({y for (y, m), h in dh.items() if h})
            md.append(f"- {st.name} ({poste}) : ETP homogénéisée {ye[0]}-{ye[-1]} ({len(ye)} années touchées), "
                      f"P − ETP homogénéisé {yd[0]}-{yd[-1]} ({len(yd)} années touchées), latitude {st.latitude}")
        except Exception as exc:  # noqa: BLE001
            md.append(f"- {poste} : ÉCHEC {type(exc).__name__} {exc}")
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
