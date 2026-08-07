"""
LAT-CES Control & Optimization Core
LQR Controller Reference Implementation (LAT-CTRL-CORE-0011)
"""

from typing import List


class LQRError(Exception):
    """Base exception for LQR Controller operations."""

    pass


class SimpleLQRController:
    """
    Implements state-feedback optimal control u = -K * x.
    """

    def __init__(self, K_gain: List[List[float]]):
        if not K_gain or not K_gain[0]:
            raise LQRError("Gain matrix K cannot be empty.")
        self.K_gain = K_gain
        self.n_inputs = len(K_gain)
        self.n_states = len(K_gain[0])

    def compute_control(self, state: List[float]) -> List[float]:
        """Calculates optimal control action vector given current system state."""
        if len(state) != self.n_states:
            raise LQRError("State vector dimension mismatch with LQR gain matrix K.")

        # u_i = - sum(K_ij * x_j)
        control_actions = []
        for row in self.K_gain:
            action = -sum(row[j] * state[j] for j in range(self.n_states))
            control_actions.append(action)

        return control_actions
