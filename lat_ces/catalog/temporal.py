"""Temporal manufacturer-product facts and independent verification.

AI only records manufacturer-declared observations. A separate verification
loop decides whether a fact is current, stale, superseded, or rejected.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class FactState(str, Enum):
    CURRENT = "current"
    STALE = "stale"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"
    UNVERIFIED = "unverified"


@dataclass(frozen=True)
class ProductIdentity:
    product_id: str
    manufacturer: str
    product_family: str
    model_code: str


@dataclass(frozen=True)
class TechnicalFact:
    fact_id: str
    product_id: str
    property_name: str
    value: object
    unit: str
    source_url: str
    source_document: str
    observed_at: datetime
    valid_from: datetime
    valid_until: datetime | None = None
    state: FactState = FactState.UNVERIFIED
    supersedes_fact_id: str | None = None


@dataclass(frozen=True)
class VerificationRecord:
    verification_id: str
    fact_id: str
    checked_at: datetime
    verifier: str
    source_url: str
    result: str
    notes: str = ""


@dataclass(frozen=True)
class OfferEligibility:
    product_id: str
    eligible: bool
    checked_at: datetime
    current_fact_ids: tuple[str, ...]
    reasons: tuple[str, ...] = ()


def current_facts(facts: tuple[TechnicalFact, ...], at: datetime) -> tuple[TechnicalFact, ...]:
    return tuple(
        fact for fact in facts
        if fact.valid_from <= at
        and (fact.valid_until is None or at < fact.valid_until)
        and fact.state == FactState.CURRENT
    )


def evaluate_offer(
    identity: ProductIdentity,
    facts: tuple[TechnicalFact, ...],
    verifications: tuple[VerificationRecord, ...],
    at: datetime,
    required_properties: tuple[str, ...],
) -> OfferEligibility:
    current = current_facts(facts, at)
    current_ids = {fact.fact_id for fact in current}
    verified_ids = {record.fact_id for record in verifications if record.result == "confirmed" and record.checked_at <= at}
    missing = tuple(
        prop for prop in required_properties
        if not any(f.property_name == prop and f.fact_id in verified_ids for f in current)
    )
    reasons = tuple(f"Nedostaje nezavisno potvrđen podatak: {prop}" for prop in missing)
    return OfferEligibility(
        product_id=identity.product_id,
        eligible=not missing,
        checked_at=at,
        current_fact_ids=tuple(sorted(current_ids)),
        reasons=reasons,
    )
