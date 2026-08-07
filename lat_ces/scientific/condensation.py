import math


class CondensationError(Exception):
    pass


class CondensationModel:
    def __init__(self):
        pass

    def compute_dew_point(self, air_temp: float, rel_humidity: float) -> float:
        """
        Magnusova formula za izračunavanje temperature rosišta (°C).
        """
        if not (0.0 <= rel_humidity <= 100.0):
            raise CondensationError("Relative humidity must be between 0 and 100%.")

        a = 17.27
        b = 237.7
        alpha = ((a * air_temp) / (b + air_temp)) + math.log(rel_humidity / 100.0)
        dew_point = (b * alpha) / (a - alpha)
        return round(dew_point, 2)

    def evaluate_condensation_risk(self, air_temp: float, rel_humidity: float, surface_temp: float) -> bool:
        """
        vraća True ako je temperatura površine manja ili jednaka tački rosišta (postoji rizik od kondenzacije).
        """
        dew_point = self.compute_dew_point(air_temp, rel_humidity)
        return surface_temp <= dew_point
