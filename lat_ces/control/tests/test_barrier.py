"""
LAT-CES Control & Optimization Core
Safety Barrier Engine Verification Tests (LAT-CTRL-CORE-0012-TEST)
"""

import pytest

from lat_ces.control.barrier import BarrierError, SafetyBarrier


def test_safety_barrier_within_bounds():
    barrier = SafetyBarrier(min_limit=-10.0, max_limit=10.0)
    safe_action = [5.0]

    filtered = barrier.enforce(safe_action)
    assert filtered == [5.0]


def test_safety_barrier_clips_violation():
    barrier = SafetyBarrier(min_limit=-10.0, max_limit=10.0)
    unsafe_action = [15.0]  # Exceeds max limit

    filtered = barrier.enforce(unsafe_action)
    assert filtered == [10.0]
