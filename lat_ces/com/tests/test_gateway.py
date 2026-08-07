"""
LAT-CES Communication Core
Secure Gateway Verification Tests (LAT-COM-CORE-0012-TEST)
"""

import pytest

from lat_ces.com.gateway import SecureGateway
from lat_ces.gov.axiom import ConstitutionalEngine


def test_secure_gateway_enforcement():
    # Setup mock Governance engine
    gov = ConstitutionalEngine()
    gov.add_axiom("API_LIMIT", lambda state: state.get("value", 0) < 100)

    gateway = SecureGateway(governance=gov)

    # Safe request
    assert gateway.process_request({"value": 50}) is True

    # Unsafe request (violates axiom)
    with pytest.raises(Exception):
        gateway.process_request({"value": 150})
