"""
LAT-CES Governance Core
Constitutional Axiom Engine Verification Tests (LAT-GOV-CORE-0011-TEST)
"""

from lat_ces.gov.axiom import ConstitutionalEngine


def test_axiom_validation_success():
    engine = ConstitutionalEngine()
    engine.add_axiom("AXIOM-01", lambda state: state["energy"] >= 0.0)

    valid_state = {"energy": 10.0}
    assert engine.verify_state(valid_state) == []


def test_axiom_validation_failure():
    engine = ConstitutionalEngine()
    engine.add_axiom("AXIOM-01", lambda state: state["energy"] >= 0.0)

    invalid_state = {"energy": -5.0}
    assert engine.verify_state(invalid_state) == ["AXIOM-01"]
