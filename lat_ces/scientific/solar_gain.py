class SolarGainError(Exception):
    pass


class SolarGainModel:
    def __init__(self, shgc: float = 0.5):
        if not (0.0 <= shgc <= 1.0):
            raise SolarGainError("SHGC (Solar Heat Gain Coefficient) must be between 0.0 and 1.0.")
        self.shgc = shgc

    def compute_solar_gain(self, area_m2: float, solar_irradiance_W_m2: float) -> float:
        r"""
        Izračunava ukupni solarni toplotni dobitak kroz zastakljenu površinu (u W).
        Formula: Q_solar = A * I * SHGC
        """
        if area_m2 < 0.0 or solar_irradiance_W_m2 < 0.0:
            raise SolarGainError("Area and solar irradiance must be non-negative.")

        solar_gain = area_m2 * solar_irradiance_W_m2 * self.shgc
        return round(solar_gain, 2)
