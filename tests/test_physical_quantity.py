import math

import pytest

from lat_ces.scientific.dimensions.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.quantities.quantity import PhysicalQuantity
from lat_ces.scientific.units.derived_units import ENERGY_DIM, FORCE_DIM, PLANCK_CONSTANT, SPEED_OF_LIGHT
from lat_ces.scientific.units.unit import (
    CENTIMETER,
    KILOGRAM,
    METER,
    METERS_PER_SECOND_SQUARED,
    SECOND,
    IncompatibleUnitsError,
)
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

    with pytest.raises(IncompatibleUnitsError):
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


def test_quantity_creation():
    q = PhysicalQuantity(10.0, METER)
    assert q.value == 10.0
    assert q.unit == METER
    assert q.dimension == LENGTH


def test_quantity_addition_compatible():
    q1 = PhysicalQuantity(1.0, METER)
    q2 = PhysicalQuantity(50.0, CENTIMETER)
    result = q1 + q2
    assert result.unit == METER
    assert result.value == 1.5


def test_quantity_addition_incompatible():
    q1 = PhysicalQuantity(1.0, METER)
    q2 = PhysicalQuantity(1.0, SECOND)
    with pytest.raises(IncompatibleUnitsError):
        _ = q1 + q2


def test_quantity_scalar_multiplication():
    q = PhysicalQuantity(2.0, METER)
    result = q * 3.0
    assert result.value == 6.0
    assert result.unit == METER


def test_velocity_calculation():
    distance = PhysicalQuantity(100.0, METER)
    time = PhysicalQuantity(10.0, SECOND)
    velocity = distance / time
    assert velocity.value == 10.0
    assert velocity.dimension.is_compatible(LENGTH / TIME)


def test_force_calculation():
    mass = PhysicalQuantity(10.0, KILOGRAM)
    accel = PhysicalQuantity(9.81, METERS_PER_SECOND_SQUARED)
    force = mass * accel
    assert force.value == pytest.approx(98.1)
    assert force.unit.symbol == "N"


def test_quantity_multiplication_area():
    q1 = PhysicalQuantity(5.0, METER)
    q2 = PhysicalQuantity(2.0, METER)
    area = q1 * q2
    assert area.value == 10.0
    assert area.dimension.exponents["length"] == 2


def test_quantity_multiplication_force():
    mass = PhysicalQuantity(2.0, KILOGRAM)
    accel = PhysicalQuantity(5.0, METERS_PER_SECOND_SQUARED)
    force = mass * accel
    assert force.value == 10.0
    assert force.dimension.is_compatible(FORCE_DIM)


def test_speed_of_light():
    assert SPEED_OF_LIGHT.value == 299792458.0
    assert SPEED_OF_LIGHT.dimension.is_compatible(LENGTH / TIME)


def test_planck_constant():
    assert PLANCK_CONSTANT.value == 6.62607015e-34
    assert PLANCK_CONSTANT.dimension.is_compatible(ENERGY_DIM * TIME)
