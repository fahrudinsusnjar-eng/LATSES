import pytest

from lat_ces.scientific.pressure_drop import PressureDropModel, PressureError


def test_pressure_drop_calculation():
    model = PressureDropModel(loss_coefficient=1.5, air_density=1.2)
    # v = 4.0 m/s -> dP = 1.5 * 1.2 * (4.0^2) / 2 = 1.5 * 1.2 * 16 / 2 = 14.4 Pa
    dp = model.compute_pressure_drop(velocity=4.0)
    assert dp == pytest.approx(14.4, rel=1e-3)
