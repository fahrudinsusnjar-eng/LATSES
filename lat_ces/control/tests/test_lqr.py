"""
LAT-CES Control & Optimization Core
LQR Control Engine Verification Tests (LAT-CTRL-CORE-0011-TEST)
"""

import pytest

from lat_ces.control.lqr import LQRError, SimpleLQRController


def test_lqr_control_signal_generation():
    # Gain matrix K = [[2.0, 1.5]]
    K = [[2.0, 1.5]]
    controller = SimpleLQRController(K_gain=K)

    state = [1.0, 2.0]
    # u = -K * x = -(2.0*1.0 + 1.5*2.0) = -(2.0 + 3.0) = -5.0
    control_action = controller.compute_control(state)

    assert len(control_action) == 1
    assert pytest.approx(control_action[0], abs=1e-5) == -5.0
