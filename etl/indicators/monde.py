"""P6 — monde : indicateurs combinés ou à deux périodes (critères K1-K8 validés par Grég le 31/10/2026, avant calcul).

Les séries simples (niveau marin, pH, puits, troposphère) passent par `etl.indicators.serie.build` ; ce module ne
contient que :
- la part des émissions absorbée par les puits (Global Carbon Budget 2025) ;
- le trou d'ozone, dont la tendance mise en avant porte sur 2000-2025 (choix fixé avant calcul).
"""

from __future__ import annotations

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import serie as S
from etl.indicators import temperature as T
from etl.schema import Indicator, Provenance
from etl.sources import globaux as G
from etl.stats.trend import annual_trend

OZONE_RECENT = (2000, 2025)
OZONE_EARLY = (1979, 1994)


def _prov(ctx: BuildContext, src: G.Source) -> Provenance:
    return Provenance(source_name=src.name, source_url=src.page, license=src.license, extracted_at=ctx.extracted_at,
                      script="etl.indicators.monde", etl_version=ctx.etl_version, homogenized=True)


def sink_fraction(ocean: dict[int, float], land: dict[int, float], fossil: dict[int, float],
                  luc: dict[int, float]) -> dict[int, float]:
    ys = sorted(set(ocean) & set(land) & set(fossil) & set(luc))
    return {y: round(100 * (ocean[y] + land[y]) / (fossil[y] + luc[y]), 2) for y in ys}


def build_fraction(ctx: BuildContext) -> Indicator:
    series = sink_fraction(*(G.load(s, ctx.raw_dir) for s in ("gcb-ocean", "gcb-land", "gcb-fossil", "gcb-luc")))
    bad = {y: v for y, v in series.items() if not 0 <= v <= 100}
    if bad:
        raise ValueError(f"part absorbée hors [0 ; 100] % (K7) : {list(bad.items())[:3]}")
    src = G.SOURCES["gcb-ocean"]
    return S.assemble(ctx, ind_id="part-puits-monde", scale="monde", variable="part-puits",
                      place=vocab.composite("monde", "Monde"), title="Part des émissions de CO₂ absorbée par l'océan et les terres",
                      description="Puits océanique + puits terrestre, rapportés aux émissions de CO₂ (combustibles fossiles, "
                                  "ciment, changement d'usage des sols), d'après le Global Carbon Budget 2025. Le reste "
                                  "s'accumule dans l'atmosphère.",
                      unit="%", series=series, hom=set(series), provenance=_prov(ctx, src),
                      limitations=[
                          "Puits estimés par des modèles contraints par les observations (± 0,4 GtC/an pour l'océan, "
                          "± 0,5 pour les terres) ; le puits terrestre varie fortement d'une année à l'autre (El Niño, "
                          "sécheresses, éruptions).",
                          "Rapport de deux grandeurs incertaines : une année isolée ne dit rien, seule la tendance compte.",
                          "Aucune référence indépendante : la source est elle-même la référence ; confiance au plus « moyenne ».",
                      ],
                      stations=[], method_note="(puits océanique + puits terrestre) / (émissions fossiles + changement "
                      "d'usage des sols) × 100, estimation GCB de chaque terme.", reference=None, baseline=None,
                      group="Synthèse monde — puits de carbone", where="À l'échelle du globe",
                      label="la part des émissions absorbée par les puits")


def build_ozone(ctx: BuildContext) -> Indicator:
    src = G.SOURCES["ozone-trou"]
    series = G.load("ozone-trou", ctx.raw_dir)
    bad = {y: v for y, v in series.items() if not 0 <= v <= 35}
    if bad:
        raise ValueError(f"trou d'ozone hors [0 ; 35] millions de km² (K7) : {list(bad.items())[:3]}")
    ind = S.assemble(ctx, ind_id="trou-ozone-monde", scale="monde", variable="trou-ozone",
                     place=vocab.composite("monde", "Monde"), title="Surface du trou d'ozone antarctique",
                     description="Surface moyenne du trou d'ozone au-dessus de l'Antarctique, du 7 septembre au 13 octobre "
                                 "(zone où la colonne d'ozone passe sous 220 unités Dobson), NASA Ozone Watch.",
                     unit="millions de km²", series=series, hom=set(series), provenance=_prov(ctx, src),
                     limitations=[
                         "La surface dépend aussi de la météo stratosphérique de l'année (températures, vortex polaire) : "
                         "les écarts d'une année à l'autre sont grands.",
                         "Tendance mise en avant sur 2000-2025 (après le maximum des substances destructrices d'ozone), "
                         "choix fixé avant calcul ; 1979-1994 publié à côté ; 1995 manque.",
                         "Aucune référence chiffrée retenue : confiance au plus « moyenne ».",
                     ],
                     stations=[], method_note="Série publiée, reprise sans modification.", reference=None, baseline=None,
                     group="Synthèse monde — ozone", where="Au-dessus de l'Antarctique", label="la surface du trou d'ozone")
    ys = [y for y in range(OZONE_RECENT[0], OZONE_RECENT[1] + 1) if y in series]
    early = [y for y in range(OZONE_EARLY[0], OZONE_EARLY[1] + 1) if y in series]
    main = annual_trend(ys, [series[y] for y in ys], label=f"{ys[0]}-{ys[-1]}, depuis le maximum des substances destructrices")
    alt = annual_trend(early, [series[y] for y in early], label=f"{early[0]}-{early[-1]}, creusement")
    breaks = S.detect_break(ys, series, [], "millions de km²")
    finding = S._finding("Au-dessus de l'Antarctique", "la surface du trou d'ozone", "millions de km²", main, None) + (
        f" Sur {early[0]}-{early[-1]}, elle avait évolué de {T.fr(alt.slope_per_decade)} millions de km² par décennie.")
    return ind.model_copy(update={"trend": main, "alt_trends": [alt], "breakpoints": breaks, "finding": finding,
                                  "confidence": S.confidence(main, None)})

