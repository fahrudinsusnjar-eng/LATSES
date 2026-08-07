import pytest
from lat_ces.scientific.fan_affinity import FanAffinityModel, FanAffinityError


def test_affinity_scaling():
    model = FanAffinityModel(base_rpm=1000.0, base_flow=1.0, base_pressure=200.0, base_power=1.5)
    # Povecanje brzine na 1200 RPM
    flow, pressure, power = model.scale_performance(new_rpm=1200.0)
    assert flow > 1.0
    assert pressure > 200.0
    assert power > 1.5
