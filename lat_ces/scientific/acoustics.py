class AcousticsError(Exception):
    pass


class AcousticsModel:
    def __init__(self, duct_attenuation_rate: float, silencer_insertion_loss: float):
        if duct_attenuation_rate < 0.0 or silencer_insertion_loss < 0.0:
            raise AcousticsError("Attenuation parameters must be non-negative.")
        self.attenuation_rate = duct_attenuation_rate # dB po metru
        self.silencer_loss = silencer_insertion_loss # dB

    def compute_outlet_noise(self, source_noise_db: float, duct_length: float) -> float:
        """
        Računa nivo buke na izlazu iz kanala nakon prirodnog prigušenja i prigušivača zvuka.
        """
        if source_noise_db < 0.0 or duct_length < 0.0:
            raise AcousticsError("Source noise and duct length cannot be negative.")

        total_attenuation = (self.attenuation_rate * duct_length) + self.silencer_loss
        outlet_noise = max(0.0, source_noise_db - total_attenuation)
        return round(outlet_noise, 1)
