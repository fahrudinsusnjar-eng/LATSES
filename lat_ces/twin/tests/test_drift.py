"""
LAT-CES Dynamic Twin Core
Adaptive Parameter Drift Monitor Verification Tests (LAT-TWIN-CORE-0013-TEST)
"""

import pytest

from lat_ces.twin.drift import DriftError, DriftMonitor


def test_drift_monitor_normal_operation():
    monitor = DriftMonitor(window_size=5, threshold=1.0)

    # Small residuals within threshold
    for res in [0.1, 0.05, -0.1, 0.02, 0.0]:
        drift_detected = monitor.update(res)

    assert not drift_detected
    assert monitor.is_drift_detected() is False


def test_drift_monitor_triggers_on_persistent_bias():
    monitor = DriftMonitor(window_size=4, threshold=0.5)

    # Persistent large residuals
    monitor.update(0.6)
    monitor.update(0.7)
    monitor.update(0.8)
    triggered = monitor.update(0.9)

    assert triggered is True
    assert monitor.is_drift_detected() is True
