import pytest
from lat_ces.scientific.duct_leakage import DuctLeakageModel, DuctLeakageError


def test_leakage_calculation():
    # leakage_coefficient i exponent (obicno oko 0.65 za kanale)
    model = DuctLeakageModel(leakage_factor=0.01)
    leak_flow = model.compute_leakage_flow(static_pressure=250.0, surface_area=50.0)
    assert leak_flow > 0.0
