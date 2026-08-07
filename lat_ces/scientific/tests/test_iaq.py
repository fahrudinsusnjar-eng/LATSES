import pytest
from lat_ces.scientific.iaq import IAQModel, IAQError


def test_co2_evolution():
    model = IAQModel(room_volume_m3=100.0)
    # Trenutna koncentracija, dotok svjezeg zraka, generisanje od ljudi
    next_co2 = model.update_co2_concentration(current_co2=600.0, fresh_air_flow=0.05, occupants=3, dt_seconds=60.0)
    assert next_co2 > 600.0
