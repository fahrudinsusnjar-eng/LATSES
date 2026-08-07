"""
LAT-CES Mathematical Core
State-Space Engine Verification Tests (LAT-MATH-CORE-0013-TEST)
"""

import pytest

from lat_ces.math.state_space import LinearStateSpace, StateSpaceError


def test_state_space_dimensions_mismatch():
    # Matrix A: 2x2, Matrix B: 3x1 (Incompatible dimensions)
    A = [[0.0, 1.0], [-2.0, -3.0]]
    B = [[0.0], [1.0], [0.0]]
    C = [[1.0, 0.0]]
    D = [[0.0]]

    with pytest.raises(StateSpaceError):
        LinearStateSpace(A=A, B=B, C=C, D=D)


def test_state_space_step_integration():
    # Simple 1st order system: dx/dt = -x + u
    A = [[-1.0]]
    B = [[1.0]]
    C = [[1.0]]
    D = [[0.0]]

    sys = LinearStateSpace(A=A, B=B, C=C, D=D)
    x0 = [0.0]
    u0 = [1.0]
    dt = 0.1

    x_next = sys.step(x=x0, u=u0, dt=dt)
    # x1 = x0 + dt * (-1*0 + 1*1) = 0.1
    assert pytest.approx(x_next[0], abs=1e-5) == 0.1
