import pytest

from lat_ces.evidence.historical import EvidenceRecord, EvidenceState, HistoricalEvidenceLedger


def _record(evidence_id: str, supersedes: str | None = None) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id=evidence_id,
        location="Bihac",
        period_start="1980",
        period_end="2020",
        object_type="stambeni objekat",
        system_type="zid",
        material_or_system="keramicki blok",
        source="historijski elaborat",
        recorded_at="2026-08-16",
        state=EvidenceState.HISTORICAL,
        supersedes=supersedes,
    )


def test_history_is_append_only_and_preserved():
    ledger = HistoricalEvidenceLedger()
    ledger.append(_record("E-001"))
    ledger.append(_record("E-002", supersedes="E-001"))

    assert [item.evidence_id for item in ledger.records] == ["E-001", "E-002"]
    assert [item.evidence_id for item in ledger.history("E-002")] == ["E-002", "E-001"]


def test_duplicate_evidence_id_is_rejected_instead_of_overwriting():
    ledger = HistoricalEvidenceLedger()
    ledger.append(_record("E-001"))
    with pytest.raises(ValueError, match="already exists"):
        ledger.append(_record("E-001"))
