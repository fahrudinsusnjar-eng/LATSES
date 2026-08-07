"""
LAT-CES Simulation Core
HIL Test Orchestrator Reference Implementation (LAT-SIM-CORE-0012)
"""

from typing import Callable


class HILError(Exception):
    """Base exception for HIL Orchestrator operations."""

    pass


class HILOrchestrator:
    """
    Orchestrates hardware-in-the-loop and software-in-the-loop simulation loops.
    """

    def __init__(self, step_callback: Callable[[float], None], step_size: float = 0.01):
        if step_size <= 0:
            raise HILError("Step size must be strictly positive.")
        self.step_callback = step_callback
        self.step_size = step_size

    def run_ticks(self, ticks: int) -> None:
        """Executes a defined number of synchronous simulation ticks."""
        if ticks <= 0:
            raise HILError("Ticks count must be a positive integer.")

        for _ in range(ticks):
            self.step_callback(self.step_size)
