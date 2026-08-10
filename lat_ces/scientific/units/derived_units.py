"""
LAT-CES Scientific Core
Derived Units & Compound Quantities Reference Implementation Rev B
"""

from lat_ces.scientific.units.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.quantities.quantity import PhysicalQuantity
from lat_ces.scientific.units.unit import Unit


# ============================================================
# COMPOUND DIMENSIONS
# ============================================================

VELOCITY_DIM = LENGTH / TIME

ACCELERATION_DIM = LENGTH / (TIME ** 2)

FORCE_DIM = MASS * LENGTH / (TIME ** 2)

ENERGY_DIM = FORCE_DIM * LENGTH


# ============================================================
# DERIVED UNITS
# ============================================================

METERS_PER_SECOND = Unit(
    name="meters per second",
    symbol="m/s",
    dimension=VELOCITY_DIM,
    scale_factor=1.0,
)

METERS_PER_SECOND_SQUARED = Unit(
    name="meters per second squared",
    symbol="m/s^2",
    dimension=ACCELERATION_DIM,
    scale_factor=1.0,
)

NEWTON = Unit(
    name="newton",
    symbol="N",
    dimension=FORCE_DIM,
    scale_factor=1.0,
)

JOULE = Unit(
    name="joule",
    symbol="J",
    dimension=ENERGY_DIM,
    scale_factor=1.0,
)


# ============================================================
# FUNDAMENTAL PHYSICAL CONSTANTS
# ============================================================

SPEED_OF_LIGHT = PhysicalQuantity(
    299792458.0,
    METERS_PER_SECOND,
)

PLANCK_CONSTANT_UNIT = Unit(
    name="joule second",
    symbol="J*s",
    dimension=ENERGY_DIM * TIME,
    scale_factor=1.0,
)

PLANCK_CONSTANT = PhysicalQuantity(
    6.62607015e-34,
    PLANCK_CONSTANT_UNIT,
)


__all__ = [
    "VELOCITY_DIM",
    "ACCELERATION_DIM",
    "FORCE_DIM",
    "ENERGY_DIM",
    "METERS_PER_SECOND",
    "METERS_PER_SECOND_SQUARED",
    "NEWTON",
    "JOULE",
    "SPEED_OF_LIGHT",
    "PLANCK_CONSTANT",
]
