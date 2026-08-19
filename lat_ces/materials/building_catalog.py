"""Parameterized Building Material / Element Catalog.

This is deliberately separate from the manufacturer-information catalog in
``data/material_catalog``. Entries describe construction families and data
requirements; commercial dimensions and normative design values are not
invented here.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class BuildingCatalogItem:
    item_id: str
    name: str
    unit: str
    requires_dimensions: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BuildingCatalogItem":
        return cls(
            item_id=str(data["id"]),
            name=str(data["name"]),
            unit=str(data["unit"]),
            requires_dimensions=bool(data.get("requires_dimensions", False)),
        )


@dataclass(frozen=True)
class GlazingOption:
    option_id: str
    panes: int
    gas_fill: str | None
    low_e: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GlazingOption":
        return cls(
            option_id=str(data["id"]),
            panes=int(data["panes"]),
            gas_fill=data.get("gas_fill"),
            low_e=bool(data.get("low_e", False)),
        )


class BuildingMaterialCatalog:
    """Read-only parameterized catalog for GUI/model selection."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        self.catalog_id = str(payload["catalog_id"])
        self.catalog_version = str(payload["catalog_version"])
        self._items = tuple(BuildingCatalogItem.from_dict(item) for item in payload.get("categories", ()))
        self._glazing = tuple(GlazingOption.from_dict(item) for item in payload.get("glazing_options", ()))

    @classmethod
    def default(cls) -> "BuildingMaterialCatalog":
        return cls(Path(__file__).resolve().parents[2] / "data" / "building_materials.catalog.json")

    @property
    def items(self) -> tuple[BuildingCatalogItem, ...]:
        return self._items

    @property
    def glazing_options(self) -> tuple[GlazingOption, ...]:
        return self._glazing

    def search(self, text: str) -> tuple[BuildingCatalogItem, ...]:
        needle = text.casefold().strip()
        if not needle:
            return self.items
        return tuple(item for item in self.items if needle in item.item_id.casefold() or needle in item.name.casefold())

    def by_id(self, item_id: str) -> BuildingCatalogItem:
        for item in self.items:
            if item.item_id == item_id:
                return item
        raise KeyError(item_id)

    def __iter__(self) -> Iterable[BuildingCatalogItem]:
        return iter(self.items)


__all__ = ["BuildingCatalogItem", "BuildingMaterialCatalog", "GlazingOption"]
