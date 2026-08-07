class DuctError(Exception):
    pass


class DuctFrictionModel:
    def __init__(self, friction_factor: float = 0.02):
        if friction_factor <= 0.0:
            raise DuctError("Friction factor must be positive.")
        self.friction_factor = friction_factor

    def compute_friction_loss(self, length_m: float, diameter_m: float, velocity_m_s: float, air_density: float = 1.2) -> float:
        r"""
        Izračunava pad pritiska u ravnom kanalu usljed trenja (Pa).
        Formula: dP = f * (L / D) * (rho * v^2 / 2)
        """
        if length_m < 0.0 or diameter_m <= 0.0 or velocity_m_s < 0.0:
            raise DuctError("Length, diameter, and velocity must be valid positive numbers.")

        dynamic_pressure = 0.5 * air_density * (velocity_m_s ** 2)
        pressure_loss = self.friction_factor * (length_m / diameter_m) * dynamic_pressure

        return round(pressure_loss, 2)
