"""Vocabulaire des variables (etl/config/variables.yaml) : libellés et thèmes, définis une seule fois."""

from __future__ import annotations

from functools import lru_cache

import yaml

from etl.context import ROOT
from etl.schema import Place, Variable

PATH = ROOT / "etl" / "config" / "variables.yaml"


@lru_cache(maxsize=1)
def _load() -> dict:
    with PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    themes = data["themes"]
    for vid, v in data["variables"].items():
        extra = set(v) - {"code", "label", "theme", "order"}
        if extra:   # une virgule non protégée dans un libellé YAML en ligne le coupe en deux clés
            raise ValueError(f"{PATH.name} : clés inattendues {sorted(extra)} pour '{vid}' (libellé à mettre entre guillemets ?)")
        if v["theme"] not in themes:
            raise ValueError(f"{PATH.name} : thème inconnu '{v['theme']}' pour la variable '{vid}'")
    return data


def variable(vid: str) -> Variable:
    data = _load()
    if vid not in data["variables"]:
        raise KeyError(f"variable '{vid}' absente de {PATH.name}")
    v = data["variables"][vid]
    return Variable(id=vid, code=v["code"], label=v["label"], theme=v["theme"],
                    theme_label=data["themes"][v["theme"]], order=v["order"])


def station(slug: str, name: str) -> Place:
    return Place(id=slug, name=name, kind="station")


def composite(scale: str, name: str) -> Place:
    return Place(id=scale, name=name, kind="composite")
