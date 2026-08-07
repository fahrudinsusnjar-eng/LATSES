class BoilerError(Exception):
    pass


class BoilerModel:
    def __init__(self, efficiency: float = 0.9):
        if not (0.0 < efficiency <= 1.0):
            raise BoilerError("Boiler efficiency must be between 0.0 (exclusive) and 1.0.")
        self.efficiency = efficiency

    def compute_fuel_consumption(self, heat_output_kW: float, heating_value_kWh_m3: float) -> float:
        r"""
        Izračunava potrošnju goriva (m3/h) na osnovu toplotnog učinka i ogrjevne moći.
        Formula: V_fuel = Q_out / (eta * H_i)
        """
        if heat_output_kW < 0.0 or heating_value_kWh_m3 <= 0.0:
            raise BoilerError("Heat output must be non-negative and heating value must be positive.")

        fuel_consumption = heat_output_kW / (self.efficiency * heating_value_kWh_m3)
        return round(fuel_consumption, 3)
