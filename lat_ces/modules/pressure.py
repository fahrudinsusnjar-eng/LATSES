"""
LAT-CES Module 015: Pressure Drop & Fan Power Engine
Dokument: LAT-SCI-MOD-0015

Compatibility facade. Canonical pressure-drop physics lives in
``lat_ces.scientific.pressure_drop``; this module preserves the legacy API.
"""

from lat_ces.core.dimensions import FLOW_RATE, PRESSURE, POWER
from lat_ces.scientific.pressure_drop import PressureDropModel, PressureError
from lat_ces.scientific.quantity import PhysicalQuantity


class PressureDropEngine:
    """Legacy adapter for the canonical scientific pressure-drop model."""

    def __init__(self, loss_coefficient: float, air_density: float = 1.2):
        self._model = PressureDropModel(
            loss_coefficient=loss_coefficient,
            air_density=air_density,
        )

    def compute_pressure_drop(self, velocity: float) -> float:
        return self._model.compute_pressure_drop(velocity)


class FanEngine:
    """Compatibility facade for the legacy fan-power API."""

    @staticmethod
    def _require_dimension(quantity: PhysicalQuantity, expected, name: str) -> None:
        if quantity.dimension != expected:
            raise ValueError(
                f"{name} must have dimension {expected}, got {quantity.dimension}"
            )

    def calculate_fan_power(
        self,
        flow_rate: PhysicalQuantity,
        pressure_drop: PhysicalQuantity,
        efficiency: float = 1.0,
    ) -> PhysicalQuantity:
        """Calculate fan power P = Q * ΔP / η while preserving the legacy API."""
        if efficiency <= 0 or efficiency > 1.0:
            raise ValueError("Stepen iskorištenja (efficiency) mora biti u opsegu (0, 1.0]!")

        self._require_dimension(flow_rate, FLOW_RATE, "flow_rate")
        self._require_dimension(pressure_drop, PRESSURE, "pressure_drop")

        raw_power = flow_rate * pressure_drop
        return PhysicalQuantity(
            value=raw_power.value / efficiency,
            dimension=POWER,
            uncertainty=raw_power.uncertainty / efficiency,
        )


__all__ = ["FanEngine", "PressureDropEngine", "PressureDropModel", "PressureError"]
