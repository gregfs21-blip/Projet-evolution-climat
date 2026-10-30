"""Sonde P5 bis : contours des départements pour la carte départementale. Aucun indicateur calculé.

Candidats : contours administratifs Etalab (dérivés d'Admin Express, IGN), généralisés à 1 000 m, plusieurs millésimes.
Usage : python -m etl.probe.p5b   → docs/sonde-p5b.md
"""

from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-p5b.md"
BASE = "https://etalab-datasets.geo.data.gouv.fr/contours-administratifs/{y}/geojson/departements-{r}.geojson"


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P5 bis — contours des départements (généré)", "", f"Généré le {now}.", ""]
    for y in (2025, 2024, 2023):
        for r in ("1000m", "100m"):
            url = BASE.format(y=y, r=r)
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "projet-evolution-climat"}),
                                            timeout=120) as resp:
                    data = resp.read()
                j = json.loads(data)
                feats = j.get("features", [])
                props = feats[0]["properties"] if feats else {}
                codes = sorted(f["properties"].get("code", "?") for f in feats)
                npts = sum(len(str(f["geometry"]["coordinates"])) for f in feats)
                md.append(f"- `{url}` → 200, {len(data) / 1e6:.2f} Mo, {len(feats)} entités, propriétés {sorted(props)}, "
                          f"exemple {props}, codes {codes[:3]}…{codes[-3:]}, taille des coordonnées {npts / 1e6:.2f} M caractères")
            except Exception as exc:  # noqa: BLE001
                md.append(f"- `{url}` → {type(exc).__name__} {str(exc)[:150]}")
            OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
