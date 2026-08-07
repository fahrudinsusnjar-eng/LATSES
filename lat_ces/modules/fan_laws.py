"""
LAT-CES Module 018: Fan Affinity Laws Engine
Dokument: LAT-SCI-MOD-0018
"""
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import FLOW_RATE
from lat_ces.modules.pressure import PRESSURE, POWER

class FanAffinityEngine:
    @staticmethod
    def scale_by_rpm(
        flow: PhysicalQuantity,
        pressure: PhysicalQuantity,
        power: PhysicalQuantity,
        n1_rpm: float,
        n2_rpm: float
    ):
        """
        Preračunava parametre ventilatora pri promjeni obrtaja sa n1 na n2:
        Q2 = Q1 * (n2/n1)
        P2 = P1 * (n2/n1)^2
        W2 = W1 * (n2/n1)^3
        """
        if n1_rpm <= 0 or n2_rpm <= 0:
            raise ValueError("Broj obrtaja (RPM) mora biti pozitivan!")

        ratio = n2_rpm / n1_rpm

        scaled_q = PhysicalQuantity(flow.value * ratio, FLOW_RATE, flow.uncertainty * ratio)
        scaled_p = PhysicalQuantity(pressure.value * (ratio**2), PRESSURE, pressure.uncertainty * (ratio**2))
        scaled_w = PhysicalQuantity(power.value * (ratio**3), POWER, power.uncertainty * (ratio**3))

        return scaled_q, scaled_p, scaled_w