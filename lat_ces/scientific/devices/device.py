"""Compatibility exports for scientific measurement devices."""

from lat_ces.scientific.measurement import (
    AccuracySpec,
    MeasurementDevice,
    OutOfRangeError,
    create_diff_pressure_sensor,
    create_pitot_tube,
)

__all__ = [
    "MeasurementDevice",
    "AccuracySpec",
    "OutOfRangeError",
    "create_pitot_tube",
    "create_diff_pressure_sensor",
]
