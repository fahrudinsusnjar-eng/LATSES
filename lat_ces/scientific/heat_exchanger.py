import math


class HeatExchangerError(Exception):
    pass


class HeatExchangerNTUModel:
    def __init__(self):
        pass

    def compute_counterflow_effectiveness(self, ntu: float, capacity_ratio: float) -> float:
        r"""
        Izračunava efikasnost protustrujnog izmjenjivača toplote pomoću NTU metode.
        Formula: epsilon = (1 - exp(-NTU * (1 - C_r))) / (1 - C_r * exp(-NTU * (1 - C_r)))
        """
        if ntu < 0.0 or not (0.0 <= capacity_ratio <= 1.0):
            raise HeatExchangerError("NTU must be non-negative and capacity ratio between 0.0 and 1.0.")

        if capacity_ratio == 1.0:
            effectiveness = ntu / (1.0 + ntu)
        else:
            num = 1.0 - math.exp(-ntu * (1.0 - capacity_ratio))
            den = 1.0 - capacity_ratio * math.exp(-ntu * (1.0 - capacity_ratio))
            effectiveness = num / den

        return round(effectiveness, 4)
