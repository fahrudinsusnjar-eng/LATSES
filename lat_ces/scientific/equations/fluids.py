from __future__ import annotations

from typing import Dict

from lat_ces.scientific.dimensions.dimension import Dimension, LENGTH, MASS, TIME
from lat_ces.scientific.equations.engine import PhysicalDomainError, PhysicalEquation
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


AREA = LENGTH**2
VELOCITY = LENGTH / TIME
VOLUMETRIC_FLOW = LENGTH**3 / TIME
DENSITY = MASS / (LENGTH**3)
PRESSURE = MASS / (LENGTH * (TIME**2))


class ContinuityEquation(PhysicalEquation):
    """Volumetric flow equation, Q = A * v."""

    @property
    def name(self) -> str:
        return "Continuity equation (Q = A * v)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {"area": AREA, "velocity": VELOCITY}

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        if kwargs["area"].value <= 0.0:
            raise PhysicalDomainError("Površina mora biti veća od nule.")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        return kwargs["area"] * kwargs["velocity"]


class DynamicPressureEquation(PhysicalEquation):
    """Dynamic pressure equation, q = 0.5 * rho * v^2."""

    @property
    def name(self) -> str:
        return "Dynamic pressure (q = 0.5 * rho * v^2)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {"density": DENSITY, "velocity": VELOCITY}

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        if kwargs["density"].value <= 0.0:
            raise PhysicalDomainError("Gustoća mora biti veća od nule.")
        if kwargs["velocity"].value < 0.0:
            raise PhysicalDomainError("Brzina ne može biti negativna.")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        raw_pressure = kwargs["density"] * (kwargs["velocity"] ** 2)
        pascal = Unit("pascal", "Pa", PRESSURE)
        return PhysicalQuantity(
            value=0.5 * raw_pressure.value,
            uncertainty=0.5 * raw_pressure.uncertainty,
            unit=pascal,
        )


__all__ = ["ContinuityEquation", "DynamicPressureEquation"]