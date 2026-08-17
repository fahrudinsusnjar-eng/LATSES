import pytest

from lat_ces.structural.construction_inputs import FloorInput, SlabInput, WallInput, build_permanent_load_ledger
from lat_ces.structural.load_ledger import ConstructionLayer


def test_slab_wall_floor_inputs_feed_one_load_ledger() -> None:
    layers = (ConstructionLayer("generic layer", "catalog:item", surface_mass_kg_m2=10.0),)
    ledger = build_permanent_load_ledger(
        slabs=(SlabInput("Ploča", 100.0, layers),),
        walls=(WallInput("Vanjski zid", 50.0, layers),),
        floors=(FloorInput("Pod", 100.0, layers),),
    )
    assert ledger.total_mass_kg == pytest.approx(2500.0)
    assert ledger.total_weight_kn == pytest.approx(24.525)
