"""
LAT-CES Module 014: Thermal & Thermodynamic Engine
Dokument: LAT-SCI-MOD-0014
"""
from lat_ces.core.dimensions import Dimension, MASS, TIME
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.equation import PhysicalEquation

# Definisanje specifičnih termodinamičkih dimenzija
TEMPERATURE = Dimension(Theta=1)                                # Kelvin (K)
SPECIFIC_HEAT = Dimension(L=2, T=-2, Theta=-1)                  # J / (kg * K) -> m² / (s² * K)
HEAT_RATE = Dimension(M=1, L=2, T=-3)                           # Watt (W) -> kg * m² / s³

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