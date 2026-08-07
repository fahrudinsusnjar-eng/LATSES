import math

import pytest

from lat_ces.scientific.dimensions.dimension import LENGTH, MASS
from lat_ces.scientific.quantities.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit, UnitSKOError


def test_physical_quantity_uncertainty_propagation():
    meter = Unit("meter", "m", LENGTH)
    second = Unit("second", "s", LENGTH)

    q1 = PhysicalQuantity(10.0, 0.5, meter)
    q2 = PhysicalQuantity(5.0, 0.25, meter)

    summed = q1 + q2
    assert summed.value == 15.0
    assert math.isclose(summed.uncertainty, 0.5590169943749475)


def test_physical_quantity_dimension_mismatch_raises():
    meter = Unit("meter", "m", LENGTH)
    kilogram = Unit("kilogram", "kg", MASS)

    q1 = PhysicalQuantity(1.0, 0.1, meter)
    q2 = PhysicalQuantity(1.0, 0.1, kilogram)

    with pytest.raises(UnitSKOError):
        _ = q1 + q2
