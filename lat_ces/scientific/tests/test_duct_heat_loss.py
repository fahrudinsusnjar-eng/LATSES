import pytest
from lat_ces.scientific.duct_loss import DuctLossModel, DuctLossError


def test_duct_temperature_drop():
    model = DuctLossModel(surface_area=10.0, overall_heat_transfer_coef=1.2)
    final_temp = model.compute_outlet_temperature(inlet_temp=18.0, ambient_temp=10.0, mass_flow=0.5, specific_heat=1005.0)
    assert final_temp > 10.0 and final_temp < 18.0
