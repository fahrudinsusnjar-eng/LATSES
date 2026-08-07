"""
LAT-CES Simulation Core
Monte Carlo Engine Verification Tests (LAT-SIM-CORE-0011-TEST)
"""

import pytest

from lat_ces.sim.monte_carlo import MonteCarloEngine, SimulationError


def test_monte_carlo_execution():
    def mock_model(params):
        return params["a"] + params["b"]

    param_ranges = {"a": (0.0, 10.0), "b": (5.0, 15.0)}

    engine = MonteCarloEngine(model_func=mock_model, iterations=100)
    results = engine.run(param_ranges)

    assert len(results) == 100
    assert all(5.0 <= r <= 25.0 for r in results)
