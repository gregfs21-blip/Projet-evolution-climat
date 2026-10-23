"""Orchestrateur de l'ETL.

Usage :
    python -m etl.pipeline                 # tous les indicateurs actifs
    python -m etl.pipeline --only demo-temperature-annuelle

Pour chaque indicateur déclaré dans etl/config/indicators.yaml :
appel du constructeur → validation pydantic → écriture du JSON.
Puis reconstruction du manifeste à partir de tous les JSON publiés.
Un indicateur en échec fait échouer l'exécution entière (code de sortie 1) :
on ne publie jamais un jeu de résultats partiellement faux sans le savoir.
"""

from __future__ import annotations

import argparse
import importlib
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

from etl.context import PROCESSED_DIR, ROOT, BuildContext, etl_version, make_context
from etl.schema import Indicator, Manifest, ManifestEntry

CONFIG = ROOT / "etl" / "config" / "indicators.yaml"
log = logging.getLogger("etl")


def load_registry(path: Path = CONFIG) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        entries = yaml.safe_load(f)["indicators"]
    keys = [(e["scale"], e["id"]) for e in entries]
    if len(set(keys)) != len(keys):
        raise ValueError(f"{path} : couple (scale, id) dupliqué")
    return entries


def resolve(builder: str) -> Callable[..., Indicator]:
    module_name, func_name = builder.split(":")
    return getattr(importlib.import_module(module_name), func_name)


def indicator_path(out_dir: Path, scale: str, ind_id: str) -> Path:
    return out_dir / scale / f"{ind_id}.json"


def write_indicator(ind: Indicator, out_dir: Path) -> Path:
    path = indicator_path(out_dir, ind.scale, ind.id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ind.model_dump_json(indent=1) + "\n", encoding="utf-8")
    return path


def prune(out_dir: Path, registry: list[dict]) -> list[Path]:
    """Supprime les JSON d'indicateurs retirés du registre."""
    keep = {indicator_path(out_dir, e["scale"], e["id"]) for e in registry if e.get("enabled", True)}
    removed = []
    for path in out_dir.glob("*/*.json"):
        if path not in keep:
            path.unlink()
            removed.append(path)
    return removed


def build_manifest(out_dir: Path, registry: list[dict] | None = None) -> Manifest:
    """Manifeste de tous les JSON publiés, dans l'ordre du registre (ordre d'affichage du site), puis alphabétique."""
    rank = {(e["scale"], e["id"]): i for i, e in enumerate(registry or [])}
    paths = sorted(out_dir.glob("*/*.json"), key=lambda p: (rank.get((p.parent.name, p.stem), len(rank)), p.as_posix()))
    entries = []
    for path in paths:
        ind = Indicator.model_validate_json(path.read_text(encoding="utf-8"))
        entries.append(
            ManifestEntry(
                id=ind.id,
                scale=ind.scale,
                title=ind.title,
                unit=ind.unit,
                path=path.relative_to(out_dir).as_posix(),
                confidence=ind.confidence,
                is_demo=ind.is_demo,
                group=ind.group,
                variable=ind.variable,
                place=ind.place,
            )
        )
    return Manifest(
        generated_at=datetime.now(timezone.utc).replace(microsecond=0),
        etl_version=etl_version(),
        indicators=entries,
    )


def run(only: set[str] | None = None, out_dir: Path = PROCESSED_DIR, registry_path: Path = CONFIG,
        raw_dir: Path | None = None) -> int:
    registry = load_registry(registry_path)
    ctx = make_context(raw_dir) if raw_dir else make_context()
    failures: list[str] = []

    for entry in registry:
        if not entry.get("enabled", True) or (only and entry["id"] not in only):
            continue
        try:
            ind = resolve(entry["builder"])(ctx, **entry.get("params", {}))
            if (ind.scale, ind.id) != (entry["scale"], entry["id"]):
                raise ValueError(
                    f"le constructeur a produit {ind.scale}/{ind.id}, "
                    f"le registre attend {entry['scale']}/{entry['id']}"
                )
            path = write_indicator(ind, out_dir)
            log.info("OK   %s → %s", entry["id"], path.relative_to(out_dir))
        except Exception as exc:  # noqa: BLE001 — on veut le rapport complet
            log.error("ÉCHEC %s : %s", entry["id"], exc)
            failures.append(entry["id"])

    for path in prune(out_dir, registry):
        log.info("RETIRÉ %s", path.relative_to(out_dir))

    manifest = build_manifest(out_dir, registry)
    (out_dir / "manifest.json").write_text(manifest.model_dump_json(indent=1) + "\n", encoding="utf-8")
    log.info("Manifeste : %d indicateur(s)", len(manifest.indicators))
    from etl import couverture  # import local : la couverture dépend du manifeste, pas l'inverse

    couverture.write(manifest, out_dir)

    if failures:
        log.error("%d indicateur(s) en échec : %s", len(failures), ", ".join(failures))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--only", nargs="*", help="identifiants à recalculer")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    return run(set(args.only) if args.only else None)


if __name__ == "__main__":
    sys.exit(main())
