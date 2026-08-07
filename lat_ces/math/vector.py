"""
LAT-CES Mathematical Core
Vector Engine Reference Implementation (LAT-MATH-CORE-0011)
"""

import math
from typing import List, Union

from lat_ces.scientific.units.quantity import Quantity, QuantityError


class VectorError(Exception):
    """Base exception for Mathematical Vector operations."""

    pass


class PhysicalVector:
    """
    Represents an n-dimensional vector of Physical Quantities.
    Guarantees physical consistency across components and vector operations.
    """

    def __init__(self, components: List[Quantity]):
        if not components:
            raise VectorError("Vector cannot be empty.")
        if not all(isinstance(c, Quantity) for c in components):
            raise VectorError("All components of PhysicalVector must be Quantity instances.")

        # Enforce component dimensional homogeneity for simple vectors
        base_unit = components[0].unit
        for c in components[1:]:
            if not c.unit.is_compatible(base_unit):
                raise VectorError("All vector components must share compatible physical dimensions.")

        self._components: List[Quantity] = components

    def __len__(self) -> int:
        return len(self._components)

    def __getitem__(self, index: int) -> Quantity:
        return self._components[index]

    def magnitude(self) -> Quantity:
        """Calculates Euclidean norm (magnitude) with propagated physical unit."""
        sum_sq = sum(c.value ** 2 for c in self._components)
        mag_val = math.sqrt(sum_sq)

        # Uncertainty propagation for magnitude: sqrt(sum(x_i^2 * u_i^2)) / mag
        unc_sq_sum = sum((c.value ** 2) * (c.uncertainty ** 2) for c in self._components)
        mag_unc = math.sqrt(unc_sq_sum) / mag_val if mag_val != 0 else 0.0

        return Quantity(value=mag_val, unit=self._components[0].unit, uncertainty=mag_unc)

    def dot(self, other: "PhysicalVector") -> Quantity:
        """Calculates dot product of two vectors: A . B"""
        if not isinstance(other, PhysicalVector):
            raise VectorError("Dot product requires another PhysicalVector.")
        if len(self) != len(other):
            raise VectorError("Vectors must have identical dimensions for dot product.")

        acc = self._components[0] * other._components[0]
        for i in range(1, len(self)):
            acc = acc + (self._components[i] * other._components[i])

        return acc

    def __add__(self, other: "PhysicalVector") -> "PhysicalVector":
        if not isinstance(other, PhysicalVector):
            raise VectorError("Can only add PhysicalVector to another PhysicalVector.")
        if len(self) != len(other):
            raise VectorError("Vectors must have same dimension for addition.")

        new_comp = [self._components[i] + other._components[i] for i in range(len(self))]
        return PhysicalVector(new_comp)

    def __mul__(self, scalar: Union[float, int, Quantity]) -> "PhysicalVector":
        new_comp = [c * scalar for c in self._components]
        return PhysicalVector(new_comp)
