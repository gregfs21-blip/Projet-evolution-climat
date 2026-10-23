"""Contrôle des données publiées, lancé par la CI à chaque push.

Vérifie que chaque JSON de data/processed respecte le schéma, et que le
manifeste correspond exactement aux fichiers présents.

Usage : python -m etl.validate [dossier]
"""

from __future__ import annotations

import sys
from pathlib import Path

from etl.context import PROCESSED_DIR
from etl.schema import Indicator, Manifest, ValidationReport


def validate(out_dir: Path = PROCESSED_DIR) -> list[str]:
    errors: list[str] = []
    manifest_path = out_dir / "manifest.json"
    if not manifest_path.exists():
        return [f"{manifest_path} absent"]

    try:
        manifest = Manifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"manifest.json invalide : {exc}"]

    files = {p.relative_to(out_dir).as_posix() for p in out_dir.glob("*/*.json")}
    listed = {e.path for e in manifest.indicators}
    errors += [f"fichier absent du manifeste : {p}" for p in sorted(files - listed)]
    errors += [f"fichier du manifeste introuvable : {p}" for p in sorted(listed - files)]

    for entry in manifest.indicators:
        path = out_dir / entry.path
        if not path.exists():
            continue
        try:
            ind = Indicator.model_validate_json(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{entry.path} invalide : {exc}")
            continue
        if (ind.scale, ind.id, ind.title, ind.is_demo, ind.variable, ind.place) != (
            entry.scale, entry.id, entry.title, entry.is_demo, entry.variable, entry.place
        ):
            errors.append(f"{entry.path} : contenu incohérent avec le manifeste")
        if entry.path != f"{ind.scale}/{ind.id}.json":
            errors.append(f"{entry.path} : chemin incohérent avec scale/id")

    # Rapports de validation de phase (validation-p1.json…) : hors manifeste, mais contrôlés aussi.
    for path in sorted(out_dir.glob("validation-*.json")):
        try:
            ValidationReport.model_validate_json(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.name} invalide : {exc}")
    return errors


def main() -> int:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else PROCESSED_DIR
    errors = validate(out_dir)
    for e in errors:
        print(f"ERREUR  {e}")
    print("Données valides." if not errors else f"{len(errors)} erreur(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
