"""Canonical user-driven Building Model workflow.

The workflow is intentionally ordered: floor plan -> levels/heights -> openings -> 3-D.
All steps mutate one shared :class:`BuildingModel`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .floor_plan import FloorPlan
from .geometry3d import LevelGeometry3D, build_geometry
from .model import BuildingModel, Level


@dataclass
class BuildingWorkflow:
    """State machine for the first four Building Model project steps."""

    model: BuildingModel
    current_step: int = 1
    active_level_id: str | None = None

    def set_floor_plan(self, plan: FloorPlan) -> Level:
        if self.model.levels:
            level = self.model.levels[self.active_level_id or next(iter(self.model.levels))]
            level.set_floor_plan(plan)
        else:
            level = self.model.add_level(
                Level(name="Prizemlje", elevation=0.0, height=2.80, floor_plan=plan)
            )
        self.active_level_id = level.level_id
        self.current_step = max(self.current_step, 1)
        return level

    def add_level(self, name: str, height: float) -> Level:
        if self.model.levels:
            previous = list(self.model.levels.values())[-1]
            elevation = previous.top_elevation
        else:
            elevation = 0.0
        level = self.model.add_level(Level(name=name, elevation=elevation, height=height))
        self.active_level_id = level.level_id
        self.current_step = max(self.current_step, 2)
        return level

    def set_active_level_height(self, height: float) -> Level:
        level = self.active_level
        level.height = float(height)
        if level.height <= 0:
            raise ValueError("Level height must be > 0")
        self.current_step = max(self.current_step, 2)
        return level

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

    def advance_to_openings(self) -> None:
        if self.active_level.floor_plan is None:
            raise ValueError("Floor plan is required before openings")
        self.current_step = max(self.current_step, 3)

    def advance_to_3d(self) -> tuple[LevelGeometry3D, ...]:
        self.advance_to_openings()
        geometries = build_geometry(self.model)
        self.current_step = 4
        return geometries

    def validate(self) -> list[str]:
        findings = self.model.validate()
        if not self.model.levels:
            findings.append("At least one building level is required")
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
        }
