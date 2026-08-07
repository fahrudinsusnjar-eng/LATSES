import math

import pytest

from lat_ces.scientific.dimensions.dimension import DIMENSIONLESS, LENGTH, MASS, TIME
from lat_ces.scientific.equations.engine import DimensionalityError, PhysicalDomainError
from lat_ces.scientific.equations.fluids import PlenumPressureDropEquation
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


def test_plenum_pressure_drop_calculation_and_uncertainty():
    """Validate Delta-p = zeta * p_dyn and uncertainty propagation."""
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    dimless = Unit("dimensionless", "-", DIMENSIONLESS)

    zeta = PhysicalQuantity(1.5, 0.05, dimless)
    p_dyn = PhysicalQuantity(200.0, 10.0, pascal)

    equation = PlenumPressureDropEquation()
    delta_p = equation.calculate(resistance_coefficient=zeta, dynamic_pressure=p_dyn)

    assert delta_p.value == pytest.approx(300.0)
    assert delta_p.unit.symbol == "Pa"

    expected_rel_unc = math.sqrt((0.05 / 1.5) ** 2 + (10.0 / 200.0) ** 2)
    assert delta_p.relative_uncertainty == pytest.approx(expected_rel_unc, rel=1e-4)
    assert delta_p.uncertainty == pytest.approx(300.0 * expected_rel_unc, rel=1e-4)


def test_plenum_pressure_drop_domain_validation():
    """Reject negative resistance coefficient or dynamic pressure."""
    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    dimless = Unit("dimensionless", "-", DIMENSIONLESS)

    negative_zeta = PhysicalQuantity(-1.0, 0.05, dimless)
    p_dyn = PhysicalQuantity(200.0, 10.0, pascal)

    equation = PlenumPressureDropEquation()
    with pytest.raises(PhysicalDomainError):
        equation.calculate(resistance_coefficient=negative_zeta, dynamic_pressure=p_dyn)


def test_plenum_pressure_drop_dimensionality_rejection():
    """Reject wrong pressure dimension (e.g. length instead of pressure)."""
    meter = Unit("meter", "m", LENGTH)
    dimless = Unit("dimensionless", "-", DIMENSIONLESS)

    zeta = PhysicalQuantity(1.5, 0.05, dimless)
    wrong_pressure = PhysicalQuantity(200.0, 10.0, meter)

    equation = PlenumPressureDropEquation()
    with pytest.raises(DimensionalityError):
        equation.calculate(resistance_coefficient=zeta, dynamic_pressure=wrong_pressure)
