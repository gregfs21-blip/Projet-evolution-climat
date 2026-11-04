"""P7 — indicateurs exploratoires (critères L1-L5 validés par Grég le 31/10/2026, avant calcul).

- Blocages euro-atlantiques (Tibaldi et Molteni, 1990) : jours bloqués par hiver et par été, secteur 30° O-30° E ;
  longitudes bloquées fournies par le relevé (etl/sources/era5_blocking.py) ; contiguïté (≥ 3 longitudes, 7,5°) et
  persistance (≥ 5 jours) appliquées ici. Plafond « signal non établi » (D-V).
- Z500 moyen Atlantique-Europe (35-70° N, 30° O-30° E) : moyenne annuelle ; règle ERA5 (au plus « moyenne »).
- CAPE moyenne de juin à août sur la Gironde : indicateur indirect d'orages ; plafond « signal non établi ».
"""

from __future__ import annotations

import calendar
from datetime import date, timedelta

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import serie as S
from etl.schema import Indicator, Provenance
from etl.sources import cds_era5 as cds
from etl.sources import era5_blocking as B

LON0, STEP = -60.0, 2.5
SECTOR = (-30.0, 30.0)
SECTOR_ALT = (-20.0, 40.0)        # L4, information
MIN_LON = 3
MIN_DAYS = 5
CAP = "Indicateur exploratoire : confiance plafonnée à « signal non établi » (décision de Grég du 31/10/2026, P7)."


# ---------------------------------------------------------------- calculs purs (testés)


def sector_blocked(bits: str, sector: tuple[float, float] = SECTOR, min_lon: int = MIN_LON) -> bool:
    i0, i1 = int(round((sector[0] - LON0) / STEP)), int(round((sector[1] - LON0) / STEP))
    run = best = 0
    for c in bits[i0:i1 + 1]:
        run = run + 1 if c == "1" else 0
        best = max(best, run)
    return best >= min_lon


def episode_days(flags: dict[str, bool], min_days: int = MIN_DAYS) -> set[str]:
    """Jours appartenant à une suite d'au moins `min_days` jours bloqués consécutifs (jours civils)."""
    out: set[str] = set()
    run: list[str] = []
    prev = None
    for d in sorted(flags):
        cur = date.fromisoformat(d)
        if flags[d] and prev is not None and run and cur - prev == timedelta(days=1):
            run.append(d)
        elif flags[d]:
            run = [d]
        else:
            run = []
        if len(run) >= min_days:
            out.update(run)
        prev = cur
    return out


def season_days(year: int, season: str) -> list[str]:
    if season == "hiver":
        months = [(year - 1, 12), (year, 1), (year, 2)]
    else:
        months = [(year, 6), (year, 7), (year, 8)]
    return [f"{y}-{m:02d}-{d:02d}" for y, m in months for d in range(1, calendar.monthrange(y, m)[1] + 1)]


def seasonal_counts(rows: list[dict], season: str, sector: tuple[float, float] = SECTOR) -> dict[int, float]:
    flags = {r["day"]: sector_blocked(r["blocked"], sector) for r in rows}
    ep = episode_days(flags)
    years = sorted({int(d[:4]) for d in flags})
    out = {}
    for y in years:
        days = season_days(y, season)
        if all(d in flags for d in days):
            out[y] = float(sum(d in ep for d in days))
    return out


# ---------------------------------------------------------------- indicateurs


def _prov(ctx: BuildContext, name: str, page: str) -> Provenance:
    return Provenance(source_name=name, source_url=page, license=cds.LICENSE, extracted_at=ctx.extracted_at,
                      script="etl.indicators.exploratoire", etl_version=ctx.etl_version, homogenized=False)


def _cap(ind: Indicator) -> Indicator:
    return ind.model_copy(update={"confidence": "non_etabli", "limitations": list(ind.limitations) + [CAP]})


SEASONS = {"hiver": ("décembre à février", "jours-blocage-hiver"), "ete": ("juin à août", "jours-blocage-ete")}


def build_blocking(ctx: BuildContext, season: str) -> Indicator:
    rows = B.load()
    series = seasonal_counts(rows, season)
    what, variable = SEASONS[season]
    bad = {y: v for y, v in series.items() if not 0 <= v <= 92}
    if bad or len(series) < 60:
        raise ValueError(f"blocages {season} : valeurs hors bornes ou série courte : {list(bad.items())[:3]}, {len(series)} saisons")
    ind = S.assemble(ctx, ind_id=f"{variable}-monde", scale="monde", variable=variable,
                     place=vocab.composite("monde", "Monde"),
                     title=f"Jours de blocage atlantique-européen ({'hiver' if season == 'hiver' else 'été'})",
                     description=f"Nombre de jours de {what} pendant lesquels un anticyclone de blocage persiste au moins "
                                 "5 jours sur l'Atlantique-Europe (30° O-30° E) : la circulation d'ouest est bloquée et le "
                                 "même temps dure (canicules en été, froid sec en hiver). Indice de Tibaldi et Molteni sur "
                                 "ERA5.",
                     unit="jours", series=series, hom=set(series), provenance=_prov(ctx, B.SOURCE_NAME, B.PAGE),
                     limitations=[
                         "Indice défini par un seuil sur le gradient de géopotentiel : d'autres définitions des blocages "
                         "donnent d'autres fréquences ; la littérature ne retient pas de tendance robuste observée.",
                         "ERA5 avant 1979 repose sur beaucoup moins d'observations en altitude (pas de satellites).",
                         "Grille de 2,5° : décalages de latitude de ± 5° au lieu des ± 4° de la définition d'origine.",
                     ],
                     stations=[], method_note="Longitude bloquée si GHGS > 0 et GHGN < −10 m par degré (φN = 80°, φ0 = 60°, "
                     "φS = 40°, décalés de −5°, 0 ou +5°) ; jour bloqué si au moins 3 longitudes contiguës (7,5°) le sont "
                     "dans 30° O-30° E ; épisode d'au moins 5 jours ; Z500 quotidien moyen ERA5, grille 2,5°.",
                     reference=None, baseline=None, group="Exploratoire — circulation atmosphérique",
                     where="Sur l'Atlantique et l'Europe", label=f"le nombre de jours de blocage de {what}")
    return _cap(ind)


def build_z500(ctx: BuildContext) -> Indicator:
    rows = B.load()
    per: dict[int, list[float]] = {}
    for r in rows:
        per.setdefault(int(r["day"][:4]), []).append(float(r["z500_sector"]))
    series = {y: round(sum(v) / len(v), 2) for y, v in per.items() if len(v) == (366 if calendar.isleap(y) else 365)}
    bad = {y: v for y, v in series.items() if not 5000 <= v <= 6000}
    if bad:
        raise ValueError(f"Z500 hors [5000 ; 6000] m : {list(bad.items())[:3]}")
    return S.assemble(ctx, ind_id="z500-europe-monde", scale="monde", variable="z500-europe",
                      place=vocab.composite("monde", "Monde"), title="Géopotentiel 500 hPa moyen sur l'Atlantique-Europe",
                      description="Altitude moyenne annuelle de la surface 500 hPa (environ 5 500 m) entre 35 et 70° N et "
                                  "30° O et 30° E (ERA5). Elle monte quand la colonne d'air se réchauffe et se dilate.",
                      unit="m", series=series, hom=set(series), provenance=_prov(ctx, B.SOURCE_NAME, B.PAGE),
                      limitations=[
                          "Réanalyse ERA5 : avant 1979, peu d'observations en altitude ; aucune homogénéisation.",
                          "Aucune référence retenue : confiance au plus « moyenne ».",
                      ],
                      stations=[], method_note="Moyenne quotidienne du Z500 sur la zone, pondérée par le cosinus de la "
                      "latitude, puis moyenne de l'année.", reference=None, baseline=None,
                      group="Exploratoire — circulation atmosphérique", where="Sur l'Atlantique et l'Europe",
                      label="l'altitude de la surface 500 hPa")


def build_cape(ctx: BuildContext) -> Indicator:
    monthly = cds.load_value("cape-gironde")
    years = sorted({int(m[:4]) for m in monthly})
    series = {y: round(sum(monthly[f"{y}-{m:02d}"] for m in (6, 7, 8)) / 3, 1) for y in years
              if all(f"{y}-{m:02d}" in monthly for m in (6, 7, 8))}
    bad = {y: v for y, v in series.items() if not 0 <= v <= 3000}
    if bad:
        raise ValueError(f"CAPE hors [0 ; 3000] J/kg : {list(bad.items())[:3]}")
    ind = S.assemble(ctx, ind_id="cape-gironde", scale="gironde", variable="cape",
                     place=vocab.station("gironde-era5", "Gironde (ERA5, 44,2-45,6° N, 1,3° O-0,4° E)"),
                     title="Énergie de convection en été en Gironde (indicateur indirect d'orages)",
                     description="CAPE moyenne de juin à août sur la Gironde (ERA5) : l'énergie disponible pour faire monter "
                                 "l'air et former des orages. Une CAPE élevée rend les orages possibles, elle ne les "
                                 "déclenche pas.",
                     unit="J/kg", series=series, hom=set(series), provenance=_prov(ctx, cds.SOURCE_NAME.replace(
                         "niveaux de pression", "niveaux uniques"), "https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means"),
                     limitations=[
                         "Ce n'est pas la foudre : aucune série ouverte d'impacts de foudre n'existe (Météorage, réseau "
                         "privé) ; la densité d'éclairs du modèle ERA5 n'est pas disponible en moyenne mensuelle.",
                         "Moyenne mensuelle de la CAPE : les orages dépendent de pics de quelques heures et d'un "
                         "déclencheur, que cette moyenne ne voit pas.",
                     ],
                     stations=[cds_station()], method_note="Moyenne pondérée des mailles de la boîte, chaque mois, puis "
                     "moyenne de juin, juillet et août.", reference=None, baseline=None,
                     group="Exploratoire — orages", where="En Gironde", label="la CAPE moyenne de l'été")
    return _cap(ind)


def cds_station():
    from etl.schema import Station
    n, w, s, e = cds.CAPE_BOX
    return Station(id="era5-cape-gironde", name="Gironde (ERA5)", latitude=(n + s) / 2, longitude=(w + e) / 2, altitude=0.0)
