import pytest
from lat_ces.scientific.hydronic_pump import HydronicPumpModel, PumpError


def test_pump_power_calculation():
    model = HydronicPumpModel(pump_efficiency=0.75)
    power = model.compute_pump_power(flow_rate_m3h=10.0, head_kPa=50.0)
    assert power > 0.0
