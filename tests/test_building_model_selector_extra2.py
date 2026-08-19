from lat_ces.building.model import BuildingModel
from lat_ces.building_model_selector import BuildingModelSelector


def test_selector_component_imports():
    assert BuildingModelSelector.__name__ == "BuildingModelSelector"
    assert BuildingModel("Kuca").name == "Kuca"
