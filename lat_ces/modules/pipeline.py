"""
LAT-CES System Integration & Simulation Engine
Spaja Module 010 (Quantity), 011 (Equation), 012 (Plenum) i 013 (Acoustics)
u jedinstvenu simulaciju plenum sistema.
"""
from typing import Dict, Any
from lat_ces.core.dimensions import Dimension
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import PlenumEngine
from lat_ces.modules.acoustics import AcousticsEngine

class PlenumSystemSimulation:
    def __init__(self, max_allowed_noise_db: float = 45.0):
        self.plenum_engine = PlenumEngine()
        self.acoustics_engine = AcousticsEngine()
        self.max_allowed_noise_db = max_allowed_noise_db

    def run_simulation(
        self,
        area: PhysicalQuantity,
        velocity: PhysicalQuantity,
        density: PhysicalQuantity,
        sound_pressure_pa: float
    ) -> Dict[str, Any]:
        """Izvršava cjelovitu simulaciju plenuma i vraća inženjerski izvještaj."""
        airflow = self.plenum_engine.calculate_airflow(area, velocity)
        mass_flow = self.plenum_engine.calculate_mass_flow(density, airflow)

        noise_db = self.acoustics_engine.pressure_to_db(sound_pressure_pa)
        is_acceptable = self.acoustics_engine.is_noise_acceptable(noise_db, self.max_allowed_noise_db)

        return {
            "airflow": airflow,
            "mass_flow": mass_flow,
            "noise_db": noise_db,
            "noise_acceptable": is_acceptable,
            "status": "PASS" if is_acceptable else "FAIL"
        }