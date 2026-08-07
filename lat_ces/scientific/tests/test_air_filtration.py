import pytest
from lat_ces.scientific.air_filtration import AirFiltrationModel, FiltrationError


def test_filtration_pressure_drop():
    model = AirFiltrationModel(initial_pressure_drop=50.0, dust_capacity_factor=0.5)
    current_dp = model.compute_current_pressure_drop(accumulated_dust_grams=100.0)
    assert current_dp > 50.0
    assert current_dp == 100.0
