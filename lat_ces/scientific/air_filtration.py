class FiltrationError(Exception):
    pass


class AirFiltrationModel:
    def __init__(self, initial_pressure_drop: float, dust_capacity_factor: float):
        if initial_pressure_drop < 0.0 or dust_capacity_factor <= 0.0:
            raise FiltrationError("Initial pressure drop and dust capacity factor must be valid.")
        self.initial_dp = initial_pressure_drop
        self.capacity_factor = dust_capacity_factor

    def compute_current_pressure_drop(self, accumulated_dust_grams: float) -> float:
        r"""
        Računa trenutni pad pritiska na filteru (u Pa) u zavisnosti od nakupljene prašine.
        Formula: $\Delta P = \Delta P_0 + k \cdot m_{\text{dust}}$
        """
        if accumulated_dust_grams < 0.0:
            raise FiltrationError("Accumulated dust cannot be negative.")

        current_dp = self.initial_dp + (self.capacity_factor * accumulated_dust_grams)
        return round(current_dp, 2)
