"""Canonical Scientific Provenance contract with a legacy-ledger adapter.

The adapter preserves the existing JSONL storage format while giving Scientific
Models one stable provenance API. It intentionally does not delete or rewrite
legacy history.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from lat_ces.gov.provenance import ProvenanceLedger


@dataclass(frozen=True)
class ProvenanceRecord:
    event: str
    metrics: Mapping[str, Any]
    timestamp: str
    source: Optional[str] = None
    model_id: Optional[str] = None
    revision: Optional[str] = None


class ScientificProvenance:
    """Canonical provenance facade used by Scientific Model implementations."""

    def __init__(self, file_path: str = "data/provenance_ledger.jsonl") -> None:
        self._ledger = ProvenanceLedger(file_path)

    @property
    def ledger(self) -> ProvenanceLedger:
        return self._ledger

    def record(
        self,
        event: str,
        metrics: Mapping[str, Any],
        *,
        source: Optional[str] = None,
        model_id: Optional[str] = None,
        revision: Optional[str] = None,
    ) -> ProvenanceRecord:
        record = ProvenanceRecord(
            event=event,
            metrics=dict(metrics),
            timestamp=datetime.now(timezone.utc).isoformat(),
            source=source,
            model_id=model_id,
            revision=revision,
        )
        self._ledger.record(event, asdict(record))
        return record

    def history(self) -> list[dict[str, Any]]:
        return self._ledger.get_history()


__all__ = ["ProvenanceRecord", "ScientificProvenance"]
