"""
LAT-CES Module 015: Pressure Drop & Fan Power Engine
Dokument: LAT-SCI-MOD-0015
"""
from lat_ces.core.dimensions import Dimension, PRESSURE, POWER
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.equation import PhysicalEquation

class FanEngine:
    def __init__(self):
        self.fan_power_equation = PhysicalEquation(
            name="Snaga ventilatora (P = Q * delta_P)",
            expected_dimension=POWER,
            formula=lambda Q, delta_P: Q * delta_P
        )

    def calculate_fan_power(
        self,
        flow_rate: PhysicalQuantity,
        pressure_drop: PhysicalQuantity,
        efficiency: float = 1.0
    ) -> PhysicalQuantity:
        """
        Računa potrebnu snagu ventilatora (W) na osnovu protoka,
        pada pritiska i efikasnosti ventilatora (eta).
        """
        if efficiency <= 0 or efficiency > 1.0:
            raise ValueError("Stepen iskorištenja (efficiency) mora biti u opsegu (0, 1.0]!")

        raw_power = self.fan_power_equation.compute(Q=flow_rate, delta_P=pressure_drop)

        return PhysicalQuantity(
            value=raw_power.value / efficiency,
            dimension=POWER,
            uncertainty=raw_power.uncertainty / efficiency
        )
