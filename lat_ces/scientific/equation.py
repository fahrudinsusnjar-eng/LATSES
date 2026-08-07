"""Backward-compatible import for the scientific equation API."""

from lat_ces.scientific.equations.equation import (
    DimensionalityError,
    PhysicalDomainError,
    PhysicalEquation,
)

__all__ = ["DimensionalityError", "PhysicalDomainError", "PhysicalEquation"]