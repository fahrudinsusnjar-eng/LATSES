from __future__ import annotations

from pathlib import Path

from lat_ces.building.floor_plan import Point2D, Segment2D, Wall
from lat_ces.building.project_io import load_workflow, save_workflow
from lat_ces.building.workflow import BuildingWorkflow, make_square_floor_plan
from lat_ces.building.model import BuildingModel


def test_default_plan_is_square_and_dimensional() -> None:
    plan = make_square_floor_plan("Prizemlje", 10.0)
    assert plan.wall_count == 4
    lengths = sorted(round(wall.segment.length, 6) for wall in plan.walls.values())
    assert lengths == [10.0, 10.0, 10.0, 10.0]


def test_level_plans_are_independent() -> None:
    workflow = BuildingWorkflow(model=BuildingModel(name="Test"))
    first = workflow.set_floor_plan(make_square_floor_plan("Prizemlje", 10.0))
    second = workflow.add_level("Sprat", 2.8)
    assert first.floor_plan is not second.floor_plan
    assert first.floor_plan is not None and second.floor_plan is not None

    second.floor_plan.walls.clear()
    second.floor_plan.add_wall(
        Wall("Drugi nivo zid", Segment2D(Point2D(0, 0), Point2D(6, 0)), 0.20)
    )
    assert first.floor_plan.wall_count == 4
    assert second.floor_plan.wall_count == 1


def test_save_and_load_preserves_level_layouts(tmp_path: Path) -> None:
    workflow = BuildingWorkflow(model=BuildingModel(name="Konfiguracija"))
    workflow.set_floor_plan(make_square_floor_plan("Prizemlje", 10.0))
    second = workflow.add_level("Sprat", 2.8)
    second.floor_plan.walls.clear()
    second.floor_plan.add_wall(
        Wall("Sprat pregrada", Segment2D(Point2D(0, 0), Point2D(5, 0)), 0.20)
    )

    target = tmp_path / "building.json"
    save_workflow(workflow, target)
    loaded = load_workflow(target)

    levels = list(loaded.model.levels.values())
    assert len(levels) == 2
    assert levels[0].floor_plan is not None and levels[1].floor_plan is not None
    assert levels[0].floor_plan.wall_count == 4
    assert levels[1].floor_plan.wall_count == 1
