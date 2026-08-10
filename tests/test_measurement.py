import math

import pytest

from lat_ces.scientific.dimensions.dimension import LENGTH
from lat_ces.scientific.measurement import (
    AccuracySpec,
    Measurement,
    MeasurementDevice,
    OutOfRangeError,
    create_diff_pressure_sensor,
    create_pitot_tube,
)
from lat_ces.scientific.units.unit import METER
from lat_ces.scientific.units.units import Unit


def test_measurement_creation():
    m = Measurement(value=10.0, unit=METER, uncertainty=0.1)

    assert m.value == 10.0
    assert m.uncertainty == 0.1
    assert m.relative_uncertainty == 0.01


def test_measurement_addition():
    m1 = Measurement(10.0, METER, uncertainty=0.3)
    m2 = Measurement(20.0, METER, uncertainty=0.4)

    res = m1 + m2

    assert isinstance(res, Measurement)
    assert res.value == 30.0
    assert res.uncertainty == 0.5


def test_measurement_device_applies_calibration_and_uncertainty():
    meter = Unit("meter", "m", LENGTH)
    device = MeasurementDevice(
        name="laser rangefinder",
        device_type="distance",
        unit=meter,
        accuracy_spec=AccuracySpec(relative_error=0.01, absolute_error=0.05),
        min_range=0.0,
        max_range=200.0,
        calibration_offset=0.5,
        sko_uuid="device-123",
    )

    measurement = device.measure(100.0)

    assert measurement.value == 99.5
    assert math.isclose(measurement.uncertainty, 1.045)
    assert measurement.unit is meter
    assert measurement._uuid == "device-123"


def test_measurement_device_accepts_range_boundaries():
    meter = Unit("meter", "m", LENGTH)
    device = MeasurementDevice("meter", "distance", meter, AccuracySpec(), 1.0, 2.0)

    assert device.measure(1.0).value == 1.0
    assert device.measure(2.0).value == 2.0


def test_measurement_device_rejects_out_of_range_values():
    meter = Unit("meter", "m", LENGTH)
    device = MeasurementDevice("meter", "distance", meter, AccuracySpec(), 1.0, 2.0)

    with pytest.raises(OutOfRangeError):
        device.measure(0.99)
    with pytest.raises(OutOfRangeError):
        device.measure(2.01)


def test_measurement_configuration_rejects_invalid_errors_and_range():
    meter = Unit("meter", "m", LENGTH)

    with pytest.raises(ValueError):
        AccuracySpec(relative_error=-0.01)
    with pytest.raises(ValueError):
        AccuracySpec(absolute_error=-0.01)
    with pytest.raises(ValueError):
        MeasurementDevice("meter", "distance", meter, AccuracySpec(), 2.0, 2.0)


def test_create_pitot_tube_factory():
    pitot = create_pitot_tube("Roof Pitot")

    assert pitot.name == "Roof Pitot"
    assert pitot.device_type == "Pitot Tube"
    assert pitot.unit.symbol == "m/s"
    assert pitot.min_range == 1.0
    assert pitot.max_range == 40.0
    assert pitot.accuracy_spec.relative_error == 0.015
    assert pitot.accuracy_spec.absolute_error == 0.1


def test_create_diff_pressure_sensor_factory():
    sensor = create_diff_pressure_sensor()

    assert sensor.name == "Plenum DP Sensor"
    assert sensor.device_type == "Differential Pressure Transmitter"
    assert sensor.unit.symbol == "Pa"
    assert sensor.min_range == 0.0
    assert sensor.max_range == 2000.0
    assert sensor.accuracy_spec.relative_error == 0.005
    assert sensor.accuracy_spec.absolute_error == 1.0