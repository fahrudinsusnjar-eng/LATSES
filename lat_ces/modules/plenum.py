"""
LAT-CES Module 012: Air Plenum & Fluid Dynamics Engine
Dokument: LAT-SCI-MOD-0012
"""
from lat_ces.core.dimensions import VELOCITY, AREA, FLOW_RATE, DENSITY, MASS_FLOW
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.equation import PhysicalEquation


class PlenumEngine:
    """Fluid-flow engine with explicit canonical physical-dimension contracts."""

    @staticmethod
    def _require_dimension(quantity: PhysicalQuantity, expected, name: str) -> None:
        if quantity.dimension != expected:
            raise ValueError(
                f"{name} must have dimension {expected}, got {quantity.dimension}"
            )

    def __init__(self):
        self.flow_equation = PhysicalEquation(
            name="Volumetrijski protok (Q = A * v)",
            expected_dimension=FLOW_RATE,
            formula=lambda area, velocity: area * velocity,
        )
        self.mass_flow_equation = PhysicalEquation(
            name="Maseni protok (m_dot = rho * Q)",
            expected_dimension=MASS_FLOW,
            formula=lambda density, flow_rate: density * flow_rate,
        )

    def calculate_airflow(self, area: PhysicalQuantity, velocity: PhysicalQuantity) -> PhysicalQuantity:
        """Računa volumetrijski protok zraka u plenumu."""
        self._require_dimension(area, AREA, "area")
        self._require_dimension(velocity, VELOCITY, "velocity")
        return self.flow_equation.compute(area=area, velocity=velocity)

    def calculate_mass_flow(self, density: PhysicalQuantity, flow_rate: PhysicalQuantity) -> PhysicalQuantity:
        """Računa maseni protok zraka."""
        self._require_dimension(density, DENSITY, "density")
        self._require_dimension(flow_rate, FLOW_RATE, "flow_rate")
        return self.mass_flow_equation.compute(density=density, flow_rate=flow_rate)
