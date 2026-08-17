"""Location and independently verified environmental inputs for engineering models."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class VerificationState(str, Enum):
    MISSING = "missing"
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    STALE = "stale"
    REJECTED = "rejected"


@dataclass(frozen=True)
class EnvironmentalFact:
    key: str
    value: float
    unit: str
    source_url: str
    source_name: str
    observation_date: str
    retrieval_date: str
    verification_state: VerificationState = VerificationState.UNVERIFIED
    verifier: str = ""
    verification_date: str = ""
    verification_source_url: str = ""

    def is_usable(self) -> bool:
        return self.verification_state == VerificationState.VERIFIED


@dataclass
class SiteEnvironment:
    latitude_deg: float
    longitude_deg: float
    elevation_m: float | None = None
    country: str = ""
    municipality: str = ""
    cadastral_reference: str = ""
    facts: list[EnvironmentalFact] = field(default_factory=list)

    def add_fact(self, fact: EnvironmentalFact) -> None:
        self.facts.append(fact)

    def require_verified(self, key: str) -> EnvironmentalFact:
        matches = [fact for fact in self.facts if fact.key == key]
        for fact in reversed(matches):
            if fact.is_usable():
                return fact
        raise ValueError(f"No independently verified environmental fact available: {key}")


CLIMATIC_ACTION_KEYS = (
    "snow_ground_characteristic",
    "wind_basic_velocity",
    "wind_basic_pressure",
    "extreme_precipitation",
    "design_air_temperature",
)


@dataclass
class SiteVerificationGate:
    required_keys: tuple[str, ...] = CLIMATIC_ACTION_KEYS

    def ready_for_climatic_structural_analysis(self, site: SiteEnvironment) -> bool:
        try:
            for key in self.required_keys:
                site.require_verified(key)
        except ValueError:
            return False
        return True
