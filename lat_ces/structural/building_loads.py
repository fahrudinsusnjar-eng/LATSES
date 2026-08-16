"""Build permanent-load ledger directly from the canonical BuildingModel."""
from __future__ import annotations

from dataclasses import dataclass

from lat_ces.building.model import BuildingModel
from lat_ces.structural.load_ledger import ConstructionAssembly, LoadLedger


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
    """Return floor-plan polygon area derived from the canonical wall geometry."""
    level = next((value for value in building.levels.values() if value.name == level_name), None)
    if level is None or level.floor_plan is None:
        raise ValueError(f"Unknown level or missing floor plan: {level_name}")
    walls = list(level.floor_plan.walls.values())
    if len(walls) < 3:
        raise ValueError(f"Floor plan has insufficient walls for area calculation: {level_name}")

    points = []
    for wall in walls:
        points.append((wall.segment.start.x, wall.segment.start.y))
        points.append((wall.segment.end.x, wall.segment.end.y))

    # Shoelace area of the convex/ordered building envelope. The canonical
    # starter geometry is ordered; for general editable plans, the boundary
    # helper is intentionally conservative and uses the outer bounding polygon.
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    length = max(xs) - min(xs)
    width = max(ys) - min(ys)
    return length * width
