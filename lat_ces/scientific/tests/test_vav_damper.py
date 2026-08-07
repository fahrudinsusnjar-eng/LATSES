import pytest
from lat_ces.scientific.vav_damper import VAVDamperModel, VAVError


def test_damper_position_adjustment():
    model = VAVDamperModel(max_flow=1.0)
    position = model.compute_damper_position(requested_flow=0.5, current_pressure=50.0)
    assert 0.0 <= position <= 100.0
    assert position == 50.0
