"""Canonical SI unit registry used by compatibility bridges."""

from __future__ import annotations

from lat_ces.core.dimensions import (
    AMOUNT,
    CURRENT,
    DIMENSIONLESS,
    LENGTH,
    LUMINOUS_INTENSITY,
    MASS,
    TEMPERATURE,
    TIME,
    Unit,
    ampere,
    candela,
    kilogram,
    kelvin,
    meter,
    mole,
    second,
)


# Legacy module callers use TEMPERATURE for delta-T values.  Keep that bridge
# mapping zero-offset so temperature differences can safely participate in unit
# algebra. Canonical callers that need absolute temperature already provide an
# explicit Unit (e.g. kelvin).
kelvin_interval = Unit(
    name="kelvin interval",
    symbol="K",
    dimension=TEMPERATURE,
    scale_factor=1.0,
    offset=0.0,
)


_DERIVED_UNITS = {
    DIMENSIONLESS: Unit("dimensionless", "1", DIMENSIONLESS),
    LENGTH: meter,
    MASS: kilogram,
    TIME: second,
    CURRENT: ampere,
    TEMPERATURE: kelvin_interval,
    AMOUNT: mole,
    LUMINOUS_INTENSITY: candela,
    LENGTH / TIME: meter / second,
    LENGTH**2: meter**2,
    LENGTH**3 / TIME: (meter**3) / second,
    MASS / TIME: kilogram / second,
    MASS / (LENGTH**3): kilogram / (meter**3),
    MASS / (LENGTH * (TIME**2)): kilogram / meter / (second**2),
    MASS / (LENGTH * TIME): kilogram / meter / second,
    (MASS * (LENGTH**2)) / (TIME**3): (kilogram * (meter**2)) / (second**3),
    (LENGTH**2) / (TIME**2) / TEMPERATURE: (meter**2) / (second**2) / kelvin_interval,
}


def dimension_to_unit(dimension) -> Unit:
    """Return the canonical SI unit for a supported physical dimension."""

    if dimension in _DERIVED_UNITS:
        return _DERIVED_UNITS[dimension]
    raise ValueError(f"No canonical SI unit is registered for dimension {dimension!r}")


__all__ = ["dimension_to_unit", "kelvin_interval"]
