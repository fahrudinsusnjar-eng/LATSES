import math


class FanCurveError(Exception):
    pass


class FanCurveModel:
    def __init__(self, max_pressure: float, coefficient_a: float):
        if max_pressure <= 0.0 or coefficient_a <= 0.0:
            raise FanCurveError("Fan curve parameters must be positive.")
        self.max_pressure = max_pressure
        self.coefficient_a = coefficient_a

    def compute_operating_flow(self, system_resistance: float) -> float:
        """
        Izračunava tačku presjeka krive ventilatora i krive sistema.
        """
        if system_resistance < 0.0:
            raise FanCurveError("System resistance cannot be negative.")

        denominator = self.coefficient_a + system_resistance
        if denominator == 0:
            raise FanCurveError("Denominator cannot be zero.")

        flow = math.sqrt(self.max_pressure / denominator)
        return round(flow, 3)
