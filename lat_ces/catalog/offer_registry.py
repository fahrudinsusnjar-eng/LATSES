"""Current product-offer projection from the temporal fact history.

The offer registry is a projection, not an authority: only facts that are
current and independently confirmed are eligible for display as product
options to engineering workflows.
"""
from __future__ import annotations

from datetime import datetime

from .temporal import (
    OfferEligibility,
    ProductIdentity,
    TechnicalFact,
    VerificationRecord,
    evaluate_offer,
)


def eligible_offer(
    identity: ProductIdentity,
    facts: tuple[TechnicalFact, ...],
    verifications: tuple[VerificationRecord, ...],
    at: datetime,
    required_properties: tuple[str, ...],
) -> OfferEligibility:
    return evaluate_offer(identity, facts, verifications, at, required_properties)
