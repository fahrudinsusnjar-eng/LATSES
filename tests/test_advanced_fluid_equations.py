import pytest

from lat_ces.scientific.dimensions.dimension import DIMENSIONLESS, LENGTH, MASS, TIME
from lat_ces.scientific.equations.engine import DimensionalityError, PhysicalDomainError
from lat_ces.scientific.equations.fluids import (
    BernoulliTotalPressureEquation,
    VOLUMETRIC_FLOW,
    VenturiFlowEquation,
)
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


def test_venturi_flow_equation_calculation():
    m2 = Unit("square meter", "m2", LENGTH**2)
    pa = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    rho_u = Unit("kilogram per cubic meter", "kg/m3", MASS / (LENGTH**3))
    dimless = Unit("dimensionless", "-", DIMENSIONLESS)

    area_1 = PhysicalQuantity(0.1, 0.001, m2)
    area_2 = PhysicalQuantity(0.05, 0.0005, m2)
    delta_p = PhysicalQuantity(500.0, 10.0, pa)
    density = PhysicalQuantity(1.2, 0.012, rho_u)
    discharge_coefficient = PhysicalQuantity(0.98, 0.01, dimless)

    flow = VenturiFlowEquation().calculate(
        area_1=area_1,
        area_2=area_2,
        delta_p=delta_p,
        density=density,
        discharge_coefficient=discharge_coefficient,
    )

    assert flow.value == pytest.approx(1.6333333333, rel=1e-6)
    assert flow.uncertainty > 0
    assert flow.unit.dimension == VOLUMETRIC_FLOW


def test_venturi_flow_equation_domain_checks():
    m2 = Unit("square meter", "m2", LENGTH**2)
    pa = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    rho_u = Unit("kilogram per cubic meter", "kg/m3", MASS / (LENGTH**3))
    dimless = Unit("dimensionless", "-", DIMENSIONLESS)

    area_1 = PhysicalQuantity(0.1, 0.0, m2)
    area_2 = PhysicalQuantity(0.1, 0.0, m2)
    delta_p = PhysicalQuantity(500.0, 0.0, pa)
    density = PhysicalQuantity(1.2, 0.0, rho_u)
    discharge_coefficient = PhysicalQuantity(1.2, 0.0, dimless)

    equation = VenturiFlowEquation()

    with pytest.raises(PhysicalDomainError):
        equation.calculate(
            area_1=area_1,
            area_2=area_2,
            delta_p=delta_p,
            density=density,
            discharge_coefficient=PhysicalQuantity(0.98, 0.0, dimless),
        )

    with pytest.raises(PhysicalDomainError):
        equation.calculate(
            area_1=PhysicalQuantity(0.1, 0.0, m2),
            area_2=PhysicalQuantity(0.05, 0.0, m2),
            delta_p=delta_p,
            density=density,
            discharge_coefficient=discharge_coefficient,
        )


def test_bernoulli_total_pressure_equation_calculation():
    pa = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    v_u = Unit("meter per second", "m/s", LENGTH / TIME)
    rho_u = Unit("kilogram per cubic meter", "kg/m3", MASS / (LENGTH**3))
    z_u = Unit("meter", "m", LENGTH)
    g_u = Unit("meter per second squared", "m/s2", LENGTH / (TIME**2))

    p_static = PhysicalQuantity(100000.0, 50.0, pa)
    velocity = PhysicalQuantity(10.0, 0.1, v_u)
    density = PhysicalQuantity(1.2, 0.01, rho_u)
    elevation = PhysicalQuantity(5.0, 0.02, z_u)
    gravity = PhysicalQuantity(9.81, 0.0, g_u)

    total_pressure = BernoulliTotalPressureEquation().calculate(
        static_pressure=p_static,
        velocity=velocity,
        density=density,
        elevation=elevation,
        gravity=gravity,
    )

    assert total_pressure.value == pytest.approx(100118.86, rel=1e-6)
    assert total_pressure.unit.symbol == "Pa"


def test_bernoulli_total_pressure_equation_validation():
    pa = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    v_u = Unit("meter per second", "m/s", LENGTH / TIME)
    rho_u = Unit("kilogram per cubic meter", "kg/m3", MASS / (LENGTH**3))
    z_u = Unit("meter", "m", LENGTH)
    wrong_g_u = Unit("meter", "m", LENGTH)

    equation = BernoulliTotalPressureEquation()

    with pytest.raises(PhysicalDomainError):
        equation.calculate(
            static_pressure=PhysicalQuantity(100000.0, 0.0, pa),
            velocity=PhysicalQuantity(-1.0, 0.0, v_u),
            density=PhysicalQuantity(1.2, 0.0, rho_u),
            elevation=PhysicalQuantity(0.0, 0.0, z_u),
            gravity=PhysicalQuantity(9.81, 0.0, Unit("m/s2", "m/s2", LENGTH / (TIME**2))),
        )

    with pytest.raises(DimensionalityError):
        equation.calculate(
            static_pressure=PhysicalQuantity(100000.0, 0.0, pa),
            velocity=PhysicalQuantity(1.0, 0.0, v_u),
            density=PhysicalQuantity(1.2, 0.0, rho_u),
            elevation=PhysicalQuantity(0.0, 0.0, z_u),
            gravity=PhysicalQuantity(9.81, 0.0, wrong_g_u),
        )
