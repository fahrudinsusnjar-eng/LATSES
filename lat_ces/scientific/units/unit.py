"""
LAT-CES Scientific Units Compatibility Layer.

Canonical Unit implementation:
    lat_ces.core.dimensions.Unit
"""

from lat_ces.core.dimensions import SIUnit, Unit, UnitSKOError, convert_unit
from lat_ces.scientific.dimensions.dimension import (
    ACCELERATION,
    AMOUNT,
    CURRENT,
    DIMENSIONLESS,
    DENSITY,
    FORCE,
    LENGTH,
    LUMINOUS_INTENSITY,
    MASS,
    TEMPERATURE,
    TIME,
    VELOCITY,
)

UnitError = UnitSKOError
IncompatibleUnitsError = UnitSKOError
convert = convert_unit


def _dimensions_compatible(left, right) -> bool:
    if hasattr(left, "is_compatible"):
        return left.is_compatible(right)
    return left == right


def _unit_is_compatible(self: Unit, other: object) -> bool:
    if not isinstance(other, Unit):
        return False
    return _dimensions_compatible(self.dimension, other.dimension)


def _unit_convert_to_base(self: Unit, value: float) -> float:
    return (value * self.scale_factor) + self.offset


def _unit_convert_from_base(self: Unit, base_value: float) -> float:
    return (base_value - self.offset) / self.scale_factor


def _unit_get_conversion_factor_to(self: Unit, target_unit: Unit) -> float:
    if not self.is_compatible(target_unit):
        raise IncompatibleUnitsError(
            f"Cannot convert {self.symbol} ({self.dimension}) to {target_unit.symbol} ({target_unit.dimension})"
        )
    if self.offset != 0.0 or target_unit.offset != 0.0:
        raise UnitError("Use convert() for affine conversions with offsets.")
    return self.scale_factor / target_unit.scale_factor


if not hasattr(Unit, "is_compatible"):
    Unit.is_compatible = _unit_is_compatible
if not hasattr(Unit, "convert_to_base"):
    Unit.convert_to_base = _unit_convert_to_base
if not hasattr(Unit, "convert_from_base"):
    Unit.convert_from_base = _unit_convert_from_base
if not hasattr(Unit, "get_conversion_factor_to"):
    Unit.get_conversion_factor_to = _unit_get_conversion_factor_to

METER = Unit("meter", "m", LENGTH, 1.0)
CENTIMETER = Unit("centimeter", "cm", LENGTH, 0.01)
KILOGRAM = Unit("kilogram", "kg", MASS, 1.0)
SECOND = Unit("second", "s", TIME, 1.0)
AMPERE = Unit("ampere", "A", CURRENT, 1.0)
KELVIN = Unit("kelvin", "K", TEMPERATURE, 1.0)
MOLE = Unit("mole", "mol", AMOUNT, 1.0)
CANDELA = Unit("candela", "cd", LUMINOUS_INTENSITY, 1.0)

NEWTON = Unit("newton", "N", FORCE, 1.0)
METER_PER_SECOND = METER / SECOND
METERS_PER_SECOND_SQUARED = Unit("meter per second squared", "m/s^2", ACCELERATION, 1.0)

SI_REGISTRY = {
    "m": METER,
    "cm": CENTIMETER,
    "kg": KILOGRAM,
    "s": SECOND,
    "A": AMPERE,
    "K": KELVIN,
    "mol": MOLE,
    "cd": CANDELA,
    "N": NEWTON,
    "m/s": METER_PER_SECOND,
    "m/s^2": METERS_PER_SECOND_SQUARED,
}

__all__ = [
    "Unit",
    "UnitError",
    "UnitSKOError",
    "IncompatibleUnitsError",
    "SIUnit",
    "convert",
    "convert_unit",
    "SI_REGISTRY",
    "METER",
    "CENTIMETER",
    "KILOGRAM",
    "SECOND",
    "AMPERE",
    "KELVIN",
    "MOLE",
    "CANDELA",
    "NEWTON",
    "METER_PER_SECOND",
    "METERS_PER_SECOND_SQUARED",
]
