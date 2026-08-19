from lat_ces.building.model import BuildingModel
from lat_ces.building.model_selector import BuildingModelSelector


def test_selector_starts_with_canonical_model() -> None:
    model = BuildingModel(name="Projekt")
    selector = BuildingModelSelector(model)
    assert selector.selected is model
    assert selector.selected_id == model.model_id
    assert [option.model_id for option in selector.options()] == [model.model_id]


def test_selector_switches_between_registered_models() -> None:
    first = BuildingModel(name="Prvi")
    second = BuildingModel(name="Drugi")
    selector = BuildingModelSelector(first)
    option = selector.register(second, description="Testni model", source="test")
    assert option.model_id == second.model_id
    assert selector.select(second.model_id) is second


def test_selector_does_not_remove_active_model() -> None:
    model = BuildingModel(name="Projekt")
    selector = BuildingModelSelector(model)
    try:
        selector.remove(model.model_id)
    except ValueError as exc:
        assert "trenutno odabrani" in str(exc)
    else:
        raise AssertionError("Active BuildingModel must not be removable")
