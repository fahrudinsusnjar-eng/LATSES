class HumidityError(Exception):
    """Base exception for humidity and condensation calculations."""
    pass


class HumidityModel:
    """
    Evaluates moisture levels and condensation risks in HVAC environments.
    """

    def evaluate_condensation_risk(self, relative_humidity: float, surface_temp: float, dew_point: float) -> str:
        """Categorizes condensation risk based on surface temperature and dew point."""
        if not (0.0 <= relative_humidity <= 100.0):
            raise HumidityError("Relative humidity must be between 0.0 and 100.0.")

        if surface_temp <= dew_point or relative_humidity >= 90.0:
            return "HIGH_RISK"
        elif relative_humidity >= 75.0:
            return "MODERATE_RISK"
        else:
            return "SAFE"
