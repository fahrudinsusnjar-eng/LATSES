import pytest
from lat_ces.scientific.condensation import CondensationModel, CondensationError


def test_condensation_risk():
    model = CondensationModel()
    risk = model.evaluate_condensation_risk(air_temp=24.0, rel_humidity=70.0, surface_temp=15.0)
    assert isinstance(risk, bool)
