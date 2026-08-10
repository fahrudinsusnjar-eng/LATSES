from __future__ import annotations

import math
import uuid
from typing import Optional, Union

from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.units.units import Unit


class Measurement(PhysicalQuantity):
    """Physical quantity with explicit uncertainty-aware arithmetic."""

    def __init__(self, value: float, unit: Unit, uncertainty: float = 0.0, sko_uuid: Optional[str] = None):
        super().__init__(value=value, unit_or_uncertainty=uncertainty, maybe_unit=unit)
        self._uuid = sko_uuid or str(uuid.uuid4())

    @property
    def relative_uncertainty(self) -> float:
        if self.value == 0.0:
            return 0.0 if self.uncertainty == 0.0 else float("inf")
        return abs(self.uncertainty / self.value)

    def _coerce_measurement_operand(self, other: object) -> Optional["Measurement"]:
        if not isinstance(other, PhysicalQuantity):
            return None

        if isinstance(other, Measurement):
            return other

        return Measurement(
            value=other.value,
            unit=other.unit,
            uncertainty=float(getattr(other, "uncertainty", 0.0)),
        )

    def __add__(self, other: object) -> "Measurement":
        other_measurement = self._coerce_measurement_operand(other)
        if other_measurement is None:
            return NotImplemented

        result = super().__add__(other_measurement)
        return Measurement(result.value, result.unit, result.uncertainty)

    def __sub__(self, other: object) -> "Measurement":
        other_measurement = self._coerce_measurement_operand(other)
        if other_measurement is None:
            return NotImplemented

        result = super().__sub__(other_measurement)
        return Measurement(result.value, result.unit, result.uncertainty)

    def __mul__(self, other: Union[int, float, PhysicalQuantity]) -> "Measurement":
        if not isinstance(other, (int, float, PhysicalQuantity)):
            return NotImplemented

        result = super().__mul__(other)
        return Measurement(result.value, result.unit, result.uncertainty)

    def __repr__(self) -> str:
        return f"({self.value} +/- {self.uncertainty}) {self.unit.symbol}"


class OutOfRangeError(Exception):
    """Raised when a measurement is outside the device operating range."""


class AccuracySpec:
    """Accuracy specification combining relative and fixed absolute error."""

    def __init__(self, relative_error: float = 0.0, absolute_error: float = 0.0):
        if relative_error < 0.0 or absolute_error < 0.0:
            raise ValueError("Greške u specifikaciji tačnosti ne mogu biti negativne.")
        self.relative_error = float(relative_error)
        self.absolute_error = float(absolute_error)

    def calculate_uncertainty(self, measured_value: float) -> float:
        """Calculate absolute uncertainty for a measured value."""
        return self.absolute_error + self.relative_error * abs(measured_value)


class MeasurementDevice:
    """Measurement instrument that produces calibrated physical quantities."""

    def __init__(
        self,
        name: str,
        device_type: str,
        unit: Unit,
        accuracy_spec: AccuracySpec,
        min_range: float,
        max_range: float,
        calibration_offset: float = 0.0,
        sko_uuid: Optional[str] = None,
    ):
        if min_range >= max_range:
            raise ValueError("Minimalni opseg mora biti manji od maksimalnog.")

        self.name = name
        self.device_type = device_type
        self.unit = unit
        self.accuracy_spec = accuracy_spec
        self.min_range = float(min_range)
        self.max_range = float(max_range)
        self.calibration_offset = float(calibration_offset)
        self.uuid = sko_uuid or str(uuid.uuid4())

    def measure(self, raw_value: float) -> PhysicalQuantity:
        """Return a calibrated quantity with uncertainty from the device spec."""
        if not self.min_range <= raw_value <= self.max_range:
            raise OutOfRangeError(
                f"Očitanje {raw_value} {self.unit.symbol} je izvan radnog opsega "
                f"instrumenta '{self.name}' [{self.min_range}, {self.max_range}]."
            )

        corrected_value = raw_value - self.calibration_offset
        uncertainty = self.accuracy_spec.calculate_uncertainty(corrected_value)

        return Measurement(
            value=corrected_value,
            unit=self.unit,
            uncertainty=uncertainty,
            sko_uuid=self.uuid,
        )

    def __repr__(self) -> str:
        return (
            f"<MeasurementDevice '{self.name}' ({self.device_type}): "
            f"[{self.min_range} - {self.max_range}] {self.unit.symbol}>"
        )


def create_pitot_tube(name: str = "Standard Pitot Tube") -> MeasurementDevice:
    """Create a standard Pitot-Prandtl airflow velocity instrument."""
    from lat_ces.scientific.dimensions.dimension import LENGTH, TIME

    meter_per_second = Unit("meter per second", "m/s", LENGTH / TIME)
    accuracy = AccuracySpec(relative_error=0.015, absolute_error=0.1)
    return MeasurementDevice(
        name,
        "Pitot Tube",
        meter_per_second,
        accuracy,
        min_range=1.0,
        max_range=40.0,
    )


def create_diff_pressure_sensor(name: str = "Plenum DP Sensor") -> MeasurementDevice:
    """Create a differential-pressure transmitter for ducts and plenums."""
    from lat_ces.scientific.dimensions.dimension import LENGTH, MASS, TIME

    pascal = Unit("pascal", "Pa", MASS / (LENGTH * (TIME**2)))
    accuracy = AccuracySpec(relative_error=0.005, absolute_error=1.0)
    return MeasurementDevice(
        name,
        "Differential Pressure Transmitter",
        pascal,
        accuracy,
        min_range=0.0,
        max_range=2000.0,
    )