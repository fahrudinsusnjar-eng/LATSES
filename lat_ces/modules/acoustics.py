"""
LAT-CES Module 013: Acoustic & Noise Engine
Dokument: LAT-SCI-MOD-0013
"""
import math
from typing import List

# Referentni zvučni pritisak na pragu čujnosti (20 uPa)
P_REF = 2e-5

class AcousticsEngine:
    @staticmethod
    def pressure_to_db(pressure_pa: float) -> float:
        """Pretvara zvučni pritisak u Paskalima (Pa) u nivo buke u decibelima (dB)."""
        if pressure_pa <= 0:
            raise ValueError("Zvučni pritisak mora biti pozitivan!")
        return 20.0 * math.log10(pressure_pa / P_REF)

    @staticmethod
    def combine_noise_levels(levels_db: List[float]) -> float:
        """Logaritamski sabira više izvora buke u decibelima."""
        if not levels_db:
            return 0.0
        sum_linear = sum(10.0 ** (db / 10.0) for db in levels_db)
        return 10.0 * math.log10(sum_linear)

    @staticmethod
    def is_noise_acceptable(total_db: float, max_limit_db: float = 45.0) -> bool:
        """Proverava da li je nivo buke unutar dozvoljenih granica."""
        return total_db <= max_limit_db