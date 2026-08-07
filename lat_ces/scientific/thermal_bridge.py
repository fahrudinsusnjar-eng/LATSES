class ThermalBridgeError(Exception):
    pass


class ThermalBridgeModel:
    def __init__(self):
        pass

    def compute_linear_heat_loss(self, psi_value: float, length_m: float, temp_diff: float) -> float:
        r"""
        Izračunava toplotne gubitke kroz linijski toplinski most (u W).
        Formula: Phi = psi * L * dT
        """
        if psi_value < 0.0 or length_m < 0.0 or temp_diff < 0.0:
            raise ThermalBridgeError("Psi value, length, and temperature difference must be non-negative.")

        heat_loss = psi_value * length_m * temp_diff
        return round(heat_loss, 2)
