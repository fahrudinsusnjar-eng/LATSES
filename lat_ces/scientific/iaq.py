class IAQError(Exception):
    pass


class IAQModel:
    def __init__(self, room_volume_m3: float, base_outdoor_co2: float = 400.0, generation_rate_l_s_person: float = 0.005):
        if room_volume_m3 <= 0.0:
            raise IAQError("Room volume must be positive.")
        self.volume = room_volume_m3
        self.outdoor_co2 = base_outdoor_co2
        self.gen_rate = generation_rate_l_s_person

    def update_co2_concentration(self, current_co2: float, fresh_air_flow: float, occupants: int, dt_seconds: float) -> float:
        """
        Računa novu koncentraciju CO2 (u ppm) bazirano na bilansu mase gasa.
        """
        if current_co2 < 0.0 or fresh_air_flow < 0.0 or occupants < 0 or dt_seconds <= 0.0:
            raise IAQError("Invalid input parameters for IAQ calculation.")

        occupant_term = occupants * 4.2  # empirijski faktor porasta ppm/s po osobi pri slaboj ventilaciji

        delta_co2 = ((occupant_term + (fresh_air_flow * (self.outdoor_co2 - current_co2) / (self.volume / 100.0))) * dt_seconds)
        new_co2 = current_co2 + delta_co2

        return round(max(self.outdoor_co2, new_co2), 1)
