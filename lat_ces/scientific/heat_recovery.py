class HeatRecoveryError(Exception):
    pass


class HeatRecoveryModel:
    def __init__(self, nominal_effectiveness: float = 0.75):
        if not (0.0 <= nominal_effectiveness <= 1.0):
            raise HeatRecoveryError("Effectiveness must be between 0.0 and 1.0.")
        self.effectiveness = nominal_effectiveness

    def compute_supply_outlet_temp(self, supply_in: float, exhaust_in: float) -> float:
        """
        Izračunava izlaznu temperaturu svježeg zraka nakon prolaska kroz rekuperator.
        Formula: T_sup_out = T_sup_in + effectiveness * (T_ex_in - T_sup_in)
        """
        if exhaust_in < supply_in and self.effectiveness > 0:
            # Moguće hlađenje ili obrnuti režim, ali standardno računamo razliku
            pass

        supply_out = supply_in + self.effectiveness * (exhaust_in - supply_in)
        return round(supply_out, 2)
