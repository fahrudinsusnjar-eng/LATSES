import pytest
from lat_ces.scientific.stack_effect import StackEffectModel, StackEffectError


def test_stack_pressure():
    model = StackEffectModel()
    dp = model.compute_stack_pressure(indoor_temp=20.0, outdoor_temp=-5.0, height_m=10.0)
    assert dp > 0.0
