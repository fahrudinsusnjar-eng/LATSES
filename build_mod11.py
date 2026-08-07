import os
import subprocess

files = {
    "lat_ces/modules/equation.py": '''"""
LAT-CES Module 011: Physical Equation & Formula Engine
Dokument: LAT-SCI-MOD-0011
"""
from typing import Callable
from lat_ces.core.dimensions import Dimension
from lat_ces.modules.quantity import PhysicalQuantity

class PhysicalEquation:
    """
    Predstavlja fizikalnu jednačinu koja prihvata ulazne fizikalne veličine,
    izvršava proračun i verifikuje da dobijena dimenzija odgovara očekivanoj.
    """
    def __init__(self, name: str, expected_dimension: Dimension, formula: Callable[..., PhysicalQuantity]):
        self.name = name
        self.expected_dimension = expected_dimension
        self.formula = formula

    def compute(self, **kwargs: PhysicalQuantity) -> PhysicalQuantity:
        result = self.formula(**kwargs)

        if result.dimension != self.expected_dimension:
            raise ValueError(
                f"Greška u jednačini '{self.name}': Očekivana dimenzija {self.expected_dimension}, "
                f"ali je dobijena {result.dimension}!"
            )
        return result
''',
    "tests/test_equation.py": '''import pytest
from lat_ces.core.dimensions import LENGTH, TIME, VELOCITY, MASS, FORCE
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.modules.equation import PhysicalEquation

def test_equation_valid_calculation():
    speed_eq = PhysicalEquation(
        name="Brzina",
        expected_dimension=VELOCITY,
        formula=lambda s, t: s / t
    )

    s = PhysicalQuantity(100.0, LENGTH, 1.0)
    t = PhysicalQuantity(10.0, TIME, 0.2)

    v = speed_eq.compute(s=s, t=t)
    assert v.value == 10.0
    assert v.dimension == VELOCITY

def test_equation_dimension_mismatch():
    faulty_eq = PhysicalEquation(
        name="Pogrešna Sila",
        expected_dimension=FORCE,
        formula=lambda s, t: s / t
    )

    s = PhysicalQuantity(100.0, LENGTH, 1.0)
    t = PhysicalQuantity(10.0, TIME, 0.2)

    with pytest.raises(ValueError):
        _ = faulty_eq.compute(s=s, t=t)
'''
}

print("🚀 Kreiram fajlove za Modul 011...")
for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  [OK] Kreiran: {filepath}")

print("\n🧪 Pokrećem pytest verifikaciju...")
test_res = subprocess.run(["pytest"], capture_output=True, text=True)

if test_res.returncode == 0:
    print("✅ Svi testovi su PROŠLI!")
else:
    print("❌ Testovi nisu prošli! Pogledajte grešku:")
    print(test_res.stdout)
    print(test_res.stderr)
