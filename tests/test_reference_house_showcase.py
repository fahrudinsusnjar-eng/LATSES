from lat_ces.reference_house import ReferenceHouse


def test_reference_house_is_complete_and_deterministic():
    house = ReferenceHouse.default()
    assert len(house.levels) == 3
    assert {level["id"] for level in house.levels} == {"P", "S1", "S2"}
    assert house.data["roof"]["type"] == "dvovodni"
    assert house.data["heating"]["plant_room"] == "P-BOIL"
    assert house.data["joinery"]["glazing"]["panes"] == 3
    summary = house.summary()
    assert summary.floor_area_m2 > 300
    assert summary.volume_m3 > 800
    assert summary.roof_area_m2 > 120
    assert summary.wall_area_m2 > 200
    assert summary.blocks > 10000
    assert summary.slab_concrete_m3 > 60
    assert summary.heating_load_w > 20000
    assert summary.heating_mass_flow_kg_s > 0
    assert summary.ventilation_m3_h > 2000
    assert summary.lighting_w > 100


def test_heating_circuits_and_comfort_guidance():
    house = ReferenceHouse.default()
    circuits = house.heating_circuits()
    assert len(circuits) == 3
    assert circuits[0].type == "underfloor"
    assert circuits[1].type == "radiator"
    assert circuits[0].delta_t_k == 7.0
    assert house.simulation_guidance(0.05).startswith("Vrlo blago")
    assert house.simulation_guidance(0.25).startswith("Visoko")
