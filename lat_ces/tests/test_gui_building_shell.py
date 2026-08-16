from lat_ces.gui import MODE_DESCRIPTIONS, build_default_floor_plan


def test_building_first_gui_has_floor_plan_as_primary_model():
    plan = build_default_floor_plan()

    assert plan.name == "Novi objekat"
    assert plan.wall_count == 6
    assert plan.validate() == []


def test_gui_exposes_building_operating_modes():
    expected = {
        "Projektovanje",
        "Geometrija",
        "Instalacije",
        "Konstrukcija",
        "Simulacija",
        "Provjera i izvještaj",
    }

    assert set(MODE_DESCRIPTIONS) == expected
