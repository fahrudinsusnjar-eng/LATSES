import math


class VAVTerminalError(Exception):
    pass


class VAVTerminalModel:
    def __init__(self, max_flow: float, k_factor: float = 0.01):
        if max_flow <= 0.0 or k_factor <= 0.0:
            raise VAVTerminalError("Max flow and k_factor must be positive.")
        self.max_flow = max_flow
        self.k_factor = k_factor

    def compute_vav_flow(self, damper_position_pct: float, pressure_drop_pa: float) -> float:
        r"""
        Izračunava protok zraka kroz VAV terminalnu jedinicu (u m3/s).
        Formula koristi aproksimaciju baziranu na položaju klapne i kvadratnom korijenu pada pritiska.
        """
        if not (0.0 <= damper_position_pct <= 100.0):
            raise VAVTerminalError("Damper position must be between 0 and 100%.")
        if pressure_drop_pa < 0.0:
            raise VAVTerminalError("Pressure drop cannot be negative.")

        position_fraction = damper_position_pct / 100.0
        calculated_flow = self.k_factor * position_fraction * math.sqrt(pressure_drop_pa)

        # Ograničenje na maksimalni projektovani protok VAV kutije
        return round(min(calculated_flow, self.max_flow), 4)
