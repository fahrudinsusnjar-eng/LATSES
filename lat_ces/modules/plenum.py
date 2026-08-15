"""
LAT-CES Module 012: Air Plenum & Fluid Dynamics Engine
Dokument: LAT-SCI-MOD-0012
"""
from lat_ces.core.dimensions import (
    Dimension,
    LENGTH,
    TIME,
    VELOCITY,
    MASS,
    AREA,
    FLOW_RATE,
    DENSITY,
    MASS_FLOW,
)
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.equation import PhysicalEquation

class PlenumEngine:
    def __init__(self):
        self.flow_equation = PhysicalEquation(
            name="Volumetrijski protok (Q = A * v)",
            expected_dimension=FLOW_RATE,
            formula=lambda area, velocity: area * velocity
        )
        self.mass_flow_equation = PhysicalEquation(
            name="Maseni protok (m_dot = rho * Q)",
            expected_dimension=MASS_FLOW,
            formula=lambda density, flow_rate: density * flow_rate
        )

    def calculate_airflow(self, area: PhysicalQuantity, velocity: PhysicalQuantity) -> PhysicalQuantity:
        """Računa volumetrijski protok zraka u plenumu."""
        return self.flow_equation.compute(area=area, velocity=velocity)

    def calculate_mass_flow(self, density: PhysicalQuantity, flow_rate: PhysicalQuantity) -> PhysicalQuantity:
        """Računa maseni protok zraka."""
        return self.mass_flow_equation.compute(density=density, flow_rate=flow_rate)
