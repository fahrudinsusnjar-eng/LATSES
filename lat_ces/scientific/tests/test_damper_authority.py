import pytest
from lat_ces.scientific.damper_authority import DamperAuthorityModel, DamperError


def test_damper_authority():
    model = DamperAuthorityModel()
    auth = model.compute_authority(dp_damper_fully_open=50.0, dp_system_total=200.0)
    assert 0.0 <= auth <= 1.0
    assert auth == 0.25
