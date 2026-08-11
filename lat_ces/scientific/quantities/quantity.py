"""
LAT-CES Scientific Core
Quantity Engine Reference Implementation Rev A
Princip: Value + Unit -> PhysicalQuantity
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional, Union

from lat_ces.scientific.units.dimension import Dimension, FORCE
from lat_ces.scientific.units.unit import IncompatibleUnitsError, NEWTON, Unit, UnitError, convert
from lat_ces.scientific.units.units import UnitSKOError


@dataclass(init=False)
class PhysicalQuantity:
    """
    Represents a physical quantity consisting of a numerical value and a unit.
    Provides safe arithmetic operations with automatic dimensional consistency.
    """

    value: float
    unit: Unit
    uncertainty: float = 0.0

    def __init__(
        self,
        value: float,
        unit_or_uncertainty: Union[Unit, float],
        maybe_unit: Optional[Unit] = None,
    ):
        # Rev A form: PhysicalQuantity(value, unit)
        if maybe_unit is None:
            if not hasattr(unit_or_uncertainty, "dimension") or not hasattr(
                unit_or_uncertainty, "scale_factor"
            ):
                raise UnitSKOError("Skraćeni oblik zahtijeva PhysicalQuantity(value, unit).")
            self.value = float(value)
            self.unit = unit_or_uncertainty
            self.uncertainty = 0.0
            return

        # Backward-compatible form: PhysicalQuantity(value, uncertainty, unit)
        uncertainty = float(unit_or_uncertainty)
        if uncertainty < 0.0:
            raise UnitSKOError("Mjerna neodređenost ne može biti negativna vrijednost.")

        self.value = float(value)
        self.unit = maybe_unit
        self.uncertainty = uncertainty

    @property
    def dimension(self) -> Dimension:
        return self.unit.dimension

    @property
    def relative_uncertainty(self) -> float:
        if self.value == 0.0:
            return 0.0 if self.uncertainty == 0.0 else float("inf")
        return abs(self.uncertainty / self.value)

    def _convert_value(self, value: float, from_unit: Unit, to_unit: Unit) -> float:
        # Prefer canonical converter from scientific unit engine.
        try:
            return convert(value, from_unit, to_unit)
        except (IncompatibleUnitsError, UnitError):
            raise
        except Exception:
            # Fallback for alternative unit implementation in lat_ces.scientific.units.units
            if from_unit.dimension != to_unit.dimension:
                raise IncompatibleUnitsError(
                    f"Cannot convert {from_unit.symbol} to {to_unit.symbol}: incompatible dimensions."
                )
            from_scale = float(from_unit.scale_factor)
            to_scale = float(to_unit.scale_factor)
            from_offset = float(getattr(from_unit, "offset", 0.0))
            to_offset = float(getattr(to_unit, "offset", 0.0))
            base_value = value * from_scale + from_offset
            return (base_value - to_offset) / to_scale

    def _unit_factor(self, unit_obj) -> float:
        return float(getattr(unit_obj, "factor", getattr(unit_obj, "scale_factor", 1.0)))

    def _build_compound_unit(self, symbol: str, dimension: Dimension, factor: float):
        if dimension.is_compatible(FORCE) and factor == 1.0:
            return NEWTON

        unit_cls = self.unit.__class__ if self.unit.__class__ is type(getattr(self, "unit", self.unit)) else Unit

        try:
            return unit_cls(
                name=f"compound_{symbol}",
                symbol=symbol,
                dimension=dimension,
                factor=factor,
            )
        except TypeError:
            return unit_cls(
                name=f"compound_{symbol}",
                symbol=symbol,
                dimension=dimension,
                scale_factor=factor,
            )

    def convert_to(self, target_unit: Unit) -> "PhysicalQuantity":
        """Converts this quantity to a target compatible unit."""
        new_value = self._convert_value(self.value, self.unit, target_unit)

        # Uncertainty follows linear scale ratio for compatible units.
        ratio = float(self.unit.scale_factor) / float(target_unit.scale_factor)
        new_uncertainty = self.uncertainty * abs(ratio)
        return PhysicalQuantity(new_value, new_uncertainty, target_unit)

    def __add__(self, other: "PhysicalQuantity") -> "PhysicalQuantity":
        if not isinstance(other, PhysicalQuantity):
            raise TypeError("Operand must be a PhysicalQuantity")

        converted_other_value = self._convert_value(other.value, other.unit, self.unit)

        ratio = float(other.unit.scale_factor) / float(self.unit.scale_factor)
        converted_other_uncertainty = other.uncertainty * abs(ratio)
        new_uncertainty = math.sqrt(self.uncertainty**2 + converted_other_uncertainty**2)

        return PhysicalQuantity(
            value=self.value + converted_other_value,
            unit_or_uncertainty=new_uncertainty,
            maybe_unit=self.unit,
        )

    def __sub__(self, other: "PhysicalQuantity") -> "PhysicalQuantity":
        if not isinstance(other, PhysicalQuantity):
            raise TypeError("Operand must be a PhysicalQuantity")

        converted_other_value = self._convert_value(other.value, other.unit, self.unit)

        ratio = float(other.unit.scale_factor) / float(self.unit.scale_factor)
        converted_other_uncertainty = other.uncertainty * abs(ratio)
        new_uncertainty = math.sqrt(self.uncertainty**2 + converted_other_uncertainty**2)

        return PhysicalQuantity(
            value=self.value - converted_other_value,
            unit_or_uncertainty=new_uncertainty,
            maybe_unit=self.unit,
        )

    def __mul__(self, other: Union[int, float, "PhysicalQuantity"]) -> "PhysicalQuantity":
        if isinstance(other, (int, float)):
            scalar = float(other)
            return PhysicalQuantity(value=self.value * scalar, unit_or_uncertainty=self.uncertainty * abs(scalar), maybe_unit=self.unit)
        if isinstance(other, PhysicalQuantity):
            new_value = self.value * other.value
            new_dimension = self.dimension * other.dimension
            new_symbol = f"{self.unit.symbol}·{other.unit.symbol}"
            new_factor = self._unit_factor(self.unit) * self._unit_factor(other.unit)
            new_unit = self._build_compound_unit(new_symbol, new_dimension, new_factor)
            rel_unc_sq = self.relative_uncertainty**2 + other.relative_uncertainty**2
            new_uncertainty = abs(new_value) * math.sqrt(rel_unc_sq)
            return PhysicalQuantity(value=new_value, unit_or_uncertainty=new_uncertainty, maybe_unit=new_unit)
        raise TypeError("Unsupported operand type for multiplication")

    def __rmul__(self, other: Union[int, float]) -> "PhysicalQuantity":
        return self.__mul__(other)

    def __truediv__(self, other: Union[int, float, "PhysicalQuantity"]) -> "PhysicalQuantity":
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Division by zero in PhysicalQuantity")
            scalar = float(other)
            return PhysicalQuantity(value=self.value / scalar, unit_or_uncertainty=self.uncertainty / abs(scalar), maybe_unit=self.unit)
        if isinstance(other, PhysicalQuantity):
            if other.value == 0:
                raise ZeroDivisionError("Division by zero in PhysicalQuantity")
            new_value = self.value / other.value
            new_dimension = self.dimension / other.dimension
            new_symbol = f"{self.unit.symbol}/{other.unit.symbol}"
            new_factor = self._unit_factor(self.unit) / self._unit_factor(other.unit)
            new_unit = self._build_compound_unit(new_symbol, new_dimension, new_factor)
            rel_unc_sq = self.relative_uncertainty**2 + other.relative_uncertainty**2
            new_uncertainty = abs(new_value) * math.sqrt(rel_unc_sq)
            return PhysicalQuantity(value=new_value, unit_or_uncertainty=new_uncertainty, maybe_unit=new_unit)
        raise TypeError("Unsupported operand type for division")

    def __rtruediv__(self, other: Union[int, float]) -> "PhysicalQuantity":
        if not isinstance(other, (int, float)):
            return NotImplemented
        if self.value == 0.0:
            raise ZeroDivisionError("Division by zero in PhysicalQuantity")

        scalar = float(other)
        new_value = scalar / self.value
        new_unit = self.unit ** -1
        new_uncertainty = abs(new_value) * self.relative_uncertainty
        return PhysicalQuantity(new_value, new_uncertainty, new_unit)

    def __pow__(self, exponent: Union[int, float]) -> "PhysicalQuantity":
        if not isinstance(exponent, (int, float)):
            return NotImplemented

        exp = float(exponent)
        new_value = self.value**exp
        new_unit = self.unit**exp
        new_uncertainty = abs(new_value) * abs(exp) * self.relative_uncertainty
        return PhysicalQuantity(new_value, new_uncertainty, new_unit)

    def sqrt(self) -> "PhysicalQuantity":
        return self ** 0.5

    def __repr__(self) -> str:
        return f"{self.value} {self.unit.symbol}"
