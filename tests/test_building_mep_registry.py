from dataclasses import replace

from lat_ces.building.mep import ensure_mep_registry
from lat_ces.building.model import BuildingModel
from lat_ces.building_model.systems import VentilationOpening


def test_building_model_owns_one_mep_registry():
    model = BuildingModel(name="MEP test")
    registry = ensure_mep_registry(model)
    assert ensure_mep_registry(model) is registry

    opening = VentilationOpening(
        "VO-1",
        "ROOM-1",
        "supply",
        0.10,
        0.05,
        0.70,
        2.0,
        1.5,
    )
    registry.add_ventilation_opening(opening)
    assert registry.all_ventilation_openings == (opening,)


def test_ventilation_opening_can_be_updated_and_removed():
    model = BuildingModel(name="MEP edit")
    registry = ensure_mep_registry(model)
    opening = VentilationOpening("VO-2", "ROOM-2", "extract", 0.10, 0.05, 2.40, 4.0, 3.0)
    registry.add_ventilation_opening(opening)

    updated = registry.update_ventilation_opening(opening.id, diameter_m=0.125, elevation_m=2.50)
    assert updated.diameter_m == 0.125
    assert updated.elevation_m == 2.50
    assert registry.ventilation_openings[opening.id] == replace(opening, diameter_m=0.125, elevation_m=2.50)

    removed = registry.remove_ventilation_opening(opening.id)
    assert removed.id == opening.id
    assert registry.all_ventilation_openings == ()


def test_ventilation_opening_rejects_negative_plan_coordinates():
    import pytest

    with pytest.raises(ValueError, match="coordinates"):
        VentilationOpening("VO-3", "ROOM-3", "supply", 0.10, 0.05, 0.70, -0.1, 1.0)


def test_mep_gui_module_imports_without_creating_a_window():
    from lat_ces.gui_mep import MEPEnabledDraftingApp

    assert MEPEnabledDraftingApp.__name__ == "MEPEnabledDraftingApp"
