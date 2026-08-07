"""
LAT-CES Dynamic Twin Core
State Observer Reference Implementation (LAT-TWIN-CORE-0012)
"""

from typing import List


class ObserverError(Exception):
    """Base exception for State Observer operations."""

    pass


class LuenbergerObserver:
    """
    Implements a discrete-time Luenberger state observer for digital twin correction.
    x_hat_next = A*x_hat + B*u + L*(y - C*x_hat)
    """

    def __init__(self, A: List[List[float]], B: List[List[float]], C: List[List[float]], L: List[List[float]]):
        self.A = A
        self.B = B
        self.C = C
        self.L = L

        self.n_states = len(A)
        self.n_inputs = len(B[0]) if len(B) > 0 else 0
        self.n_outputs = len(C)

        self._validate_dimensions()

    def _validate_dimensions(self):
        if len(self.L) != self.n_states or any(len(row) != self.n_outputs for row in self.L):
            raise ObserverError("Observer gain matrix L dimensions must match n x p.")

    def update(self, x_hat: List[float], u: List[float], y_measured: List[float]) -> List[float]:
        """Executes one observer prediction and correction cycle."""
        if len(x_hat) != self.n_states or len(u) != self.n_inputs or len(y_measured) != self.n_outputs:
            raise ObserverError("State, input, or measurement dimension mismatch in observer update.")

        # 1. Prediction: x_pred = A*x_hat + B*u
        ax = [sum(self.A[i][j] * x_hat[j] for j in range(self.n_states)) for i in range(self.n_states)]
        bu = [sum(self.B[i][j] * u[j] for j in range(self.n_inputs)) for i in range(self.n_states)]
        x_pred = [ax[i] + bu[i] for i in range(self.n_states)]

        # 2. Output estimation: y_hat = C * x_hat
        y_hat = [sum(self.C[i][j] * x_hat[j] for j in range(self.n_states)) for i in range(self.n_outputs)]

        # 3. Residual: y - y_hat
        residual = [y_measured[i] - y_hat[i] for i in range(self.n_outputs)]

        # 4. Correction: L * residual
        correction = [sum(self.L[i][j] * residual[j] for j in range(self.n_outputs)) for i in range(self.n_states)]

        # Final state estimation update
        return [x_pred[i] + correction[i] for i in range(self.n_states)]
