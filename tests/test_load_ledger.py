import pytest

from lat_ces.structural.load_ledger import ConstructionAssembly, ConstructionLayer, LoadLedger


def test_layer_density_and_thickness_produce_area_mass_and_load() -> None:
    layer = ConstructionLayer("AB", "manufacturer:concrete", density_kg_m3=2500, thickness_m=0.16)
    assert layer.mass_kg_m2 == pytest.approx(400.0)
    assert layer.load_kn_m2 == pytest.approx(3.924)


def test_surface_mass_can_be_declared_directly() -> None:
    layer = ConstructionLayer("Crijep", "manufacturer:tile", surface_mass_kg_m2=45.0)
    assert layer.mass_kg_m2 == 45.0


def test_missing_or_ambiguous_mass_is_rejected() -> None:
    with pytest.raises(ValueError):
        ConstructionLayer("Unknown", "manufacturer:unknown")
    with pytest.raises(ValueError):
        ConstructionLayer("Bad", "manufacturer:bad", density_kg_m3=1000, thickness_m=0.1, surface_mass_kg_m2=10)


def test_load_ledger_sums_roof_slab_and_floor_assemblies() -> None:
    slab = ConstructionAssembly(
        "AB ploča",
        area_m2=100,
        layers=(ConstructionLayer("AB", "manufacturer:concrete", density_kg_m3=2500, thickness_m=0.16),),
    )
    floor = ConstructionAssembly(
        "Podni slojevi",
        area_m2=100,
        layers=(ConstructionLayer("Estrih", "manufacturer:screed", surface_mass_kg_m2=24),),
    )
    ledger = LoadLedger()
    ledger.add(slab)
    ledger.add(floor)
    assert ledger.total_mass_kg == pytest.approx(42400.0)
    assert ledger.total_weight_kn == pytest.approx(415.944)
