import pytest
from lat_ces.scientific.psychrometrics import PsychrometricsModel, PsychrometricsError


def test_enthalpy_calculation():
    model = PsychrometricsModel()
    enthalpy = model.compute_air_enthalpy(dry_bulb_temp=25.0, rel_humidity=50.0)
    assert enthalpy > 0.0
