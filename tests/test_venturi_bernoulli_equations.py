import pytest

from lat_ces.scientific.dimensions.dimension import DIMENSIONLESS, LENGTH, MASS, TIME
from lat_ces.scientific.equations.engine import PhysicalDomainError
from lat_ces.scientific.equations.fluids import BernoulliTotalPressureEquation, VenturiFlowEquation
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


def test_venturi_flow_calculation():
    """Verifikuje proračun zapreminskog protoka kroz Venturi cijev sa neodređenošću."""
    m2 = Unit("square meter", "m²", LENGTH**2)
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    kg_m3 = Unit("kilogram per cubic meter", "kg/m³", MASS / (LENGTH**3))
    dimless = Unit("dimensionless", "-", DIMENSIONLESS)

    a1 = PhysicalQuantity(0.1, 0.001, m2)
    a2 = PhysicalQuantity(0.025, 0.0005, m2)
    dp = PhysicalQuantity(5000.0, 50.0, pascal)
    rho = PhysicalQuantity(1.2, 0.01, kg_m3)
    cd = PhysicalQuantity(0.98, 0.01, dimless)

    equation = VenturiFlowEquation()
    flow = equation.calculate(
        area_1=a1,
        area_2=a2,
        delta_p=dp,
        density=rho,
        discharge_coefficient=cd,
    )

    assert flow.value == pytest.approx(2.3098, rel=1e-3)
    assert flow.unit.symbol == "m³/s"
    assert flow.uncertainty > 0.0


def test_venturi_flow_domain_error_when_a2_greater_than_a1():
    """Verifikuje odbijanje kada je grlo veće od ulaza (A2 >= A1)."""
    m2 = Unit("square meter", "m²", LENGTH**2)
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    kg_m3 = Unit("kilogram per cubic meter", "kg/m³", MASS / (LENGTH**3))
    dimless = Unit("dimensionless", "-", DIMENSIONLESS)

    a1 = PhysicalQuantity(0.025, 0.001, m2)
    a2 = PhysicalQuantity(0.1, 0.0005, m2)
    dp = PhysicalQuantity(5000.0, 50.0, pascal)
    rho = PhysicalQuantity(1.2, 0.01, kg_m3)
    cd = PhysicalQuantity(0.98, 0.01, dimless)

    equation = VenturiFlowEquation()
    with pytest.raises(PhysicalDomainError):
        equation.calculate(
            area_1=a1,
            area_2=a2,
            delta_p=dp,
            density=rho,
            discharge_coefficient=cd,
        )


def test_bernoulli_total_pressure():
    """Verifikuje Bernoulli-jev ukupni pritisak p_total = p_stat + p_dyn + p_hydro."""
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)
    kg_m3 = Unit("kilogram per cubic meter", "kg/m³", MASS / (LENGTH**3))
    meter = Unit("meter", "m", LENGTH)
    m_s2 = Unit("meter per second squared", "m/s²", LENGTH / (TIME**2))

    p_stat = PhysicalQuantity(101325.0, 100.0, pascal)
    velocity = PhysicalQuantity(10.0, 0.2, m_s)
    rho = PhysicalQuantity(1.2, 0.01, kg_m3)
    z = PhysicalQuantity(5.0, 0.1, meter)
    g = PhysicalQuantity(9.81, 0.001, m_s2)

    equation = BernoulliTotalPressureEquation()
    p_total = equation.calculate(
        static_pressure=p_stat,
        velocity=velocity,
        density=rho,
        elevation=z,
        gravity=g,
    )

    assert p_total.value == pytest.approx(101443.86, rel=1e-4)
    assert p_total.unit.symbol == "Pa"
    assert p_total.uncertainty > 0.0
