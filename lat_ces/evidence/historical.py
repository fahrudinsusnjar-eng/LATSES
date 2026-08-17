"""Append-only historical evidence and local experience layer.

This layer records evidence; it does not select or approve engineering solutions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EvidenceState(str, Enum):
    CONFIRMED = "confirmed"
    PARTIALLY_CONFIRMED = "partially_confirmed"
    HISTORICAL = "historical"
    UNCERTAIN = "uncertain"
    REJECTED = "rejected"


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    location: str
    period_start: str
    period_end: str
    object_type: str
    system_type: str
    material_or_system: str
    source: str
    recorded_at: str
    state: EvidenceState = EvidenceState.HISTORICAL
    age_years: float | None = None
    documented_repairs: int | None = None
    observations: str = ""
    verification_source: str = ""
    supersedes: str | None = None


@dataclass
class HistoricalEvidenceLedger:
    """Append-only ledger. Existing records are never overwritten or deleted."""

    records: list[EvidenceRecord] = field(default_factory=list)

    def append(self, record: EvidenceRecord) -> None:
        if any(item.evidence_id == record.evidence_id for item in self.records):
            raise ValueError(f"Evidence id already exists: {record.evidence_id}")
        self.records.append(record)

    def compare(self, *, location: str, system_type: str) -> tuple[EvidenceRecord, ...]:
        return tuple(
            record
            for record in self.records
            if record.location == location and record.system_type == system_type
            and record.state != EvidenceState.REJECTED
        )

    def history(self, evidence_id: str) -> tuple[EvidenceRecord, ...]:
        chain: list[EvidenceRecord] = []
        current = next((item for item in self.records if item.evidence_id == evidence_id), None)
        if current is None:
            raise KeyError(evidence_id)
        while current is not None:
            chain.append(current)
            previous_id = current.supersedes
            current = next((item for item in self.records if item.evidence_id == previous_id), None) if previous_id else None
        return tuple(chain)
