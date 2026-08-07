"""
LAT-CES Control & Optimization Core
Safety Barrier Reference Implementation (LAT-CTRL-CORE-0012)
"""

from typing import List


class BarrierError(Exception):
    """Base exception for Safety Barrier operations."""

    pass


class SafetyBarrier:
    """
    Enforces constitutional and physical bounds on control or state vectors
    using clipping projection.
    """

    def __init__(self, min_limit: float, max_limit: float):
        if min_limit >= max_limit:
            raise BarrierError("min_limit must be strictly less than max_limit.")
        self.min_limit = min_limit
        self.max_limit = max_limit

    def enforce(self, action: List[float]) -> List[float]:
        """Projects control actions into safe constitutional bounds."""
        if not isinstance(action, list):
            raise BarrierError("Action must be a list of numerical values.")

        filtered_action = []
        for val in action:
            clipped = max(self.min_limit, min(val, self.max_limit))
            filtered_action.append(clipped)

        return filtered_action
