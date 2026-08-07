import math


class DuctLossError(Exception):
    pass


class DuctLossModel:
    def __init__(self, surface_area: float, overall_heat_transfer_coef: float):
        if surface_area < 0.0 or overall_heat_transfer_coef < 0.0:
            raise DuctLossError("Surface area and heat transfer coefficient must be non-negative.")
        self.area = surface_area
        self.u_coef = overall_heat_transfer_coef

    def compute_outlet_temperature(self, inlet_temp: float, ambient_temp: float, mass_flow: float, specific_heat: float = 1005.0) -> float:
        """
        Računa izlaznu temperaturu zraka iz kanala primjenom eksponencijalnog zakona hlađenja/grijanja.
        Formula: T_out = T_amb + (T_in - T_amb) * exp(- (U * A) / (m_dot * Cp))
        """
        if mass_flow <= 0.0 or specific_heat <= 0.0:
            raise DuctLossError("Mass flow and specific heat must be positive.")

        exponent = - (self.u_coef * self.area) / (mass_flow * specific_heat)
        outlet_temp = ambient_temp + (inlet_temp - ambient_temp) * math.exp(exponent)
        return round(outlet_temp, 2)
