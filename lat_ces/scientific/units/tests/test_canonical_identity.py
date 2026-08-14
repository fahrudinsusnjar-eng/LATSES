"""
LAT-CES Scientific Core
Canonical Unit / Dimension / PhysicalQuantity identity regression tests.

ADAPT-001: ensure compatibility import paths resolve to the same canonical
class objects rather than introducing parallel implementations.
"""

from lat_ces.core.dimensions import Dimension as CoreDimension
from lat_ces.core.dimensions import Unit as CoreUnit
from lat_ces.scientific.dimensions.dimension import Dimension as ScientificDimension
from lat_ces.scientific.units.dimension import Dimension as UnitsDimension
from lat_ces.scientific.units.units import Unit as ScientificUnit
from lat_ces.scientific.quantity import PhysicalQuantity
from lat_ces.scientific.quantity.quantity import PhysicalQuantity as QuantityModulePhysicalQuantity


def test_dimension_identity_is_canonical():
    assert ScientificDimension is CoreDimension
    assert UnitsDimension is CoreDimension


def test_unit_identity_is_canonical():
    assert ScientificUnit is CoreUnit


def test_physical_quantity_identity_is_canonical():
    assert PhysicalQuantity is QuantityModulePhysicalQuantity
