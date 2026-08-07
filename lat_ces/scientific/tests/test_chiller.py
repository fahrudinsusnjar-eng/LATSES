import pytest
from lat_ces.scientific.chiller import ChillerModel, ChillerError


def test_chiller_cop():
    model = ChillerModel(nominal_cop=4.5)
    actual_cop = model.compute_actual_cop(plr=0.5)
    assert actual_cop > 0.0
    assert actual_cop != 4.5
