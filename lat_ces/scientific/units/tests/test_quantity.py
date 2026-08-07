"""
LAT-CES Scientific Core
Quantity Engine Verification Tests (LAT-SCI-CORE-0018)
"""

import pytest

from lat_ces.scientific.units.quantity import Quantity, QuantityError
from lat_ces.scientific.units.unit import KILOGRAM, METER, NEWTON, SECOND


def test_quantity_creation():
    q = Quantity(value=10.5, unit=METER)
    assert q.value == 10.5
    assert q.unit == METER
    assert q.dimension == METER.dimension


def test_quantity_addition_same_unit():
    q1 = Quantity(10.0, METER)
    q2 = Quantity(5.0, METER)
    res = q1 + q2
    assert res.value == 15.0
    assert res.unit == METER


def test_quantity_addition_incompatible_units():
    q1 = Quantity(10.0, METER)
    q2 = Quantity(5.0, SECOND)
    with pytest.raises(QuantityError):
        _ = q1 + q2


def test_quantity_multiplication_physics():
    mass = Quantity(2.0, KILOGRAM)
    accel = Quantity(9.81, METER / (SECOND * SECOND))
    force = mass * accel

    assert force.value == 19.62
    assert force.unit.dimension == NEWTON.dimension


def test_quantity_conversion():
    from lat_ces.scientific.units.dimension import LENGTH
    from lat_ces.scientific.units.unit import Unit

    kilometer = Unit("kilometer", "km", LENGTH, 1000.0)
    q_m = Quantity(1500.0, METER)
    q_km = q_m.to(kilometer)

    assert q_km.value == 1.5
    assert q_km.unit == kilometer
