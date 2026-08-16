"""Read-only reader for cross-domain manufacturer product research data."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TechnicalProductRecord:
    record_id: str
    category: str
    manufacturer: str
    product: dict[str, Any]
    properties: tuple[dict[str, Any], ...]
    sources: tuple[dict[str, Any], ...]


class TechnicalCatalog:
    """Read-only catalog facade for engineering layers.

    This class intentionally exposes no persistence or mutation methods.
    Engineering modules may read and filter manufacturer-declared data, but
    project decisions remain outside this layer.
    """

    def __init__(self, index_path: str | Path, records_root: str | Path | None = None) -> None:
        self._index_path = Path(index_path)
        self._records_root = Path(records_root) if records_root else self._index_path.parent
        self._index = json.loads(self._index_path.read_text(encoding="utf-8"))
        if not self._index.get("research_boundary", {}).get("informational_only", False):
            raise ValueError("Technical catalog must be informational-only")

    @property
    def categories(self) -> tuple[str, ...]:
        return tuple(self._index.get("categories", ()))

    def list_records(self, category: str | None = None) -> tuple[TechnicalProductRecord, ...]:
        records: list[TechnicalProductRecord] = []
        for item in self._index.get("records", ()):
            if category and item.get("category") != category:
                continue
            path = self._records_root / str(item["path"])
            data = json.loads(path.read_text(encoding="utf-8"))
            records.append(self._record(data))
        return tuple(records)

    @staticmethod
    def _record(data: dict[str, Any]) -> TechnicalProductRecord:
        boundary = data.get("research_boundary", {})
        if (
            boundary.get("informational_only") is not True
            or boundary.get("engineering_decision_by_ai") is not False
            or boundary.get("normative_decision_by_ai") is not False
            or boundary.get("design_value_by_ai") is not False
        ):
            raise ValueError("Catalog record violates AI research boundary")
        return TechnicalProductRecord(
            record_id=str(data["record_id"]),
            category=str(data["category"]),
            manufacturer=str(data["manufacturer"]),
            product=dict(data["product"]),
            properties=tuple(dict(v) for v in data.get("properties", ())),
            sources=tuple(dict(v) for v in data.get("sources", ())),
        )
