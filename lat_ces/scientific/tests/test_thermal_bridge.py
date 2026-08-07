import pytest
from lat_ces.scientific.thermal_bridge import ThermalBridgeModel, ThermalBridgeError


def test_thermal_bridge_loss():
    model = ThermalBridgeModel()
    loss = model.compute_linear_heat_loss(psi_value=0.05, length_m=12.0, temp_diff=25.0)
    assert loss > 0.0
