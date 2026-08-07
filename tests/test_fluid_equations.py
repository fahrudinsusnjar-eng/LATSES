import math

import pytest

from lat_ces.scientific.dimensions.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.equations.engine import DimensionalityError
from lat_ces.scientific.equations.fluids import ContinuityEquation
from lat_ces.scientific.quantity import PhysicalQuantity
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


def test_continuity_equation_rejects_wrong_area_dimension():
    meter = Unit("meter", "m", LENGTH)
    m_s = Unit("meter per second", "m/s", LENGTH / TIME)
    wrong_area = PhysicalQuantity(2.0, 0.1, meter)
    velocity = PhysicalQuantity(10.0, 0.2, m_s)

    with pytest.raises(DimensionalityError):
        ContinuityEquation().calculate(area=wrong_area, velocity=velocity)