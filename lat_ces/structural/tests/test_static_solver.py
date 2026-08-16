import pytest

from lat_ces.building.model import BuildingModel, Material
from lat_ces.structural.model import LoadCase, StructuralMember, StructuralModel, StructuralNode, SupportCondition
from lat_ces.structural.static_solver import solve_2d_truss


def test_single_bar_axial_solution():
    building = BuildingModel("Static test")
    building.add_material(Material("Steel", density=7850.0))
    material_id = next(iter(building.materials))

    structural = StructuralModel(building)
    structural.add_node(StructuralNode("N1", 0.0, 0.0, 0.0))
    structural.add_node(StructuralNode("N2", 2.0, 0.0, 0.0))
    structural.add_member(
        StructuralMember(
            "M1",
            "N1",
            "N2",
            material_id=material_id,
            area_m2=0.01,
        )
    )
    structural.add_support(SupportCondition("N1", (True, True, False, False, False, False)))
    structural.add_support(SupportCondition("N2", (False, True, False, False, False, False)))
    case = structural.add_load_case(LoadCase("TEST"))
    case.loads.append(type(case.loads).__args__[0]("N2", fx_n=10000.0)) if False else None
    from lat_ces.structural.model import NodalLoad
    case.add_load(NodalLoad("N2", fx_n=10000.0))

    result = solve_2d_truss(structural, {material_id: 200e9}, "TEST")

    assert result.displacements["N1"] == pytest.approx((0.0, 0.0))
    assert result.displacements["N2"][0] == pytest.approx(1e-5)
    assert result.displacements["N2"][1] == pytest.approx(0.0)
    assert result.member_axial_forces_n["M1"] == pytest.approx(10000.0)
