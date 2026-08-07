"""
LAT-CES Simulation Core
HIL Orchestrator Verification Tests (LAT-SIM-CORE-0012-TEST)
"""

import pytest

from lat_ces.sim.hil import HILError, HILOrchestrator


def test_hil_orchestrator_tick_loop():
    tick_count = 0

    def dummy_step_callback(dt):
        nonlocal tick_count
        tick_count += 1

    orchestrator = HILOrchestrator(step_callback=dummy_step_callback, step_size=0.1)
    orchestrator.run_ticks(ticks=5)

    assert tick_count == 5
