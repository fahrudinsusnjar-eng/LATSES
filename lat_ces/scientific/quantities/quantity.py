from __future__ import annotations

import math
import uuid
from typing import Optional, Union

from lat_ces.scientific.units.units import Unit, UnitSKOError


class PhysicalQuantity:
    """
    Native representation of a physical quantity with uncertainty propagation
    and SKO lifecycle metadata.
    """

    def __init__(
        self,
        value: float,
        uncertainty: float,
        unit: Unit,
        confidence_level: float = 0.95,
        sko_uuid: Optional[str] = None,
        status: str = "DRAFT",
    ):
        if uncertainty < 0.0:
            raise UnitSKOError("Mjerna neodređenost ne može biti negativna vrijednost.")

        self._value = float(value)
        self._uncertainty = float(uncertainty)
        self._unit = unit
        self._confidence_level = confidence_level
        self._uuid = sko_uuid or str(uuid.uuid4())
        self._status = status

    @property
    def value(self) -> float:
        return self._value

    @property
    def uncertainty(self) -> float:
        return self._uncertainty

    @property
    def relative_uncertainty(self) -> float:
        if self._value == 0.0:
            return 0.0 if self._uncertainty == 0.0 else float("inf")
        return abs(self._uncertainty / self._value)

    @property
    def unit(self) -> Unit:
        return self._unit

    def __add__(self, other: "PhysicalQuantity") -> "PhysicalQuantity":
        if self._unit.dimension != other._unit.dimension:
            raise UnitSKOError(
                f"Dimenzionalna neslaganja: {self._unit.dimension} vs {other._unit.dimension}"
            )

        other_converted_val = (other.value * other.unit.scale_factor) / self._unit.scale_factor
        other_converted_unc = (other.uncertainty * other.unit.scale_factor) / self._unit.scale_factor

        new_val = self._value + other_converted_val
        new_unc = math.sqrt(self._uncertainty**2 + other_converted_unc**2)

        return PhysicalQuantity(new_val, new_unc, self._unit)

    def __mul__(self, other: Union["PhysicalQuantity", int, float]) -> "PhysicalQuantity":
        if isinstance(other, PhysicalQuantity):
            new_val = self._value * other.value
            new_unit = self._unit * other.unit
            rel_unc_sq = self.relative_uncertainty**2 + other.relative_uncertainty**2
            new_unc = abs(new_val) * math.sqrt(rel_unc_sq)
            return PhysicalQuantity(new_val, new_unc, new_unit)

        if isinstance(other, (int, float)):
            scalar = float(other)
            return PhysicalQuantity(self._value * scalar, self._uncertainty * abs(scalar), self._unit)

        return NotImplemented

    def __truediv__(self, other: Union["PhysicalQuantity", int, float]) -> "PhysicalQuantity":
        if isinstance(other, PhysicalQuantity):
            if other.value == 0.0:
                raise ZeroDivisionError(
                    "Dijeljenje sa fizikalnom veličinom čija je vrijednost 0.0 nije dozvoljeno."
                )

            new_val = self._value / other.value
            new_unit = self._unit / other.unit
            rel_unc_sq = self.relative_uncertainty**2 + other.relative_uncertainty**2
            new_unc = abs(new_val) * math.sqrt(rel_unc_sq)
            return PhysicalQuantity(new_val, new_unc, new_unit)

        if isinstance(other, (int, float)):
            scalar = float(other)
            if scalar == 0.0:
                raise ZeroDivisionError("Dijeljenje sa skalarom 0 nije dozvoljeno.")
            return PhysicalQuantity(
                self._value / scalar,
                self._uncertainty / abs(scalar),
                self._unit,
            )

        return NotImplemented

    def __rtruediv__(self, other: Union[int, float]) -> "PhysicalQuantity":
        if isinstance(other, (int, float)):
            if self._value == 0.0:
                raise ZeroDivisionError("Dijeljenje skalara sa nulom nije dozvoljeno.")

            scalar = float(other)
            new_val = scalar / self._value
            new_unit = self._unit ** -1
            new_unc = abs(new_val) * self.relative_uncertainty
            return PhysicalQuantity(new_val, new_unc, new_unit)

        return NotImplemented

    def __pow__(self, exponent: Union[int, float]) -> "PhysicalQuantity":
        if not isinstance(exponent, (int, float)):
            return NotImplemented

        exp = float(exponent)
        new_val = self._value ** exp
        new_unit = self._unit ** exp
        new_unc = abs(new_val) * abs(exp) * self.relative_uncertainty
        return PhysicalQuantity(new_val, new_unc, new_unit)

    def sqrt(self) -> "PhysicalQuantity":
        """Return the square root of this physical quantity."""
        return self ** 0.5

    def __repr__(self) -> str:
        return (
            f"{self._value:.4f} ± {self._uncertainty:.4f} {self._unit.symbol} "
            f"(u_rel: {self.relative_uncertainty * 100:.2f}%)"
        )
