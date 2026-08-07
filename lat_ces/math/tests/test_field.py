"""
LAT-CES Mathematical Core
Differential & Field Engine Verification Tests (LAT-MATH-CORE-0012-TEST)
"""

import pytest

from lat_ces.math.field import FieldEngine, FieldError
from lat_ces.math.vector import PhysicalVector
from lat_ces.scientific.units.quantity import Quantity
from lat_ces.scientific.units.unit import METER, SECOND


def test_gradient_1d_finite_difference():
    # Polje skalarne velicine: phi(x) = x^2 na x=2m sa dx=0.001m
    # Gradijent bi trebao biti ~ 2*x = 4.0 [dimenzija: unit / m]
    dx = Quantity(0.001, METER)

    def scalar_field(x: Quantity) -> Quantity:
        return Quantity(x.value ** 2, METER * METER)  # npr. m^2

    x_point = Quantity(2.0, METER)
    grad = FieldEngine.gradient_1d(scalar_field, x_point, dx)

    assert pytest.approx(grad.value, abs=1e-2) == 4.0
    # Dimenzijska provjera: m^2 / m = m
    assert grad.unit == METER
