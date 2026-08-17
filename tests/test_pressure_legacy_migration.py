from lat_ces.modules.pressure import FanEngine, PressureDropEngine
from lat_ces.scientific.pressure_drop import PressureDropModel, PressureError
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.core.dimensions import FLOW_RATE, PRESSURE, POWER


def test_pressure_drop_legacy_adapter_delegates_to_canonical_model():
    legacy = PressureDropEngine(loss_coefficient=2.0, air_density=1.2)
    canonical = PressureDropModel(loss_coefficient=2.0, air_density=1.2)
    assert legacy.compute_pressure_drop(5.0) == canonical.compute_pressure_drop(5.0)
    assert legacy.compute_pressure_drop(5.0) == 30.0


def test_fan_engine_preserves_legacy_api_with_canonical_quantity():
    engine = FanEngine()
    flow = PhysicalQuantity(0.1, FLOW_RATE, 0.005)
    pressure = PhysicalQuantity(200.0, PRESSURE, 10.0)
    result = engine.calculate_fan_power(flow, pressure, efficiency=0.8)
    assert result.value == 25.0
    assert result.dimension == POWER
    assert result.uncertainty > 0


def test_pressure_drop_canonical_validation_is_preserved():
    try:
        PressureDropEngine(loss_coefficient=1.0).compute_pressure_drop(-1.0)
    except PressureError:
        pass
    else:
        raise AssertionError("negative velocity must raise PressureError")
