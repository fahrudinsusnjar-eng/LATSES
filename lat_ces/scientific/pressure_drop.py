class PressureError(Exception):
    pass


class PressureDropModel:
    def __init__(self, loss_coefficient: float, air_density: float = 1.2):
        if loss_coefficient < 0.0 or air_density <= 0.0:
            raise PressureError("Invalid physical parameters for pressure drop.")
        self.k = loss_coefficient
        self.rho = air_density

    def compute_pressure_drop(self, velocity: float) -> float:
        """Computes dynamic pressure drop in Pascals (Pa): dP = K * rho * v^2 / 2"""
        if velocity < 0.0:
            raise PressureError("Velocity cannot be negative.")
        dp = self.k * self.rho * (velocity ** 2) / 2.0
        return round(dp, 2)
