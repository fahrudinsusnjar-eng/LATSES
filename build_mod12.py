import os
import subprocess

files = {
    "lat_ces/modules/plenum.py": '''"""
LAT-CES Module 012: Air Plenum & Fluid Dynamics Engine
Dokument: LAT-SCI-MOD-0012
"""
from lat_ces.core.dimensions import Dimension, LENGTH, TIME, VELOCITY, MASS
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.equation import PhysicalEquation

# Definisanje specifičnih dimenzija za mehaniku fluida
AREA = Dimension(L=2)
FLOW_RATE = Dimension(L=3, T=-1)  # m³/s
DENSITY = Dimension(M=1, L=-3)    # kg/m³
MASS_FLOW = Dimension(M=1, T=-1)   # kg/s

class PlenumEngine:
    def __init__(self):
        self.flow_equation = PhysicalEquation(
            name="Volumetrijski protok (Q = A * v)",
            expected_dimension=FLOW_RATE,
            formula=lambda area, velocity: area * velocity
        )
        self.mass_flow_equation = PhysicalEquation(
            name="Maseni protok (m_dot = rho * Q)",
            expected_dimension=MASS_FLOW,
            formula=lambda density, flow_rate: density * flow_rate
        )

    def calculate_airflow(self, area: PhysicalQuantity, velocity: PhysicalQuantity) -> PhysicalQuantity:
        """Računa volumetrijski protok zraka u plenumu."""
        return self.flow_equation.compute(area=area, velocity=velocity)

    def calculate_mass_flow(self, density: PhysicalQuantity, flow_rate: PhysicalQuantity) -> PhysicalQuantity:
        """Računa maseni protok zraka."""
        return self.mass_flow_equation.compute(density=density, flow_rate=flow_rate)
''',
    "tests/test_plenum.py": '''import pytest
import math
from lat_ces.core.dimensions import Dimension
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import PlenumEngine, AREA, FLOW_RATE, DENSITY, MASS_FLOW

def test_plenum_flow_calculation():
    engine = PlenumEngine()

    # Površina poprečnog presjeka plenuma: A = 2.0 ± 0.05 m²
    area = PhysicalQuantity(2.0, AREA, 0.05)
    # Izmjerena brzina zraka: v = 3.0 ± 0.1 m/s
    velocity = PhysicalQuantity(3.0, Dimension(L=1, T=-1), 0.1)

    # Q = A * v = 6.0 m³/s
    q = engine.calculate_airflow(area, velocity)

    assert q.value == 6.0
    assert q.dimension == FLOW_RATE
    assert q.uncertainty > 0

def test_plenum_mass_flow_calculation():
    engine = PlenumEngine()

    # Gustoća zraka: rho = 1.2 ± 0.01 kg/m³
    density = PhysicalQuantity(1.2, DENSITY, 0.01)
    # Protok: Q = 5.0 ± 0.1 m³/s
    q = PhysicalQuantity(5.0, FLOW_RATE, 0.1)

    # m_dot = rho * Q = 6.0 kg/s
    m_dot = engine.calculate_mass_flow(density, q)

    assert m_dot.value == 6.0
    assert m_dot.dimension == MASS_FLOW
'''
}

print("🚀 Kreiram fajlove za Modul 012 (Air Plenum Engine)...")
for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  [OK] Kreiran: {filepath}")

print("\n🧪 Pokrećem pytest verifikaciju...")
test_res = subprocess.run(["pytest"], capture_output=True, text=True)

if test_res.returncode == 0:
    print("✅ Svi testovi su PROŠLI! Šaljem na GitHub...")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "feat(module-012): Implementiran Air Plenum & Fluid Dynamics Engine"])
    subprocess.run(["git", "tag", "-a", "v0.4.0-mod12", "-m", "LAT-CES Modul 012 dovrsen"])
    subprocess.run(["git", "push", "origin", "main"])
    subprocess.run(["git", "push", "origin", "v0.4.0-mod12"])
    print("\n🎉 Modul 012 je uspješno kreiran, verifikovan i zamrznut pod tagom v0.4.0-mod12!")
else:
    print("❌ Testovi nisu prošli! Pogledajte grešku:")
    print(test_res.stdout)
    print(test_res.stderr)
