from lat_ces.building.floor_plan import Opening
from lat_ces.building.model import BuildingModel
from lat_ces.building.workflow import BuildingWorkflow
from lat_ces.gui import build_default_floor_plan, new_workflow


def test_workflow_preserves_one_building_model_across_four_steps():
    workflow = new_workflow()
    assert workflow.current_step == 1
    assert len(workflow.model.levels) == 1
    assert workflow.floor_plan.wall_count == 6

    workflow.set_active_level_height(3.0)
    assert workflow.active_level.height == 3.0

    wall = next(iter(workflow.floor_plan.walls.values()))
    wall.add_opening(Opening(kind="door", offset=1.0, width=0.9))
    workflow.advance_to_openings()
    assert workflow.current_step == 3
    assert len(wall.openings) == 1

    geometries = workflow.advance_to_3d()
    assert workflow.current_step == 4
    assert len(geometries) == 1
    assert len(geometries[0].walls) == workflow.floor_plan.wall_count
    assert geometries[0].height == 3.0


def test_workflow_adds_second_level_with_continuous_elevation():
    workflow = BuildingWorkflow(model=BuildingModel("Test"))
    workflow.set_floor_plan(build_default_floor_plan())
    first = workflow.active_level
    second = workflow.add_level("Sprat 1", 2.7)
    assert second.elevation == first.top_elevation
    assert len(workflow.model.levels) == 2


def test_workflow_validation_exposes_missing_level():
    workflow = BuildingWorkflow(model=BuildingModel("Empty"))
    findings = workflow.validate()
    assert any("level" in finding.lower() for finding in findings)
