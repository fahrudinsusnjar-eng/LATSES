"""Canonical user-driven Building Model workflow."""
from __future__ import annotations

from dataclasses import dataclass

from .floor_plan import FloorPlan, Point2D, Segment2D, Wall
from .geometry3d import LevelGeometry3D, build_geometry
from .model import BuildingModel, Level
from .project_spec import BuildingProjectSpec, LevelProjectSpec


def make_blank_floor_plan(name: str) -> FloorPlan:
    return FloorPlan(name=name)


def make_envelope_floor_plan(name: str, length_m: float, width_m: float, thickness_m: float) -> FloorPlan:
    if length_m <= 0 or width_m <= 0 or thickness_m <= 0:
        raise ValueError("Dužina, širina i debljina zida moraju biti > 0")
    plan = FloorPlan(name=name)
    corners = (
        (0.0, 0.0, length_m, 0.0),
        (length_m, 0.0, length_m, width_m),
        (length_m, width_m, 0.0, width_m),
        (0.0, width_m, 0.0, 0.0),
    )
    for index, (x1, y1, x2, y2) in enumerate(corners, start=1):
        plan.add_wall(Wall(name=f"Vanjski zid {index}", segment=Segment2D(Point2D(x1, y1), Point2D(x2, y2)), thickness=thickness_m))
    return plan


@dataclass
class BuildingWorkflow:
    model: BuildingModel
    current_step: int = 1
    active_level_id: str | None = None
    project_spec: BuildingProjectSpec | None = None
    roof_shape: str = "Nije definisan"
    roof_height_m: float = 0.0

    def ensure_project_spec(self) -> BuildingProjectSpec:
        if self.project_spec is None:
            self.project_spec = BuildingProjectSpec(name=self.model.name)
        return self.project_spec

    def set_floor_plan(self, plan: FloorPlan) -> Level:
        if self.model.levels:
            level = self.model.levels[self.active_level_id or next(iter(self.model.levels))]
            level.set_floor_plan(plan)
        else:
            level = self.model.add_level(Level(name="Prizemlje", elevation=0.0, height=2.80, floor_plan=plan))
        self.active_level_id = level.level_id
        self.current_step = max(self.current_step, 1)
        return level

    def set_level_spec(self, index: int, spec: LevelProjectSpec) -> Level:
        project = self.ensure_project_spec()
        if index < 0 or index >= len(project.levels):
            raise IndexError("Nepoznata etaža")
        project.levels[index] = spec
        levels = list(self.model.levels.values())
        while len(levels) <= index:
            self.model.add_level(Level(name=f"Etaža {len(levels) + 1}", elevation=0.0, height=2.80, floor_plan=make_blank_floor_plan(f"Etaža {len(levels) + 1}")))
            levels = list(self.model.levels.values())
        level = levels[index]
        level.name = spec.name
        level.height = spec.height_m
        previous = levels[index - 1] if index else None
        level.elevation = previous.top_elevation if previous else 0.0
        level.set_floor_plan(
            make_envelope_floor_plan(spec.name, spec.length_m, spec.width_m, spec.construction.wall_thickness_m)
            if spec.length_m > 0 and spec.width_m > 0 and spec.construction.wall_thickness_m > 0
            else make_blank_floor_plan(spec.name)
        )
        self.active_level_id = level.level_id
        return level

    def set_floor_count(self, count: int) -> None:
        self.ensure_project_spec().set_floor_count(count)
        self.current_step = 2

    def advance_to_roof(self) -> None:
        project = self.ensure_project_spec()
        if not project.all_levels_finalized():
            raise ValueError("Sve etaže moraju biti popunjene i zaključane prije krova")
        project.floor_count_finalized = True
        self.current_step = 3

    def set_roof(self, shape: str, height_m: float = 0.0) -> None:
        if not shape.strip():
            raise ValueError("Oblik krova je obavezan")
        if height_m < 0:
            raise ValueError("Visina krova ne može biti negativna")
        self.roof_shape, self.roof_height_m = shape, height_m
        project = self.ensure_project_spec()
        project.roof_shape, project.roof_height_m = shape, height_m
        self.current_step = 3

    def advance_to_3d(self) -> tuple[LevelGeometry3D, ...]:
        self.advance_to_roof()
        geometries = build_geometry(self.model)
        self.current_step = 4
        return geometries

    def set_active_level(self, level_id: str) -> Level:
        if level_id not in self.model.levels:
            raise ValueError(f"Unknown level: {level_id}")
        self.active_level_id = level_id
        return self.model.levels[level_id]

    @property
    def active_level(self) -> Level:
        if self.active_level_id is None or self.active_level_id not in self.model.levels:
            raise ValueError("No active building level")
        return self.model.levels[self.active_level_id]

    @property
    def floor_plan(self) -> FloorPlan:
        plan = self.active_level.floor_plan
        if plan is None:
            raise ValueError("Active level has no floor plan")
        return plan

    def validate(self) -> list[str]:
        findings = self.model.validate()
        project = self.project_spec
        if project and project.floor_count and not project.all_levels_finalized() and project.floor_count_finalized:
            findings.append("Broj etaža je zaključan, ali nisu sve etaže završene")
        return findings

    def summary(self) -> dict[str, object]:
        return {
            "model": self.model.name,
            "levels": len(self.model.levels),
            "active_level": self.active_level.name if self.active_level_id else None,
            "floor_area_m2": self.model.floor_area,
            "volume_m3": self.model.volume,
            "rooms": self.model.room_count,
            "elements": self.model.element_count,
            "step": self.current_step,
            "roof": self.roof_shape,
        }
