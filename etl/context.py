"""Contexte d'exécution transmis à chaque constructeur d'indicateur."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from etl import __version__

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"


@dataclass(frozen=True)
class BuildContext:
    extracted_at: datetime
    etl_version: str
    raw_dir: Path


def etl_version() -> str:
    """Version du code + commit, pour tracer chaque fichier jusqu'au script exact."""
    sha = os.environ.get("GITHUB_SHA", "")[:7]
    return f"{__version__}+{sha}" if sha else f"{__version__}+local"


def make_context(raw_dir: Path = RAW_DIR) -> BuildContext:
    return BuildContext(
        extracted_at=datetime.now(timezone.utc).replace(microsecond=0),
        etl_version=etl_version(),
        raw_dir=raw_dir,
    )
