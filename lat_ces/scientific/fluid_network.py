"""Canonical HVAC fluid-network integration.

This module composes the existing scientific pressure-drop, duct-friction and
fan-curve models without changing their individual behavior. It provides one
network-level API for total system pressure loss and the fan operating point.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

from .duct_friction import DuctFrictionModel
from .fan_curve import FanCurveModel
from .pressure_drop import PressureDropModel


class FluidNetworkError(ValueError):
    """Raised when a fluid-network definition is physically invalid."""


@dataclass(frozen=True)
class FluidSegment:
    """Straight duct segment plus a lumped local-loss coefficient."""

    name: str
    length_m: float
    diameter_m: float
    velocity_m_s: float
    friction_factor: float = 0.02
    loss_coefficient: float = 0.0

    def validate(self) -> None:
        if not self.name:
            raise FluidNetworkError("Segment name must not be empty.")
        if self.length_m < 0.0:
            raise FluidNetworkError("Segment length cannot be negative.")
        if self.diameter_m <= 0.0:
            raise FluidNetworkError("Segment diameter must be positive.")
        if self.velocity_m_s < 0.0:
            raise FluidNetworkError("Segment velocity cannot be negative.")
        if self.friction_factor <= 0.0:
            raise FluidNetworkError("Segment friction factor must be positive.")
        if self.loss_coefficient < 0.0:
            raise FluidNetworkError("Local loss coefficient cannot be negative.")


class FluidNetwork:
    """Compose pressure, duct and fan models into one deterministic API."""

    def __init__(
        self,
        segments: Iterable[FluidSegment],
        *,
        air_density: float = 1.2,
        fan_max_pressure: float = 500.0,
        fan_coefficient_a: float = 200.0,
    ) -> None:
        if air_density <= 0.0:
            raise FluidNetworkError("Air density must be positive.")
        self.segments: Tuple[FluidSegment, ...] = tuple(segments)
        for segment in self.segments:
            segment.validate()

        self.air_density = air_density
        self.pressure_model = PressureDropModel(loss_coefficient=1.0, air_density=air_density)
        self.fan_model = FanCurveModel(
            max_pressure=fan_max_pressure,
            coefficient_a=fan_coefficient_a,
        )

    def segment_pressure_drop(self, segment: FluidSegment) -> float:
        """Return total straight-friction + local-loss pressure drop for one segment."""
        segment.validate()
        friction_model = DuctFrictionModel(friction_factor=segment.friction_factor)
        friction_dp = friction_model.compute_friction_loss(
            length_m=segment.length_m,
            diameter_m=segment.diameter_m,
            velocity_m_s=segment.velocity_m_s,
            air_density=self.air_density,
        )
        local_model = PressureDropModel(
            loss_coefficient=segment.loss_coefficient,
            air_density=self.air_density,
        )
        local_dp = local_model.compute_pressure_drop(segment.velocity_m_s)
        return round(friction_dp + local_dp, 2)

    def total_pressure_drop(self) -> float:
        """Return the sum of pressure losses across all series segments."""
        return round(sum(self.segment_pressure_drop(segment) for segment in self.segments), 2)

    def system_resistance(self) -> float:
        """Return equivalent Q² resistance implied by the configured segment states.

        The resistance is derived from the current segment velocities and therefore
        is intended for the existing fan-curve model, not as a new physics model.
        """
        total = 0.0
        for segment in self.segments:
            if segment.velocity_m_s == 0.0:
                continue
            total += self.segment_pressure_drop(segment) / (segment.velocity_m_s ** 2)
        return round(total, 6)

    def solve_operating_flow(self) -> float:
        """Return the fan operating flow from the existing fan-curve equation."""
        return self.fan_model.compute_operating_flow(self.system_resistance())

    def evaluate(self) -> dict:
        """Return a stable network-level result for downstream integration."""
        return {
            "segment_count": len(self.segments),
            "total_pressure_drop_pa": self.total_pressure_drop(),
            "system_resistance": self.system_resistance(),
            "operating_flow": self.solve_operating_flow(),
        }


__all__ = ["FluidNetwork", "FluidNetworkError", "FluidSegment"]
