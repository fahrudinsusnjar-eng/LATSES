"""
LAT-CES Scientific Core
Uncertainty Engine Verification Tests (LAT-SCI-CORE-0021-TEST)
"""

import math

import pytest

from lat_ces.scientific.units.quantity import Quantity
from lat_ces.scientific.units.unit import METER, SECOND
from lat_ces.scientific.uncertainty.engine import UncertaintyEngine


def test_uncertainty_addition():
    # L1 = 10.0 +/- 0.1 m, L2 = 5.0 +/- 0.2 m
    # Combined uncertainty = sqrt(0.1^2 + 0.2^2) = sqrt(0.05) ~ 0.2236
    q1 = Quantity(10.0, METER, uncertainty=0.1)
    q2 = Quantity(5.0, METER, uncertainty=0.2)

    result = UncertaintyEngine.add(q1, q2)
    assert result.value == 15.0
    assert math.isclose(result.uncertainty, math.sqrt(0.05), rel_tol=1e-4)


def test_uncertainty_multiplication():
    # Area = L1 * L2
    # Relative uncertainty = sqrt((u1/v1)^2 + (u2/v2)^2)
    q1 = Quantity(10.0, METER, uncertainty=0.1)  # rel: 0.01
    q2 = Quantity(5.0, METER, uncertainty=0.1)  # rel: 0.02

    area = UncertaintyEngine.multiply(q1, q2)
    assert area.value == 50.0
    expected_rel_unc = math.sqrt((0.1 / 10.0) ** 2 + (0.1 / 5.0) ** 2)
    expected_abs_unc = 50.0 * expected_rel_unc
    assert math.isclose(area.uncertainty, expected_abs_unc, rel_tol=1e-4)


def test_uncertainty_power():
    # Volume = L^3 -> rel_unc(V) = 3 * rel_unc(L)
    side = Quantity(2.0, METER, uncertainty=0.02)  # rel: 0.01
    vol = UncertaintyEngine.power(side, 3)

    assert vol.value == 8.0
    # Expected rel_unc = 3 * 0.01 = 0.03 -> abs = 8.0 * 0.03 = 0.24
    assert math.isclose(vol.uncertainty, 0.24, rel_tol=1e-4)
