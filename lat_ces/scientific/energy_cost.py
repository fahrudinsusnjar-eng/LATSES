class EnergyCostError(Exception):
    pass


class EnergyCostModel:
    def __init__(self, base_tariff_per_kwh: float):
        if base_tariff_per_kwh < 0.0:
            raise EnergyCostError("Tariff cannot be negative.")
        self.tariff = base_tariff_per_kwh

    def compute_operational_cost(self, power_kw: float, duration_hours: float, tariff_multiplier: float = 1.0) -> float:
        """
        Izračunava finansijski trošak utrošene električne energije za dati vremenski interval.
        """
        if power_kw < 0.0 or duration_hours < 0.0 or tariff_multiplier < 0.0:
            raise EnergyCostError("Inputs for cost calculation must be non-negative.")

        effective_tariff = self.tariff * tariff_multiplier
        cost = power_kw * duration_hours * effective_tariff
        return round(cost, 2)
