"""
LAT-CES Governance Core
Provenance Ledger Verification Tests (LAT-GOV-CORE-0012-TEST)
"""

import pytest

from lat_ces.gov.provenance import ProvenanceLedger


def test_ledger_record_and_retrieval():
    ledger = ProvenanceLedger(file_path="data/test_provenance_ledger.jsonl")
    ledger.clear_history()
    ledger.record("MODULE_INIT", {"status": "active"})

    records = ledger.get_history()
    assert len(records) == 1
    assert records[0]["event"] == "MODULE_INIT"
    assert records[0]["metrics"]["status"] == "active"
    ledger.clear_history()


def test_ledger_returns_mutable_list():
    ledger = ProvenanceLedger(file_path="data/test_provenance_ledger.jsonl")
    ledger.clear_history()
    ledger.record("EVENT_1", {})
    records = ledger.get_history()
    records.append({"event": "MALICIOUS_INJECTION"})
    assert len(records) == 2
    ledger.clear_history()
