"""
LAT-SCI-CORE-0023: Plenum Aerodynamic & Acoustic Noise Model Reference Implementation

The ``PlenumModel`` API remains the lightweight aerodynamic/acoustic model.
``PlenumEngine`` is the canonical home for the former ``lat_ces.modules.plenum``
quantity-based flow and mass-flow calculations.  The legacy module now only
re-exports that class as a compatibility facade.
"""
import math

from lat_ces.core.dimensions import AREA, DENSITY, FLOW_RATE, MASS_FLOW, VELOCITY
from lat_ces.scientific.quantity import PhysicalQuantity


class PlenumError(Exception):
    """Base exception for Plenum aerodynamic and acoustic calculations."""


class PlenumModel:
    """
    Models air velocity, pressure dynamics, and acoustic noise generation
    within ventilation plenum chambers.
    """

    def __init__(self, cross_section_area: float):
        if cross_section_area <= 0.0:
            raise PlenumError("Cross-section area must be strictly positive.")
        self.area = cross_section_area

    def compute_velocity(self, volumetric_flow: float) -> float:
        """Computes mean air velocity (v = Q / A) in m/s."""
        if volumetric_flow < 0.0:
            raise PlenumError("Volumetric flow cannot be negative.")
        return volumetric_flow / self.area

    def estimate_acoustic_noise(self, velocity: float) -> float:
        """
        Estimates aerodynamic noise level (dB) based on empirical velocity scaling
        (e.g., L_p ~ 50 * log10(v) + baseline factor).
        """
        if velocity < 0.0:
            raise PlenumError("Velocity cannot be negative.")
        if velocity == 0.0:
            return 0.0

        # Empirijska aproksimacija buke u plenumu
        baseline_db = 30.0
        noise_db = baseline_db + 50.0 * math.log10(velocity)
        return round(noise_db, 2)


class PlenumEngine:
    """Canonical quantity-based plenum flow engine.

    This class preserves the public calculation contract of the former
    ``lat_ces.modules.plenum.PlenumEngine`` while using the canonical
    scientific ``PhysicalQuantity`` implementation directly.
    """

    @staticmethod
    def _require_dimension(quantity: PhysicalQuantity, expected, name: str) -> None:
        if quantity.dimension != expected:
            raise ValueError(
                f"{name} must have dimension {expected}, got {quantity.dimension}"
            )

    def calculate_airflow(
        self, area: PhysicalQuantity, velocity: PhysicalQuantity
    ) -> PhysicalQuantity:
        """Calculate volumetric airflow (Q = A * v)."""
        self._require_dimension(area, AREA, "area")
        self._require_dimension(velocity, VELOCITY, "velocity")
        result = area * velocity
        return PhysicalQuantity(
            result.value,
            uncertainty=result.uncertainty,
            dimension=FLOW_RATE,
        )

    def calculate_mass_flow(
        self, density: PhysicalQuantity, flow_rate: PhysicalQuantity
    ) -> PhysicalQuantity:
        """Calculate mass flow (m_dot = rho * Q)."""
        self._require_dimension(density, DENSITY, "density")
        self._require_dimension(flow_rate, FLOW_RATE, "flow_rate")
        result = density * flow_rate
        return PhysicalQuantity(
            result.value,
            uncertainty=result.uncertainty,
            dimension=MASS_FLOW,
        )


__all__ = ["PlenumError", "PlenumModel", "PlenumEngine"]
