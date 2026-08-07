import os
import subprocess

files = {
    "lat_ces/modules/duct.py": '''"""
LAT-CES Module 016: Duct Friction & Friction Loss Engine
Dokument: LAT-SCI-MOD-0016
"""
import math
from lat_ces.core.dimensions import Dimension, DENSITY, VELOCITY, LENGTH
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.pressure import PRESSURE

# Dinamička viskoznost zraka na sobnoj temperaturi (Pa·s -> kg/(m·s))
VISCOSITY_AIR = Dimension(M=1, L=-1, T=-1)

class DuctFrictionEngine:
    @staticmethod
    def calculate_reynolds_number(
        density: PhysicalQuantity,
        velocity: PhysicalQuantity,
        hydraulic_diameter: PhysicalQuantity,
        dynamic_viscosity: PhysicalQuantity
    ) -> float:
        """
        Računa bezdimenzionalni Reynoldsov broj (Re).
        """
        re = (density.value * velocity.value * hydraulic_diameter.value) / dynamic_viscosity.value
        return re

    @staticmethod
    def estimate_friction_factor(reynolds: float) -> float:
        """
        Određuje Darcy-Weisbachov faktor trenja (f).
        Laminarno (Re < 2300): f = 64 / Re
        Turbulentno (Re >= 2300): Aproksimacija za glatke kanale f = 0.3164 / Re^0.25 (Blasius)
        """
        if reynolds <= 0:
            raise ValueError("Reynoldsov broj mora biti pozitivan!")
        if reynolds < 2300.0:
            return 64.0 / reynolds
        else:
            return 0.3164 / (reynolds ** 0.25)

    def calculate_friction_loss(
        self,
        friction_factor: float,
        length: PhysicalQuantity,
        hydraulic_diameter: PhysicalQuantity,
        density: PhysicalQuantity,
        velocity: PhysicalQuantity
    ) -> PhysicalQuantity:
        """
        Računa pad pritiska uslijed trenja u kanalu:
        delta_P = f * (L / D_h) * (rho * v^2 / 2)
        """
        dp_value = friction_factor * (length.value / hydraulic_diameter.value) * (density.value * (velocity.value ** 2) / 2.0)

        u_rel = math.sqrt(
            (length.uncertainty / length.value)**2 +
            (hydraulic_diameter.uncertainty / hydraulic_diameter.value)**2 +
            (density.uncertainty / density.value)**2 +
            (2.0 * velocity.uncertainty / velocity.value)**2
        )

        return PhysicalQuantity(
            value=dp_value,
            dimension=PRESSURE,
            uncertainty=dp_value * u_rel
        )
''',
    "tests/test_duct.py": '''import math
from lat_ces.core.dimensions import DENSITY, VELOCITY, LENGTH
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.pressure import PRESSURE
from lat_ces.modules.duct import DuctFrictionEngine, VISCOSITY_AIR


def test_reynolds_and_friction_factor():
    engine = DuctFrictionEngine()

    rho = PhysicalQuantity(1.2, DENSITY, 0.01)
    v = PhysicalQuantity(3.0, VELOCITY, 0.1)
    d_h = PhysicalQuantity(0.5, LENGTH, 0.01)
    mu = PhysicalQuantity(1.81e-5, VISCOSITY_AIR, 1e-7)

    re = engine.calculate_reynolds_number(rho, v, d_h, mu)
    assert re > 2300.0

    f = engine.estimate_friction_factor(re)
    assert 0.01 < f < 0.05


def test_friction_loss_calculation():
    engine = DuctFrictionEngine()

    f = 0.02
    length = PhysicalQuantity(10.0, LENGTH, 0.1)
    d_h = PhysicalQuantity(0.5, LENGTH, 0.01)
    rho = PhysicalQuantity(1.2, DENSITY, 0.01)
    v = PhysicalQuantity(4.0, VELOCITY, 0.1)

    dp = engine.calculate_friction_loss(f, length, d_h, rho, v)

    assert math.isclose(dp.value, 3.84, abs_tol=1e-2)
    assert dp.dimension == PRESSURE
    assert dp.uncertainty > 0
'''
}

print("🚀 Kreiram fajlove za Modul 016 (Duct Friction & Friction Loss Engine)...")
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
    subprocess.run(["git", "commit", "-m", "feat(module-016): Implementiran Duct Friction & Friction Loss Engine"])
    subprocess.run(["git", "tag", "-a", "v0.10.0-mod16", "-m", "LAT-CES Modul 016 dovrsen"])
    subprocess.run(["git", "push", "origin", "main"])
    subprocess.run(["git", "push", "origin", "v0.10.0-mod16"])
    print("\n🎉 Modul 016 je uspješno kreiran, verifikovan i zamrznut pod tagom v0.10.0-mod16!")
else:
    print("❌ Testovi nisu prošli! Pogledajte grešku:")
    print(test_res.stdout)
    print(test_res.stderr)
