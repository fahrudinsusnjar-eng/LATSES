from lat_ces.core.axioms import AuthorityLevel, ConstitutionalAxiom, ConstitutionalAxioms


def test_constitutional_axioms_are_available():
    axioms = ConstitutionalAxioms.all()

    assert len(axioms) >= 4
    assert any(axiom.name == "identity" for axiom in axioms)
    assert any("realnost" in axiom.statement.lower() for axiom in axioms)


def test_axiom_authority():
    assert ConstitutionalAxiom.validate_authority(
        AuthorityLevel.PHYSICAL_REALITY, AuthorityLevel.SOFTWARE_ENGINE
    ) is True
    assert ConstitutionalAxiom.validate_authority(
        AuthorityLevel.AI_ASSISTANT, AuthorityLevel.PHYSICAL_REALITY
    ) is False
