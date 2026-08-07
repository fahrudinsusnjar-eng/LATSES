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


def test_physical_quantity_division_and_scalar_operations():
    meter = Unit("meter", "m", LENGTH)
    quantity = PhysicalQuantity(10.0, 0.5, meter)

    divided = quantity / 2
    assert divided.value == 5.0
    assert divided.uncertainty == 0.25
    assert divided.unit is meter

    reciprocal = 20 / quantity
    assert reciprocal.value == 2.0
    assert math.isclose(reciprocal.uncertainty, 0.1)
    assert reciprocal.unit.dimension == LENGTH ** -1


def test_physical_quantity_power_and_sqrt():
    meter = Unit("meter", "m", LENGTH)
    quantity = PhysicalQuantity(4.0, 0.2, meter)

    squared = quantity**2
    assert squared.value == 16.0
    assert math.isclose(squared.uncertainty, 1.6)
    assert squared.unit.dimension == LENGTH**2

    square_root = quantity.sqrt()
    assert square_root.value == 2.0
    assert math.isclose(square_root.uncertainty, 0.05)
    assert square_root.unit.dimension == LENGTH**0.5


def test_physical_quantity_division_by_zero_raises():
    meter = Unit("meter", "m", LENGTH)
    quantity = PhysicalQuantity(10.0, 0.5, meter)
    zero = PhysicalQuantity(0.0, 0.0, meter)

    with pytest.raises(ZeroDivisionError):
        _ = quantity / zero
    with pytest.raises(ZeroDivisionError):
        _ = quantity / 0
    with pytest.raises(ZeroDivisionError):
        _ = 1 / zero
