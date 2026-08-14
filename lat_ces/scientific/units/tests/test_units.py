"""
LAT-CES Scientific Core
Unit Engine Verification Tests (LAT-SCI-CORE-0015)

ADAPT-001: exercise the canonical Unit implementation from core.dimensions.
"""

import pytest

from lat_ces.core.dimensions import LENGTH, TIME, VELOCITY
from lat_ces.core.dimensions import Unit, UnitSKOError


def test_unit_creation_valid():
    meter = Unit(name="meter", symbol="m", dimension=LENGTH, scale_factor=1.0)
    assert meter.name == "meter"
    assert meter.symbol == "m"
    assert meter.dimension == LENGTH
    assert meter.scale_factor == 1.0


def test_unit_requires_dimension():
    with pytest.raises(TypeError):
        Unit(name="invalid", symbol="inv", dimension=None, scale_factor=1.0)


def test_unit_multiplication_derived_dimension():
    meter = Unit(name="meter", symbol="m", dimension=LENGTH, scale_factor=1.0)
    second = Unit(name="second", symbol="s", dimension=TIME, scale_factor=1.0)

    mps = meter / second
    assert mps.dimension == VELOCITY
    assert mps.symbol == "m/s"


def test_unit_compatibility():
    meter = Unit(name="meter", symbol="m", dimension=LENGTH, scale_factor=1.0)
    kilometer = Unit(name="kilometer", symbol="km", dimension=LENGTH, scale_factor=1000.0)
    second = Unit(name="second", symbol="s", dimension=TIME, scale_factor=1.0)

    assert meter.dimension == kilometer.dimension
    assert meter.dimension != second.dimension


def test_unit_conversion_factor():
    meter = Unit(name="meter", symbol="m", dimension=LENGTH, scale_factor=1.0)
    kilometer = Unit(name="kilometer", symbol="km", dimension=LENGTH, scale_factor=1000.0)

    assert kilometer.scale_factor / meter.scale_factor == 1000.0
