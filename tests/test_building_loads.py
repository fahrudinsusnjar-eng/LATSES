from lat_ces.building.floor_plan import Point2D, Segment2D, Wall
from lat_ces.building.model import BuildingModel, Level
from lat_ces.building.workflow import make_blank_floor_plan
from lat_ces.structural.building_loads import floor_area_m2, wall_area_m2


def _building() -> BuildingModel:
    building = BuildingModel("Test")
    plan = make_blank_floor_plan("Prizemlje")
    plan.add_wall(Wall("w1", Segment2D(Point2D(0, 0), Point2D(10, 0)), thickness=0.25))
    plan.add_wall(Wall("w2", Segment2D(Point2D(10, 0), Point2D(10, 8)), thickness=0.25))
    plan.add_wall(Wall("w3", Segment2D(Point2D(10, 8), Point2D(0, 8)), thickness=0.25))
    plan.add_wall(Wall("w4", Segment2D(Point2D(0, 8), Point2D(0, 0)), thickness=0.25))
    building.add_level(Level("Prizemlje", elevation=0.0, height=2.8, floor_plan=plan))
    return building


def test_floor_area_comes_from_building_model():
    assert floor_area_m2(_building(), "Prizemlje") == 80.0


def test_wall_area_comes_from_building_model():
    assert wall_area_m2(_building(), "Prizemlje") == 100.8
