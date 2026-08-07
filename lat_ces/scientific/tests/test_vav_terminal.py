import pytest
from lat_ces.scientific.vav_terminal import VAVTerminalModel, VAVTerminalError


def test_vav_flow_calculation():
    model = VAVTerminalModel(max_flow=0.5, k_factor=0.01)
    flow = model.compute_vav_flow(damper_position_pct=80.0, pressure_drop_pa=150.0)
    assert flow > 0.0
    assert flow <= 0.5
