"""Independent verification-loop boundary for manufacturer product facts.

The research collector and verifier are intentionally separate actors. The
collector supplies observations; the verifier decides whether an observation
is currently confirmed. This module contains no engineering design logic.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .temporal import TechnicalFact, VerificationRecord


@dataclass(frozen=True)
class VerificationCheck:
    fact_id: str
    checked_at: datetime
    verifier_id: str
    manufacturer_source_url: str
    result: str
    notes: str = ""

    def to_record(self) -> VerificationRecord:
        return VerificationRecord(
            verification_id=f"{self.verifier_id}:{self.fact_id}:{self.checked_at.isoformat()}",
            fact_id=self.fact_id,
            checked_at=self.checked_at,
            verifier=self.verifier_id,
            source_url=self.manufacturer_source_url,
            result=self.result,
            notes=self.notes,
        )


def requires_recheck(fact: TechnicalFact, now: datetime, max_age_days: int) -> bool:
    age_days = (now - fact.observed_at).days
    return age_days >= max_age_days or fact.valid_until is not None and now >= fact.valid_until
