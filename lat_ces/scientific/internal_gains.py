class InternalGainsError(Exception):
    pass


class InternalGainsModel:
    def __init__(self):
        pass

    def compute_total_internal_gain(self, occupant_count: int, heat_per_person_w: float, lighting_power_w: float, lighting_usage_factor: float = 1.0) -> float:
        r"""
        Izračunava ukupne unutrašnje toplotne dobitke od ljudi i rasvjete (u W).
        Formula: Q_total = (N * q_person) + (P_lighting * F_usage)
        """
        if occupant_count < 0 or heat_per_person_w < 0.0 or lighting_power_w < 0.0:
            raise InternalGainsError("Occupant count, heat per person, and lighting power must be non-negative.")
        if not (0.0 <= lighting_usage_factor <= 1.0):
            raise InternalGainsError("Lighting usage factor must be between 0.0 and 1.0.")

        occupant_gain = occupant_count * heat_per_person_w
        lighting_gain = lighting_power_w * lighting_usage_factor

        total_gain = occupant_gain + lighting_gain
        return round(total_gain, 2)
