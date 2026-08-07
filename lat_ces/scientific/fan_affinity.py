class FanAffinityError(Exception):
    pass


class FanAffinityModel:
    def __init__(self, base_rpm: float, base_flow: float, base_pressure: float, base_power: float):
        if base_rpm <= 0.0 or base_flow < 0.0 or base_pressure < 0.0 or base_power < 0.0:
            raise FanAffinityError("Base parameters must be valid non-negative values, RPM must be positive.")
        self.base_rpm = base_rpm
        self.base_flow = base_flow
        self.base_pressure = base_pressure
        self.base_power = base_power

    def scale_performance(self, new_rpm: float) -> tuple:
        """
        Izračunava novi protok, pritisak i snagu na osnovu promjene broja obrtaja (RPM).
        Zakoni srodnosti:
        - Q2 = Q1 * (N2 / N1)
        - P2 = P1 * (N2 / N1)^2
        - Power2 = Power1 * (N2 / N1)^3
        """
        if new_rpm < 0.0:
            raise FanAffinityError("New RPM cannot be negative.")

        ratio = new_rpm / self.base_rpm

        new_flow = self.base_flow * ratio
        new_pressure = self.base_pressure * (ratio ** 2)
        new_power = self.base_power * (ratio ** 3)

        return round(new_flow, 3), round(new_pressure, 2), round(new_power, 3)
