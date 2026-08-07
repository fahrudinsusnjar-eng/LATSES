"""
LAT-CES Module 019: Psychrometrics & Humidity Engine
Dokument: LAT-SCI-MOD-0019
"""
import math

class PsychrometricEngine:
    @staticmethod
    def saturation_vapor_pressure_pa(temp_celsius: float) -> float:
        """Pritisak zasićenja vodene pare u Paskalima (Magnusova formula)."""
        return 610.78 * math.exp((17.27 * temp_celsius) / (temp_celsius + 237.3))

    @staticmethod
    def calculate_relative_humidity(actual_vapor_pressure_pa: float, temp_celsius: float) -> float:
        """Računa relativnu vlažnost zraka RH (%) = (p_v / p_sat) * 100."""
        p_sat = PsychrometricEngine.saturation_vapor_pressure_pa(temp_celsius)
        if p_sat <= 0:
            return 0.0
        rh = (actual_vapor_pressure_pa / p_sat) * 100.0
        return min(max(rh, 0.0), 100.0)