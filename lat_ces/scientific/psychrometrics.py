import math


class PsychrometricsError(Exception):
    pass


class PsychrometricsModel:
    def __init__(self, atmospheric_pressure_kpa: float = 101.325):
        if atmospheric_pressure_kpa <= 0.0:
            raise PsychrometricsError("Pressure must be positive.")
        self.pressure = atmospheric_pressure_kpa

    def compute_air_enthalpy(self, dry_bulb_temp: float, rel_humidity: float) -> float:
        """
        Inženjerska aproksimacija specifične entalpije vlažnog zraka (kJ/kg).
        """
        if not (0.0 <= rel_humidity <= 100.0):
            raise PsychrometricsError("Relative humidity must be between 0 and 100%.")

        p_sat = 0.61078 * math.exp((17.27 * dry_bulb_temp) / (dry_bulb_temp + 237.3))
        p_v = (rel_humidity / 100.0) * p_sat

        w = 0.622 * p_v / (self.pressure - p_v)
        enthalpy = 1.006 * dry_bulb_temp + w * (2501.0 + 1.86 * dry_bulb_temp)
        return round(enthalpy, 2)
