"""Compatibility facade for the legacy duct-friction module.

Canonical duct-friction execution lives in ``lat_ces.scientific.duct_friction``.
This module preserves the legacy ``DuctFrictionEngine`` API for existing callers
while delegating the actual Darcy-Weisbach friction-loss calculation to the
canonical scientific model.
"""

import math

from lat_ces.core.dimensions import DENSITY, VELOCITY, LENGTH, DYNAMIC_VISCOSITY, PRESSURE
from lat_ces.scientific.duct_friction import DuctError, DuctFrictionModel
from lat_ces.scientific.quantity import PhysicalQuantity

VISCOSITY_AIR = DYNAMIC_VISCOSITY


class DuctFrictionEngine:
    """Legacy adapter around the canonical :class:`DuctFrictionModel`."""

    @staticmethod
    def _require_dimension(quantity: PhysicalQuantity, expected, name: str) -> None:
        if quantity.dimension != expected:
            raise ValueError(
                f"{name} must have dimension {expected}, got {quantity.dimension}"
            )

    @classmethod
    def calculate_reynolds_number(
        cls,
        density: PhysicalQuantity,
        velocity: PhysicalQuantity,
        hydraulic_diameter: PhysicalQuantity,
        dynamic_viscosity: PhysicalQuantity,
    ) -> float:
        cls._require_dimension(density, DENSITY, "density")
        cls._require_dimension(velocity, VELOCITY, "velocity")
        cls._require_dimension(hydraulic_diameter, LENGTH, "hydraulic_diameter")
        cls._require_dimension(dynamic_viscosity, DYNAMIC_VISCOSITY, "dynamic_viscosity")
        return (
            density.value * velocity.value * hydraulic_diameter.value
        ) / dynamic_viscosity.value

    @staticmethod
    def estimate_friction_factor(reynolds: float) -> float:
        if reynolds <= 0:
            raise ValueError("Reynoldsov broj mora biti pozitivan!")
        if reynolds < 2300.0:
            return 64.0 / reynolds
        return 0.3164 / (reynolds ** 0.25)

    def calculate_friction_loss(
        self,
        friction_factor: float,
        length: PhysicalQuantity,
        hydraulic_diameter: PhysicalQuantity,
        density: PhysicalQuantity,
        velocity: PhysicalQuantity,
    ) -> PhysicalQuantity:
        self._require_dimension(length, LENGTH, "length")
        self._require_dimension(hydraulic_diameter, LENGTH, "hydraulic_diameter")
        self._require_dimension(density, DENSITY, "density")
        self._require_dimension(velocity, VELOCITY, "velocity")

        canonical = DuctFrictionModel(friction_factor=friction_factor)
        value = canonical.compute_friction_loss(
            length_m=length.value,
            diameter_m=hydraulic_diameter.value,
            velocity_m_s=velocity.value,
            air_density=density.value,
        )

        # Preserve the legacy uncertainty contract while delegating the
        # actual friction-loss calculation to the canonical scientific model.
        u_rel = math.sqrt(
            (length.uncertainty / length.value) ** 2
            + (hydraulic_diameter.uncertainty / hydraulic_diameter.value) ** 2
            + (density.uncertainty / density.value) ** 2
            + (2.0 * velocity.uncertainty / velocity.value) ** 2
        )
        return PhysicalQuantity(
            value=value,
            dimension=PRESSURE,
            uncertainty=value * u_rel,
        )


__all__ = ["DuctError", "DuctFrictionEngine", "VISCOSITY_AIR"]
