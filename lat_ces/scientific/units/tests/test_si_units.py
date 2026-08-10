"""Unit tests for SI unit behavior and constants."""

from lat_ces.scientific.units.dimension import LENGTH, MASS, TIME
from lat_ces.scientific.units.unit import KILOGRAM, METER, SECOND
from lat_ces.core.sko import ScientificKnowledgeObject


def test_si_base_units_exist():
	assert METER.dimension == LENGTH
	assert KILOGRAM.dimension == MASS
	assert SECOND.dimension == TIME


def test_unit_is_sko():
	assert isinstance(METER, ScientificKnowledgeObject)
	assert METER.uuid is not None
