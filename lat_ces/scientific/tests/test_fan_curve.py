import pytest
from lat_ces.scientific.fan_curve import FanCurveModel, FanCurveError


def test_operating_point_calculation():
    # Kriva ventilatora: P = max_pressure - a * Q^2
    model = FanCurveModel(max_pressure=500.0, coefficient_a=200.0)
    system_resistance = 150.0  # R u ΔP = R * Q^2
    flow = model.compute_operating_flow(system_resistance)
    assert flow > 0.0
