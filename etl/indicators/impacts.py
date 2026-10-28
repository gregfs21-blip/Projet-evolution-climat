"""P4 — impacts en Gironde : viticulture et canicule (critères I1-I9 validés par Grég le 28/10/2026, avant calcul).

Toutes les grandeurs de station partent du quotidien Météo-France corrigé mois par mois par les séries homogénéisées
LSH (méthode de la P2a, `etl.indicators.extremes.station_daily`). Une année n'entre dans une tendance que si TN et TX
y sont tous deux corrigés sur les 12 mois (I2, I3) ; aucune valeur n'est complétée.

- Indice de Huglin (Huglin, 1978) : somme, du 1er avril au 30 septembre, de max(0, ((TM − 10) + (TX − 10)) / 2),
  TM = (TN + TX) / 2, multipliée par K = 1,04 (latitudes 44°1'-46°0', toutes les stations de Gironde). Référence R9.
- Fraîcheur des nuits (Tonietto et Carbonneau, 2004) : TN moyen de septembre, série LSH mensuelle.
- Gelées tardives : jours TN ≤ 0 °C du 1er avril au 15 mai.
- Canicule : jours appartenant à au moins une fenêtre de 3 jours consécutifs où la moyenne des TN atteint 21 °C ET
  celle des TX 35 °C (seuils préfectoraux de la Gironde, station de Mérignac).
- Dates de vendanges de Bordeaux (Daux et al., 2012), produit publié ; contrôle I5 contre le Huglin composite.

Règle de confiance (fixée avec les critères, avant calcul) : Huglin, règle des séries simples avec R9 ; indicateurs
sans référence, au plus « moyenne » ; comptages rares (médiane 1961-1990 < 5 jours), règle E9 ; vendanges : I5 non
satisfait → « non établi ».
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import extremes as X
from etl.indicators import serie as S
from etl.indicators import temperature as T
from etl.schema import Indicator, Provenance, Series, Station
from etl.sources import globaux as G
from etl.sources import meteofrance_lsh as lsh
from etl.sources import meteofrance_quot as quot
from etl.stats.trend import annual_trend

K_HUGLIN = 1.04
SEASON = ((4, 1), (9, 30))
LATE_FROST = ((4, 1), (5, 15))
CANICULE = {"poste": "33281001", "tn": 21.0, "tx": 35.0, "days": 3}
I5_MAX_R = -0.6
I5_MIN_YEARS = 30
COMPOSITE_SPAN = X.COMPOSITE_SPAN

R9 = {
    "kind": "difference", "base": [1980, 1999], "period": [2000, 2019], "range": [102.0, 152.0], "unit": "°C·j",
    "fixed_on": "2026-10-28",
    "statement": ("Bordelais : indice de Huglin + 127 °C·j entre 1980-1999 et 2000-2019 (SAFRAN, points de grille du "
                  "vignoble), fourchette ± 20 % fixée par Grég faute d'incertitude publiée"),
    "source": "N. Ollat et al., « La diversité des vignobles français face au changement climatique », Climatologie 18, 2021",
    "url": "https://doi.org/10.1051/climat/202118003",
}

PLAUSIBLE = {"huglin": (1200.0, 2800.0), "fraicheur-nuits": (5.0, 20.0), "gelees-tardives": (0.0, 45.0),
             "canicule": (0.0, 60.0), "vendanges": (-30.0, 60.0)}


# ---------------------------------------------------------------- calculs (purs, testés)


def in_window(day: str, window: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    m, d = int(day[5:7]), int(day[8:10])
    return window[0] <= (m, d) <= window[1]


def huglin_year(tn: dict[str, float], tx: dict[str, float], year: int) -> float:
    """Somme du 1er avril au 30 septembre sur les jours où TN et TX existent (aucun jour complété)."""
    total = 0.0
    for m in range(4, 10):
        for d in X.days_of(year, m):
            if d in tn and d in tx:
                tm = (tn[d] + tx[d]) / 2
                total += max(0.0, ((tm - 10) + (tx[d] - 10)) / 2)
    return round(total * K_HUGLIN, 1)


def late_frost_days(tn: dict[str, float], year: int) -> int:
    return sum(1 for m in (4, 5) for d in X.days_of(year, m) if in_window(d, LATE_FROST) and d in tn and tn[d] <= 0.0)


def canicule_days(tn: dict[str, float], tx: dict[str, float], year: int, tn_min: float = CANICULE["tn"],
                  tx_min: float = CANICULE["tx"], n: int = CANICULE["days"]) -> int:
    """Jours de l'année couverts par au moins une fenêtre de n jours consécutifs (tous présents) dont la moyenne des TN
    et celle des TX atteignent les seuils. Les fenêtres sont prises de mai à septembre ; un jour manquant les rompt."""
    days = [d for m in range(5, 10) for d in X.days_of(year, m)]
    hit: set[str] = set()
    for i in range(len(days) - n + 1):
        w = days[i:i + n]
        if all(d in tn and d in tx for d in w):
            if sum(tn[d] for d in w) / n >= tn_min and sum(tx[d] for d in w) / n >= tx_min:
                hit.update(w)
    return len(hit)


def correlation(a: dict[int, float], b: dict[int, float]) -> tuple[float | None, list[int]]:
    ys = sorted(set(a) & set(b))
    if len(ys) < 3:
        return None, ys
    return float(np.corrcoef([a[y] for y in ys], [b[y] for y in ys])[0, 1]), ys


# ---------------------------------------------------------------- données


@lru_cache(maxsize=16)
def pair(poste: str, raw_dir: str) -> tuple[X.StationDaily, X.StationDaily, Station]:
    tn = X.station_daily("TN", poste, Path(raw_dir))
    tx = X.station_daily("TX", poste, Path(raw_dir))
    cfg = T.station_config()[poste]
    return tn, tx, tn.station.model_copy(update={"name": cfg["name"]})


def _years(tn: X.StationDaily, tx: X.StationDaily) -> tuple[list[int], set[int]]:
    """Années complètes (ETCCDI) pour TN et TX ; homogénéisées si les deux le sont sur les 12 mois."""
    years = sorted(set(tn.year_status) & set(tx.year_status))
    hom = {y for y in years if tn.year_status[y] == "homogenized" and tx.year_status[y] == "homogenized"}
    return years, hom


def _values(sd: X.StationDaily, year: int, hom: set[int]) -> dict[str, float]:
    return sd.corrected if year in hom else sd.raw


def station_series(index: str, poste: str, raw_dir: Path) -> tuple[dict[int, float], set[int], Station]:
    if index == "gelees-tardives":            # TN seul : aussi pour les postes sans série TX (Lacanau, Sauternes)
        tn = X.station_daily("TN", poste, Path(raw_dir))
        hom = {y for y, s in tn.year_status.items() if s == "homogenized"}
        st = tn.station.model_copy(update={"name": T.station_config()[poste]["name"]})
        return ({y: float(late_frost_days(_values(tn, y, hom), y)) for y in sorted(tn.year_status)}, hom, st)
    tn, tx, st = pair(poste, str(raw_dir))
    years, hom = _years(tn, tx)
    out = {}
    for y in years:
        n, x = _values(tn, y, hom), _values(tx, y, hom)
        if index == "huglin":
            out[y] = huglin_year(n, x, y)
        elif index == "canicule":
            out[y] = float(canicule_days(n, x, y))
        else:
            raise KeyError(index)
    return out, hom, st


def huglin_stations(raw_dir: Path) -> list[str]:
    return sorted(set(T.stations_with("TN", raw_dir)) & set(T.stations_with("TX", raw_dir)))


def huglin_composite(raw_dir: Path) -> tuple[dict[int, float], set[int], list[Station], list[str]]:
    """Réseau constant (comme la P2a) : stations dont TN et TX sont corrigés sur toute la période 1961-2022."""
    members, excluded = [], []
    for p in huglin_stations(raw_dir):
        s, hom, st = station_series("huglin", p, raw_dir)
        ok = all(y in hom for y in range(COMPOSITE_SPAN.start, COMPOSITE_SPAN.end + 1))
        (members if ok else excluded).append((s, hom, st) if ok else st.name)
    if len(members) < 3:
        raise ValueError(f"Huglin composite : seulement {len(members)} station(s) à réseau constant")
    years = sorted(set.intersection(*(set(m[0]) for m in members)))
    series = {y: round(sum(m[0][y] for m in members) / len(members), 1) for y in years}
    hom = {y for y in years if all(y in m[1] for m in members)}
    return series, hom, [m[2] for m in members], excluded


# ---------------------------------------------------------------- provenance, limites


def _prov(ctx: BuildContext) -> Provenance:
    return Provenance(source_name=f"{quot.SOURCE_NAME}, corrigées par les {lsh.SOURCE_NAME.split('— ')[-1]}",
                      source_url=quot.DATASET_URL, license=quot.LICENSE, extracted_at=ctx.extracted_at,
                      script="etl.indicators.impacts", etl_version=ctx.etl_version, homogenized=True)


DAILY_LIMITS = [
    "Valeurs quotidiennes non homogénéisées, corrigées mois par mois par l'écart entre la série homogénéisée LSH et la "
    "moyenne mensuelle brute (méthode de la P2a) : la moyenne de chaque mois est rétablie, pas la forme de la "
    "distribution. Les seuils (10 °C, 0 °C, 21 et 35 °C) peuvent garder un biais résiduel.",
    "Une année n'est calculée que si TN et TX sont complets (au plus 3 jours absents par mois) ; elle n'entre dans les "
    "tendances que si les 12 mois des deux séries sont corrigés (2023 et après : affichées pour information).",
]
HUGLIN_LIMITS = [
    "Indice calculé à la station, pas sur le vignoble : la référence R9 porte sur les points de grille SAFRAN des "
    "parcelles de vigne du Bordelais, plus continentales que Cap-Ferret ou Cazaux.",
]


def _check(variable: str, series: dict[int, float], where: str) -> None:
    lo, hi = PLAUSIBLE[variable]
    bad = {y: v for y, v in series.items() if not lo <= v <= hi}
    if bad:
        raise ValueError(f"{variable} {where} : valeurs hors de [{lo} ; {hi}] (I7) : {list(bad.items())[:3]}")


# ---------------------------------------------------------------- Huglin, fraîcheur des nuits


HUGLIN_NOTE = ("Indice de Huglin : somme du 1er avril au 30 septembre de max(0 ; ((TM − 10) + (TX − 10)) / 2), "
               "multipliée par K = 1,04 (latitude), sur les valeurs quotidiennes corrigées.")


def build_huglin(ctx: BuildContext, station: str | None = None) -> Indicator:
    if station is None:
        series, hom, members, excluded = huglin_composite(ctx.raw_dir)
        _check("huglin", {y: series[y] for y in hom}, "Gironde")
        names = ", ".join(s.name for s in members)
        note = (f"Moyenne des indices de {len(members)} stations ({names}), réseau constant {COMPOSITE_SPAN.start}-"
                f"{COMPOSITE_SPAN.end}" + (f" ; exclues : {', '.join(excluded)}" if excluded else "") + ". " + HUGLIN_NOTE)
        return S.assemble(ctx, ind_id="huglin-gironde", scale="gironde", variable="huglin",
                          place=vocab.composite("gironde", "Gironde"), title="Indice de Huglin en Gironde",
                          description="Somme des températures utiles à la vigne d'avril à septembre (indice héliothermique "
                                      "de Huglin), moyenne de stations longues de Gironde. Repères : 1 800-2 100 « tempéré "
                                      "chaud », 2 100-2 400 « chaud ».",
                          unit="°C·j", series=series, hom=hom, provenance=_prov(ctx),
                          limitations=DAILY_LIMITS + HUGLIN_LIMITS, stations=members, method_note=note, reference=R9,
                          baseline=None, group="Synthèse Gironde — viticulture", where="En Gironde",
                          label="l'indice de Huglin")
    cfg = next(c for c in T.station_config().values() if c["slug"] == station)
    if cfg["id"] not in huglin_stations(ctx.raw_dir):
        raise ValueError(f"{cfg['name']} : pas de séries LSH TN et TX (exclusion I1)")
    series, hom, st = station_series("huglin", cfg["id"], ctx.raw_dir)
    _check("huglin", {y: series[y] for y in hom}, cfg["name"])
    return S.assemble(ctx, ind_id=f"huglin-{station}", scale="gironde", variable="huglin",
                      place=vocab.station(station, cfg["name"]), title=f"Indice de Huglin à {cfg['name']}",
                      description=f"Somme des températures utiles à la vigne d'avril à septembre (indice héliothermique de "
                                  f"Huglin) à {cfg['name']}. {cfg['note']}",
                      unit="°C·j", series=series, hom=hom, provenance=_prov(ctx),
                      limitations=DAILY_LIMITS + HUGLIN_LIMITS + [f"Particularité du site : {cfg['note']}"], stations=[st],
                      method_note=HUGLIN_NOTE, reference=R9, baseline=None, group="Stations — viticulture",
                      where=f"À {cfg['name']}", label="l'indice de Huglin")


def build_fraicheur(ctx: BuildContext, station: str) -> Indicator:
    cfg = next(c for c in T.station_config().values() if c["slug"] == station)
    s = next((x for x in lsh.load_department("TN", "33", ctx.raw_dir, download=not T._offline())
              if x.station.id == cfg["id"]), None)
    if s is None:
        raise ValueError(f"{cfg['name']} : pas de série LSH TN")
    series = {y: v for (y, m), v in s.values.items() if m == 9}
    hom = {y for (y, m), h in s.homogenized.items() if m == 9 and h}
    _check("fraicheur-nuits", series, cfg["name"])
    st = s.station.model_copy(update={"name": cfg["name"]})
    prov = Provenance(source_name=lsh.SOURCE_NAME, source_url=lsh.DATASET_URL, license=lsh.LICENSE,
                      extracted_at=ctx.extracted_at, script="etl.indicators.impacts", etl_version=ctx.etl_version,
                      homogenized=True)
    return S.assemble(ctx, ind_id=f"fraicheur-nuits-{station}", scale="gironde", variable="fraicheur-nuits",
                      place=vocab.station(station, cfg["name"]), title=f"Fraîcheur des nuits de septembre à {cfg['name']}",
                      description=f"Température minimale moyenne de septembre (indice de fraîcheur des nuits de Tonietto "
                                  f"et Carbonneau), le mois de la maturation : des nuits fraîches préservent arômes et "
                                  f"couleur. {cfg['note']}",
                      unit="°C", series=series, hom=hom, provenance=prov,
                      limitations=S.LSH_LIMITS[:1] + [f"Particularité du site : {cfg['note']}"], stations=[st],
                      method_note="TN mensuel de septembre de la série homogénéisée LSH.", reference=None, baseline=None,
                      group="Stations — viticulture", where=f"À {cfg['name']}",
                      label="la température minimale moyenne de septembre")


# ---------------------------------------------------------------- comptages (gelées tardives, canicule)


COUNTS = {
    "gelees-tardives": ("Gelées tardives", "jours de gelée tardive (TN ≤ 0 °C du 1er avril au 15 mai)",
                        "Nombre de jours de gelée (TN ≤ 0 °C) entre le 1er avril et le 15 mai, quand le débourrement de "
                        "la vigne la rend vulnérable.", "Stations — viticulture"),
    "canicule": ("Jours de canicule", "jours de canicule (seuils de la Gironde : 21 °C la nuit, 35 °C le jour, sur 3 jours)",
                 "Nombre de jours appartenant à un épisode où, sur 3 jours consécutifs, la moyenne des minimales atteint "
                 "21 °C et celle des maximales 35 °C : les seuils de la vigilance canicule en Gironde.",
                 "Stations — santé"),
}


def _count_confidence(main, rare: bool, comp) -> str:
    if rare:
        return "moyenne" if comp is not None and comp.significant else "non_etabli"
    if main is None:
        return "non_etabli"
    if main.significant:
        return "moyenne"                 # aucune référence publiée (I4)
    if main.p_value_classical is not None and main.p_value_classical < main.alpha:
        return "faible"
    return "non_etabli"


def build_count(ctx: BuildContext, index: str, station: str) -> Indicator:
    cfg = next(c for c in T.station_config().values() if c["slug"] == station)
    if cfg["id"] not in T.stations_with("TN", ctx.raw_dir):
        raise ValueError(f"{cfg['name']} : pas de série LSH TN (exclusion I1)")
    if index == "canicule" and cfg["id"] != CANICULE["poste"]:
        raise ValueError("canicule : seuils départementaux définis pour Bordeaux-Mérignac seulement")
    series, hom, st = station_series(index, cfg["id"], ctx.raw_dir)
    _check(index, series, cfg["name"])
    title, what, desc, group = COUNTS[index]
    years = sorted(series)
    run = X.longest_run(sorted(hom))
    main = annual_trend(run, [series[y] for y in run], label=f"Série corrigée {run[0]}-{run[-1]}") if len(run) >= 10 else None
    rare = X.is_rare(series, hom)
    comp = X.compare_normals(series, hom)
    idx = X.IndexDef(index, "TN", ">=", 0.0, title, what)
    where = f"À {cfg['name']}"
    annual = T.AnnualSeries("TN", {y: series[y] for y in run}, {y: True for y in run}, (st,))
    breaks = T.detect_break(annual, annual.values, False, unit="jours") if main is not None else []
    lims = DAILY_LIMITS + [f"Particularité du site : {cfg['note']}",
                           "Aucune référence publiée n'a été fixée pour cet indicateur : confiance au plus « moyenne »."]
    if rare:
        lims.append(f"Indice rare (médiane 1961-1990 inférieure à {X.RARE_MEDIAN} jours par an) : la pente annuelle est "
                    "peu informative ; le chiffre mis en avant est l'écart entre normales (règle E9).")
    return Indicator(
        id=f"{index}-{station}", scale="gironde", group=group, variable=vocab.variable(index),
        place=vocab.station(station, cfg["name"]), title=f"{title} à {cfg['name']}", unit="jours",
        description=f"{desc} {cfg['note']}", frequency="annual", is_anomaly=False, reference_period=None,
        series=Series(time=[str(y) for y in years], value=[round(series[y], 2) for y in years],
                      quality=["homogenized" if y in hom else "raw" for y in years]),
        normals=X.normals_of(series, hom), trend=main, alt_trends=[],
        headline="normals" if rare and comp is not None else "trend", normals_comparison=comp, breakpoints=breaks,
        stations=[st], method_note="Comptage annuel sur les valeurs quotidiennes corrigées (méthode de la P2a).",
        finding=X._finding(where, idx, main, rare, comp), confidence=_count_confidence(main, rare, comp),
        limitations=lims, provenance=_prov(ctx),
    )


# ---------------------------------------------------------------- dates de vendanges (Daux et al., 2012)


VENDANGES_LIMITS = [
    "Série composite reconstituée à partir de plusieurs propriétés et archives du Bordelais (Daux et al., 2012) : les "
    "vignobles, les cépages et les sources changent au cours du temps ; elle s'arrête en 2006.",
    "La date de vendange dépend aussi des pratiques : la recherche d'une maturité plus poussée depuis les années "
    "1980-1990 retarde la récolte ; la tendance sous-estime donc l'effet du climat.",
    "Aucune référence publiée n'a été fixée pour cet indicateur : confiance au plus « moyenne ».",
]


def build_vendanges(ctx: BuildContext) -> Indicator:
    src = G.SOURCES["vendanges-bordeaux"]
    series = G.load("vendanges-bordeaux", ctx.raw_dir)
    _check("vendanges", series, "Bordeaux")
    prov = Provenance(source_name=src.name, source_url=src.page, license=src.license, extracted_at=ctx.extracted_at,
                      script="etl.indicators.impacts", etl_version=ctx.etl_version, homogenized=True)
    ind = S.assemble(ctx, ind_id="vendanges-bordeaux", scale="gironde", variable="vendanges",
                     place=vocab.station("bordelais", "Bordelais (série composite)"), title="Date de début des vendanges dans le Bordelais",
                     description="Date de début des vendanges, en jours après le 31 août (0 = 31 août, 15 = 15 septembre), "
                                 "base européenne des dates de vendanges (Daux et al., 2012). Une vendange précoce "
                                 "signale une saison chaude.",
                     unit="jours", series=series, hom=set(series), provenance=prov, limitations=VENDANGES_LIMITS[:2],
                     stations=[Station(id="ghd-bordeaux", name="Bordelais (Daux et al., 2012)", latitude=45.18,
                                       longitude=-0.75, altitude=0.0)],   # coordonnées données par le fichier
                     method_note="Série publiée, reprise sans modification.", reference=None, baseline=None,
                     group="Synthèse Gironde — viticulture", where="Dans le Bordelais",
                     label="la date de début des vendanges (jours après le 31 août)")
    hug, hom, _members, _ex = huglin_composite(ctx.raw_dir)
    r, ys = correlation({y: series[y] for y in series}, {y: hug[y] for y in hom})
    ok = r is not None and len(ys) >= I5_MIN_YEARS and r <= I5_MAX_R
    detail = (f"Contrôle I5 : corrélation avec l'indice de Huglin de Gironde r = {T.fr(r, 2, True) if r is not None else '—'}"
              f" sur {len(ys)} années ({ys[0] if ys else '—'}-{ys[-1] if ys else '—'}), seuil r ≤ −0,6 fixé avant calcul")
    lims = list(ind.limitations)
    if ok:
        lims.append(detail + " : satisfait.")
        conf = ind.confidence
    else:
        lims.append(detail + " : NON satisfait, signal non établi.")
        conf = "non_etabli"
    return ind.model_copy(update={"limitations": lims, "confidence": conf})


def i5(raw_dir: Path) -> tuple[float | None, list[int]]:
    """Pour la validation P4."""
    series = G.load("vendanges-bordeaux", raw_dir)
    hug, hom, _m, _e = huglin_composite(raw_dir)
    return correlation(series, {y: hug[y] for y in hom})

