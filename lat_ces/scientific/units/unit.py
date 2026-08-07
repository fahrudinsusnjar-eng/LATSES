"""
LAT-CES Scientific Core
Unit Engine Reference Implementation (LAT-SCI-CORE-0016)
"""

from dataclasses import dataclass
from typing import Dict, Optional

from lat_ces.scientific.units.dimension import (
    ACCELERATION,
    AMOUNT,
    CURRENT,
    FORCE,
    LENGTH,
    LUMINOUS_INTENSITY,
    MASS,
    TEMPERATURE,
    TIME,
    VELOCITY,
    Dimension,
)


class UnitError(Exception):
    """Base exception for Unit engine operations."""

    pass


@dataclass(frozen=True)
class Unit:
    """
    Represents a physical unit bound to a Dimension.
    """

    name: str
    symbol: str
    dimension: Dimension
    scale_factor: float = 1.0
    offset: float = 0.0

    def __post_init__(self):
        if not self.name or not self.symbol:
            raise UnitError("Unit requires valid name and symbol.")
        if not isinstance(self.dimension, Dimension):
            raise UnitError("Unit must be bound to a valid Dimension instance.")
        if self.scale_factor <= 0:
            raise UnitError("Scale factor must be strictly positive.")

    def is_compatible(self, other: "Unit") -> bool:
        """Checks if two units share the same physical dimension."""
        if not isinstance(other, Unit):
            return False
        return self.dimension == other.dimension

    def get_conversion_factor_to(self, target_unit: "Unit") -> float:
        """Calculates scale factor to convert value to target unit."""
        if not self.is_compatible(target_unit):
            raise UnitError(f"Incompatible unit conversion: {self.symbol} -> {target_unit.symbol}")
        return self.scale_factor / target_unit.scale_factor

    def __mul__(self, other: "Unit") -> "Unit":
        if not isinstance(other, Unit):
            raise UnitError("Can only multiply Unit with another Unit.")
        new_dim = self.dimension * other.dimension
        return Unit(
            name=f"{self.name}*{other.name}",
            symbol=f"{self.symbol}*{other.symbol}",
            dimension=new_dim,
            scale_factor=self.scale_factor * other.scale_factor,
        )

    def __truediv__(self, other: "Unit") -> "Unit":
        if not isinstance(other, Unit):
            raise UnitError("Can only divide Unit by another Unit.")
        new_dim = self.dimension / other.dimension
        return Unit(
            name=f"{self.name}/{other.name}",
            symbol=f"{self.symbol}/{other.symbol}",
            dimension=new_dim,
            scale_factor=self.scale_factor / other.scale_factor,
        )


METER = Unit("meter", "m", LENGTH, 1.0)
KILOGRAM = Unit("kilogram", "kg", MASS, 1.0)
SECOND = Unit("second", "s", TIME, 1.0)
AMPERE = Unit("ampere", "A", CURRENT, 1.0)
KELVIN = Unit("kelvin", "K", TEMPERATURE, 1.0)
MOLE = Unit("mole", "mol", AMOUNT, 1.0)
CANDELA = Unit("candela", "cd", LUMINOUS_INTENSITY, 1.0)

NEWTON = Unit("newton", "N", FORCE, 1.0)
METER_PER_SECOND = METER / SECOND

SI_REGISTRY: Dict[str, Unit] = {
    "m": METER,
    "kg": KILOGRAM,
    "s": SECOND,
    "A": AMPERE,
    "K": KELVIN,
    "mol": MOLE,
    "cd": CANDELA,
    "N": NEWTON,
    "m/s": METER_PER_SECOND,
}

__all__ = ["Unit", "UnitError", "SI_REGISTRY"]
