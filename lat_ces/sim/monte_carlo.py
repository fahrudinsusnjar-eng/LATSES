"""
LAT-CES Simulation Core
Monte Carlo Engine Reference Implementation (LAT-SIM-CORE-0011)
"""

import random
from typing import Callable, Dict, List, Tuple


class SimulationError(Exception):
    """Base exception for Monte Carlo simulation operations."""

    pass


class MonteCarloEngine:
    """
    Executes stochastic Monte Carlo simulations over physical system models.
    """

    def __init__(self, model_func: Callable[[Dict[str, float]], float], iterations: int = 1000):
        if iterations <= 0:
            raise SimulationError("Iterations must be a positive integer.")
        self.model_func = model_func
        self.iterations = iterations

    def run(self, param_bounds: Dict[str, Tuple[float, float]]) -> List[float]:
        """Runs stochastic simulations by uniformly sampling parameter bounds."""
        if not param_bounds:
            raise SimulationError("Parameter bounds cannot be empty.")

        results = []
        for _ in range(self.iterations):
            sampled_params = {
                param: random.uniform(low, high)
                for param, (low, high) in param_bounds.items()
            }
            output = self.model_func(sampled_params)
            results.append(output)

        return results
