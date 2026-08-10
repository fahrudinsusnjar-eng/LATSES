"""
LAT-CES Scientific Core
Physical Constants Registry Reference Implementation Rev A
Princip: Constants as typed PhysicalQuantities with SKO traceability
"""

from lat_ces.scientific.quantities.quantity import PhysicalQuantity
from lat_ces.scientific.units.derived_units import ENERGY_DIM, VELOCITY_DIM
from lat_ces.scientific.units.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.units.unit import Unit

# =====================================================
# FUNDAMENTAL PHYSICAL CONSTANTS REGISTRY
# =====================================================

_C_UNIT = Unit(
    name="speed_of_light_unit",
    symbol="m/s",
    dimension=VELOCITY_DIM,
    factor=1.0,
)

SPEED_OF_LIGHT = PhysicalQuantity(
    value=299792458.0,
    unit_or_uncertainty=_C_UNIT,
)

_H_UNIT = Unit(
    name="planck_unit",
    symbol="J*s",
    dimension=ENERGY_DIM * TIME,
    factor=1.0,
)

PLANCK_CONSTANT = PhysicalQuantity(
    value=6.62607015e-34,
    unit_or_uncertainty=_H_UNIT,
)

_G_UNIT = Unit(
    name="gravitational_unit",
    symbol="m^3/(kg*s^2)",
    dimension=(LENGTH**3) / (MASS * (TIME**2)),
    factor=1.0,
)

GRAVITATIONAL_CONSTANT = PhysicalQuantity(
    value=6.67430e-11,
    unit_or_uncertainty=_G_UNIT,
)

__all__ = [
    "SPEED_OF_LIGHT",
    "PLANCK_CONSTANT",
    "GRAVITATIONAL_CONSTANT",
]
