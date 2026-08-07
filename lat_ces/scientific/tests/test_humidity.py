"""
LAT-CES Scientific Core
Humidity & Condensation Risk Verification Tests (LAT-SCI-CORE-0027-TEST)
"""

import pytest

from lat_ces.scientific.humidity import HumidityError, HumidityModel


def test_condensation_risk_evaluation():
    model = HumidityModel()
    risk = model.evaluate_condensation_risk(relative_humidity=92.5, surface_temp=15.0, dew_point=16.2)
    assert risk == "HIGH_RISK"
