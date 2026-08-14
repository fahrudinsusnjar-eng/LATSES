import math

import pytest

from lat_ces.scientific.dimensions.dimension import LENGTH, MASS
from lat_ces.scientific.quantity import (
    AuditRecord,
    Equation,
    PhysicalQuantity,
    generate_quantity_hash,
    verify_quantity_integrity,
)
from lat_ces.scientific.quantities.quantity import PhysicalQuantity as LegacyPhysicalQuantity
from lat_ces.scientific.units.units import Unit, UnitSKOError


def test_canonical_and_legacy_imports_share_physical_quantity_api():
    meter = Unit("meter", "m", LENGTH)
    canonical = PhysicalQuantity(10.0, 0.5, meter)
    legacy = LegacyPhysicalQuantity(10.0, 0.5, meter)

    assert canonical.value == legacy.value == 10.0
    assert canonical.unit is meter
    assert canonical.dimension == LENGTH


def test_legacy_two_argument_constructor_is_preserved():
    meter = Unit("meter", "m", LENGTH)
    quantity = PhysicalQuantity(10.0, meter)

    assert quantity.value == 10.0
    assert quantity.uncertainty == 0.0
    assert quantity.unit is meter


def test_legacy_arithmetic_and_conversion_are_preserved():
    meter = Unit("meter", "m", LENGTH, scale_factor=1.0)
    centimetre = Unit("centimetre", "cm", LENGTH, scale_factor=0.01)
    q = PhysicalQuantity(1.0, 0.1, meter)

    converted = q.convert_to(centimetre)
    assert math.isclose(converted.value, 100.0)
    assert math.isclose(converted.uncertainty, 10.0)

    difference = converted - PhysicalQuantity(50.0, 5.0, centimetre)
    assert math.isclose(difference.value, 50.0)


def test_hardening_audit_equation_and_integrity_contracts():
    meter = Unit("meter", "m", LENGTH)
    equation = Equation("v = s / t")
    quantity = PhysicalQuantity(
        10.0,
        0.5,
        meter,
        quantity_id="PQ-TEST-001",
        name="distance",
        symbol="s",
        definition="Measured distance",
        equation=equation,
        revision="A",
    )

    assert quantity.quantity_id == "PQ-TEST-001"
    assert quantity.revision == "A"
    assert quantity.equation_object == equation
    record = quantity.add_audit("CREATE", actor="TEST")
    assert isinstance(record, AuditRecord)
    assert record.object_id == quantity.quantity_id
    assert verify_quantity_integrity(quantity, generate_quantity_hash(quantity))
    assert quantity.verify_integrity()


def test_dimension_lock_and_mismatch_regression():
    meter = Unit("meter", "m", LENGTH)
    kilogram = Unit("kilogram", "kg", MASS)
    quantity = PhysicalQuantity(1.0, 0.1, meter)

    assert quantity.validate_dimension_lock(LENGTH)
    with pytest.raises(UnitSKOError):
        quantity.validate_dimension_lock(MASS)
    with pytest.raises(UnitSKOError):
        _ = quantity + PhysicalQuantity(1.0, 0.1, kilogram)
