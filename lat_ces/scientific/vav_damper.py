class VAVError(Exception):
    pass


class VAVDamperModel:
    def __init__(self, max_flow: float):
        if max_flow <= 0.0:
            raise VAVError("Max flow must be positive.")
        self.max_flow = max_flow

    def compute_damper_position(self, requested_flow: float, current_pressure: float) -> float:
        """
        Računa poziciju VAV prigušivača (u procentima 0-100%) na osnovu traženog protoka.
        """
        if requested_flow < 0.0 or current_pressure < 0.0:
            raise VAVError("Flow and pressure cannot be negative.")

        ratio = min(1.0, requested_flow / self.max_flow)
        position_pct = ratio * 100.0
        return round(position_pct, 1)
