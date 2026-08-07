import os
import subprocess

files = {
    "lat_ces/modules/pipeline.py": '''"""
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
''',
    "tests/test_pipeline.py": '''import math
from lat_ces.core.dimensions import Dimension
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import AREA, DENSITY, FLOW_RATE, MASS_FLOW
from lat_ces.modules.pipeline import PlenumSystemSimulation


def test_plenum_system_simulation_pass():
    sim = PlenumSystemSimulation(max_allowed_noise_db=50.0)

    area = PhysicalQuantity(1.5, AREA, 0.02)
    velocity = PhysicalQuantity(2.5, Dimension(L=1, T=-1), 0.1)
    density = PhysicalQuantity(1.2, DENSITY, 0.01)

    sound_pressure_pa = 0.002

    report = sim.run_simulation(area, velocity, density, sound_pressure_pa)

    assert report["airflow"].value == 3.75
    assert report["airflow"].dimension == FLOW_RATE
    assert math.isclose(report["mass_flow"].value, 4.5)
    assert report["mass_flow"].dimension == MASS_FLOW
    assert report["noise_acceptable"] is True
    assert report["status"] == "PASS"


def test_plenum_system_simulation_fail_noise():
    sim = PlenumSystemSimulation(max_allowed_noise_db=35.0)

    area = PhysicalQuantity(1.0, AREA, 0.01)
    velocity = PhysicalQuantity(2.0, Dimension(L=1, T=-1), 0.05)
    density = PhysicalQuantity(1.2, DENSITY, 0.01)

    sound_pressure_pa = 1.0

    report = sim.run_simulation(area, velocity, density, sound_pressure_pa)

    assert report["noise_acceptable"] is False
    assert report["status"] == "FAIL"
'''
}

print("🚀 Kreiram fajlove za Integracijski Pipeline...")
for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  [OK] Kreiran: {filepath}")

print("\n🧪 Pokrećem pytest verifikaciju svih modula i pipeline-a...")
test_res = subprocess.run(["pytest"], capture_output=True, text=True)

if test_res.returncode == 0:
    print("✅ Svi testovi su PROŠLI! Šaljem na GitHub...")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "feat(pipeline): Implementiran System Integration Engine za simulaciju plenuma"])
    subprocess.run(["git", "tag", "-a", "v0.6.0-pipeline", "-m", "LAT-CES Integracijski Pipeline dovrsen"])
    subprocess.run(["git", "push", "origin", "main"])
    subprocess.run(["git", "push", "origin", "v0.6.0-pipeline"])
    print("\n🎉 Integracijski Pipeline je uspješno verifikovan i zamrznut pod tagom v0.6.0-pipeline!")
else:
    print("❌ Testovi nisu prošli! Pogledajte grešku:")
    print(test_res.stdout)
    print(test_res.stderr)
