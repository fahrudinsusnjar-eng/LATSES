import math


class ThermalComfortError(Exception):
    pass


class ThermalComfortModel:
    def __init__(self, metabolic_rate: float = 1.2, clothing_insulation: float = 0.5):
        # metabolic_rate u met (1.2 ~ sjedenje/kancelarijski rad), clothing_insulation u clo (0.5 ~ ljetna odjeća)
        if metabolic_rate <= 0.0 or clothing_insulation < 0.0:
            raise ThermalComfortError("Metabolic rate and clothing insulation must be valid positive values.")
        self.met = metabolic_rate
        self.clo = clothing_insulation

    def compute_pmv_ppd(self, air_temp: float, mean_rad_temp: float, air_velocity: float, rel_humidity: float) -> tuple:
        """
        Pojednostavljena inženjerska aproksimacija ISO 7730 standarda za PMV i PPD.
        """
        if air_velocity < 0.0 or not (0.0 <= rel_humidity <= 100.0):
            raise ThermalComfortError("Invalid environmental parameters.")

        # Pojednostavljeni termalni balans za brzu procjenu u real-time sistemu
        t_diff = air_temp - 24.0
        pmv = 0.303 * math.exp(-0.036 * 50.0 + 0.028) * (t_diff * 1.5 - 0.05 * (air_velocity * 100.0))
        pmv = round(max(-3.0, min(3.0, pmv)), 2)

        # Izračun PPD na osnovu PMV
        ppd = 100.0 - 95.0 * math.exp(-0.03353 * math.pow(pmv, 4.0) - 0.2179 * math.pow(pmv, 2.0))
        ppd = round(max(0.0, min(100.0, ppd)), 1)

        return pmv, ppd
