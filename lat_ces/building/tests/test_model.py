from lat_ces.building import Box3D, BuildingElement, BuildingModel, Level, Material, Point3D, Room


def test_building_model_topology_and_totals():
    model = BuildingModel("Demo House")
    material = model.add_material(
        Material("Concrete", density=2400.0, youngs_modulus=30e9, poisson_ratio=0.2)
    )

    level = model.add_level(Level("Ground", elevation=0.0, height=2.8))
    room = level.add_room(
        Room(
            "Living",
            Box3D(Point3D(0.0, 0.0, 0.0), length=7.6, width=3.6, height=2.8),
        )
    )
    room.add_element(
        BuildingElement(
            "North Wall",
            Box3D(Point3D(0.0, 3.5, 0.0), length=7.6, width=0.2, height=2.8),
            element_type="wall",
            material=material,
        )
    )

    assert model.floor_area == 7.6 * 3.6
    assert model.volume == 7.6 * 3.6 * 2.8
    assert model.room_count == 1
    assert model.element_count == 1
    assert model.validate() == []


def test_duplicate_ids_are_rejected():
    model = BuildingModel("Test")
    level = Level("Ground", 0.0, 2.5, level_id="LVL-1")
    model.add_level(level)

    try:
        model.add_level(Level("Ground Copy", 0.0, 2.5, level_id="LVL-1"))
    except ValueError as exc:
        assert "Duplicate level id" in str(exc)
    else:
        raise AssertionError("duplicate level id was accepted")


def test_level_overlap_is_reported():
    model = BuildingModel("Overlap")
    model.add_level(Level("Ground", 0.0, 3.0))
    model.add_level(Level("First", 2.5, 2.8))

    findings = model.validate()
    assert findings
    assert findings[0].startswith("Level overlap:")
