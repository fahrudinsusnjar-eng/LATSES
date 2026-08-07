class CoilError(Exception):
    pass


class CoilPerformanceModel:
    def __init__(self, effectiveness: float = 0.8):
        if not (0.0 <= effectiveness <= 1.0):
            raise CoilError("Coil effectiveness must be between 0.0 and 1.0.")
        self.effectiveness = effectiveness

    def compute_coil_heat_transfer(self, air_mass_flow: float, entering_temp: float, coil_surface_temp: float, specific_heat: float = 1005.0) -> float:
        r"""
        Izračunava ukupni toplotni učinak zavojnice (grijanje ili hlađenje) u W.
        Formula: $Q = \dot{m} C_p \varepsilon (T_{\text{in}} - T_{\text{surface}})$
        """
        if air_mass_flow < 0.0 or specific_heat <= 0.0:
            raise CoilError("Air mass flow and specific heat must be positive.")

        q_transfer = air_mass_flow * specific_heat * self.effectiveness * (entering_temp - coil_surface_temp)
        return round(q_transfer, 2)
