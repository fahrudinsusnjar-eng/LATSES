import pytest

from lat_ces.building.model import BuildingModel, BuildingElement, Level, Material, Room
from lat_ces.building.geometry import Box3D, Point3D
from lat_ces.structural import (
    LoadCase,
    NodalLoad,
    StructuralMember,
    StructuralModel,
    StructuralNode,
    SupportCondition,
)


def test_structural_model_references_shared_building_model():
    building = BuildingModel("Test")
    building.add_material(Material("Concrete", density=2400.0))
    level = Level("Ground", 0.0, 3.0)
    room = Room("Room", Box3D(Point3D(0, 0, 0), 4, 4, 3))
    element = BuildingElement("Column", Box3D(Point3D(0, 0, 0), 0.3, 0.3, 3), element_type="column")
    room.add_element(element)
    level.add_room(room)
    building.add_level(level)

    structural = StructuralModel(building)
    structural.add_node(StructuralNode("N1", 0, 0, 0, (element.element_id,)))
    structural.add_node(StructuralNode("N2", 0, 0, 3, (element.element_id,)))
    structural.add_member(
        StructuralMember(
            "M1",
            "N1",
            "N2",
            element_id=element.element_id,
            material_id=next(iter(building.materials)),
            area_m2=0.09,
            inertia_m4=0.000675,
        )
    )
    structural.add_support(SupportCondition("N1", (True, True, True, False, False, False)))
    case = structural.add_load_case(LoadCase("G"))
    case.add_load(NodalLoad("N2", fz_n=-10000.0))

    assert structural.building is building
    assert structural.validate() == []


def test_structural_model_detects_missing_references():
    building = BuildingModel("Test")
    structural = StructuralModel(building)
    structural.add_node(StructuralNode("N1", 0, 0, 0))
    structural.add_member(StructuralMember("M1", "N1", "N2", area_m2=0.01))
    structural.add_support(SupportCondition("N3", (True, False, False, False, False, False)))
    case = structural.add_load_case(LoadCase("G"))
    case.add_load(NodalLoad("N4", fz_n=-1.0))

    findings = structural.validate()
    assert "Missing end node: N2" in findings
    assert "Missing support node: N3" in findings
    assert "Missing load node: N4" in findings


def test_structural_member_rejects_nonpositive_area():
    with pytest.raises(ValueError):
        StructuralMember("M1", "N1", "N2", area_m2=0.0)
