from lat_ces.building.model import BuildingModel
from lat_ces.building.project_spec import BuildingProjectSpec, LevelProjectSpec, WallConstructionSpec, RoomSpec
from lat_ces.building.workflow import BuildingWorkflow


def make_level(name: str, length: float, width: float, height: float) -> LevelProjectSpec:
    return LevelProjectSpec(
        name=name,
        length_m=length,
        width_m=width,
        height_m=height,
        construction=WallConstructionSpec(wall_thickness_m=0.25, insulation_type="EPS", insulation_thickness_m=0.10, render_thickness_m=0.005),
        rooms=[RoomSpec("Hodnik", length_m=min(3.0, length - 0.5), width_m=min(2.0, width - 0.5))],
        finalized=True,
    )


def test_ground_floor_and_upper_floors_are_independent_and_ordered():
    levels = [
        make_level("Prizemlje", 12.0, 8.0, 2.80),
        make_level("Sprat 1", 10.0, 7.0, 2.70),
        make_level("Sprat 2", 9.0, 6.0, 2.60),
    ]
    spec = BuildingProjectSpec(
        name="Test objekat",
        floor_count=3,
        levels=levels,
        floor_count_finalized=True,
        roof_shape="Dvovodni",
        roof_height_m=2.20,
    )
    workflow = BuildingWorkflow(
        model=BuildingModel("Test objekat"),
        project_spec=spec,
        current_step=4,
        roof_shape=spec.roof_shape,
        roof_height_m=spec.roof_height_m,
    )
    for index, level in enumerate(levels):
        workflow.set_level_spec(index, level)

    assert list(workflow.model.levels.values())[0].floor_plan.walls
    assert list(workflow.model.levels.values())[1].floor_plan.walls
    assert list(workflow.model.levels.values())[2].floor_plan.walls
    assert [lvl.height for lvl in workflow.model.levels.values()] == [2.8, 2.7, 2.6]
    assert [lvl.floor_plan.name for lvl in workflow.model.levels.values()] == ["Prizemlje", "Sprat 1", "Sprat 2"]
    assert [lvl.floor_plan.walls[wid].segment.length for lvl in workflow.model.levels.values() for wid in list(lvl.floor_plan.walls)[:1]] == [12.0, 10.0, 9.0]
    assert spec.roof_shape == "Dvovodni"
    assert spec.roof_height_m == 2.20
    assert workflow.current_step == 4
