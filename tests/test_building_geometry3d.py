from lat_ces.building.floor_plan import FloorPlan, Point2D, Segment2D, Wall
from lat_ces.building.geometry3d import MaterialLayer, build_geometry
from lat_ces.building.model import BuildingModel, Level


def test_build_geometry_extrudes_existing_floor_plan():
    model = BuildingModel("Test Building")
    level = Level("Ground", 0.0, 3.0)
    plan = FloorPlan("Ground plan")
    wall = Wall("North", Segment2D(Point2D(0, 0), Point2D(4, 0)), thickness=0.2)
    plan.add_wall(wall)
    level.set_floor_plan(plan)
    model.add_level(level)

    geometry = build_geometry(model)

    assert len(geometry) == 1
    assert len(geometry[0].walls) == 1
    assert geometry[0].walls[0].length == 4.0
    assert geometry[0].walls[0].gross_area == 12.0
    assert geometry[0].walls[0].volume == 2.4


def test_material_layer_requires_positive_thickness():
    layer = MaterialLayer("Concrete", 0.20)
    assert layer.material == "Concrete"
    assert layer.thickness == 0.20
