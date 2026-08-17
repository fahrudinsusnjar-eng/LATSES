from lat_ces.building.floor_plan import FloorPlan, Opening, Point2D, Segment2D, Wall


def test_floor_plan_supports_editor_mutations() -> None:
    plan = FloorPlan(name="Editor test")
    wall = Wall(
        name="Zid 1",
        segment=Segment2D(Point2D(0.0, 0.0), Point2D(5.0, 0.0)),
        thickness=0.20,
    )
    plan.add_wall(wall)

    door = Opening(kind="door", offset=1.0, width=0.9)
    wall.add_opening(door)
    assert wall.net_length == 4.1

    wall.segment = Segment2D(Point2D(1.0, 1.0), Point2D(6.0, 1.0))
    assert wall.segment.start == Point2D(1.0, 1.0)
    assert wall.segment.end == Point2D(6.0, 1.0)
    assert plan.wall_count == 1

    del plan.walls[wall.wall_id]
    assert plan.wall_count == 0
