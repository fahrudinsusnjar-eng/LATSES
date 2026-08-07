import os
import subprocess

files = {
    "lat_ces/modules/pressure.py": '''"""
LAT-CES Module 015: Pressure Drop & Fan Power Engine
Dokument: LAT-SCI-MOD-0015
"""
from lat_ces.core.dimensions import Dimension
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.equation import PhysicalEquation

# Definisanje specifičnih dimenzija za pritisak i snagu
PRESSURE = Dimension(M=1, L=-1, T=-2)   # Pascal (Pa) -> kg / (m * s²)
POWER = Dimension(M=1, L=2, T=-3)      # Watt (W) -> kg * m² / s³

class FanEngine:
    def __init__(self):
        self.fan_power_equation = PhysicalEquation(
            name="Snaga ventilatora (P = Q * delta_P)",
            expected_dimension=POWER,
            formula=lambda Q, delta_P: Q * delta_P
        )

    def calculate_fan_power(
        self,
        flow_rate: PhysicalQuantity,
        pressure_drop: PhysicalQuantity,
        efficiency: float = 1.0
    ) -> PhysicalQuantity:
        """
        Računa potrebnu snagu ventilatora (W) na osnovu protoka,
        pada pritiska i efikasnosti ventilatora (eta).
        """
        if efficiency <= 0 or efficiency > 1.0:
            raise ValueError("Stepen iskorištenja (efficiency) mora biti u opsegu (0, 1.0]!")

        raw_power = self.fan_power_equation.compute(Q=flow_rate, delta_P=pressure_drop)

        return PhysicalQuantity(
            value=raw_power.value / efficiency,
            dimension=POWER,
            uncertainty=raw_power.uncertainty / efficiency
        )
''',
    "tests/test_pressure.py": '''import pytest
from lat_ces.core.dimensions import Dimension
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.plenum import FLOW_RATE
from lat_ces.modules.pressure import FanEngine, PRESSURE, POWER


def test_fan_power_calculation():
    engine = FanEngine()

    q = PhysicalQuantity(2.0, FLOW_RATE, 0.05)
    dp = PhysicalQuantity(250.0, PRESSURE, 10.0)

    p_ideal = engine.calculate_fan_power(q, dp, efficiency=1.0)
    assert p_ideal.value == 500.0
    assert p_ideal.dimension == POWER
    assert p_ideal.uncertainty > 0

    p_real = engine.calculate_fan_power(q, dp, efficiency=0.8)
    assert p_real.value == 625.0
    assert p_real.dimension == POWER


def test_invalid_efficiency():
    engine = FanEngine()
    q = PhysicalQuantity(2.0, FLOW_RATE, 0.05)
    dp = PhysicalQuantity(250.0, PRESSURE, 10.0)

    with pytest.raises(ValueError):
        _ = engine.calculate_fan_power(q, dp, efficiency=0.0)

    with pytest.raises(ValueError):
        _ = engine.calculate_fan_power(q, dp, efficiency=1.2)
'''
}

print("🚀 Kreiram fajlove za Modul 015 (Pressure Drop & Fan Power Engine)...")
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
    subprocess.run(["git", "commit", "-m", "feat(module-015): Implementiran Pressure Drop & Fan Power Engine"])
    subprocess.run(["git", "tag", "-a", "v0.8.0-mod15", "-m", "LAT-CES Modul 015 dovrsen"])
    subprocess.run(["git", "push", "origin", "main"])
    subprocess.run(["git", "push", "origin", "v0.8.0-mod15"])
    print("\n🎉 Modul 015 je uspješno kreiran, verifikovan i zamrznut pod tagom v0.8.0-mod15!")
else:
    print("❌ Testovi nisu prošli! Pogledajte grešku:")
    print(test_res.stdout)
    print(test_res.stderr)
