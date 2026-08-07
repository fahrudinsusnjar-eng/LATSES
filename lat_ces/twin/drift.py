"""
LAT-CES Dynamic Twin Core
Adaptive Parameter Drift Monitor Reference Implementation (LAT-TWIN-CORE-0013)
"""

from collections import deque
import math


class DriftError(Exception):
    """Base exception for Drift Monitor operations."""

    pass


class DriftMonitor:
    """
    Monitors observer residuals over a sliding window to detect structural
    model drift or sensor degradation.
    """

    def __init__(self, window_size: int = 50, threshold: float = 0.5):
        if window_size <= 0:
            raise DriftError("Window size must be a positive integer.")
        if threshold <= 0:
            raise DriftError("Drift threshold must be strictly positive.")

        self.window_size = window_size
        self.threshold = threshold
        self._residuals: deque = deque(maxlen=window_size)
        self._drift_flag: bool = False

    def update(self, residual: float) -> bool:
        """
        Pushes a new residual value and checks if mean absolute residual
        exceeds the configured drift threshold.
        """
        self._residuals.append(float(residual))

        if len(self._residuals) == self.window_size:
            mean_abs = sum(abs(r) for r in self._residuals) / self.window_size
            if mean_abs > self.threshold:
                self._drift_flag = True
            else:
                self._drift_flag = False

        return self._drift_flag

    def is_drift_detected(self) -> bool:
        """Returns current system drift status flag."""
        return self._drift_flag

    def reset(self) -> bool:
        """Resets the drift monitor internal buffer and state flag."""
        self._residuals.clear()
        self._drift_flag = False
        return True
