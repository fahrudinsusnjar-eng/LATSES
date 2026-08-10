import pytest

from lat_ces.core.sko import ScientificKnowledgeObject, SKOState


def test_sko_immutability():
    sko = ScientificKnowledgeObject("SKO-001", "Test SKO", {"param": 42})
    assert sko.state == SKOState.DRAFT

    sko_hash = sko.lock_and_release()
    assert sko.state == SKOState.RELEASED
    assert len(sko_hash) == 64

    with pytest.raises(AttributeError):
        sko.title = "Novi Naslov"


def test_sko_hash_is_deterministic():
    sko = ScientificKnowledgeObject("sko-002", "Deterministic", {"nested": {"b": 2}})

    first_hash = sko.compute_hash()
    second_hash = sko.compute_hash()

    assert first_hash == second_hash


def test_sko_initialization():
    sko = ScientificKnowledgeObject(
        name="Test Object",
        object_type="Generic",
        definition="Test definition",
        assumptions=["Ideal conditions"],
        limitations=["None"],
    )
    assert sko.uuid is not None
    assert sko.status == "Draft"


def test_sko_status_transition():
    sko = ScientificKnowledgeObject(
        name="Test Object",
        object_type="Generic",
        definition="Test definition",
    )
    sko.approve(approved_by="Lead Architect")
    assert sko.status == "Approved"
    assert sko.approved_by == "Lead Architect"
