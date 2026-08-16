"""Compatibility facade for the canonical LAT-CES Dimension API.

The implementation and all dimension constants live in ``lat_ces.core.dimensions``.
This module remains as a stable legacy import path and must not define a second
Dimension system.
"""

from lat_ces.core.dimensions import (
    ACCELERATION,
    AMOUNT,
    CURRENT,
    DENSITY,
    DIMENSIONLESS,
    FORCE,
    LENGTH,
    LUMINOUS_INTENSITY,
    MASS,
    TEMPERATURE,
    TIME,
    VELOCITY,
    Dimension,
)

__all__ = [
    "Dimension",
    "DIMENSIONLESS",
    "LENGTH",
    "MASS",
    "TIME",
    "CURRENT",
    "TEMPERATURE",
    "AMOUNT",
    "LUMINOUS_INTENSITY",
    "VELOCITY",
    "DENSITY",
    "ACCELERATION",
    "FORCE",
]
