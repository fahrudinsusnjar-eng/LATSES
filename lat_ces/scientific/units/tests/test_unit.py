"""Unit tests for unit definitions and behavior."""

import pytest

from lat_ces.scientific.units.dimension import LENGTH
from lat_ces.scientific.units.unit import Unit


def test_unit_requires_dimension():
	meter = Unit("meter", "m", LENGTH)
	assert meter.dimension == LENGTH


def test_unit_without_dimension_fails():
	with pytest.raises(Exception):
		Unit("invalid", "inv", None)
