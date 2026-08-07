"""Public engine API for validated scientific equations."""

from lat_ces.scientific.equations.equation import (
    DimensionalityError,
    PhysicalDomainError,
    PhysicalEquation,
)

__all__ = ["DimensionalityError", "PhysicalDomainError", "PhysicalEquation"]