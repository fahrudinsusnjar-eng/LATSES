import pytest
from lat_ces.scientific.room_dynamics import RoomDynamicsModel, RoomDynamicsError


def test_room_temperature_evolution():
    model = RoomDynamicsModel(room_volume_m3=100.0, thermal_mass_kJ_K=5000.0)
    next_temp = model.compute_next_temperature(current_temp=20.0, heat_gain_w=1000.0, time_step_s=60.0)
    assert next_temp > 20.0
