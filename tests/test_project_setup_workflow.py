from lat_ces.building.floor_plan import FloorPlan
from lat_ces.building.model import BuildingModel
from lat_ces.building.project_spec import BuildingProjectSpec, LevelProjectSpec, RoomSpec, WallConstructionSpec
from lat_ces.building.workflow import BuildingWorkflow


def make_spec(name: str, length: float, width: float, height: float) -> LevelProjectSpec:
    return LevelProjectSpec(
        name=name,
        length_m=length,
        width_m=width,
        height_m=height,
        construction=WallConstructionSpec(
            block_brand="TestBlock",
            wall_thickness_m=0.25,
            insulation_type="EPS",
            insulation_thickness_m=0.10,
            render_thickness_m=0.005,
        ),
        rooms=[RoomSpec("hodnik", 3.0, 1.5), RoomSpec("kuhinja", 4.0, 3.0)],
        finalized=True,
    )


def test_new_building_starts_with_empty_floor_plan():
    workflow = BuildingWorkflow(model=BuildingModel("Novi objekat"), project_spec=BuildingProjectSpec())
    level = workflow.set_floor_plan(FloorPlan("Prizemlje"))
    assert level.floor_plan is not None
    assert level.floor_plan.wall_count == 0


def test_floors_are_independent_and_locked_before_roof():
    project = BuildingProjectSpec(name="Kuća")
    project.set_floor_count(2)
    project.levels[0] = make_spec("Etaža 1", 12.0, 8.0, 2.8)
    project.levels[1] = make_spec("Etaža 2", 10.0, 7.0, 2.6)
    workflow = BuildingWorkflow(model=BuildingModel("Kuća"), project_spec=project)
    workflow.set_level_spec(0, project.levels[0])
    workflow.set_level_spec(1, project.levels[1])
    assert workflow.model.levels
    levels = list(workflow.model.levels.values())
    assert levels[0].floor_plan is not levels[1].floor_plan
    assert levels[0].floor_plan.walls
    assert levels[1].floor_plan.walls
    workflow.advance_to_roof()
    assert project.floor_count_finalized


def test_building_rejects_invalid_floor_count():
    project = BuildingProjectSpec()
    try:
        project.set_floor_count(51)
    except ValueError:
        pass
    else:
        raise AssertionError("51 etaža mora biti odbijeno")
