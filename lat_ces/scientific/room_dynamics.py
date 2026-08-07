class RoomDynamicsError(Exception):
    pass


class RoomDynamicsModel:
    def __init__(self, room_volume_m3: float, thermal_mass_kJ_K: float):
        if room_volume_m3 <= 0.0 or thermal_mass_kJ_K <= 0.0:
            raise RoomDynamicsError("Room volume and thermal mass must be positive.")
        self.volume = room_volume_m3
        self.thermal_mass = thermal_mass_kJ_K

    def compute_next_temperature(self, current_temp: float, heat_gain_w: float, time_step_s: float) -> float:
        r"""
        Računa novu temperaturu u prostoriji nakon proteklog vremenskog koraka (u sekundama).
        Formula: T_new = T_current + (Q * dt) / (C_th * 1000)
        """
        if time_step_s <= 0.0:
            raise RoomDynamicsError("Time step must be positive.")

        # Q (W) * dt (s) = Džuli. Toplotni kapacitet je u kJ/K, pa dijelimo sa 1000 radi konverzije u kJ.
        energy_added_kJ = (heat_gain_w * time_step_s) / 1000.0
        temp_change = energy_added_kJ / self.thermal_mass
        new_temp = current_temp + temp_change
        return round(new_temp, 2)
