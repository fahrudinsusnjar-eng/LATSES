from lat_ces.building import (
    BuildingModel,
    FloorPlan,
    Level,
    Opening,
    Point2D,
    Segment2D,
    Wall,
)


def test_floor_plan_wall_opening_net_length() -> None:
    wall = Wall(
        "North",
        Segment2D(Point2D(0, 0), Point2D(10, 0)),
    )
    wall.add_opening(Opening("window", offset=2.0, width=1.5))
    wall.add_opening(Opening("door", offset=6.0, width=0.9))

    assert wall.segment.length == 10.0
    assert wall.net_length == 7.6


def test_opening_overlap_and_bounds_are_rejected() -> None:
    wall = Wall("South", Segment2D(Point2D(0, 0), Point2D(5, 0)))
    wall.add_opening(Opening("door", offset=1.0, width=1.0))

    try:
        wall.add_opening(Opening("window", offset=1.5, width=1.0))
    except ValueError as exc:
        assert "overlaps" in str(exc)
    else:
        raise AssertionError("overlapping opening was accepted")

    try:
        wall.add_opening(Opening("window", offset=4.5, width=1.0))
    except ValueError as exc:
        assert "beyond" in str(exc)
    else:
        raise AssertionError("out-of-bounds opening was accepted")


def test_floor_plan_is_attached_to_level_and_validated() -> None:
    plan = FloorPlan("Ground floor")
    plan.add_wall(Wall("West", Segment2D(Point2D(0, 0), Point2D(8, 0))))

    level = Level("Ground", elevation=0.0, height=2.7)
    level.set_floor_plan(plan)
    building = BuildingModel("House")
    building.add_level(level)

    assert building.levels[level.level_id].floor_plan is plan
    assert plan.wall_count == 1
    assert plan.gross_wall_length == 8.0
    assert building.validate() == []
