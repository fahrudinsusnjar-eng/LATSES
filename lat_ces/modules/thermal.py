"""
LAT-CES Module 014: Thermal & Thermodynamic Engine
Dokument: LAT-SCI-MOD-0014
"""
from lat_ces.core.dimensions import TEMPERATURE, SPECIFIC_HEAT, HEAT_RATE
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.equation import PhysicalEquation

class ThermalEngine:
    def __init__(self):
        self.heat_rate_equation = PhysicalEquation(
            name="Toplotna snaga (Q_dot = m_dot * cp * delta_T)",
            expected_dimension=HEAT_RATE,
            formula=lambda m_dot, cp, delta_T: m_dot * cp * delta_T
        )

    def calculate_heat_rate(
        self,
        mass_flow: PhysicalQuantity,
        specific_heat: PhysicalQuantity,
        delta_temp: PhysicalQuantity
    ) -> PhysicalQuantity:
        """Računa toplotnu snagu izmjene toplote u zraku (W)."""
        return self.heat_rate_equation.compute(
            m_dot=mass_flow,
            cp=specific_heat,
            delta_T=delta_temp
        )
