"""Unit tests for unit conversion behavior."""

import pytest

from lat_ces.scientific.units.dimension import LENGTH, TEMPERATURE
from lat_ces.scientific.units.unit import KELVIN, METER, SECOND, Unit, UnitError


CENTIMETER = Unit("centimeter", "cm", LENGTH, 0.01)
CELSIUS = Unit("celsius", "degC", TEMPERATURE, 1.0, 273.15)


def convert(value: float, from_unit: Unit, to_unit: Unit) -> float:
	if not from_unit.is_compatible(to_unit):
		raise UnitError("Incompatible unit conversion")

	base_value = value * from_unit.scale_factor + from_unit.offset
	return (base_value - to_unit.offset) / to_unit.scale_factor


def test_linear_unit_conversion():
	result = convert(1.0, CENTIMETER, METER)
	assert result == 0.01


def test_invalid_dimension_conversion():
	with pytest.raises(Exception):
		convert(1.0, METER, SECOND)


def test_temperature_conversion():
	kelvin_val = convert(0.0, CELSIUS, KELVIN)
	assert kelvin_val == 273.15
