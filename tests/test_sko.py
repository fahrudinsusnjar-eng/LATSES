import pytest

from lat_ces.core import ScientificKnowledgeObject, SKOState


def test_sko_releases_and_freezes_after_locking():
    sko = ScientificKnowledgeObject("sko-001", "Example SKO", {"value": 1})

    assert sko.state is SKOState.DRAFT

    released_hash = sko.lock_and_release()

    assert sko.state is SKOState.RELEASED
    assert released_hash == sko.compute_hash()

    with pytest.raises(AttributeError):
        sko.title = "Changed"


def test_sko_hash_is_deterministic():
    sko = ScientificKnowledgeObject("sko-002", "Deterministic", {"nested": {"b": 2}})

    first_hash = sko.compute_hash()
    second_hash = sko.compute_hash()

    assert first_hash == second_hash
