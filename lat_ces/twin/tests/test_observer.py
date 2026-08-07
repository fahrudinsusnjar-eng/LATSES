"""
LAT-CES Dynamic Twin Core
State Observer Engine Verification Tests (LAT-TWIN-CORE-0012-TEST)
"""

import pytest

from lat_ces.twin.observer import LuenbergerObserver, ObserverError


def test_observer_correction_step():
    # Model: A = [[0]], B = [[1]], C = [[1]], D = [[0]]
    A = [[0.0]]
    B = [[1.0]]
    C = [[1.0]]
    L = [[0.5]]  # Observer gain

    observer = LuenbergerObserver(A=A, B=B, C=C, L=L)

    x_hat = [1.0]  # Current estimated state
    u = [1.0]  # Control input
    y_measured = [1.5]  # Actual sensor measurement

    # Predicted state = 0*1 + 1*1 = 1.0
    # Estimated output = 1*1.0 = 1.0
    # Residual = 1.5 - 1.0 = 0.5
    # Correction = L * residual = 0.5 * 0.5 = 0.25
    # Next state = 1.0 + 0.25 = 1.25

    x_corrected = observer.update(x_hat=x_hat, u=u, y_measured=y_measured)
    assert pytest.approx(x_corrected[0], abs=1e-5) == 1.25
