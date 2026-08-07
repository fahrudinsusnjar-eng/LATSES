import os
import subprocess

files = {
    "lat_ces/modules/pipeline.py": '''"""
LAT-CES System Integration & Simulation Engine v2
Spaja Module 010-015 u jedinstvenu sveobuhvatnu simulaciju plenum sistema.
"""
from typing import Dict, Any
from lat_ces.core.dimensions import Dimension
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import PlenumEngine
from lat_ces.modules.acoustics import AcousticsEngine
from lat_ces.modules.thermal import ThermalEngine
from lat_ces.modules.pressure import FanEngine

class FullPlenumSimulation:
    def __init__(self, max_allowed_noise_db: float = 45.0, fan_efficiency: float = 0.8):
        self.plenum_engine = PlenumEngine()
        self.acoustics_engine = AcousticsEngine()
        self.thermal_engine = ThermalEngine()
        self.fan_engine = FanEngine()
        self.max_allowed_noise_db = max_allowed_noise_db
        self.fan_efficiency = fan_efficiency

    def run_full_simulation(
        self,
        area: PhysicalQuantity,
        velocity: PhysicalQuantity,
        density: PhysicalQuantity,
        sound_pressure_pa: float,
        specific_heat: PhysicalQuantity,
        delta_temp: PhysicalQuantity,
        pressure_drop: PhysicalQuantity
    ) -> Dict[str, Any]:
        """Izvršava cjelovitu fizikalno-inženjersku simulaciju plenuma."""
        airflow = self.plenum_engine.calculate_airflow(area, velocity)
        mass_flow = self.plenum_engine.calculate_mass_flow(density, airflow)

        noise_db = self.acoustics_engine.pressure_to_db(sound_pressure_pa)
        is_noise_ok = self.acoustics_engine.is_noise_acceptable(noise_db, self.max_allowed_noise_db)

        heat_rate = self.thermal_engine.calculate_heat_rate(mass_flow, specific_heat, delta_temp)

        fan_power = self.fan_engine.calculate_fan_power(airflow, pressure_drop, self.fan_efficiency)

        status = "PASS" if is_noise_ok else "FAIL"

        return {
            "airflow": airflow,
            "mass_flow": mass_flow,
            "noise_db": noise_db,
            "noise_acceptable": is_noise_ok,
            "heat_rate": heat_rate,
            "fan_power": fan_power,
            "status": status
        }


class PlenumSystemSimulation(FullPlenumSimulation):
    def run_simulation(
        self,
        area: PhysicalQuantity,
        velocity: PhysicalQuantity,
        density: PhysicalQuantity,
        sound_pressure_pa: float
    ) -> Dict[str, Any]:
        """Backward-compatible wrapper for the older pipeline interface."""
        airflow = self.plenum_engine.calculate_airflow(area, velocity)
        mass_flow = self.plenum_engine.calculate_mass_flow(density, airflow)

        noise_db = self.acoustics_engine.pressure_to_db(sound_pressure_pa)
        is_noise_ok = self.acoustics_engine.is_noise_acceptable(noise_db, self.max_allowed_noise_db)

        return {
            "airflow": airflow,
            "mass_flow": mass_flow,
            "noise_db": noise_db,
            "noise_acceptable": is_noise_ok,
            "status": "PASS" if is_noise_ok else "FAIL",
        }
''',
    "tests/test_pipeline_v2.py": '''import math
from lat_ces.core.dimensions import Dimension
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import AREA, DENSITY, FLOW_RATE, MASS_FLOW
from lat_ces.modules.thermal import SPECIFIC_HEAT, TEMPERATURE, HEAT_RATE
from lat_ces.modules.pressure import PRESSURE, POWER
from lat_ces.modules.pipeline import FullPlenumSimulation


def test_full_plenum_simulation():
    sim = FullPlenumSimulation(max_allowed_noise_db=50.0, fan_efficiency=0.8)

    area = PhysicalQuantity(2.0, AREA, 0.05)
    velocity = PhysicalQuantity(3.0, Dimension(L=1, T=-1), 0.1)
    density = PhysicalQuantity(1.2, DENSITY, 0.01)
    sound_pressure_pa = 0.002
    cp = PhysicalQuantity(1005.0, SPECIFIC_HEAT, 5.0)
    delta_T = PhysicalQuantity(10.0, TEMPERATURE, 0.2)
    dp = PhysicalQuantity(200.0, PRESSURE, 10.0)

    report = sim.run_full_simulation(
        area=area,
        velocity=velocity,
        density=density,
        sound_pressure_pa=sound_pressure_pa,
        specific_heat=cp,
        delta_temp=delta_T,
        pressure_drop=dp
    )

    assert report["airflow"].value == 6.0
    assert report["airflow"].dimension == FLOW_RATE

    assert math.isclose(report["mass_flow"].value, 7.2)
    assert report["mass_flow"].dimension == MASS_FLOW

    assert report["noise_acceptable"] is True

    assert math.isclose(report["heat_rate"].value, 72360.0)
    assert report["heat_rate"].dimension == HEAT_RATE

    assert math.isclose(report["fan_power"].value, 1500.0)
    assert report["fan_power"].dimension == POWER

    assert report["status"] == "PASS"
'''
}

print("🚀 Kreiram fajlove za Integracijski Pipeline v2...")
for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  [OK] Kreiran: {filepath}")

print("\n🧪 Pokrećem pytest verifikaciju kompletnog sistema (Moduli 010-015 + Pipeline)...")
test_res = subprocess.run(["pytest"], capture_output=True, text=True)

if test_res.returncode == 0:
    print("✅ Svi testovi su PROŠLI! Šaljem na GitHub...")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "feat(pipeline-v2): Integrisani Moduli 010-015 u celoviti Plenum Simulator Engine"])
    subprocess.run(["git", "tag", "-a", "v0.9.0-pipeline-v2", "-m", "LAT-CES Integracijski Pipeline v2 dovrsen"])
    subprocess.run(["git", "push", "origin", "main"])
    subprocess.run(["git", "push", "origin", "v0.9.0-pipeline-v2"])
    print("\n🎉 Integracijski Pipeline v2 je uspješno kreiran, verifikovan i zamrznut pod tagom v0.9.0-pipeline-v2!")
else:
    print("❌ Testovi nisu prošli! Pogledajte grešku:")
    print(test_res.stdout)
    print(test_res.stderr)
