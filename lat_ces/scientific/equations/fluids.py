from __future__ import annotations

from typing import Dict

from lat_ces.scientific.dimensions.dimension import DIMENSIONLESS, Dimension, LENGTH, MASS, TIME
from lat_ces.scientific.equations.engine import PhysicalDomainError, PhysicalEquation
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit

AREA = LENGTH**2
VELOCITY = LENGTH / TIME
ACCELERATION = LENGTH / (TIME**2)
VOLUMETRIC_FLOW = LENGTH**3 / TIME
DENSITY = MASS / (LENGTH**3)
MASS_FLOW = MASS / TIME
PRESSURE = MASS / (LENGTH * (TIME**2))


class ContinuityEquation(PhysicalEquation):
    @property
    def name(self) -> str:
        return "Continuity equation (Q = A * v)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {"area": AREA, "velocity": VELOCITY}

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        if kwargs["area"].value <= 0.0:
            raise PhysicalDomainError("Površina mora biti veća od nule.")
        if kwargs["velocity"].value < 0.0:
            raise PhysicalDomainError("Brzina ne može biti negativna.")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        return kwargs["area"] * kwargs["velocity"]


VolumetricFlowEquation = ContinuityEquation


class DynamicPressureEquation(PhysicalEquation):
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
        return PhysicalQuantity(0.5 * raw_pressure.value, 0.5 * raw_pressure.uncertainty, Unit("pascal", "Pa", PRESSURE))


class MassFlowEquation(PhysicalEquation):
    @property
    def name(self) -> str:
        return "Mass flow equation (m_dot = rho * Q)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {"density": DENSITY, "volumetric_flow": VOLUMETRIC_FLOW}

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        if kwargs["density"].value <= 0.0:
            raise PhysicalDomainError("Gustoća mora biti veća od nule.")
        if kwargs["volumetric_flow"].value < 0.0:
            raise PhysicalDomainError("Zapreminski protok ne može biti negativan.")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        mass_flow = kwargs["density"] * kwargs["volumetric_flow"]
        return PhysicalQuantity(mass_flow.value, mass_flow.uncertainty, Unit("kilogram per second", "kg/s", MASS_FLOW))


class PlenumPressureDropEquation(PhysicalEquation):
    @property
    def name(self) -> str:
        return "Pad pritiska u plenumu (Δp = ζ * p_dyn)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {"resistance_coefficient": DIMENSIONLESS, "dynamic_pressure": PRESSURE}

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        if kwargs["resistance_coefficient"].value < 0.0:
            raise PhysicalDomainError("Koeficijent otpora (ζ) ne može biti negativan.")
        if kwargs["dynamic_pressure"].value < 0.0:
            raise PhysicalDomainError("Dinamički pritisak ne može biti negativan.")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        pressure_drop = kwargs["resistance_coefficient"] * kwargs["dynamic_pressure"]
        return PhysicalQuantity(pressure_drop.value, pressure_drop.uncertainty, kwargs["dynamic_pressure"].unit)


class VenturiFlowEquation(PhysicalEquation):
    @property
    def name(self) -> str:
        return "Venturi zapreminski protok (Q)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {"area_1": AREA, "area_2": AREA, "delta_p": PRESSURE, "density": DENSITY, "discharge_coefficient": DIMENSIONLESS}

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        area_1, area_2 = kwargs["area_1"].value, kwargs["area_2"].value
        if area_1 <= 0.0 or area_2 <= 0.0:
            raise PhysicalDomainError("Povrsine poprecnog presjeka moraju biti vece od 0.")
        if area_2 >= area_1:
            raise PhysicalDomainError("Povrsina grla (A2) mora biti manja od ulazne povrsine (A1).")
        if kwargs["delta_p"].value < 0.0:
            raise PhysicalDomainError("Pad pritiska (delta_p) ne moze biti negativan.")
        if kwargs["density"].value <= 0.0:
            raise PhysicalDomainError("Gustoca fluida mora biti veca od 0.")
        if not 0.0 < kwargs["discharge_coefficient"].value <= 1.0:
            raise PhysicalDomainError("Koeficijent praznjenja (Cd) mora biti u opsegu (0, 1].")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        a1, a2, dp, rho, cd = (kwargs[k] for k in ("area_1", "area_2", "delta_p", "density", "discharge_coefficient"))
        ratio = a2.value / a1.value
        denominator = 1.0 - ratio**2
        rel_area_ratio = (a2.relative_uncertainty**2 + a1.relative_uncertainty**2) ** 0.5
        rel_denominator = abs(ratio**2) * (2.0 * rel_area_ratio) / abs(denominator)
        velocity = ((2.0 * dp.value) / (rho.value * denominator)) ** 0.5
        rel_velocity = 0.5 * (dp.relative_uncertainty**2 + rho.relative_uncertainty**2 + rel_denominator**2) ** 0.5
        flow = cd.value * a2.value * velocity
        rel_flow = (cd.relative_uncertainty**2 + a2.relative_uncertainty**2 + rel_velocity**2) ** 0.5
        return PhysicalQuantity(flow, abs(flow) * rel_flow, Unit("cubic meter per second", "m³/s", VOLUMETRIC_FLOW))


class BernoulliTotalPressureEquation(PhysicalEquation):
    @property
    def name(self) -> str:
        return "Ukupni pritisak po Bernoulliju (p_total)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {"static_pressure": PRESSURE, "velocity": VELOCITY, "density": DENSITY, "elevation": LENGTH, "gravity": ACCELERATION}

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        if kwargs["density"].value <= 0.0:
            raise PhysicalDomainError("Gustoca fluida mora biti veca od 0.")
        if kwargs["velocity"].value < 0.0:
            raise PhysicalDomainError("Brzina strujanja ne moze biti negativna.")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        return kwargs["static_pressure"] + (kwargs["density"] * (kwargs["velocity"]**2)) * 0.5 + kwargs["density"] * kwargs["gravity"] * kwargs["elevation"]


__all__ = ["ACCELERATION", "AREA", "DENSITY", "MASS_FLOW", "PRESSURE", "VELOCITY", "VOLUMETRIC_FLOW", "BernoulliTotalPressureEquation", "ContinuityEquation", "DynamicPressureEquation", "MassFlowEquation", "PlenumPressureDropEquation", "VenturiFlowEquation", "VolumetricFlowEquation"]
