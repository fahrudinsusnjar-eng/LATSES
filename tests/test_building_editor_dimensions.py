from pathlib import Path

from lat_ces.building.floor_plan import FloorPlan, Opening, Point2D, Segment2D, Wall
from lat_ces.building.model import BuildingModel, Level
from lat_ces.building.project_io import load_workflow, save_workflow
from lat_ces.building.workflow import BuildingWorkflow


def test_opening_has_explicit_height() -> None:
    opening = Opening(kind="window", offset=1.0, width=1.2, height_m=1.4)
    assert opening.width == 1.2
    assert opening.height_m == 1.4


def test_opening_height_round_trips_through_workflow_json(tmp_path: Path) -> None:
    plan = FloorPlan("Prizemlje")
    wall = Wall("Vanjski zid", Segment2D(Point2D(0, 0), Point2D(10, 0)))
    wall.add_opening(Opening(kind="door", offset=2.0, width=0.9, height_m=2.1))
    plan.add_wall(wall)

    model = BuildingModel("Test objekat")
    level = Level("Prizemlje", elevation=0.0, height=2.8, length_m=10.0, width_m=10.0, floor_plan=plan)
    model.add_level(level)
    workflow = BuildingWorkflow(model=model, active_level_id=level.level_id)

    path = tmp_path / "building.json"
    save_workflow(workflow, path)
    loaded = load_workflow(path)
    loaded_opening = next(iter(loaded.floor_plan.walls.values())).openings[0]

    assert loaded_opening.kind == "door"
    assert loaded_opening.width == 0.9
    assert loaded_opening.height_m == 2.1
