import pytest
from lat_ces.scientific.coil_performance import CoilPerformanceModel, CoilError


def test_coil_heat_transfer():
    model = CoilPerformanceModel(effectiveness=0.8)
    q_total = model.compute_coil_heat_transfer(air_mass_flow=1.2, entering_temp=30.0, coil_surface_temp=10.0)
    assert q_total > 0.0
