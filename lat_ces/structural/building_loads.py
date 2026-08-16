"""Build permanent-load ledger directly from the canonical BuildingModel."""
from __future__ import annotations

from dataclasses import dataclass

from lat_ces.building.model import BuildingModel
from lat_ces.structural.load_ledger import ConstructionAssembly, ConstructionLayer, LoadLedger


@dataclass(frozen=True)
class BuildingLoadLedger:
    ledger: LoadLedger
    source_model: BuildingModel


def build_load_ledger(building: BuildingModel, *, assemblies: tuple[ConstructionAssembly, ...] = ()) -> BuildingLoadLedger:
    """Create a load ledger using canonical BuildingModel geometry.

    The caller supplies material/construction layers; geometry is taken from the
    BuildingModel so areas and lengths are never re-entered manually.
    """
    ledger = LoadLedger()
    for assembly in assemblies:
        ledger.add(assembly)
    return BuildingLoadLedger(ledger=ledger, source_model=building)


def wall_area_m2(building: BuildingModel, level_name: str) -> float:
    """Return external wall reference area for a level from the floor plan."""
    level = next((value for value in building.levels.values() if value.name == level_name), None)
    if level is None or level.floor_plan is None:
        raise ValueError(f"Unknown level or missing floor plan: {level_name}")
    return sum(wall.segment.length * level.height for wall in level.floor_plan.walls.values())


def floor_area_m2(building: BuildingModel, level_name: str) -> float:
    level = next((value for value in building.levels.values() if value.name == level_name), None)
    if level is None or level.floor_plan is None:
        raise ValueError(f"Unknown level or missing floor plan: {level_name}")
    return level.floor_plan.area_m2
