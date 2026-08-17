"""LAT-CES Module 018: Fan Affinity Laws Engine.

Compatibility/domain API. Scientific dimensions and quantities are imported
from canonical layers; this module does not depend on another legacy module.
"""
from lat_ces.core.dimensions import FLOW_RATE, PRESSURE, POWER
from lat_ces.scientific.quantity import PhysicalQuantity


class FanAffinityEngine:
    @staticmethod
    def scale_by_rpm(
        flow: PhysicalQuantity,
        pressure: PhysicalQuantity,
        power: PhysicalQuantity,
        n1_rpm: float,
        n2_rpm: float,
    ):
        """Scale fan flow, pressure and power using the affinity laws."""
        if n1_rpm <= 0 or n2_rpm <= 0:
            raise ValueError("Broj obrtaja (RPM) mora biti pozitivan!")

        ratio = n2_rpm / n1_rpm
        scaled_q = PhysicalQuantity(flow.value * ratio, FLOW_RATE, flow.uncertainty * ratio)
        scaled_p = PhysicalQuantity(
            pressure.value * (ratio**2), PRESSURE, pressure.uncertainty * (ratio**2)
        )
        scaled_w = PhysicalQuantity(
            power.value * (ratio**3), POWER, power.uncertainty * (ratio**3)
        )
        return scaled_q, scaled_p, scaled_w
