class FilterError(Exception):
    pass


class FilterModel:
    def __init__(self, base_resistance: float, degradation_rate: float):
        if base_resistance < 0.0 or degradation_rate < 0.0:
            raise FilterError("Parameters must be non-negative.")
        self.base_resistance = base_resistance
        self.rate = degradation_rate

    def compute_current_resistance(self, operating_hours: float) -> float:
        """Computes increased filter pressure drop resistance over time."""
        if operating_hours < 0.0:
            raise FilterError("Operating hours cannot be negative.")
        current = self.base_resistance * (1.0 + self.rate * operating_hours)
        return round(current, 2)
