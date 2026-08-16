"""Read-only reader for manufacturer-declared material information.

This module intentionally contains no write API. It exposes informational
manufacturer data to engineering layers without making normative or design
choices.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class MaterialRecord:
    """Immutable manufacturer-declared material record."""

    material_id: str
    name: str
    manufacturer: str
    product_url: str
    technical_data: dict[str, Any]
    source_documents: tuple[str, ...]
    informational_only: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MaterialRecord":
        return cls(
            material_id=str(data["material_id"]),
            name=str(data["name"]),
            manufacturer=str(data["manufacturer"]),
            product_url=str(data.get("product_url", "")),
            technical_data=dict(data.get("technical_data", {})),
            source_documents=tuple(data.get("source_documents", ())),
            informational_only=bool(data.get("informational_only", True)),
        )


class MaterialCatalog:
    """Read-only catalog facade for downstream engineering layers."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.records_path = self.root / "materials"

    def records(self) -> tuple[MaterialRecord, ...]:
        if not self.records_path.exists():
            return ()
        result: list[MaterialRecord] = []
        for path in sorted(self.records_path.glob("*.json")):
            if path.name.startswith("_"):
                continue
            result.append(MaterialRecord.from_dict(json.loads(path.read_text(encoding="utf-8"))))
        return tuple(result)

    def by_id(self, material_id: str) -> MaterialRecord:
        for record in self.records():
            if record.material_id == material_id:
                return record
        raise KeyError(material_id)

    def search(self, text: str) -> tuple[MaterialRecord, ...]:
        needle = text.casefold().strip()
        if not needle:
            return self.records()
        return tuple(
            record
            for record in self.records()
            if needle in record.material_id.casefold()
            or needle in record.name.casefold()
            or needle in record.manufacturer.casefold()
        )

    def __iter__(self) -> Iterable[MaterialRecord]:
        return iter(self.records())
