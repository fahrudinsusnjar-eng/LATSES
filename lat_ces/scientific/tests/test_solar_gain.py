import pytest
from lat_ces.scientific.solar_gain import SolarGainModel, SolarGainError


def test_solar_heat_gain():
    model = SolarGainModel(shgc=0.6)
    gain = model.compute_solar_gain(area_m2=15.0, solar_irradiance_W_m2=400.0)
    assert gain > 0.0
    assert gain == 3600.0
