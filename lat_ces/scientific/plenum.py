"""
LAT-SCI-CORE-0023: Plenum Aerodynamic & Acoustic Noise Model Reference Implementation
"""
import math


class PlenumError(Exception):
    """Base exception for Plenum aerodynamic and acoustic calculations."""


class PlenumModel:
    """
    Models air velocity, pressure dynamics, and acoustic noise generation
    within ventilation plenum chambers.
    """

    def __init__(self, cross_section_area: float):
        if cross_section_area <= 0.0:
            raise PlenumError("Cross-section area must be strictly positive.")
        self.area = cross_section_area

    def compute_velocity(self, volumetric_flow: float) -> float:
        """Computes mean air velocity (v = Q / A) in m/s."""
        if volumetric_flow < 0.0:
            raise PlenumError("Volumetric flow cannot be negative.")
        return volumetric_flow / self.area

    def estimate_acoustic_noise(self, velocity: float) -> float:
        """
        Estimates aerodynamic noise level (dB) based on empirical velocity scaling
        (e.g., L_p ~ 50 * log10(v) + baseline factor).
        """
        if velocity < 0.0:
            raise PlenumError("Velocity cannot be negative.")
        if velocity == 0.0:
            return 0.0

        # Empirijska aproksimacija buke u plenumu
        baseline_db = 30.0
        noise_db = baseline_db + 50.0 * math.log10(velocity)
        return round(noise_db, 2)