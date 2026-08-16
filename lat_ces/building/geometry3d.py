"""Solver-neutral 3-D geometry primitives for the canonical BuildingModel.

BUILDING-003: geometry is derived from the shared floor-plan/level model and
contains no structural, thermal, fluid, acoustic, or electrical solver logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from lat_ces.building.model import BuildingModel, Level


@dataclass(frozen=True)
class MaterialLayer:
    """A physical layer attached to a building element."""

    material: str
    thickness_m: float

    def __post_init__(self) -> None:
        if not self.material.strip():
            raise ValueError("material must not be empty")
        if self.thickness_m <= 0:
            raise ValueError("material layer thickness must be positive")


@dataclass(frozen=True)
class ExtrudedWall:
    """A wall extruded through a level height."""

    wall_id: str
    x1_m: float
    y1_m: float
    x2_m: float
    y2_m: float
    height_m: float
    thickness_m: float
    layers: tuple[MaterialLayer, ...] = field(default_factory=tuple)

    @property
    def length_m(self) -> float:
        dx = self.x2_m - self.x1_m
        dy = self.y2_m - self.y1_m
        return (dx * dx + dy * dy) ** 0.5

    @property
    def volume_m3(self) -> float:
        return self.length_m * self.thickness_m * self.height_m

    @property
    def area_m2(self) -> float:
        return self.length_m * self.height_m

    def __post_init__(self) -> None:
        if not self.wall_id:
            raise ValueError("wall_id must not be empty")
        if self.length_m <= 0:
            raise ValueError("wall length must be positive")
        if self.height_m <= 0:
            raise ValueError("wall height must be positive")
        if self.thickness_m <= 0:
            raise ValueError("wall thickness must be positive")


@dataclass(frozen=True)
class LevelGeometry3D:
    """Deterministic 3-D representation derived from one Level."""

    level_id: str
    height_m: float
    walls: tuple[ExtrudedWall, ...]

    @property
    def wall_volume_m3(self) -> float:
        return sum(w.volume_m3 for w in self.walls)

    @property
    def wall_area_m2(self) -> float:
        return sum(w.area_m2 for w in self.walls)


def build_level_geometry(level: Level, wall_thickness_m: float = 0.20) -> LevelGeometry3D:
    """Derive solver-neutral 3-D wall geometry from an existing floor plan."""
    if level.height_m <= 0:
        raise ValueError("level height must be positive")
    floor_plan = level.floor_plan
    if floor_plan is None:
        return LevelGeometry3D(level.id, level.height_m, ())

    walls = tuple(
        ExtrudedWall(
            wall_id=wall.id,
            x1_m=wall.start.x_m,
            y1_m=wall.start.y_m,
            x2_m=wall.end.x_m,
            y2_m=wall.end.y_m,
            height_m=level.height_m,
            thickness_m=wall_thickness_m,
        )
        for wall in floor_plan.walls
    )
    return LevelGeometry3D(level.id, level.height_m, walls)


def build_geometry(model: BuildingModel, wall_thickness_m: float = 0.20) -> tuple[LevelGeometry3D, ...]:
    """Derive 3-D geometry for every level without creating a second model."""
    return tuple(build_level_geometry(level, wall_thickness_m) for level in model.levels)
