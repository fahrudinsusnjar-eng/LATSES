from lat_ces.core.dimensions import AREA, DENSITY, FLOW_RATE, MASS_FLOW, VELOCITY
from lat_ces.modules.plenum import PlenumEngine as LegacyPlenumEngine
from lat_ces.scientific.plenum import PlenumEngine as CanonicalPlenumEngine
from lat_ces.scientific.quantity import PhysicalQuantity


def quantity(value: float, dimension):
    return PhysicalQuantity(value=value, dimension=dimension)


def test_legacy_plenum_is_canonical_facade():
    assert LegacyPlenumEngine is CanonicalPlenumEngine


def test_plenum_airflow_uses_canonical_quantity_engine():
    engine = CanonicalPlenumEngine()
    result = engine.calculate_airflow(
        quantity(2.0, AREA),
        quantity(0.5, VELOCITY),
    )

    assert result.dimension == FLOW_RATE
    assert result.value == 1.0
    assert result.unit == PhysicalQuantity(value=1.0, dimension=FLOW_RATE).unit


def test_plenum_mass_flow_uses_canonical_quantity_engine():
    engine = LegacyPlenumEngine()
    result = engine.calculate_mass_flow(
        quantity(1.2, DENSITY),
        quantity(2.0, FLOW_RATE),
    )

    assert result.dimension == MASS_FLOW
    assert result.value == 2.4


def test_plenum_rejects_wrong_dimensions():
    engine = CanonicalPlenumEngine()

    try:
        engine.calculate_airflow(
            quantity(2.0, AREA),
            quantity(1.0, FLOW_RATE),
        )
    except ValueError as exc:
        assert "velocity" in str(exc)
    else:
        raise AssertionError("Expected dimension validation failure")
