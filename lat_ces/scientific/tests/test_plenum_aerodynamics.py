"""
LAT-CES Scientific Core
Plenum Aerodynamics & Acoustics Verification Tests (LAT-SCI-CORE-0023-TEST)
"""

import pytest

from lat_ces.scientific.plenum import PlenumError, PlenumModel


def test_plenum_air_velocity_calculation():
    # Test izracunavanja brzine protoka na osnovu protoka (Q) i poprecnog presjeka (A)
    # Q = 0.5 m^3/s, A = 0.25 m^2 -> v = 2.0 m/s
    model = PlenumModel(cross_section_area=0.25)
    velocity = model.compute_velocity(volumetric_flow=0.5)

    assert velocity == pytest.approx(2.0, rel=1e-3)


def test_plenum_noise_estimation():
    model = PlenumModel(cross_section_area=0.25)
    # Procjena akusticne buke na osnovu brzine i koeficijenta turbulencije
    noise_db = model.estimate_acoustic_noise(velocity=4.0)

    assert noise_db > 0.0
    assert isinstance(noise_db, float)
