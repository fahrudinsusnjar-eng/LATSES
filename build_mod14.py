import os
import subprocess

files = {
    "lat_ces/modules/thermal.py": '''"""
LAT-CES Module 014: Thermal & Thermodynamic Engine
Dokument: LAT-SCI-MOD-0014
"""
from lat_ces.core.dimensions import Dimension, MASS, TIME
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.equation import PhysicalEquation

# Definisanje specifičnih termodinamičkih dimenzija
TEMPERATURE = Dimension(Theta=1)                                # Kelvin (K)
SPECIFIC_HEAT = Dimension(L=2, T=-2, Theta=-1)                  # J / (kg * K) -> m² / (s² * K)
HEAT_RATE = Dimension(M=1, L=2, T=-3)                           # Watt (W) -> kg * m² / s³

class ThermalEngine:
    def __init__(self):
        self.heat_rate_equation = PhysicalEquation(
            name="Toplotna snaga (Q_dot = m_dot * cp * delta_T)",
            expected_dimension=HEAT_RATE,
            formula=lambda m_dot, cp, delta_T: m_dot * cp * delta_T
        )

    def calculate_heat_rate(
        self,
        mass_flow: PhysicalQuantity,
        specific_heat: PhysicalQuantity,
        delta_temp: PhysicalQuantity
    ) -> PhysicalQuantity:
        """Računa toplotnu snagu izmjene toplote u zraku (W)."""
        return self.heat_rate_equation.compute(
            m_dot=mass_flow,
            cp=specific_heat,
            delta_T=delta_temp
        )
''',
    "tests/test_thermal.py": '''import pytest
from lat_ces.core.dimensions import Dimension, MASS
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import MASS_FLOW
from lat_ces.modules.thermal import ThermalEngine, TEMPERATURE, SPECIFIC_HEAT, HEAT_RATE


def test_heat_rate_calculation():
    engine = ThermalEngine()

    mass_flow = PhysicalQuantity(2.0, MASS_FLOW, 0.05)
    cp = PhysicalQuantity(1005.0, SPECIFIC_HEAT, 5.0)
    delta_T = PhysicalQuantity(10.0, TEMPERATURE, 0.2)

    q_dot = engine.calculate_heat_rate(mass_flow, cp, delta_T)

    assert q_dot.value == 20100.0
    assert q_dot.dimension == HEAT_RATE
    assert q_dot.uncertainty > 0


def test_invalid_dimension_thermal():
    engine = ThermalEngine()

    mass_flow = PhysicalQuantity(2.0, MASS_FLOW, 0.05)
    cp = PhysicalQuantity(1005.0, SPECIFIC_HEAT, 5.0)
    wrong_dim = PhysicalQuantity(10.0, MASS, 0.2)

    with pytest.raises(ValueError):
        _ = engine.calculate_heat_rate(mass_flow, cp, wrong_dim)
'''
}

print("🚀 Kreiram fajlove za Modul 014 (Thermal & Thermodynamic Engine)...")
for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  [OK] Kreiran: {filepath}")

print("\n🧪 Pokrećem pytest verifikaciju svih modula...")
test_res = subprocess.run(["pytest"], capture_output=True, text=True)

if test_res.returncode == 0:
    print("✅ Svi testovi su PROŠLI! Šaljem na GitHub...")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "feat(module-014): Implementiran Thermal & Thermodynamic Engine"])
    subprocess.run(["git", "tag", "-a", "v0.7.0-mod14", "-m", "LAT-CES Modul 014 dovrsen"])
    subprocess.run(["git", "push", "origin", "main"])
    subprocess.run(["git", "push", "origin", "v0.7.0-mod14"])
    print("\n🎉 Modul 014 je uspješno kreiran, verifikovan i zamrznut pod tagom v0.7.0-mod14!")
else:
    print("❌ Testovi nisu prošli! Pogledajte grešku:")
    print(test_res.stdout)
    print(test_res.stderr)
