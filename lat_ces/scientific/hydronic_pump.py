class PumpError(Exception):
    pass


class HydronicPumpModel:
    def __init__(self, pump_efficiency: float = 0.75):
        if not (0.0 < pump_efficiency <= 1.0):
            raise PumpError("Pump efficiency must be between 0 (exclusive) and 1.0.")
        self.efficiency = pump_efficiency

    def compute_pump_power(self, flow_rate_m3h: float, head_kPa: float) -> float:
        r"""
        Izračunava električnu snagu pumpe (u W).
        Formula: P = (Q * dp) / (3.6 * eta)
        Gdje je Q u m3/h, dp u kPa, a eta ukupna efikasnost pumpe.
        """
        if flow_rate_m3h < 0.0 or head_kPa < 0.0:
            raise PumpError("Flow rate and head pressure cannot be negative.")

        # Q (m3/h) * 1000 (Pa/kPa) / 3600 (s/h) = kW ili direktno W sa faktorom konverzije
        power_watts = (flow_rate_m3h * head_kPa * 1000.0) / (3600.0 * self.efficiency)
        return round(power_watts, 2)
