import math


class DuctLeakageError(Exception):
    pass


class DuctLeakageModel:
    def __init__(self, leakage_factor: float, pressure_exponent: float = 0.65):
        if leakage_factor < 0.0:
            raise DuctLeakageError("Leakage factor must be non-negative.")
        self.factor = leakage_factor
        self.exponent = pressure_exponent

    def compute_leakage_flow(self, static_pressure: float, surface_area: float) -> float:
        """
        Računa zapreminski protok curenja zraka (u m3/s) na osnovu statičkog pritiska i površine kanala.
        Formula: Q_leak = C * A * P^n
        """
        if static_pressure < 0.0 or surface_area < 0.0:
            raise DuctLeakageError("Static pressure and surface area cannot be negative.")

        # Osnovna aproksimacija curenja zraka prema standardima
        leakage = self.factor * surface_area * math.pow(static_pressure, self.exponent)
        return round(leakage, 4)
