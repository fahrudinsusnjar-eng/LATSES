"""
LAT-CES Module 014: Thermal & Thermodynamic Engine
Dokument: LAT-SCI-MOD-0014
"""
from lat_ces.core.dimensions import TEMPERATURE, SPECIFIC_HEAT, HEAT_RATE, MASS_FLOW
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.equation import PhysicalEquation

class ThermalEngine:
    def __init__(self):
        self.heat_rate_equation = PhysicalEquation(
            name="Toplotna snaga (Q_dot = m_dot * cp * delta_T)",
            expected_dimension=HEAT_RATE,
            formula=lambda m_dot, cp, delta_T: m_dot * cp * delta_T
        )

    @staticmethod
    def _require_dimension(quantity: PhysicalQuantity, expected, name: str) -> None:
        if quantity.dimension != expected:
            raise ValueError(
                f"{name} must have dimension {expected}, got {quantity.dimension}"
            )

    def calculate_heat_rate(
        self,
        mass_flow: PhysicalQuantity,
        specific_heat: PhysicalQuantity,
        delta_temp: PhysicalQuantity
    ) -> PhysicalQuantity:
        """Računa toplotnu snagu izmjene toplote u zraku (W)."""
        self._require_dimension(mass_flow, MASS_FLOW, "mass_flow")
        self._require_dimension(specific_heat, SPECIFIC_HEAT, "specific_heat")
        self._require_dimension(delta_temp, TEMPERATURE, "delta_temp")
        return self.heat_rate_equation.compute(
            m_dot=mass_flow,
            cp=specific_heat,
            delta_T=delta_temp
        )
