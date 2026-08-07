class StackEffectError(Exception):
    pass


class StackEffectModel:
    def __init__(self):
        pass

    def compute_stack_pressure(self, indoor_temp: float, outdoor_temp: float, height_m: float, rho_outdoor: float = 1.25, g: float = 9.81) -> float:
        r"""
        Izračunava razliku pritisaka usljed efekta dimnjaka (stack effect) u Pa.
        Formula: dP = rho_o * g * h * ((T_indoor_K - T_outdoor_K) / T_outdoor_K)
        """
        if height_m < 0.0:
            raise StackEffectError("Height must be non-negative.")

        t_in_k = indoor_temp + 273.15
        t_out_k = outdoor_temp + 273.15

        if t_out_k <= 0.0 or t_in_k <= 0.0:
            raise StackEffectError("Temperatures in Kelvin must be positive.")

        dp = rho_outdoor * g * height_m * ((t_in_k - t_out_k) / t_out_k)
        return round(dp, 2)
