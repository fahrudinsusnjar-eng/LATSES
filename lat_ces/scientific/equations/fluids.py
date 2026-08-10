from __future__ import annotations

from typing import Dict

from lat_ces.scientific.dimensions.dimension import (
    DIMENSIONLESS,
    Dimension,
    LENGTH,
    MASS,
    TIME,
)
from lat_ces.scientific.equations.engine import PhysicalDomainError, PhysicalEquation
from lat_ces.scientific.quantities.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


AREA = LENGTH**2
VELOCITY = LENGTH / TIME
ACCELERATION = LENGTH / (TIME**2)
VOLUMETRIC_FLOW = LENGTH**3 / TIME
DENSITY = MASS / (LENGTH**3)
MASS_FLOW = MASS / TIME
DYNAMIC_VISCOSITY = MASS / (LENGTH * TIME)
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
        if kwargs["velocity"].value < 0.0:
            raise PhysicalDomainError("Brzina ne može biti negativna.")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        return kwargs["area"] * kwargs["velocity"]


VolumetricFlowEquation = ContinuityEquation


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
            0.5 * raw_pressure.value,
            0.5 * raw_pressure.uncertainty,
            pascal,
        )


class MassFlowEquation(PhysicalEquation):
    """Mass flow equation, m_dot = rho * Q."""

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
        return PhysicalQuantity(
            mass_flow.value,
            mass_flow.uncertainty,
            Unit("kilogram per second", "kg/s", MASS_FLOW),
        )


class PlenumPressureDropEquation(PhysicalEquation):
    """Pressure drop in plenum chambers and obstructions, Δp = ζ * p_dyn."""

    @property
    def name(self) -> str:
        return "Pad pritiska u plenumu (Δp = ζ * p_dyn)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {
            "resistance_coefficient": DIMENSIONLESS,
            "dynamic_pressure": PRESSURE,
        }

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        if kwargs["resistance_coefficient"].value < 0.0:
            raise PhysicalDomainError("Koeficijent otpora (ζ) ne može biti negativan.")
        if kwargs["dynamic_pressure"].value < 0.0:
            raise PhysicalDomainError("Dinamički pritisak ne može biti negativan.")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        pressure_drop = kwargs["resistance_coefficient"] * kwargs["dynamic_pressure"]
        return PhysicalQuantity(
            pressure_drop.value,
            pressure_drop.uncertainty,
            kwargs["dynamic_pressure"].unit,
        )


class VenturiFlowEquation(PhysicalEquation):
    """Venturi volumetric flow, Q = Cd * A2 * sqrt((2*dp)/(rho*(1-(A2/A1)^2)))."""

    @property
    def name(self) -> str:
        return "Venturi zapreminski protok (Q)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {
            "area_1": AREA,
            "area_2": AREA,
            "delta_p": PRESSURE,
            "density": DENSITY,
            "discharge_coefficient": DIMENSIONLESS,
        }

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        area_1 = kwargs["area_1"].value
        area_2 = kwargs["area_2"].value
        delta_p = kwargs["delta_p"].value
        density = kwargs["density"].value
        discharge_coefficient = kwargs["discharge_coefficient"].value

        if area_1 <= 0.0 or area_2 <= 0.0:
            raise PhysicalDomainError("Povrsine poprecnog presjeka moraju biti vece od 0.")
        if area_2 >= area_1:
            raise PhysicalDomainError(
                "Povrsina grla (A2) mora biti manja od ulazne povrsine (A1)."
            )
        if delta_p < 0.0:
            raise PhysicalDomainError("Pad pritiska (delta_p) ne moze biti negativan.")
        if density <= 0.0:
            raise PhysicalDomainError("Gustoca fluida mora biti veca od 0.")
        if discharge_coefficient <= 0.0 or discharge_coefficient > 1.0:
            raise PhysicalDomainError("Koeficijent praznjenja (Cd) mora biti u opsegu (0, 1].")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        area_1 = kwargs["area_1"]
        area_2 = kwargs["area_2"]
        delta_p = kwargs["delta_p"]
        density = kwargs["density"]
        discharge_coefficient = kwargs["discharge_coefficient"]

        ratio = area_2.value / area_1.value
        ratio_squared = ratio**2
        denominator = 1.0 - ratio_squared

        rel_area_ratio = (
            (area_2.relative_uncertainty**2 + area_1.relative_uncertainty**2) ** 0.5
        )
        rel_ratio_squared = 2.0 * rel_area_ratio
        unc_ratio_squared = abs(ratio_squared) * rel_ratio_squared
        rel_denominator = unc_ratio_squared / abs(denominator)

        velocity_throat_value = ((2.0 * delta_p.value) / (density.value * denominator)) ** 0.5
        rel_inside_sqrt = (
            delta_p.relative_uncertainty**2
            + density.relative_uncertainty**2
            + rel_denominator**2
        ) ** 0.5
        rel_velocity_throat = 0.5 * rel_inside_sqrt

        flow_value = discharge_coefficient.value * area_2.value * velocity_throat_value
        rel_flow = (
            discharge_coefficient.relative_uncertainty**2
            + area_2.relative_uncertainty**2
            + rel_velocity_throat**2
        ) ** 0.5
        flow_uncertainty = abs(flow_value) * rel_flow

        return PhysicalQuantity(
            flow_value,
            flow_uncertainty,
            Unit("cubic meter per second", "m³/s", VOLUMETRIC_FLOW),
        )


class BernoulliTotalPressureEquation(PhysicalEquation):
    """Total pressure, p_total = p_static + 0.5*rho*v^2 + rho*g*z."""

    @property
    def name(self) -> str:
        return "Ukupni pritisak po Bernoulliju (p_total)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {
            "static_pressure": PRESSURE,
            "velocity": VELOCITY,
            "density": DENSITY,
            "elevation": LENGTH,
            "gravity": ACCELERATION,
        }

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        if kwargs["density"].value <= 0.0:
            raise PhysicalDomainError("Gustoca fluida mora biti veca od 0.")
        if kwargs["velocity"].value < 0.0:
            raise PhysicalDomainError("Brzina strujanja ne moze biti negativna.")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        static_pressure = kwargs["static_pressure"]
        velocity = kwargs["velocity"]
        density = kwargs["density"]
        elevation = kwargs["elevation"]
        gravity = kwargs["gravity"]

        dynamic_pressure = (density * (velocity**2)) * 0.5
        hydrostatic_pressure = density * gravity * elevation
        return static_pressure + dynamic_pressure + hydrostatic_pressure


class ReynoldsNumberEquation(PhysicalEquation):
    """Reynolds number, Re = rho * v * D / mu."""

    @property
    def name(self) -> str:
        return "Reynoldsov broj (Re = rho * v * D / mu)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {
            "density": DENSITY,
            "velocity": VELOCITY,
            "characteristic_length": LENGTH,
            "dynamic_viscosity": DYNAMIC_VISCOSITY,
        }

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        if kwargs["density"].value <= 0.0:
            raise PhysicalDomainError("Gustoća fluida mora biti veća od nule.")

        if kwargs["velocity"].value < 0.0:
            raise PhysicalDomainError("Brzina ne može biti negativna.")

        if kwargs["characteristic_length"].value <= 0.0:
            raise PhysicalDomainError("Karakteristična dužina mora biti veća od nule.")

        if kwargs["dynamic_viscosity"].value <= 0.0:
            raise PhysicalDomainError("Dinamička viskoznost mora biti veća od nule.")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        reynolds = (
            kwargs["density"]
            * kwargs["velocity"]
            * kwargs["characteristic_length"]
            / kwargs["dynamic_viscosity"]
        )

        return PhysicalQuantity(
            reynolds.value,
            reynolds.uncertainty,
            Unit("dimensionless", "-", DIMENSIONLESS),
        )


class MachNumberEquation(PhysicalEquation):
    """Mach number, Ma = velocity / speed_of_sound."""

    @property
    def name(self) -> str:
        return "Machov broj (Ma = v / a)"

    @property
    def expected_dimensions(self) -> Dict[str, Dimension]:
        return {
            "velocity": VELOCITY,
            "speed_of_sound": VELOCITY,
        }

    def _check_physical_domain(self, kwargs: Dict[str, PhysicalQuantity]) -> None:
        if kwargs["velocity"].value < 0.0:
            raise PhysicalDomainError("Brzina fluida ne može biti negativna.")

        if kwargs["speed_of_sound"].value <= 0.0:
            raise PhysicalDomainError("Brzina zvuka mora biti veća od nule.")

    def _compute(self, kwargs: Dict[str, PhysicalQuantity]) -> PhysicalQuantity:
        mach = kwargs["velocity"] / kwargs["speed_of_sound"]

        return PhysicalQuantity(
            mach.value,
            mach.uncertainty,
            Unit("dimensionless", "-", DIMENSIONLESS),
        )


__all__ = [
    "ACCELERATION",
    "AREA",
    "DENSITY",
    "DYNAMIC_VISCOSITY",
    "MASS_FLOW",
    "PRESSURE",
    "VELOCITY",
    "VOLUMETRIC_FLOW",
    "BernoulliTotalPressureEquation",
    "ContinuityEquation",
    "DynamicPressureEquation",
    "MassFlowEquation",
    "PlenumPressureDropEquation",
    "VolumetricFlowEquation",
    "VenturiFlowEquation",
    "ReynoldsNumberEquation",
    "MachNumberEquation",
]