from lat_ces.building.model import BuildingModel
from lat_ces.building.project_spec import LevelProjectSpec, RoomSpec, WallConstructionSpec
from lat_ces.building.workflow import BuildingWorkflow


def test_first_step_generates_envelope_and_room_partitions() -> None:
    spec = LevelProjectSpec(
        name="Prizemlje",
        height_m=2.8,
        length_m=12.0,
        width_m=8.0,
        construction=WallConstructionSpec(wall_thickness_m=0.25),
        rooms=[
            RoomSpec(name="Kuhinja", length_m=4.0, width_m=3.0),
            RoomSpec(name="Spavaca", length_m=4.0, width_m=3.0),
            RoomSpec(name="WC", length_m=2.0, width_m=2.0),
            RoomSpec(name="Hodnik", length_m=3.0, width_m=2.0),
        ],
        finalized=True,
    )
    workflow = BuildingWorkflow(model=BuildingModel(name="Test"), project_spec=None)
    workflow.ensure_project_spec().set_floor_count(1)
    workflow.set_level_spec(0, spec)

    plan = workflow.floor_plan
    assert plan.walls
    assert any(wall.name.startswith("Vanjski zid") for wall in plan.walls.values())
    assert any(wall.name.startswith("Pregrada —") for wall in plan.walls.values())
    assert all(room.x_m >= 0 and room.y_m >= 0 for room in spec.rooms)
    assert spec.rooms[0].area_m2 == 12.0
