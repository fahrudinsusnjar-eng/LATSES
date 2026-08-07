import pytest
from lat_ces.scientific.thermal_comfort import ThermalComfortModel, ThermalComfortError


def test_pmv_calculation():
    model = ThermalComfortModel()
    pmv, ppd = model.compute_pmv_ppd(air_temp=22.0, mean_rad_temp=22.0, air_velocity=0.15, rel_humidity=50.0)
    assert -3.0 <= pmv <= 3.0
    assert 0.0 <= ppd <= 100.0
