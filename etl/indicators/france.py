"""P5 — températures et pluie de la France métropolitaine (critères J1-J8 validés par Grég le 29/10/2026, avant calcul).

Séries mensuelles homogénéisées LSH de toute la métropole (`meteofrance_lsh.load_department(var, "")`).
- Températures : réseau constant des postes dont TN et TX sont homogénéisés sur les 12 mois de chaque année
  1959-2021 (D-N) ; anomalie annuelle de chaque station par rapport à 1961-1990 ; moyenne des stations de chaque
  département, puis moyenne des départements (D-O). TM = (TN + TX) / 2 au pas mensuel. Référence R10 sur TM.
- Pluie : réseau constant RR 1961-2014 (1961-2020 jusqu'au premier calcul), cumul annuel (mm), même pondération.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import serie as S
from etl.indicators import temperature as T
from etl.schema import Indicator, Provenance, Station
from etl.sources import meteofrance_lsh as lsh
from etl.stats.trend import annual_trend

T_SPAN = (1959, 2021)
RR_SPAN = (1961, 2014)   # 1961-2020 → 1961-2014 : décision de Grég du 29/10/2026 APRÈS calcul (31 départements seulement)
BASE = (1961, 1990)
PLAUSIBLE_TM = (-10.0, 20.0)
PLAUSIBLE_RR = (100.0, 5000.0)   # [300 ; 3000] → [100 ; 5000] : décisions de Grég du 29/10/2026 APRÈS le premier calcul
                                 # (252 mm en 1967 à 13001009, Provence ; 3 273 mm en 1996 à 48036001, Cévennes)
R10 = {
    "kind": "slope", "period": [1959, 2021], "range": [0.2, 0.4], "unit": "°C/déc.", "fixed_on": "2026-10-29",
    "statement": ("France métropolitaine, séries homogénéisées : environ + 0,3 °C par décennie sur 1959-2021, entre "
                  "+ 0,2 et + 0,4 selon les séries (fourchette publiée)"),
    "source": "ONERC / Météo-France, indicateur « température de l'air en France métropolitaine »",
    "url": "https://www.ecologie.gouv.fr/impacts-du-changement-climatique-atmosphere-temperatures-et-precipitations",
}


def department(poste: str) -> str:
    return poste.zfill(8)[:2]


@lru_cache(maxsize=4)
def _all(var: str, raw_dir: str) -> dict[str, lsh.LshSeries]:
    return {s.station.id: s for s in lsh.load_department(var, "", Path(raw_dir), download=not T._offline())}


def annual(values: dict, hom: dict) -> tuple[dict[int, float], set[int]]:
    """Année → (moyenne ou somme selon l'appelant) : ici la liste des 12 valeurs ; années de 12 mois seulement."""
    out, h = {}, set()
    for y in sorted({y for y, _ in values}):
        ks = [(y, m) for m in range(1, 13)]
        if all(k in values for k in ks):
            out[y] = [values[k] for k in ks]
            if all(hom.get(k) for k in ks):
                h.add(y)
    return out, h


def station_annual(var: str, s_tn: lsh.LshSeries | None, s_tx: lsh.LshSeries | None, s_rr: lsh.LshSeries | None = None):
    if var == "RR":
        months, hom = annual(s_rr.values, s_rr.homogenized)
        return {y: round(sum(v), 1) for y, v in months.items()}, hom
    if var == "TM":
        keys = s_tn.values.keys() & s_tx.values.keys()
        vals = {k: (s_tn.values[k] + s_tx.values[k]) / 2 for k in keys}
        hom = {k: s_tn.homogenized[k] and s_tx.homogenized[k] for k in keys}
    else:
        s = s_tn if var == "TN" else s_tx
        vals, hom = s.values, s.homogenized
    months, h = annual(vals, hom)
    return {y: sum(v) / 12 for y, v in months.items()}, h


@lru_cache(maxsize=2)
def t_network(raw_dir: str) -> tuple[str, ...]:
    tn, tx = _all("TN", raw_dir), _all("TX", raw_dir)
    out = []
    for p in sorted(tn.keys() & tx.keys()):
        _, h_tn = station_annual("TN", tn[p], tx[p])
        _, h_tx = station_annual("TX", tn[p], tx[p])
        if all(y in h_tn and y in h_tx for y in range(T_SPAN[0], T_SPAN[1] + 1)):
            out.append(p)
    return tuple(out)


@lru_cache(maxsize=2)
def rr_network(raw_dir: str) -> tuple[str, ...]:
    rr = _all("RR", raw_dir)
    out = []
    for p, s in sorted(rr.items()):
        _, h = station_annual("RR", None, None, s)
        if all(y in h for y in range(RR_SPAN[0], RR_SPAN[1] + 1)):
            out.append(p)
    return tuple(out)


def station_anomalies(var: str, raw_dir: Path) -> dict[str, tuple[dict[int, float], set[int]]]:
    """Poste → (anomalie annuelle par rapport à 1961-1990, années homogénéisées), réseau des températures."""
    tn, tx = _all("TN", str(raw_dir)), _all("TX", str(raw_dir))
    out = {}
    for p in t_network(str(raw_dir)):
        series, hom = station_annual(var, tn[p], tx[p])
        if var == "TM":
            bad = {y: v for y, v in series.items() if not PLAUSIBLE_TM[0] <= v <= PLAUSIBLE_TM[1]}
            if bad:
                raise ValueError(f"TM {p} : moyennes annuelles hors {PLAUSIBLE_TM} (J7) : {list(bad.items())[:3]}")
        base = [series[y] for y in range(BASE[0], BASE[1] + 1)]
        m = sum(base) / len(base)
        out[p] = ({y: v - m for y, v in series.items()}, hom)
    return out


def composite(per_station: dict[str, tuple[dict[int, float], set[int]]], weighted: bool = True
              ) -> tuple[dict[int, float], set[int]]:
    """Années où toutes les stations ont une valeur ; homogénéisées si toutes le sont."""
    years = sorted(set.intersection(*(set(s) for s, _ in per_station.values())))
    out, hom = {}, set()
    for y in years:
        if weighted:
            by_dep: dict[str, list[float]] = {}
            for p, (s, _h) in per_station.items():
                by_dep.setdefault(department(p), []).append(s[y])
            out[y] = round(sum(sum(v) / len(v) for v in by_dep.values()) / len(by_dep), 4)
        else:
            out[y] = round(sum(s[y] for s, _ in per_station.values()) / len(per_station), 4)
        if all(y in h for _s, h in per_station.values()):
            hom.add(y)
    return out, hom


def station_slopes(raw_dir: Path) -> dict[str, float]:
    """J5 : pente de Sen (°C/déc.) de l'anomalie TM de chaque station du réseau sur 1959-2021."""
    ys = list(range(T_SPAN[0], T_SPAN[1] + 1))
    return {p: annual_trend(ys, [s[y] for y in ys]).slope_per_decade for p, (s, _h) in station_anomalies("TM", raw_dir).items()}


def _prov(ctx: BuildContext) -> Provenance:
    return Provenance(source_name=lsh.SOURCE_NAME, source_url=lsh.DATASET_URL, license=lsh.LICENSE,
                      extracted_at=ctx.extracted_at, script="etl.indicators.france", etl_version=ctx.etl_version,
                      homogenized=True)


LIMITS = [
    "Séries homogénéisées par Météo-France (LSH), qui ne commencent pour la plupart qu'en 1953-1959 : l'évolution "
    "depuis 1900 publiée par Météo-France (indicateur thermique national, séries anciennes) n'est pas reproduite ici.",
    "Réseau constant : seules les stations complètes et homogénéisées sur toute la période entrent dans la moyenne ; "
    "les années hors de cette période ne sont affichées que si toutes les stations ont une valeur.",
    "Moyenne des départements, chacun pesant autant (proche d'une moyenne par surface) ; les départements sans "
    "station au réseau n'y figurent pas.",
]
NAMES = {"TN": ("tn", "températures minimales", "Température minimale annuelle de la France"),
         "TM": ("tm", "température moyenne", "Température moyenne annuelle de la France"),
         "TX": ("tx", "températures maximales", "Température maximale annuelle de la France")}


def _stations(ids: tuple[str, ...], var: str, raw_dir: str) -> list[Station]:
    src = _all(var, raw_dir)
    return [src[p].station for p in ids]


def build_temperature(ctx: BuildContext, var: str) -> Indicator:
    per = station_anomalies(var, ctx.raw_dir)
    if len(per) < 100:
        raise ValueError(f"réseau des températures : seulement {len(per)} stations")
    series, hom = composite(per)
    deps = {department(p) for p in per}
    vid, label, title = NAMES[var]
    note = (f"Réseau constant de {len(per)} stations dans {len(deps)} départements (TN et TX homogénéisés chaque année "
            f"{T_SPAN[0]}-{T_SPAN[1]}). Anomalie annuelle de chaque station par rapport à 1961-1990, moyenne par "
            "département, puis moyenne des départements.")
    return S.assemble(ctx, ind_id=f"{vid}-france", scale="france", variable=vid,
                      place=vocab.composite("france", "France"), title=title + " (écart à 1961-1990)",
                      description=f"Écart annuel de la {label} de la France métropolitaine à sa moyenne 1961-1990, "
                                  f"d'après {len(per)} séries homogénéisées de Météo-France.",
                      unit="°C", series=series, hom=hom, provenance=_prov(ctx), limitations=LIMITS,
                      stations=_stations(tuple(per), "TN", str(ctx.raw_dir)), method_note=note,
                      reference=R10 if var == "TM" else None, baseline=list(BASE),
                      group="Synthèse France — températures", where="En France métropolitaine",
                      label=f"l'écart de {label}")


def build_rain(ctx: BuildContext) -> Indicator:
    rr = _all("RR", str(ctx.raw_dir))
    per = {}
    for p in rr_network(str(ctx.raw_dir)):
        s, h = station_annual("RR", None, None, rr[p])
        bad = {y: v for y, v in s.items() if y in h and not PLAUSIBLE_RR[0] <= v <= PLAUSIBLE_RR[1]}
        if bad:
            raise ValueError(f"RR {p} : cumuls hors {PLAUSIBLE_RR} (J7) : {list(bad.items())[:3]}")
        per[p] = (s, h)
    if len(per) < 100:
        raise ValueError(f"réseau de la pluie : seulement {len(per)} stations")
    series, hom = composite(per)
    deps = {department(p) for p in per}
    note = (f"Réseau constant de {len(per)} stations dans {len(deps)} départements (pluie homogénéisée chaque année "
            f"{RR_SPAN[0]}-{RR_SPAN[1]}). Cumul annuel, moyenne par département, puis moyenne des départements.")
    return S.assemble(ctx, ind_id="rr-cumul-france", scale="france", variable="rr-cumul",
                      place=vocab.composite("france", "France"), title="Cumul annuel de pluie en France",
                      description=f"Cumul annuel moyen des précipitations de la France métropolitaine, d'après {len(per)} "
                                  "séries homogénéisées de Météo-France.",
                      unit="mm", series=series, hom=hom, provenance=_prov(ctx),
                      limitations=LIMITS[1:] + ["Pluie homogénéisée jusqu'en 2014-2021 selon les régions : le réseau "
                                                "constant s'arrête en 2014 pour couvrir tout le territoire (sur "
                                                "1961-2020, il ne comptait que 31 départements, surtout au sud).",
                                                "Aucune référence publiée n'a été fixée : confiance au plus « moyenne »."],
                      stations=[rr[p].station for p in per], method_note=note, reference=None, baseline=None,
                      group="Synthèse France — précipitations", where="En France métropolitaine",
                      label="le cumul annuel de pluie")
