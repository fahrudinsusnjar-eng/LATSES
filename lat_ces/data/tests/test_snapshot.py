"""
LAT-CES Storage Core
Ledger Snapshot & Recovery Engine Verification Tests (LAT-DATA-CORE-0012-TEST)
"""

import pytest

from lat_ces.data.snapshot import LedgerSnapshotEngine, SnapshotError


def test_snapshot_creation_and_recovery():
    engine = LedgerSnapshotEngine()
    ledger_history = [{"sequence_id": 1, "event": "INIT"}, {"sequence_id": 2, "event": "RUN"}]

    snapshot_id = engine.create_snapshot(ledger_history)
    assert snapshot_id is not None

    recovered = engine.recover_snapshot(snapshot_id)
    assert len(recovered) == 2
    assert recovered[1]["event"] == "RUN"
