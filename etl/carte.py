"""Carte départementale des tendances de température 1959-2021 (P5 bis ; choix fixés le 30/10/2026 avant calcul,
docs/phases.md). Écrit data/processed/carte-departements.json.

Usage : python -m etl.carte
"""

from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from etl.context import PROCESSED_DIR, RAW_DIR, make_context
from etl.indicators import france as F
from etl.schema import DepartmentMap, DepartmentMapVariable, DepartmentShape, DepartmentValue, Indicator, Period, Provenance
from etl.sources import meteofrance_lsh as lsh
from etl.stats.trend import annual_trend

GEO_URL = "https://etalab-datasets.geo.data.gouv.fr/contours-administratifs/2025/geojson/departements-1000m.geojson"
GEO_SOURCE = ("Contours administratifs Etalab 2025 (dérivés d'Admin Express, IGN), généralisés à 1 000 m, "
              "Licence Ouverte 2.0")
OUT = PROCESSED_DIR / "carte-departements.json"
OUT_RR = PROCESSED_DIR / "carte-departements-pluie.json"
VARS = (("TN", "tn", "TN", "températures minimales"), ("TM", "tm", "TM", "température moyenne"),
        ("TX", "tx", "TX", "températures maximales"))


def fetch_geo(raw_dir: Path) -> dict:
    path = raw_dir / "geo" / "departements-1000m-2025.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(urllib.request.Request(GEO_URL, headers={"User-Agent": "projet-evolution-climat"}),
                                    timeout=120) as r:
            data = r.read()
        json.loads(data)
        path.write_bytes(data)
    except Exception as exc:  # noqa: BLE001
        if not path.exists():
            raise RuntimeError(f"contours des départements : téléchargement impossible et aucun cache : {exc}") from exc
    return json.loads(path.read_text(encoding="utf-8"))


def _round(coords, nd: int = 3):
    if isinstance(coords[0], (int, float)):
        return [round(coords[0], nd), round(coords[1], nd)]
    return [_round(c, nd) for c in coords]


def shapes(geo: dict) -> list[DepartmentShape]:
    out = []
    for f in geo["features"]:
        code = f["properties"]["code"]
        if len(code) != 2:                     # outre-mer (971…) : hors métropole
            continue
        g = f["geometry"]
        out.append(DepartmentShape(code=code, name=f["properties"]["nom"], value_code="20" if code in ("2A", "2B") else code,
                                   geometry={"type": g["type"], "coordinates": _round(g["coordinates"])}))
    return sorted(out, key=lambda s: s.code)


def department_values(var: str, raw_dir: Path) -> list[DepartmentValue]:
    per = F.station_anomalies(var, raw_dir)
    by_dep: dict[str, list[dict[int, float]]] = {}
    for p, (s, _h) in per.items():
        by_dep.setdefault(F.department(p), []).append(s)
    ys = list(range(F.T_SPAN[0], F.T_SPAN[1] + 1))
    out = []
    for dep, members in sorted(by_dep.items()):
        series = [sum(m[y] for m in members) / len(members) for y in ys]
        t = annual_trend(ys, series)
        out.append(DepartmentValue(code=dep, n_stations=len(members), slope_per_decade=round(t.slope_per_decade, 4),
                                   slope_ci_low=t.slope_ci_low, slope_ci_high=t.slope_ci_high,
                                   p_value=round(t.p_value, 6), significant=t.significant))
    return out


def build(out_dir: Path = PROCESSED_DIR, raw_dir: Path = RAW_DIR) -> DepartmentMap:
    ctx = make_context(raw_dir)
    variables = []
    for var, vid, code, label in VARS:
        nat = Indicator.model_validate_json((out_dir / "france" / f"{vid}-france.json").read_text(encoding="utf-8"))
        variables.append(DepartmentMapVariable(id=vid, code=code, label=label,
                                               national_slope_per_decade=nat.trend.slope_per_decade,
                                               departments=department_values(var, raw_dir)))
    n = len(F.t_network(str(raw_dir)))
    return DepartmentMap(
        generated_at=datetime.now(timezone.utc).replace(microsecond=0),
        title="Tendance des températures par département, 1959-2021",
        unit="°C", period=Period(start=F.T_SPAN[0], end=F.T_SPAN[1]),
        method_note=(f"Réseau constant de la P5 ({n} stations homogénéisées sur 1959-2021). Série d'un département : "
                     "moyenne des anomalies (écart à 1961-1990) de ses stations ; pente de Sen, test de Mann-Kendall "
                     "corrigé de l'autocorrélation (Hamed et Rao)."),
        limitations=[
            "Un département à une ou deux stations est représenté par elles seules : sa valeur est plus bruitée et "
            "peut refléter un site particulier (littoral, altitude, ville).",
            "Départements sans station au réseau : en gris, aucune valeur n'est interpolée.",
            "Aucune référence publiée par département : ces pentes ne portent pas de niveau de confiance « élevée ».",
            "La Corse est traitée comme un seul département (stations « 20 »), affiché sur 2A et 2B.",
        ],
        provenance=Provenance(source_name=lsh.SOURCE_NAME, source_url=lsh.DATASET_URL, license=lsh.LICENSE,
                              extracted_at=ctx.extracted_at, script="etl.carte", etl_version=ctx.etl_version,
                              homogenized=True),
        geometry_source=GEO_SOURCE, variables=variables, shapes=shapes(fetch_geo(raw_dir)),
    )


# ---------------------------------------------------------------- pluie (choix fixés le 30/10/2026 avant calcul)

SEASONS = (("annee", "Année", "cumul annuel", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)),
           ("hiver", "Hiver", "cumul de décembre à février", (12, 1, 2)),
           ("printemps", "Printemps", "cumul de mars à mai", (3, 4, 5)),
           ("ete", "Été", "cumul de juin à août", (6, 7, 8)),
           ("automne", "Automne", "cumul de septembre à novembre", (9, 10, 11)))


def season_total(values: dict, hom: dict, year: int, months: tuple[int, ...]) -> float | None:
    """Cumul de la saison ; décembre de l'hiver pris l'année précédente. Tous les mois présents et homogénéisés."""
    keys = [(year - 1, m) if (m == 12 and len(months) == 3) else (year, m) for m in months]
    if all(k in values and hom.get(k) for k in keys):
        return sum(values[k] for k in keys)
    return None


def rain_department_series(raw_dir: Path) -> dict[str, dict[str, dict[int, float]]]:
    """Saison → département → année → moyenne des cumuls des stations du réseau (années 1961-2014 complètes)."""
    rr = F._all("RR", str(raw_dir))
    network = F.rr_network(str(raw_dir))
    out: dict[str, dict[str, dict[int, float]]] = {}
    for sid, _label, _what, months in SEASONS:
        first = F.RR_SPAN[0] + (1 if sid == "hiver" else 0)
        years = range(first, F.RR_SPAN[1] + 1)
        by_dep: dict[str, list[dict[int, float]]] = {}
        for p in network:
            s = rr[p]
            tot = {y: season_total(s.values, s.homogenized, y, months) for y in years}
            if any(v is None for v in tot.values()):
                raise ValueError(f"pluie {p} {sid} : saison incomplète dans le réseau constant")
            by_dep.setdefault(F.department(p), []).append(tot)
        out[sid] = {d: {y: sum(m[y] for m in ms) / len(ms) for y in years} for d, ms in by_dep.items()}
    return out


def relative_trend(series: dict[int, float]) -> tuple[float, float | None, float | None, float, bool]:
    ys = sorted(series)
    t = annual_trend(ys, [series[y] for y in ys])
    base = [series[y] for y in ys if 1961 <= y <= 1990]
    m = sum(base) / len(base)
    rel = lambda x: None if x is None else round(100 * x / m, 3)  # noqa: E731
    return rel(t.slope_per_decade), rel(t.slope_ci_low), rel(t.slope_ci_high), t.p_value, t.significant


def build_rain(out_dir: Path = PROCESSED_DIR, raw_dir: Path = RAW_DIR) -> DepartmentMap:
    ctx = make_context(raw_dir)
    deps = rain_department_series(raw_dir)
    rr = F._all("RR", str(raw_dir))
    network = F.rr_network(str(raw_dir))
    n_by_dep: dict[str, int] = {}
    for p in network:
        n_by_dep[F.department(p)] = n_by_dep.get(F.department(p), 0) + 1
    variables = []
    for sid, label, what, _months in SEASONS:
        values = []
        for d, series in sorted(deps[sid].items()):
            slope, lo, hi, p_value, sig = relative_trend(series)
            values.append(DepartmentValue(code=d, n_stations=n_by_dep[d], slope_per_decade=slope, slope_ci_low=lo,
                                          slope_ci_high=hi, p_value=round(p_value, 6), significant=sig))
        years = sorted(next(iter(deps[sid].values())))
        france = {y: sum(s[y] for s in deps[sid].values()) / len(deps[sid]) for y in years}
        variables.append(DepartmentMapVariable(id=sid, code=label, label=what,
                                               national_slope_per_decade=relative_trend(france)[0],
                                               departments=values))
    del rr
    return DepartmentMap(
        generated_at=datetime.now(timezone.utc).replace(microsecond=0),
        title="Tendance de la pluie par département, 1961-2014",
        unit="%", period=Period(start=F.RR_SPAN[0], end=F.RR_SPAN[1]),
        method_note=(f"Réseau constant de la pluie de la P5 ({len(network)} stations homogénéisées sur 1961-2014). "
                     "Cumul saisonnier ou annuel de chaque station, moyenne par département ; pente de Sen rapportée à "
                     "la moyenne 1961-1990 du département (% par décennie) ; test de Mann-Kendall corrigé de "
                     "l'autocorrélation (Hamed et Rao). Hiver : décembre à février (1962-2014)."),
        limitations=[
            "La pluie n'est homogénéisée partout que jusqu'en 2014 : les dix dernières années manquent.",
            "La pluie varie beaucoup d'une année à l'autre : une pente non significative (teinte pâle) ne permet de "
            "conclure ni à une hausse ni à une baisse.",
            # Ajouté le 30/10/2026 après le premier calcul (mise en garde de lecture, sans effet sur les valeurs).
            "Tests multiples : au seuil de 5 %, environ 5 départements sur 95 sortent « significatifs » par le seul "
            "hasard, pour chaque carte. Quelques départements significatifs isolés ne prouvent pas une tendance.",
            "Un département à une ou deux stations est représenté par elles seules ; le relief rend la pluie très "
            "locale.",
            "Aucune référence publiée par département : ces pentes ne portent pas de niveau de confiance « élevée ».",
        ],
        provenance=Provenance(source_name=lsh.SOURCE_NAME, source_url=lsh.DATASET_URL, license=lsh.LICENSE,
                              extracted_at=ctx.extracted_at, script="etl.carte", etl_version=ctx.etl_version,
                              homogenized=True),
        geometry_source=GEO_SOURCE, variables=variables, shapes=shapes(fetch_geo(raw_dir)),
    )


def main() -> int:
    m = build()
    OUT.write_text(m.model_dump_json() + "\n", encoding="utf-8")
    covered = {d.code for d in m.variables[0].departments}
    print(f"→ {OUT.name} : {len(covered)} départements colorés sur {len({s.value_code for s in m.shapes})}, "
          f"{OUT.stat().st_size / 1e3:.0f} ko")
    r = build_rain()
    OUT_RR.write_text(r.model_dump_json() + "\n", encoding="utf-8")
    print(f"→ {OUT_RR.name} : {len(r.variables[0].departments)} départements colorés")
    return 0


if __name__ == "__main__":
    sys.exit(main())
