"""JSON persistence for the canonical BuildingModel workflow."""
from __future__ import annotations

import json
from pathlib import Path

from .floor_plan import FloorPlan, Point2D, Segment2D, Wall
from .model import BuildingModel, Level
from .workflow import BuildingWorkflow


def _plan_to_dict(plan: FloorPlan) -> dict[str, object]:
    return {
        "name": plan.name,
        "plan_id": plan.plan_id,
        "walls": [
            {
                "name": wall.name,
                "wall_id": wall.wall_id,
                "thickness": wall.thickness,
                "start": {"x": wall.segment.start.x, "y": wall.segment.start.y},
                "end": {"x": wall.segment.end.x, "y": wall.segment.end.y},
                "openings": [
                    {
                        "kind": opening.kind,
                        "offset": opening.offset,
                        "width": opening.width,
                        "opening_id": opening.opening_id,
                    }
                    for opening in wall.openings
                ],
            }
            for wall in plan.walls.values()
        ],
    }


def _plan_from_dict(data: dict[str, object]) -> FloorPlan:
    plan = FloorPlan(name=str(data.get("name", "Etaža")))
    for item in data.get("walls", []):
        wall_data = dict(item)
        start = dict(wall_data["start"])
        end = dict(wall_data["end"])
        wall = Wall(
            name=str(wall_data.get("name", "Zid")),
            segment=Segment2D(
                Point2D(float(start["x"]), float(start["y"])),
                Point2D(float(end["x"]), float(end["y"])),
            ),
            thickness=float(wall_data.get("thickness", 0.20)),
        )
        for opening_data in wall_data.get("openings", []):
            from .floor_plan import Opening

            opening = Opening(
                kind=str(opening_data["kind"]),
                offset=float(opening_data["offset"]),
                width=float(opening_data["width"]),
            )
            wall.add_opening(opening)
        plan.add_wall(wall)
    return plan


def workflow_to_dict(workflow: BuildingWorkflow) -> dict[str, object]:
    return {
        "schema": "LAT-CES-BUILDING-1",
        "model": {
            "name": workflow.model.name,
            "model_id": workflow.model.model_id,
            "levels": [
                {
                    "name": level.name,
                    "level_id": level.level_id,
                    "elevation": level.elevation,
                    "height": level.height,
                    "floor_plan": _plan_to_dict(level.floor_plan) if level.floor_plan else None,
                }
                for level in workflow.model.levels.values()
            ],
        },
        "current_step": workflow.current_step,
        "active_level_id": workflow.active_level_id,
    }


def save_workflow(workflow: BuildingWorkflow, path: str | Path) -> Path:
    target = Path(path)
    target.write_text(json.dumps(workflow_to_dict(workflow), indent=2, ensure_ascii=False), encoding="utf-8")
    return target


def load_workflow(path: str | Path) -> BuildingWorkflow:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    model_data = dict(data["model"])
    model = BuildingModel(name=str(model_data.get("name", "Novi objekat")))
    workflow = BuildingWorkflow(model=model, current_step=int(data.get("current_step", 1)))
    for level_data in model_data.get("levels", []):
        item = dict(level_data)
        level = model.add_level(
            Level(
                name=str(item["name"]),
                elevation=float(item["elevation"]),
                height=float(item["height"]),
            )
        )
        if item.get("floor_plan"):
            level.set_floor_plan(_plan_from_dict(dict(item["floor_plan"])))
    active = data.get("active_level_id")
    if active and active in model.levels:
        workflow.active_level_id = str(active)
    elif model.levels:
        workflow.active_level_id = next(iter(model.levels))
    return workflow
