import pytest
from lat_ces.scientific.acoustics import AcousticsModel, AcousticsError


def test_sound_attenuation():
    model = AcousticsModel(duct_attenuation_rate=0.5, silencer_insertion_loss=10.0)
    final_noise = model.compute_outlet_noise(source_noise_db=75.0, duct_length=10.0)
    assert final_noise < 75.0
