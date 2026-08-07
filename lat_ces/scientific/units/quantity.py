"""
LAT-CES Scientific Core
Quantity Engine Reference Implementation (LAT-SCI-CORE-0019)
"""

from dataclasses import dataclass
from typing import Union

from lat_ces.scientific.units.unit import Unit, UnitError


class QuantityError(Exception):
    """Base exception for Quantity engine operations."""

    pass


@dataclass(frozen=True)
class Quantity:
    """
    Represents a physical quantity combining value, unit, and dimension.
    Guarantees strict physical consistency across arithmetic operations.
    """

    value: float
    unit: Unit
    uncertainty: float = 0.0

    @property
    def dimension(self):
        return self.unit.dimension

    def to(self, target_unit: Unit) -> "Quantity":
        """Converts quantity value to target unit if compatible."""
        if not isinstance(target_unit, Unit):
            raise QuantityError("Target must be a valid Unit instance.")
        factor = self.unit.get_conversion_factor_to(target_unit)
        new_value = self.value * factor
        new_uncertainty = self.uncertainty * factor
        return Quantity(value=new_value, unit=target_unit, uncertainty=new_uncertainty)

    def __add__(self, other: "Quantity") -> "Quantity":
        if not isinstance(other, Quantity):
            raise QuantityError("Can only add Quantity to another Quantity.")
        if not self.unit.is_compatible(other.unit):
            raise QuantityError(
                f"Cannot add incompatible physical dimensions: {self.dimension} and {other.dimension}"
            )

        # Convert other to self.unit before adding
        other_converted = other.to(self.unit)
        return Quantity(
            value=self.value + other_converted.value,
            unit=self.unit,
            uncertainty=(self.uncertainty**2 + other_converted.uncertainty**2) ** 0.5,
        )

    def __sub__(self, other: "Quantity") -> "Quantity":
        if not isinstance(other, Quantity):
            raise QuantityError("Can only subtract Quantity from another Quantity.")
        if not self.unit.is_compatible(other.unit):
            raise QuantityError(
                f"Cannot subtract incompatible physical dimensions: {self.dimension} and {other.dimension}"
            )

        other_converted = other.to(self.unit)
        return Quantity(
            value=self.value - other_converted.value,
            unit=self.unit,
            uncertainty=(self.uncertainty**2 + other_converted.uncertainty**2) ** 0.5,
        )

    def __mul__(self, other: Union["Quantity", float, int]) -> "Quantity":
        if isinstance(other, (int, float)):
            return Quantity(
                value=self.value * float(other),
                unit=self.unit,
                uncertainty=self.uncertainty * float(other),
            )
        if isinstance(other, Quantity):
            new_unit = self.unit * other.unit
            return Quantity(
                value=self.value * other.value,
                unit=new_unit,
                uncertainty=abs(self.value * other.value)
                * (
                    (
                        (self.uncertainty / (self.value or 1e-12)) ** 2
                        + (other.uncertainty / (other.value or 1e-12)) ** 2
                    )
                    ** 0.5
                ),
            )
        raise QuantityError("Unsupported operand type for multiplication.")

    def __truediv__(self, other: Union["Quantity", float, int]) -> "Quantity":
        if isinstance(other, (int, float)):
            if other == 0:
                raise QuantityError("Division by zero scalar.")
            return Quantity(
                value=self.value / float(other),
                unit=self.unit,
                uncertainty=self.uncertainty / float(other),
            )
        if isinstance(other, Quantity):
            if other.value == 0:
                raise QuantityError("Division by zero quantity.")
            new_unit = self.unit / other.unit
            return Quantity(
                value=self.value / other.value,
                unit=new_unit,
                uncertainty=abs(self.value / other.value)
                * (
                    (
                        (self.uncertainty / (self.value or 1e-12)) ** 2
                        + (other.uncertainty / (other.value or 1e-12)) ** 2
                    )
                    ** 0.5
                ),
            )
        raise QuantityError("Unsupported operand type for division.")


__all__ = ["Quantity", "QuantityError", "Unit", "UnitError"]
