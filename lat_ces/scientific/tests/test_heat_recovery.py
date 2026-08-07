import pytest
from lat_ces.scientific.heat_recovery import HeatRecoveryModel, HeatRecoveryError


def test_heat_recovery_efficiency():
    model = HeatRecoveryModel(nominal_effectiveness=0.75)
    # supply_in = -5.0degC, exhaust_in = 22.0degC
    supply_out = model.compute_supply_outlet_temp(supply_in=-5.0, exhaust_in=22.0)
    assert supply_out > -5.0 and supply_out < 22.0
