"""
LAT-CES Mathematical Core
Vector Engine Verification Tests (LAT-MATH-CORE-0011-TEST)
"""

import math

import pytest

from lat_ces.math.vector import PhysicalVector, VectorError
from lat_ces.scientific.units.quantity import Quantity
from lat_ces.scientific.units.unit import METER, SECOND


def test_vector_creation():
    v1 = Quantity(3.0, METER)
    v2 = Quantity(4.0, METER)
    vec = PhysicalVector([v1, v2])

    assert len(vec) == 2
    assert vec[0] == v1
    assert vec[1] == v2


def test_vector_magnitude():
    # 3m i 4m -> Magnitude 5m
    v1 = Quantity(3.0, METER)
    v2 = Quantity(4.0, METER)
    vec = PhysicalVector([v1, v2])

    mag = vec.magnitude()
    assert mag.value == 5.0
    assert mag.unit == METER


test_vector_creation()
test_vector_magnitude()
