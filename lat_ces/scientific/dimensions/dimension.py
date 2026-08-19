"""
LAT-CES Scientific Core
Dimension Engine & Compound Analysis Implementation Rev A
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class Dimension:
    """
    Represents a physical dimension using exponents of base physical quantities.
    Example: Velocity = Length^1 * Time^-1
    """

    exponents: Dict[str, int] = field(default_factory=dict)

    @property
    def name(self) -> str:
        non_zero = [k for k, v in self.exponents.items() if v != 0]
        if len(non_zero) == 1 and self.exponents[non_zero[0]] == 1:
            return non_zero[0].upper()
        if not non_zero:
            return "DIMENSIONLESS"
        return "DERIVED"

    def is_compatible(self, other: "Dimension") -> bool:
        """Checks if another dimension has identical base exponents."""
        all_keys = set(self.exponents.keys()).union(set(other.exponents.keys()))
        for key in all_keys:
            if self.exponents.get(key, 0) != other.exponents.get(key, 0):
                return False
        return True

    def __mul__(self, other: "Dimension") -> "Dimension":
        if not isinstance(other, Dimension):
            raise TypeError("Can only multiply with another Dimension")

        new_exponents = dict(self.exponents)
        for key, val in other.exponents.items():
            new_exponents[key] = new_exponents.get(key, 0) + val

        cleaned = {k: v for k, v in new_exponents.items() if v != 0}
        return Dimension(exponents=cleaned)

    def __truediv__(self, other: "Dimension") -> "Dimension":
        if not isinstance(other, Dimension):
            raise TypeError("Can only divide by another Dimension")

        new_exponents = dict(self.exponents)
        for key, val in other.exponents.items():
            new_exponents[key] = new_exponents.get(key, 0) - val

        cleaned = {k: v for k, v in new_exponents.items() if v != 0}
        return Dimension(exponents=cleaned)

    def __pow__(self, power: int | float) -> "Dimension":
        if not isinstance(power, (int, float)):
            raise TypeError("Dimension power must be numeric")
        new_exponents = {k: v * power for k, v in self.exponents.items()}
        cleaned = {k: v for k, v in new_exponents.items() if v != 0}
        return Dimension(exponents=cleaned)


# =====================================================
# BASE SI DIMENSIONS REGISTRY
# =====================================================

LENGTH = Dimension(exponents={"length": 1})
MASS = Dimension(exponents={"mass": 1})
TIME = Dimension(exponents={"time": 1})
CURRENT = Dimension(exponents={"current": 1})
TEMPERATURE = Dimension(exponents={"temperature": 1})
SUBSTANCE = Dimension(exponents={"substance": 1})
LUMINOUS_INTENSITY = Dimension(exponents={"luminous_intensity": 1})
DIMENSIONLESS = Dimension(exponents={})

# Compatibility aliases and commonly used derived dimensions.
AMOUNT = SUBSTANCE
VELOCITY = LENGTH / TIME
ACCELERATION = LENGTH / (TIME**2)
FORCE = MASS * ACCELERATION
DENSITY = MASS / (LENGTH**3)

__all__ = [
    "Dimension",
    "LENGTH",
    "MASS",
    "TIME",
    "CURRENT",
    "TEMPERATURE",
    "SUBSTANCE",
    "AMOUNT",
    "LUMINOUS_INTENSITY",
    "VELOCITY",
    "ACCELERATION",
    "FORCE",
    "DENSITY",
    "DIMENSIONLESS",
]
