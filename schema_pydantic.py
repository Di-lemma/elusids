from __future__ import annotations

from enum import Enum
from typing import Annotated, List, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


# ---------- Common constrained scalars ----------
Percentage = Annotated[float, Field(ge=0, le=100, description="0–100 percentage")]
NonNegativeNumber = Annotated[float, Field(ge=0, description="Non-negative number")]

# Optional: permissive ISO-8601 duration pattern for strings like 'PT2H', 'P3D', etc.
ISO_DURATION_PATTERN = r"^P(?=.*[T\d])(?:\d+Y)?(?:\d+M)?(?:\d+D)?(?:T(?:\d+H)?(?:\d+M)?(?:\d+S)?)?$"


# ---------- Enums ----------
class DurationUnits(str, Enum):
    hours = "hours"
    minutes = "minutes"
    days = "days"


class ToleranceTimelineUnits(str, Enum):
    hours = "hours"
    days = "days"
    weeks = "weeks"


class ToleranceConfidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    very_low = "very-low"


class ToleranceConfidenceWithUnknown(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    very_low = "very-low"
    unknown = "unknown"


class ToleranceRelationship(str, Enum):
    established = "established"
    likely = "likely"
    possible = "possible"
    theoretical = "theoretical"
    unclear = "unclear"


class ToleranceDataQuality(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    anecdotal = "anecdotal"
    theoretical = "theoretical"
    unknown = "unknown"


class QualitativeTimeLabel(str, Enum):
    minutes = "minutes"
    hours = "hours"
    one_to_two_days = "1-2 days"
    several_days = "several days"
    one_to_two_weeks = "1-2 weeks"
    weeks = "weeks"
    months = "months"
    variable = "variable"
    unknown = "unknown"


class QualitativeTimeUnits(str, Enum):
    hours = "hours"
    days = "days"
    weeks = "weeks"
    months = "months"


class CategoryEnum(str, Enum):
    psychedelic = "psychedelic"
    gabapentinoid = "gabapentinoid"
    antipsychotic = "antipsychotic"
    medical_off_label = "medical|off-label"
    cannabinoid = "cannabinoid"
    cardiotoxic = "cardiotoxic"
    hepatotoxic = "hepatotoxic"
    ototoxic = "ototoxic"
    neurotoxic = "neurotoxic"
    carcinogenic = "carcinogenic"
    toxic_unspecified = "toxic|unspecified"
    irreversible_damage = "irreversible-damage"
    dissociative = "dissociative"
    stimulant = "stimulant"
    research_chemical = "research-chemical"
    empathogen = "empathogen"
    habit_forming = "habit-forming"
    opioid = "opioid"
    depressant = "depressant"
    hallucinogen = "hallucinogen"
    entactogen = "entactogen"
    deliriant = "deliriant"
    antidepressant = "antidepressant"
    sedative = "sedative"
    nootropic = "nootropic"
    barbiturate = "barbiturate"
    benzodiazepine = "benzodiazepine"
    supplement = "supplement"
    stimulant_sedative = "stimulant-sedative"
    anorectic = "anorectic"
    antiepileptic = "antiepileptic"
    antihistamine = "antihistamine"


# ---------- $defs ----------
class DurationRange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    min: float = Field(description="Minimum duration value")
    max: float = Field(description="Maximum duration value")
    iso: List[Annotated[str, Field(pattern=ISO_DURATION_PATTERN)]] = Field(
        description="ISO 8601 duration format representations"
    )
    note: str = Field(description="Additional notes about the duration")


class DurationPhase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start: float = Field(description="Start time of this phase")
    end: float = Field(description="End time of this phase")
    iso_start: List[Annotated[str, Field(pattern=ISO_DURATION_PATTERN)]] = Field(
        description="ISO 8601 duration format for start time"
    )
    iso_end: List[Annotated[str, Field(pattern=ISO_DURATION_PATTERN)]] = Field(
        description="ISO 8601 duration format for end time"
    )


class DurationCurveData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reference: str = Field(description="Citation or reference for the duration data")
    units: DurationUnits = Field(description="Time units used (e.g., hours, minutes)")
    total_duration: DurationRange
    onset: DurationPhase
    peak: DurationPhase
    offset: DurationPhase
    after_effects: DurationPhase


class DurationCurveEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    method: str = Field(
        description="Route of administration (e.g., oral, IV, insufflated, smoked)"
    )
    duration_curve: DurationCurveData


class DoseRanges(BaseModel):
    model_config = ConfigDict(extra="forbid")

    threshold: str = Field(description="Threshold dose.")
    light: str = Field(description="Light dose.")
    common: str = Field(description="Common dose.")
    strong: str = Field(description="Strong dose.")
    heavy: str = Field(description="Heavy dose.")


class RouteOfAdministration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    route: Annotated[
        str,
        Field(
            # JSON schema said single word or abbreviation only.
            # This allows letters and common abbreviation punctuation.
            pattern=r"^[A-Za-z][A-Za-z0-9/-]*$",
            description="The route of administration. SINGLE WORD OR ABBREVIATION ONLY (e.g., oral, smoked, IV, insufflated).",
        ),
    ]
    units: str = Field(description="Units of measurement (e.g., mg, µg, ml).")
    notes: str = Field(
        description=(
            "Commentary on the provenance of the information, including any relevant details "
            "about the source or context. Explicit mentions of the source are not required, "
            "but the information should be verifiable. If the information is mostly derived "
            "from user reports, it should ALWAYS be noted as such."
        )
    )
    dose_ranges: DoseRanges


class Dosages(BaseModel):
    model_config = ConfigDict(extra="forbid")

    routes_of_administration: List[RouteOfAdministration] = Field(
        description="Dosages information for different routes of administration."
    )


class DurationSummary(BaseModel):
    """String-based duration summary ($defs.duration in the schema)."""

    model_config = ConfigDict(extra="forbid")

    total_duration: str = Field(description="Total duration of effects.")
    onset: str = Field(description="Onset time of effects.")
    peak: str = Field(description="Peak time of effects.")
    offset: str = Field(description="Offset time of effects.")
    after_effects: str = Field(description="Duration of after-effects.")


class Interactions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dangerous: List[str] = Field(description="Dangerous drug interactions.")
    unsafe: List[str] = Field(description="Unsafe drug interactions.")
    caution: List[str] = Field(description="Interactions that require caution.")


class Citation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="The name or title of the citation.")
    reference: str = Field(description="The URL or other reference of the citation.")


class QualitativeTimeEstimate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: QualitativeTimeLabel
    min_value: Optional[float]
    max_value: Optional[float]
    units: Optional[QualitativeTimeUnits]
    confidence: ToleranceConfidenceWithUnknown
    notes: str


class ToleranceTimelineEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    time: float
    units: ToleranceTimelineUnits
    relative_tolerance: Percentage = Field(
        description="Relative tolerance as a percentage from 0 to 100"
    )
    confidence: ToleranceConfidence
    notes: str


class ToleranceBaselines(BaseModel):
    model_config = ConfigDict(extra="forbid")

    onset_of_tolerance: QualitativeTimeEstimate
    partial_reset: QualitativeTimeEstimate
    near_baseline: QualitativeTimeEstimate


class CrossToleranceEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    substance: str
    relationship: ToleranceRelationship
    confidence: ToleranceConfidence
    notes: str


class ToleranceData(BaseModel):
    """Complex tolerance object used by the root schema."""

    model_config = ConfigDict(extra="forbid")

    timeline: List[ToleranceTimelineEntry]
    baselines: ToleranceBaselines
    cross_tolerances: List[CrossToleranceEntry]
    notes: str
    data_quality: ToleranceDataQuality


# ---------- Root model ----------
class DrugInfo(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    drug_name: str = Field(
        description=(
            "The primary name of the substance as commonly recognized across various "
            "sources, including scientific literature, user reports, and drug databases."
        )
    )
    alternative_names: List[str] = Field(
        description=(
            "A comprehensive list of alternative names for the substance, including street "
            "names, colloquialisms, chemical nomenclature variants, abbreviations, and "
            "regional terminology. This aggregation synthesizes nomenclature from diverse "
            "sources including user communities, research literature, clinical contexts, and "
            "underground markets. Includes systematic IUPAC names, common abbreviations "
            "(e.g., MDMA, LSD), brand names, research chemical designations "
            "(e.g., '5-MeO-DMT'), and vernacular terms. Sources may include trip reports, "
            "forum discussions, published literature, and drug checking services."
        )
    )
    search_url: Annotated[
        HttpUrl,
        Field(pattern=r"^(?!.*psychonautwiki\.org).*"),
    ] = Field(
        description=(
            "URL linking to a comprehensive repository of detailed information about the "
            "substance, synthesized from diverse sources including research articles, "
            "clinical studies, and user experiences. Must NOT be PsychonautWiki.org URL."
        )
    )
    chemical_class: str = Field(
        description=(
            "The chemical class of the substance, identified based on structural and "
            "functional similarities with other compounds, as aggregated from chemical "
            "databases and research studies."
        )
    )
    psychoactive_class: str = Field(
        description=(
            "The psychoactive class of the substance, reflecting its effects on the central "
            "nervous system, derived from user reports, pharmacological studies, and expert "
            "consensus."
        )
    )

    dosages: Dosages
    duration: DurationSummary
    duration_curves: List[DurationCurveEntry] = Field(
        description="ROA-specific duration curve data for plotting drug effect timelines"
    )

    addiction_potential: str = Field(
        description=(
            "A description of the substance's addiction potential, synthesized from "
            "epidemiological studies, case reports, and user accounts, reflecting a "
            "consensus on the risk of dependency."
        )
    )
    interactions: Interactions

    notes: str = Field(
        description=(
            "Additional notes or warnings about the substance, synthesizing a wide range of "
            "data points from user experiences, clinical observations, and expert "
            "guidelines. Must have at least 3 sentences (minimum), but ideally should be "
            "5-20 sentences long. Every sentence should carry a concisely stated pertinent "
            "fact about the substance that is vital for harm reduction in recreational use."
        )
    )
    subjective_effects: List[str] = Field(
        description=(
            "List of subjective effects commonly associated with the substance, aggregated "
            "from user reports, clinical studies, and psychopharmacological research, "
            "representing typical experiences and outliers."
        )
    )

    tolerance: ToleranceData

    half_life: str = Field(
        description=(
            "Half-life of the substance, reflecting the average time for the concentration "
            "of the substance to decrease by half in the body, as reported in "
            "pharmacokinetic studies."
        )
    )

    citations: List[Citation] = Field(
        description=(
            "List of citations supporting the information provided, including names and "
            "references, aggregated from scientific literature, user reports, and other "
            "reputable sources."
        )
    )
    categories: List[CategoryEnum] = Field(
        description="List of categories the drug belongs to."
    )

    # ----- Validators -----
    @field_validator("search_url")
    @classmethod
    def _no_psychonautwiki(cls, v: HttpUrl) -> HttpUrl:
        host = getattr(v, "host", "")
        if host and "psychonautwiki.org" in host.lower():
            raise ValueError("search_url must not be a PsychonautWiki.org URL")
        if "psychonautwiki.org" in str(v).lower():
            raise ValueError("search_url must not be a PsychonautWiki.org URL")
        return v

    @field_validator("notes")
    @classmethod
    def _notes_min_sentences(cls, v: str) -> str:
        import re

        sentences = [s for s in re.split(r"[.!?]+", v) if s.strip()]
        if len(sentences) < 3:
            raise ValueError("notes must contain at least 3 sentences")
        return v


# ---------- Helper: emit OpenAI Structured Outputs schema ----------
def to_openai_structured_output() -> dict:
    """
    Build the exact response_format payload for OpenAI Structured Outputs.

    Returns:
        {
          "type": "json_schema",
          "json_schema": {
             "name": "drug_info",
             "strict": True,
             "schema": <DrugInfo JSON Schema Draft 2020-12>
          }
        }
    """
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "drug_info",
            "strict": True,
            "schema": DrugInfo.model_json_schema(),
        },
    }
