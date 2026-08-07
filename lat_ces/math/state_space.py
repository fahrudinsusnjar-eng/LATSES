"""
LAT-CES Mathematical Core
State-Space Engine Reference Implementation (LAT-MATH-CORE-0013)
"""

from typing import List


class StateSpaceError(Exception):
    """Base exception for State-Space System operations."""

    pass


class LinearStateSpace:
    """
    Continuous/Discrete Linear Time-Invariant (LTI) State-Space System.
    dx/dt = A*x + B*u
    y = C*x + D*u
    """

    def __init__(self, A: List[List[float]], B: List[List[float]], C: List[List[float]], D: List[List[float]]):
        self.A = A
        self.B = B
        self.C = C
        self.D = D

        self.n_states = len(A)
        self.n_inputs = len(B[0]) if len(B) > 0 else 0
        self.n_outputs = len(C)

        self._validate_dimensions()

    def _validate_dimensions(self) -> None:
        # Validate A is square (n x n)
        if any(len(row) != self.n_states for row in self.A):
            raise StateSpaceError("Matrix A must be square (n x n).")

        # Validate B is (n x m)
        if len(self.B) != self.n_states or any(len(row) != self.n_inputs for row in self.B):
            raise StateSpaceError("Matrix B dimensions must match state count n x m.")

        # Validate C is (p x n)
        if any(len(row) != self.n_states for row in self.C):
            raise StateSpaceError("Matrix C dimensions must match state count p x n.")

    def step(self, x: List[float], u: List[float], dt: float) -> List[float]:
        """
        Executes a 1st-order Euler forward numerical integration step.
        dx/dt = A*x + B*u
        x_next = x + dt * (dx/dt)
        """
        if len(x) != self.n_states or len(u) != self.n_inputs:
            raise StateSpaceError("State or Input vector dimension mismatch.")

        # Calculate A*x
        ax = [sum(self.A[i][j] * x[j] for j in range(self.n_states)) for i in range(self.n_states)]

        # Calculate B*u
        bu = [sum(self.B[i][j] * u[j] for j in range(self.n_inputs)) for i in range(self.n_states)]

        # dx/dt = ax + bu
        dxdt = [ax[i] + bu[i] for i in range(self.n_states)]

        # Integration
        return [x[i] + dt * dxdt[i] for i in range(self.n_states)]
