"""Contrat de données entre l'ETL et le site.

Ce schéma est la référence unique. Le site Next.js en possède le miroir exact
(web/lib/schema.ts, avec zod). Toute modification ici doit être reportée là-bas
et faire monter SCHEMA_VERSION.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SCHEMA_VERSION = "1.1"
Quality = Literal["homogenized", "raw"]

Scale = Literal["gironde", "france", "monde"]
Frequency = Literal["annual", "seasonal", "monthly", "daily"]
Confidence = Literal["elevee", "moyenne", "faible", "non_etabli"]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Period(_Strict):
    start: int = Field(ge=1700, le=2200)
    end: int = Field(ge=1700, le=2200)

    @model_validator(mode="after")
    def _ordered(self) -> "Period":
        if self.end < self.start:
            raise ValueError("period.end doit être >= period.start")
        return self


class Provenance(_Strict):
    source_name: str = Field(min_length=1)
    source_url: str = Field(pattern=r"^https?://")
    license: str = Field(min_length=1)
    extracted_at: datetime
    script: str = Field(min_length=1, description="Module ETL qui a produit le fichier")
    etl_version: str = Field(min_length=1)
    homogenized: bool = Field(description="Série homogénéisée (ex. LSH) ou brute")


class Trend(_Strict):
    label: str = Field(default="", description="Ex. 'Période homogénéisée', '1959-2009 (comparaison ClimatHD)'")
    method: str = Field(min_length=1, description="Ex. 'mann-kendall-hamed-rao + sen'")
    period: Period
    slope_per_decade: float = Field(description="Pente de Sen, en unité de l'indicateur par décennie")
    slope_ci_low: float | None = None
    slope_ci_high: float | None = None
    fitted_start: float = Field(description="Valeur de la droite de Sen en début de période (pour le tracé)")
    fitted_end: float = Field(description="Valeur de la droite de Sen en fin de période")
    p_value: float = Field(ge=0, le=1)
    significant: bool
    alpha: float = Field(default=0.05, gt=0, lt=1)
    p_value_classical: float | None = Field(
        default=None, ge=0, le=1, description="Mann-Kendall sans correction, pour mesurer l'effet de l'autocorrélation"
    )


class Breakpoint(_Strict):
    time: str
    method: str
    p_value: float | None = Field(default=None, ge=0, le=1)
    possible_artifact: bool = Field(
        default=False, description="À ±1 an d'une rupture d'homogénéité corrigée : non interprétable comme climatique"
    )
    detrended_p_value: float | None = Field(
        default=None, ge=0, le=1,
        description="Pettitt sur les résidus après retrait de la tendance de Sen : un p élevé signifie que la "
        "« rupture » s'explique par la tendance elle-même, pas par un saut brusque",
    )
    note: str | None = None


class Normal(_Strict):
    """Moyenne absolue d'une période de référence (ex. normale 1961-1990)."""

    period: Period
    value: float


class Station(_Strict):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    altitude: float
    series_id: str | None = Field(default=None, description="Identifiant de la série homogénéisée (ex. MTN233281001)")
    homogenized_period: Period | None = None
    min_detectable_amplitude: float | None = Field(default=None, description="Amplitude minimale détectable, °C")
    homogenization_breaks: list[str] = Field(default_factory=list, description="Ruptures corrigées, AAAA-MM")
    file_produced: str | None = Field(default=None, description="Date de production du fichier source")


class Series(_Strict):
    """Série en colonnes : plus compacte qu'une liste d'objets pour 30 000 points."""

    time: list[str] = Field(min_length=1, description="ISO : 'AAAA', 'AAAA-MM' ou 'AAAA-MM-JJ'")
    value: list[float | None]
    quality: list[Quality] | None = Field(default=None, description="Statut de chaque point : homogénéisé ou brut")

    @model_validator(mode="after")
    def _same_length(self) -> "Series":
        if len(self.time) != len(self.value):
            raise ValueError("series.time et series.value doivent avoir la même longueur")
        if self.quality is not None and len(self.quality) != len(self.time):
            raise ValueError("series.quality doit avoir la même longueur que series.time")
        if self.time != sorted(self.time):
            raise ValueError("series.time doit être trié par ordre croissant")
        if len(set(self.time)) != len(self.time):
            raise ValueError("series.time contient des doublons")
        return self


class Indicator(_Strict):
    schema_version: Literal["1.1"] = SCHEMA_VERSION
    id: str = Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    scale: Scale
    group: str | None = Field(default=None, description="Regroupement d'affichage (ex. 'Synthèse', 'Stations')")
    title: str = Field(min_length=1)
    unit: str
    description: str = Field(min_length=1)
    frequency: Frequency
    is_anomaly: bool = Field(description="Valeurs exprimées en écart à reference_period")
    reference_period: Period | None
    series: Series
    normals: list[Normal] = Field(default_factory=list)
    trend: Trend | None
    alt_trends: list[Trend] = Field(default_factory=list, description="Fenêtres de comparaison (validation)")
    breakpoints: list[Breakpoint] = Field(default_factory=list)
    stations: list[Station] = Field(default_factory=list)
    method_note: str | None = Field(default=None, description="Construction de l'indicateur (ex. composite)")
    finding: str = Field(min_length=1, description="Constat en une phrase")
    confidence: Confidence
    limitations: list[str] = Field(min_length=1, description="Au moins une limite explicite")
    provenance: Provenance
    is_demo: bool = False

    @field_validator("limitations")
    @classmethod
    def _no_empty(cls, v: list[str]) -> list[str]:
        if any(not s.strip() for s in v):
            raise ValueError("limitation vide")
        return v

    @model_validator(mode="after")
    def _coherence(self) -> "Indicator":
        if self.is_anomaly and self.reference_period is None:
            raise ValueError("une anomalie exige une reference_period")
        for t in [self.trend, *self.alt_trends]:
            if t and t.significant != (t.p_value < t.alpha):
                raise ValueError(f"tendance '{t.label}' : significant incohérent avec p_value et alpha")
        if self.series.quality is not None:
            # Règle C2 : aucune tendance ni normale ne peut s'appuyer sur un point non homogénéisé.
            raw_years = {int(t[:4]) for t, q in zip(self.series.time, self.series.quality) if q == "raw"}
            spans = [(t.label or "tendance", t.period) for t in [self.trend, *self.alt_trends] if t]
            spans += [(f"normale {n.period.start}-{n.period.end}", n.period) for n in self.normals]
            for label, period in spans:
                if any(period.start <= y <= period.end for y in raw_years):
                    raise ValueError(f"{label} inclut des années non homogénéisées")
        if self.is_demo and "démo" not in self.title.lower():
            raise ValueError("un indicateur de démonstration doit l'afficher dans son titre")
        return self


class ManifestEntry(_Strict):
    id: str
    scale: Scale
    title: str
    unit: str
    path: str = Field(description="Chemin relatif à data/processed")
    confidence: Confidence
    is_demo: bool
    group: str | None = None


class Manifest(_Strict):
    schema_version: Literal["1.1"] = SCHEMA_VERSION
    generated_at: datetime
    etl_version: str
    indicators: list[ManifestEntry]

    @model_validator(mode="after")
    def _unique(self) -> "Manifest":
        keys = [(e.scale, e.id) for e in self.indicators]
        if len(set(keys)) != len(keys):
            raise ValueError("couple (scale, id) dupliqué dans le manifeste")
        return self
