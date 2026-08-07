import os
import subprocess

files = {
    "lat_ces/modules/acoustics.py": '''"""
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
''',
    "tests/test_acoustics.py": '''import math
from lat_ces.modules.acoustics import AcousticsEngine, P_REF


def test_pressure_to_db():
    assert math.isclose(AcousticsEngine.pressure_to_db(P_REF), 0.0, abs_tol=1e-5)

    db_1pa = AcousticsEngine.pressure_to_db(1.0)
    assert math.isclose(db_1pa, 93.979, abs_tol=1e-3)


def test_combine_noise_levels():
    combined = AcousticsEngine.combine_noise_levels([50.0, 50.0])
    assert math.isclose(combined, 53.01, abs_tol=0.01)


def test_noise_acceptability():
    assert AcousticsEngine.is_noise_acceptable(40.0, max_limit_db=45.0) is True
    assert AcousticsEngine.is_noise_acceptable(50.0, max_limit_db=45.0) is False
'''
}

print("🚀 Kreiram fajlove za Modul 013 (Acoustic & Noise Engine)...")
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
    subprocess.run(["git", "commit", "-m", "feat(module-013): Implementiran Acoustic & Noise Engine"])
    subprocess.run(["git", "tag", "-a", "v0.5.0-mod13", "-m", "LAT-CES Modul 013 dovrsen"])
    subprocess.run(["git", "push", "origin", "main"])
    subprocess.run(["git", "push", "origin", "v0.5.0-mod13"])
    print("\n🎉 Modul 013 je uspješno kreiran, verifikovan i zamrznut pod tagom v0.5.0-mod13!")
else:
    print("❌ Testovi nisu prošli! Pogledajte grešku:")
    print(test_res.stdout)
    print(test_res.stderr)
