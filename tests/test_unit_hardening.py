import math

import pytest

from lat_ces.scientific.dimensions.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.units.units import Unit, UnitSKOError


def test_hardening_fractional_exponents():
    """Verifikuje ponašanje pri korjenovanju i razlomljenim eksponentima."""
    meter = Unit("meter", "m", LENGTH)
    sqrt_meter = meter ** 0.5

    assert sqrt_meter.dimension == LENGTH ** 0.5
    assert sqrt_meter.symbol == "m^0.5"
    assert sqrt_meter.scale_factor == pytest.approx(1.0)


def test_hardening_released_immutability():
    """Sprečava bilo kakvo mijenjanje statusa ili parametara nakon postavljanja u RELEASED."""
    meter = Unit("meter", "m", LENGTH, status="DRAFT")
    meter.set_status("RELEASED")

    assert meter.status == "RELEASED"

    with pytest.raises(UnitSKOError):
        meter.set_status("DRAFT")

    with pytest.raises(UnitSKOError):
        meter.set_status("VERIFIED")


def test_hardening_floating_point_precision():
    """Verifikuje da višestruke algebarske transformacije ne akumuliraju float greške."""
    second = Unit("second", "s", TIME)

    scaled = second * 1e6 / 1e6

    assert math.isclose(scaled.scale_factor, 1.0, rel_tol=1e-9)


def test_hardening_derived_unit_sko_defaults():
    """Osigurava da novonastale složene jedinice dobiju svjež UUID i defaultni DRAFT status."""
    kilogram = Unit("kilogram", "kg", MASS)
    meter = Unit("meter", "m", LENGTH)

    momentum = kilogram * meter

    assert momentum.status == "DRAFT"
    assert momentum.uuid is not None
    assert momentum.uuid != kilogram.uuid
    assert momentum.uuid != meter.uuid
