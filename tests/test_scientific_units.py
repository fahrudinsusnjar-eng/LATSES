import pytest

from lat_ces.core.dimensions import FORCE, LENGTH, MASS, TEMPERATURE, TIME, Unit, UnitSKOError


kilogram = Unit("kilogram", "kg", MASS)
meter = Unit("meter", "m", LENGTH)
second = Unit("second", "s", TIME)


def test_unit_algebra_newton_derivation():
    """UNIT-T006: N = kg * m / s^2 fully generates the FORCE dimension."""
    newton_derived = kilogram * meter / (second ** 2)

    assert newton_derived.dimension == FORCE
    assert newton_derived.symbol == "kg·m/s^2"
    assert newton_derived.scale_factor == 1.0
    assert newton_derived.status == "DRAFT"


def test_affine_unit_algebra_rejection():
    """Affine units with offsets should raise when used in compound algebra."""
    celsius = Unit("celsius", "°C", TEMPERATURE, scale_factor=1.0, offset=273.15)

    with pytest.raises(UnitSKOError):
        _ = celsius * meter