import math

from lat_ces.core.dimensions import LENGTH, MASS, TIME, VELOCITY
from lat_ces.core.dimensions import Unit
from lat_ces.modules.quantity import PhysicalQuantity as LegacyPhysicalQuantity
from lat_ces.scientific.quantity import PhysicalQuantity as CanonicalPhysicalQuantity
from lat_ces.scientific.units.registry import dimension_to_unit, kelvin_interval


def test_legacy_import_resolves_to_canonical_class():
    assert LegacyPhysicalQuantity is CanonicalPhysicalQuantity


def test_dimension_mapping_uses_canonical_units():
    quantity = LegacyPhysicalQuantity(10.0, LENGTH, 0.1)
    assert quantity.__class__ is CanonicalPhysicalQuantity
    assert quantity.dimension == LENGTH
    assert quantity.unit is dimension_to_unit(LENGTH)
    assert isinstance(quantity.unit, Unit)


def test_legacy_keyword_dimension_form_is_preserved():
    quantity = LegacyPhysicalQuantity(value=10.0, dimension=LENGTH, uncertainty=0.1)
    assert quantity.value == 10.0
    assert quantity.dimension == LENGTH
    assert quantity.uncertainty == 0.1


def test_derived_dimension_mapping_is_canonical():
    quantity = LegacyPhysicalQuantity(100.0, LENGTH, 2.0) / LegacyPhysicalQuantity(10.0, TIME, 0.1)
    assert quantity.dimension == VELOCITY
    assert quantity.unit is dimension_to_unit(VELOCITY)
    expected_u = 10.0 * math.sqrt((2.0 / 100.0) ** 2 + (0.1 / 10.0) ** 2)
    assert math.isclose(quantity.uncertainty, expected_u)


def test_temperature_interval_is_zero_offset():
    assert kelvin_interval.dimension.Theta == 1
    assert kelvin_interval.offset == 0.0
    assert kelvin_interval.scale_factor == 1.0
