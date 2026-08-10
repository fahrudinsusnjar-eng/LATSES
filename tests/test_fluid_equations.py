import math

import pytest

from lat_ces.scientific.dimensions.dimension import DIMENSIONLESS, LENGTH, MASS, TIME
from lat_ces.scientific.equations.engine import DimensionalityError, PhysicalDomainError
from lat_ces.scientific.equations.fluids import (
    ContinuityEquation,
    MassFlowEquation,
    PlenumPressureDropEquation,
    VolumetricFlowEquation,
)
from lat_ces.scientific.quantities.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


def test_continuity_equation_with_uncertainty():
    m2 = Unit("square meter", "m²", LENGTH**2)
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)
    area = PhysicalQuantity(2.0, 0.1, m2)
    velocity = PhysicalQuantity(10.0, 0.2, m_s)

    flow = ContinuityEquation().calculate(area=area, velocity=velocity)

    assert flow.value == pytest.approx(20.0)
    assert flow.unit.symbol == "m²·m/s"
    expected_relative_uncertainty = math.sqrt((0.1 / 2.0) ** 2 + (0.2 / 10.0) ** 2)
    assert flow.relative_uncertainty == pytest.approx(expected_relative_uncertainty)


def test_volumetric_flow_equation_evaluate_alias():
    m2 = Unit("square meter", "m²", LENGTH**2)
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)
    area = PhysicalQuantity(2.0, 0.1, m2)
    velocity = PhysicalQuantity(10.0, 0.2, m_s)

    result = VolumetricFlowEquation().evaluate(area=area, velocity=velocity)

    assert result.value == pytest.approx(20.0)
    assert result.unit.symbol == "m²·m/s"


def test_mass_flow_equation_evaluate_alias():
    rho_u = Unit("kilogram per cubic meter", "kg/m3", MASS / (LENGTH**3))
    q_u = Unit("cubic meter per second", "m3/s", LENGTH**3 / TIME)
    density = PhysicalQuantity(1.2, 0.012, rho_u)
    flow = PhysicalQuantity(2.0, 0.05, q_u)

    result = MassFlowEquation().evaluate(density=density, volumetric_flow=flow)

    assert result.value == pytest.approx(2.4)
    assert result.unit.symbol == "kg/s"
    expected_relative_uncertainty = math.sqrt((0.012 / 1.2) ** 2 + (0.05 / 2.0) ** 2)
    assert result.relative_uncertainty == pytest.approx(expected_relative_uncertainty)


def test_continuity_equation_rejects_wrong_area_dimension():
    meter = Unit("meter", "m", LENGTH)
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)
    wrong_area = PhysicalQuantity(2.0, 0.1, meter)
    velocity = PhysicalQuantity(10.0, 0.2, m_s)

    with pytest.raises(DimensionalityError):
        ContinuityEquation().calculate(area=wrong_area, velocity=velocity)


def test_continuity_equation_rejects_negative_velocity():
    m2 = Unit("square meter", "m²", LENGTH**2)
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)
    area = PhysicalQuantity(2.0, 0.1, m2)
    velocity = PhysicalQuantity(-1.0, 0.1, m_s)

    with pytest.raises(PhysicalDomainError):
        ContinuityEquation().calculate(area=area, velocity=velocity)


def test_plenum_pressure_drop_equation_calculation():
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    zeta = PhysicalQuantity(1.8, 0.05, Unit("dimensionless", "-", DIMENSIONLESS))
    dynamic_pressure = PhysicalQuantity(120.0, 3.0, pascal)

    pressure_drop = PlenumPressureDropEquation().calculate(
        resistance_coefficient=zeta,
        dynamic_pressure=dynamic_pressure,
    )

    assert pressure_drop.value == pytest.approx(216.0)
    assert pressure_drop.unit.symbol == "Pa"


def test_plenum_pressure_drop_equation_rejects_invalid_domain():
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    zeta = PhysicalQuantity(-0.1, 0.0, Unit("dimensionless", "-", DIMENSIONLESS))
    dynamic_pressure = PhysicalQuantity(120.0, 3.0, pascal)

    with pytest.raises(PhysicalDomainError):
        PlenumPressureDropEquation().calculate(
            resistance_coefficient=zeta,
            dynamic_pressure=dynamic_pressure,
        )