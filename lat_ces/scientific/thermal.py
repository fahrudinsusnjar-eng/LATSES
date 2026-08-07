"""
LAT-SCI-CORE-0026: Thermal Dynamics & Heat Transfer Model Reference Implementation
"""


class ThermalError(Exception):
    """Base exception for thermal dynamics calculations."""


class ThermalModel:
    """
    Models heat transfer and thermal energy distribution within ventilation circuits.
    """

    def __init__(self, specific_heat_capacity: float = 1005.0):
        if specific_heat_capacity <= 0.0:
            raise ThermalError("Specific heat capacity must be strictly positive.")
        self.cp = specific_heat_capacity

    def compute_heat_transfer(self, mass_flow: float, delta_temp: float) -> float:
        """Computes thermal heat flux in Watts (W)."""
        if mass_flow < 0.0:
            raise ThermalError("Mass flow cannot be negative.")
        heat_flux = mass_flow * self.cp * delta_temp
        return round(heat_flux, 2)
