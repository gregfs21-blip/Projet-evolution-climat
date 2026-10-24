"""Couverture du projet : croise etl/config/couverture.yaml et le manifeste publié.

Le statut « publié » d'une case (paramètre × échelle) découle du manifeste : au moins un indicateur publié à cette
échelle porte l'une des variables listées. Il n'est jamais déclaré à la main ; une variable listée mais non
publiée laisse la case au statut déclaré (« prévu » le plus souvent).

Usage : appelé par etl.pipeline après le manifeste ; ou python -m etl.couverture
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from etl.context import PROCESSED_DIR, ROOT
from etl.schema import Coverage, CoverageCell, CoverageIndicator, CoverageParameter, Manifest

CONFIG = ROOT / "etl" / "config" / "couverture.yaml"


def build(manifest: Manifest, path: Path = CONFIG) -> Coverage:
    with path.open(encoding="utf-8") as f:
        params = yaml.safe_load(f)["parametres"]
    out = []
    for p in params:
        cells = []
        for scale, c in p["echelles"].items():
            vids = set(c.get("variables", []))
            inds = [CoverageIndicator(id=e.id, title=e.title, confidence=e.confidence) for e in manifest.indicators
                    if e.scale == scale and e.variable is not None and e.variable.id in vids]
            status = "publie" if inds else c.get("statut", "prevu")
            if status == "publie" and not inds:
                raise ValueError(f"{path.name} : « publie » ne se déclare pas ({p['id']}, {scale})")
            cells.append(CoverageCell(scale=scale, status=status, source=c.get("source"), note=c.get("note"), indicators=inds))
        out.append(CoverageParameter(id=p["id"], label=p["label"], cells=cells))
    return Coverage(generated_at=datetime.now(timezone.utc).replace(microsecond=0), parameters=out)


def write(manifest: Manifest, out_dir: Path = PROCESSED_DIR) -> Path:
    target = out_dir / "couverture.json"
    target.write_text(build(manifest).model_dump_json(indent=1) + "\n", encoding="utf-8")
    return target


def main() -> int:
    manifest = Manifest.model_validate_json((PROCESSED_DIR / "manifest.json").read_text(encoding="utf-8"))
    print(f"→ {write(manifest).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
