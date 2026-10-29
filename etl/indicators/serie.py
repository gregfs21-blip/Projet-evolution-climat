"""Indicateurs « séries simples » (méthode « largeur d'abord », décision de Grég du 23/10/2026).

Une série annuelle publiée par un organisme de référence (ou une série LSH sommée sur l'année), sa tendance
(Sen + Hamed-Rao), ses normales, et UNE référence publiée fixée avant le calcul, dans le registre.

Règle de confiance (fixée le 23/10/2026, avant le premier calcul de ces indicateurs) :
- « élevée »     : tendance significative (Hamed-Rao) ET référence publiée satisfaite ;
                   une référence de NIVEAU (kind « mean », ajouté le 25/10/2026 avant le premier calcul qui l'utilise)
                   contrôle la lecture des données, pas l'évolution : elle ne suffit pas pour « élevée » ;
- « moyenne »    : tendance significative, référence absente ou non satisfaite ;
- « faible »     : significative seulement sans correction de l'autocorrélation ;
- « non établi » : sinon (y compris quand la référence elle-même annonce l'absence de tendance).
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import numpy as np

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import temperature as T
from etl.schema import Breakpoint, Indicator, Normal, Period, Place, Provenance, ReferenceCheck, Series, Station, Trend
from etl.sources import globaux as G
from etl.sources import meteofrance_lsh as lsh
from etl.stats.breaks import pettitt
from etl.stats.trend import annual_trend

NORMALS = [Period(start=1961, end=1990), Period(start=1991, end=2020)]
COMMON_WINDOW = Period(start=1962, end=2017)    # période commune des séries LSH RR (homogénéisées jusqu'en 2017)
LONG_SERIES = 80      # au-delà, tendance mise en avant sur les RECENT_YEARS dernières années (règle du 23/10/2026)
RECENT_YEARS = 50


def slugify(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def longest_run(years: list[int]) -> list[int]:
    best: list[int] = []
    cur: list[int] = []
    for y in sorted(years):
        cur = cur + [y] if cur and y == cur[-1] + 1 else [y]
        if len(cur) > len(best):
            best = cur
    return best


def mean_over(series: dict[int, float], hom: set[int], p: Period) -> float | None:
    ys = range(p.start, p.end + 1)
    if not all(y in series and y in hom for y in ys):
        return None
    return sum(series[y] for y in ys) / len(ys)


# ---------------------------------------------------------------- référence


def check_reference(ref: dict, series: dict[int, float], hom: set[int], unit: str) -> ReferenceCheck:
    """Calcule, sur nos données, la grandeur que la référence publie, et la compare à sa fourchette."""
    p = Period(start=ref["period"][0], end=ref["period"][1])
    kind = ref["kind"]
    lo, hi = ref.get("range", (None, None))
    measured: float | None = None
    satisfied = False
    ys = [y for y in range(p.start, p.end + 1) if y in series and y in hom]
    n = p.end - p.start + 1
    complete = len(ys) == n
    # Régressions (rate, relative_slope) : au moins 80 % des années de la période, sans les compléter.
    enough = len(ys) >= 0.8 * n
    ref_unit = ref.get("unit", unit)
    if kind == "difference":
        b = Period(start=ref["base"][0], end=ref["base"][1])
        m1, m2 = mean_over(series, hom, b), mean_over(series, hom, p)
        if m1 is not None and m2 is not None:
            measured = round(m2 - m1, 3)
    elif complete and kind == "slope":
        measured = annual_trend(ys, [series[y] for y in ys]).slope_per_decade
    elif enough and kind == "rate":
        measured = round(float(np.polyfit(ys, [series[y] for y in ys], 1)[0]), 4)          # régression, par an
    elif enough and kind == "relative_slope":
        b = Period(start=ref["base"][0], end=ref["base"][1])
        base = mean_over(series, hom, b)
        if base:
            measured = round(float(np.polyfit(ys, [series[y] for y in ys], 1)[0]) * 10 / base * 100, 3)
    elif complete and kind == "mean":
        measured = round(sum(series[y] for y in ys) / n, 3)
    elif complete and kind == "not_significant":
        t = annual_trend(ys, [series[y] for y in ys])
        measured = t.p_value
        satisfied = not t.significant
    if measured is not None and kind != "not_significant":
        satisfied = lo <= measured <= hi
    return ReferenceCheck(
        statement=ref["statement"], source=ref["source"], source_url=ref["url"], kind=kind, period=p,
        expected_low=lo, expected_high=hi, measured=measured, unit=ref_unit, satisfied=satisfied, fixed_on=ref["fixed_on"],
    )


def confidence(main: Trend | None, ref: ReferenceCheck | None) -> str:
    if main is None:
        return "non_etabli"
    if main.significant:
        return "elevee" if (ref is not None and ref.satisfied and ref.kind not in ("not_significant", "mean")) else "moyenne"
    if main.p_value_classical is not None and main.p_value_classical < main.alpha:
        return "faible"
    return "non_etabli"


def detect_break(years: list[int], series: dict[int, float], stations: list[Station], unit: str) -> list[Breakpoint]:
    """Test de Pettitt sur les années de la tendance, refait après retrait de la droite de Sen (même règle que P1).

    Ajouté le 25/10/2026 : jusque-là, les séries simples n'étaient pas testées alors que le site affichait
    « aucune rupture détectée ». Une rupture à ±1 an d'une correction d'homogénéité Météo-France est marquée artefact.
    """
    from scipy import stats as st
    if len(years) < 10:
        return []
    y = np.asarray([series[k] for k in years])
    res = pettitt(list(y))
    if res.p_value >= 0.05:
        return []
    new_regime = years[res.index + 1]
    x = np.asarray(years, dtype=float)
    slope, intercept, *_ = st.theilslopes(y, x)
    detr = pettitt(list(y - (intercept + slope * x)))
    artifact = any(abs(r - new_regime) <= 1 for r in T.mf_regime_years(tuple(stations)))
    note = f"écart des moyennes {T.fr(res.mean_after - res.mean_before)} {unit} avant/après {new_regime}"
    if detr.p_value >= 0.05:
        note += (f" ; après retrait de la tendance, plus aucune rupture significative (p = {T.fr(detr.p_value, 2, False)}) : "
                 "la rupture traduit la tendance elle-même, pas un saut brusque")
    else:
        note += (f" ; rupture encore significative après retrait de la tendance (p = {T.fr(detr.p_value, 3, False)}) : "
                 "saut brusque, ou accélération que la droite de Sen ne capte pas")
    if artifact:
        note += " ; coïncide avec une rupture d'homogénéité corrigée par Météo-France : non interprétable comme climatique"
    return [Breakpoint(time=str(new_regime), method="Pettitt (1979)", p_value=round(res.p_value, 6), possible_artifact=artifact,
                       detrended_p_value=round(detr.p_value, 6), note=note)]


# ---------------------------------------------------------------- assemblage


def _finding(where: str, label: str, unit: str, main: Trend | None, anomaly_ref: Period | None) -> str:
    if main is None:
        return f"{where}, la série de {label} est trop courte ou trop lacunaire pour une tendance."
    total = main.fitted_end - main.fitted_start
    verdict = ("tendance significative, corrigée de l'autocorrélation" if main.significant
               else "pas de tendance significative après correction de l'autocorrélation")
    return (f"{where}, {label} a évolué de {T.fr(main.slope_per_decade)} {unit} par décennie entre {main.period.start} "
            f"et {main.period.end}, soit {T.fr(total)} {unit} sur la période ({verdict}).")


def assemble(ctx: BuildContext, *, ind_id: str, scale: str, variable: str, place: Place, title: str, description: str,
             unit: str, series: dict[int, float], hom: set[int], provenance: Provenance, limitations: list[str],
             stations: list[Station], method_note: str | None, reference: dict | None, baseline: list[int] | str | None,
             group: str, where: str, label: str, raw_reason: str | None = None,
             common_window: Period | None = None, indicative: bool = False,
             display_only: str | None = None) -> Indicator:
    """`raw_reason` : série brute, non homogénéisée (règle C2) — publiée sans tendance ni normale, raison donnée.

    `indicative` : série brute avec tendance INDICATIVE (exception à C2, décision de Grég du 25/10/2026, prise après
    avoir vu les séries brutes) — toutes les années complètes entrent dans la tendance, points marqués « bruts »,
    aucune normale, aucune référence, confiance « faible » si Hamed-Rao significatif, « non établi » sinon.

    `display_only` : série exploitable telle que publiée mais SANS lecture climatique (critère I8 de la P4, CatNat par
    péril) — ni tendance, ni normale, ni référence ; la raison est affichée.
    """
    if sum(map(bool, (raw_reason, indicative, display_only))) > 1:
        raise ValueError("raw_reason, indicative et display_only sont exclusifs")
    quality_hom = set() if indicative else set(hom)
    if raw_reason:
        hom = set()
        quality_hom = set()
    if display_only:
        hom = set()
        reference = None
    if indicative:
        hom = set(series)
        reference = None
    ref_period = None
    if baseline == "series":
        ys_ = sorted(y for y in series if y in hom)
        baseline = [ys_[0], ys_[-1]]
        m = sum(series[y] for y in ys_) / len(ys_)
        ref_period = Period(start=baseline[0], end=baseline[1])
        series = {y: v - m for y, v in series.items()}
    elif baseline:
        ref_period = Period(start=baseline[0], end=baseline[1])
        m = mean_over(series, hom, ref_period)
        if m is None:
            raise ValueError(f"{ind_id} : période de référence {baseline} incomplète")
        series = {y: v - m for y, v in series.items()}
    years = sorted(series)
    if not years:
        raise ValueError(f"{ind_id} : série vide")
    run = longest_run(sorted(hom & set(series)))
    alts = []
    # Série de plus de LONG_SERIES ans : la tendance mise en avant porte sur les RECENT_YEARS dernières années
    # (comparables d'un indicateur à l'autre) ; la tendance sur toute la série reste publiée à côté.
    if len(run) > LONG_SERIES:
        recent = run[-RECENT_YEARS:]
        main = annual_trend(recent, [series[y] for y in recent], label=f"{recent[0]}-{recent[-1]}, {RECENT_YEARS} dernières années")
        alts.append(annual_trend(run, [series[y] for y in run], label=f"{run[0]}-{run[-1]}, toute la série"))
    else:
        main = annual_trend(run, [series[y] for y in run], label=f"{run[0]}-{run[-1]}") if len(run) >= 10 else None
    # Période commune des stations d'un même réseau (LSH) : seuls les constructeurs LSH la demandent. Une série d'une
    # autre source (ERA5…) n'a pas de « stations » à comparer (correctif du 25/10/2026, après le premier calcul ERA5).
    if common_window:
        ys = [y for y in run if common_window.start <= y <= common_window.end]
        if len(ys) == common_window.end - common_window.start + 1 and len(run) > len(ys):
            alts.append(annual_trend(ys, [series[y] for y in ys], label=f"{common_window.start}-{common_window.end}, période commune des stations"))
    check = check_reference(reference, series, hom, unit) if reference else None
    # Test sur les années de la tendance mise en avant (sur 1850-2025, une droite ne capte pas l'accélération récente
    # et le test signalerait une « rupture » vers 1937 : choix du 25/10/2026, après un premier calcul sur toute la série).
    breaks = (detect_break([y for y in run if main.period.start <= y <= main.period.end], series, stations, unit)
              if main is not None else [])
    normals = []
    if not baseline and not indicative:
        for p in NORMALS:
            m = mean_over(series, hom, p)
            if m is not None:
                normals.append(Normal(period=p, value=round(m, 3)))
    lims = list(limitations)
    if indicative:
        lims.append("Tendance INDICATIVE sur une série brute, non homogénéisée : exception à la règle C2 du projet, "
                    "décidée par Grég le 25/10/2026 après avoir vu les séries. Un changement d'instrument ou "
                    "d'emplacement peut à lui seul créer la pente affichée ; confiance au plus « faible ».")
    elif raw_reason:
        lims.append("Série brute, non homogénéisée : aucune tendance ni normale n'est calculée (règle C2 du projet).")
    elif display_only:
        lims.append(f"Affichage seulement, sans tendance ni normale : {display_only}")
    elif check is None:
        lims.append("Aucune référence publiée n'a été fixée pour cet indicateur : confiance au plus « moyenne ».")
    elif not check.satisfied:
        lims.append(f"Référence publiée non retrouvée ({check.statement}) : confiance au plus « moyenne ».")
    elif check.kind == "mean":
        lims.append("La référence publiée porte sur le niveau moyen : elle contrôle la lecture des données, pas "
                    "l'évolution ; confiance au plus « moyenne ».")
    return Indicator(
        id=ind_id, scale=scale, group=group, variable=vocab.variable(variable), place=place, title=title, unit=unit,
        description=description, frequency="annual", is_anomaly=bool(baseline), reference_period=ref_period,
        series=Series(time=[str(y) for y in years], value=[round(series[y], 4) for y in years],
                      quality=["homogenized" if y in quality_hom else "raw" for y in years]),
        normals=normals, trend=main, alt_trends=alts, reference_check=check, breakpoints=breaks, stations=stations, method_note=method_note,
        finding=(f"{where}, {label} : {raw_reason or display_only}" if (raw_reason or display_only)
                 else _finding(where, label, unit, main, ref_period)
                 + (" Tendance indicative : série brute, non homogénéisée." if indicative else "")),
        confidence=("faible" if main and main.significant else "non_etabli") if indicative else confidence(main, check),
        indicative=indicative, limitations=lims,
        provenance=provenance,
    )


# ---------------------------------------------------------------- constructeurs


def _place(scale: str, place: dict) -> Place:
    return Place(id=place["id"], name=place["name"], kind=place.get("kind", "composite" if place["id"] == scale else "station"))


def build(ctx: BuildContext, source: str, scale: str, variable: str, place: dict, title: str, description: str, label: str,
          where: str, limitations: list[str], reference: dict | None = None, baseline: list[int] | str | None = None,
          station: dict | None = None, start: int | None = None, group: str | None = None,
          display_only: str | None = None) -> Indicator:
    """Série publiée par un organisme (NOAA, NASA, Met Office, NSIDC, PSMSL…)."""
    src = G.SOURCES[source]
    series = G.load(source, ctx.raw_dir)
    if start:
        series = {y: v for y, v in series.items() if y >= start}
    hom = set(series)    # produit de référence : toutes les années sont exploitables telles que publiées
    stations = []
    if station:
        stations = [Station(id=station["id"], name=station["name"], latitude=station["lat"], longitude=station["lon"],
                            altitude=station.get("alt", 0.0))]
    v = vocab.variable(variable)
    prov = Provenance(source_name=src.name, source_url=src.page, license=src.license, extracted_at=ctx.extracted_at,
                      script="etl.indicators.serie", etl_version=ctx.etl_version, homogenized=True)
    lims = [f"Série publiée par {src.name.split(' — ')[0]}, reprise sans modification"
            + (f", sauf la période de référence ramenée à {baseline[0]}-{baseline[1]}." if baseline else ".")] + limitations
    pl = _place(scale, place)
    return assemble(ctx, ind_id=f"{variable}-{pl.id}", scale=scale, variable=variable, place=pl, title=title,
                    description=description, unit=src.unit, series=series, hom=hom, provenance=prov, limitations=lims,
                    stations=stations, method_note=None, reference=reference, baseline=baseline,
                    group=group or v.theme_label, where=where, label=label, display_only=display_only)


# --- séries LSH sommées sur l'année (précipitations, insolation)


def lsh_annual(var: str, poste: str, raw_dir: Path) -> tuple[dict[int, float], set[int], Station]:
    s = next((x for x in lsh.load_department(var, "33", raw_dir, download=not T._offline()) if x.station.id == poste), None)
    if s is None:
        raise KeyError(f"pas de série LSH {var} pour le poste {poste}")
    series, hom = {}, set()
    for y in sorted({y for y, _ in s.values}):
        months = [(y, m) for m in range(1, 13)]
        if all(k in s.values for k in months):
            series[y] = sum(s.values[k] for k in months)
            if all(s.homogenized[k] for k in months):
                hom.add(y)
    return series, hom, s.station


LSH_LIMITS = [
    "Série homogénéisée par Météo-France (méthode HOMER) ; au-delà de la période homogénéisée, valeurs brutes affichées "
    "pour information et exclues des tendances et des normales.",
    "Une année n'est calculée que si ses 12 mois existent ; aucune valeur n'est complétée.",
]


def build_lsh(ctx: BuildContext, lsh_var: str, poste: str, variable: str, title: str, description: str, label: str,
              limitations: list[str] | None = None, reference: dict | None = None) -> Indicator:
    series, hom, st = lsh_annual(lsh_var, poste, ctx.raw_dir)
    check_plausible(variable, series, f"{lsh_var} {poste}")
    name = T.station_config().get(poste, {}).get("name") or st.name
    slug = T.station_config().get(poste, {}).get("slug") or slugify(name)
    st = st.model_copy(update={"name": name})
    v = vocab.variable(variable)
    prov = Provenance(source_name=lsh.SOURCE_NAME, source_url=lsh.DATASET_URL, license=lsh.LICENSE,
                      extracted_at=ctx.extracted_at, script="etl.indicators.serie", etl_version=ctx.etl_version, homogenized=True)
    return assemble(ctx, ind_id=f"{variable}-{slug}", scale="gironde", variable=variable, place=vocab.station(slug, name),
                    title=title.format(name=name), description=description.format(name=name), unit=v_unit(variable),
                    series=series, hom=hom, provenance=prov, limitations=LSH_LIMITS + (limitations or []), stations=[st],
                    method_note=None, reference=reference, baseline=None, group=f"Stations — {v.label}", where=f"À {name}",
                    label=label, common_window=COMMON_WINDOW)


def build_lsh_composite(ctx: BuildContext, lsh_var: str, variable: str, span: list[int], title: str, description: str,
                        label: str, limitations: list[str] | None = None, reference: dict | None = None) -> Indicator:
    """Moyenne des cumuls annuels des stations homogénéisées sur toute la période `span` (réseau constant)."""
    p = Period(start=span[0], end=span[1])
    members, excluded = [], []
    for s in lsh.load_department(lsh_var, "33", ctx.raw_dir, download=not T._offline()):
        series, hom, st = lsh_annual(lsh_var, s.station.id, ctx.raw_dir)
        name = T.station_config().get(st.id, {}).get("name") or st.name
        ok = all(y in hom for y in range(p.start, p.end + 1))
        (members if ok else excluded).append((series, hom, st.model_copy(update={"name": name})))
    if len(members) < 3:
        raise ValueError(f"composite {variable} : seulement {len(members)} station(s) à réseau constant")
    years = sorted(set.intersection(*(set(m[0]) for m in members)))
    series = {y: sum(m[0][y] for m in members) / len(members) for y in years}
    hom = {y for y in years if all(y in m[1] for m in members)}
    v = vocab.variable(variable)
    prov = Provenance(source_name=lsh.SOURCE_NAME, source_url=lsh.DATASET_URL, license=lsh.LICENSE,
                      extracted_at=ctx.extracted_at, script="etl.indicators.serie", etl_version=ctx.etl_version, homogenized=True)
    names = ", ".join(m[2].name for m in members)
    note = (f"Moyenne des cumuls annuels de {len(members)} stations ({names}), homogénéisées sur toute la période "
            f"{p.start}-{p.end} (réseau constant)" + (f" ; exclues : {', '.join(e[2].name for e in excluded)}" if excluded else "") + ".")
    return assemble(ctx, ind_id=f"{variable}-gironde", scale="gironde", variable=variable,
                    place=vocab.composite("gironde", "Gironde"), title=title, description=description, unit=v_unit(variable),
                    series=series, hom=hom, provenance=prov, limitations=LSH_LIMITS + (limitations or []),
                    stations=[m[2] for m in members], method_note=note, reference=reference, baseline=None,
                    group="Synthèse Gironde — eau et soleil", where="En Gironde", label=label, common_window=COMMON_WINDOW)


UNITS = {"rr-cumul": "mm", "insolation": "h"}
PLAUSIBLE = {"rr-cumul": (300, 2500), "insolation": (1000, 3500)}   # bornes annuelles en Gironde : une unité mal lue échoue


def check_plausible(variable: str, series: dict[int, float], where: str) -> None:
    lo, hi = PLAUSIBLE[variable]
    bad = {y: v for y, v in series.items() if not lo <= v <= hi}
    if bad:
        raise ValueError(f"{where} : {len(bad)} cumul(s) annuel(s) hors de [{lo} ; {hi}] (ex. {list(bad.items())[:3]}) — unité ?")


def v_unit(variable: str) -> str:
    return UNITS[variable]
