"""
LAT-CES Scientific Core
Scientific Knowledge Registry Tests (LAT-SCI-CORE-0020-TEST)
"""

import pytest

from lat_ces.scientific.registry.registry import RegistryError, ScientificKnowledgeRegistry
from lat_ces.scientific.units.dimension import LENGTH
from lat_ces.scientific.units.unit import METER, SECOND


def test_registry_singleton_or_instance():
    reg = ScientificKnowledgeRegistry()
    reg.register_unit("m", METER)
    assert reg.get_unit("m") == METER


def test_registry_duplicate_registration_fails():
    reg = ScientificKnowledgeRegistry()
    reg.register_unit("m", METER)
    with pytest.raises(RegistryError):
        reg.register_unit("m", METER)


def test_registry_lookup_nonexistent():
    reg = ScientificKnowledgeRegistry()
    with pytest.raises(RegistryError):
        reg.get_unit("non_existent_unit")
