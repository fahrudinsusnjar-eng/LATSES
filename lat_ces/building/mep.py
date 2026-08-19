"""Runtime MEP registry attached to the canonical GUI BuildingModel.

The registry keeps MEP objects out of GUI widgets and makes them explicit
BuildingModel-owned data. Phase 1 exposes ventilation openings; water and
heating collections are reserved for the next editor slices.
"""
from __future__ import annotations

from dataclasses import replace
from typing import Dict, TypeVar

from lat_ces.building_model.systems import HeatingZone, VentilationOpening, WaterBranch

T = TypeVar("T", VentilationOpening, WaterBranch, HeatingZone)


class MEPRegistry:
    """Mutable registry owned by one BuildingModel instance."""

    def __init__(self) -> None:
        self.ventilation_openings: Dict[str, VentilationOpening] = {}
        self.water_branches: Dict[str, WaterBranch] = {}
        self.heating_zones: Dict[str, HeatingZone] = {}

    @property
    def all_ventilation_openings(self) -> tuple[VentilationOpening, ...]:
        return tuple(self.ventilation_openings.values())

    def add_ventilation_opening(self, opening: VentilationOpening) -> VentilationOpening:
        if opening.id in self.ventilation_openings:
            raise ValueError(f"Duplicate ventilation opening id: {opening.id}")
        self.ventilation_openings[opening.id] = opening
        return opening

    def update_ventilation_opening(self, opening_id: str, **changes: object) -> VentilationOpening:
        current = self.ventilation_openings[opening_id]
        updated = replace(current, **changes)
        self.ventilation_openings[opening_id] = updated
        return updated

    def remove_ventilation_opening(self, opening_id: str) -> VentilationOpening:
        return self.ventilation_openings.pop(opening_id)


def ensure_mep_registry(model: object) -> MEPRegistry:
    """Attach and return exactly one MEP registry for a BuildingModel instance."""
    registry = getattr(model, "mep", None)
    if registry is None:
        registry = MEPRegistry()
        setattr(model, "mep", registry)
    if not isinstance(registry, MEPRegistry):
        raise TypeError("BuildingModel.mep must be an MEPRegistry")
    return registry
