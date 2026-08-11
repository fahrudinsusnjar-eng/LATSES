from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from lat_ces.scientific.dimensions.dimension import Dimension
from lat_ces.scientific.quantities.quantity import PhysicalQuantity


class DimensionalityError(Exception):
    """Raised when an input has an unexpected physical dimension."""


class PhysicalDomainError(Exception):
    """Raised when inputs violate a physical domain constraint."""


class PhysicalEquation(ABC):
    """Abstract base class for validated scientific equations."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the equation name."""

    @property
    @abstractmethod
    def expected_dimensions(self) -> Dict[str, Dimension]:
        """Map each required argument name to its expected dimension."""

    def validate_inputs(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        """Validate required inputs, types, dimensions, and domain constraints."""
        for param, expected_dimension in self.expected_dimensions.items():
            if param not in kwargs:
                raise ValueError(
                    f"Nedostaje obavezni parametar '{param}' za jednačinu '{self.name}'."
                )

            argument = kwargs[param]
            if not isinstance(argument, PhysicalQuantity):
                raise TypeError(
                    f"Parametar '{param}' mora biti instanca PhysicalQuantity, "
                    f"dobijeno: {type(argument)}."
                )

            if argument.unit.dimension != expected_dimension:
                raise DimensionalityError(
                    f"Dimenzionalno neslaganje za '{param}' u jednačini '{self.name}'. "
                    f"Očekivano: {expected_dimension}, "
                    f"dobijeno: {argument.unit.dimension} ({argument.unit.symbol})."
                )

        self._check_physical_domain(kwargs)

    @abstractmethod
    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        """Validate equation-specific physical domain constraints."""

    @abstractmethod
    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        """Compute the equation using validated physical quantities."""

    def calculate(self, **kwargs: PhysicalQuantity) -> PhysicalQuantity:
        """Validate inputs and calculate the equation result."""
        self.validate_inputs(kwargs)
        return self._compute(kwargs)

    def evaluate(self, **kwargs: PhysicalQuantity) -> PhysicalQuantity:
        """Backward-compatible alias for calculate()."""
        return self.calculate(**kwargs)


__all__ = ["DimensionalityError", "PhysicalDomainError", "PhysicalEquation"]