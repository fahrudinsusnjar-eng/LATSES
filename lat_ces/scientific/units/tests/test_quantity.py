"""
LAT-CES Scientific Core
Quantity Engine Verification Tests (LAT-SCI-CORE-0018)

ADAPT-001: canonical PhysicalQuantity regression coverage.
"""

import pytest

from lat_ces.core.dimensions import LENGTH, FORCE, kilogram, meter, second, Unit
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit as PublicUnit


def test_physical_quantity_creation():
    q = PhysicalQuantity(10.5, meter)
    assert q.value == 10.5
    assert q.unit == meter
    assert q.dimension == LENGTH


def test_physical_quantity_addition_same_unit():
    q1 = PhysicalQuantity(10.0, meter)
    q2 = PhysicalQuantity(5.0, meter)
    res = q1 + q2
    assert res.value == 15.0
    assert res.unit == meter


def test_physical_quantity_addition_incompatible_units():
    q1 = PhysicalQuantity(10.0, meter)
    q2 = PhysicalQuantity(5.0, second)
    with pytest.raises(Exception):
        _ = q1 + q2


def test_physical_quantity_multiplication_physics():
    mass = PhysicalQuantity(2.0, kilogram)
    acceleration_unit = meter / (second * second)
    accel = PhysicalQuantity(9.81, acceleration_unit)
    force = mass * accel

    assert force.value == 19.62
    assert force.unit.dimension == FORCE


def test_physical_quantity_conversion():
    kilometer = Unit("kilometer", "km", LENGTH, 1000.0)
    q_m = PhysicalQuantity(1500.0, meter)
    q_km = q_m.convert_to(kilometer)

    assert q_km.value == 1.5
    assert q_km.unit == kilometer


def test_public_unit_is_canonical_unit():
    assert PublicUnit is Unit
