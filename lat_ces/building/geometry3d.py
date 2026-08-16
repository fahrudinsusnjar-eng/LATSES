"""Solver-neutral 3-D geometry derived from the canonical BuildingModel."""

from __future__ import annotations

from dataclasses import dataclass, field

from .model import BuildingModel, Level


@dataclass(frozen=True)
class MaterialLayer:
    """Physical layer attached to a 3-D building element."""

    material: str
    thickness: float

    def __post_init__(self) -> None:
        if not self.material.strip():
            raise ValueError("material must not be empty")
        if self.thickness <= 0:
            raise ValueError("material layer thickness must be positive")


@dataclass(frozen=True)
class ExtrudedWall:
    """A floor-plan wall extruded through its level height."""

    wall_id: str
    x1: float
    y1: float
    x2: float
    y2: float
    height: float
    thickness: float
    layers: tuple[MaterialLayer, ...] = field(default_factory=tuple)

    @property
    def length(self) -> float:
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        return (dx * dx + dy * dy) ** 0.5

    @property
    def gross_area(self) -> float:
        return self.length * self.height

    @property
    def volume(self) -> float:
        return self.length * self.thickness * self.height

    def __post_init__(self) -> None:
        if not self.wall_id:
            raise ValueError("wall_id must not be empty")
        if self.length <= 0 or self.height <= 0 or self.thickness <= 0:
            raise ValueError("wall dimensions must be positive")


@dataclass(frozen=True)
class LevelGeometry3D:
    """Deterministic 3-D geometry derived from one canonical Level."""

    level_id: str
    height: float
    walls: tuple[ExtrudedWall, ...]

    @property
    def wall_area(self) -> float:
        return sum(w.gross_area for w in self.walls)

    @property
    def wall_volume(self) -> float:
        return sum(w.volume for w in self.walls)


def build_level_geometry(level: Level, wall_thickness: float | None = None) -> LevelGeometry3D:
    """Extrude the existing FloorPlan; no second building model is created."""
    if level.height <= 0:
        raise ValueError("level height must be positive")
    plan = level.floor_plan
    if plan is None:
        return LevelGeometry3D(level.level_id, level.height, ())

    walls = tuple(
        ExtrudedWall(
            wall_id=wall.wall_id,
            x1=wall.segment.start.x,
            y1=wall.segment.start.y,
            x2=wall.segment.end.x,
            y2=wall.segment.end.y,
            height=level.height,
            thickness=wall.thickness if wall_thickness is None else wall_thickness,
        )
        for wall in plan.walls.values()
    )
    return LevelGeometry3D(level.level_id, level.height, walls)


def build_geometry(model: BuildingModel, wall_thickness: float | None = None) -> tuple[LevelGeometry3D, ...]:
    """Derive 3-D geometry for every level from the shared BuildingModel."""
    return tuple(build_level_geometry(level, wall_thickness) for level in model.levels.values())
