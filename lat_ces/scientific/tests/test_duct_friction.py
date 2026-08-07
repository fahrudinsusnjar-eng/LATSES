import pytest
from lat_ces.scientific.duct_friction import DuctFrictionModel, DuctError


def test_friction_loss():
    model = DuctFrictionModel(friction_factor=0.018)
    loss = model.compute_friction_loss(length_m=10.0, diameter_m=0.5, velocity_m_s=5.0, air_density=1.2)
    assert loss > 0.0
