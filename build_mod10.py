import os
import subprocess

files = {
    "lat_ces/modules/quantity.py": '''"""
LAT-CES Module 010: Physical Quantity & Uncertainty Engine
Dokument: LAT-SCI-MOD-0010
"""
import math
from dataclasses import dataclass
from lat_ces.core.dimensions import Dimension

@dataclass(frozen=True)
class PhysicalQuantity:
    value: float
    dimension: Dimension
    uncertainty: float = 0.0

    def __post_init__(self):
        if self.uncertainty < 0:
            raise ValueError("Mjerna nesigurnost ne može biti negativna!")

    def __add__(self, other: 'PhysicalQuantity') -> 'PhysicalQuantity':
        if self.dimension != other.dimension:
            raise ValueError(
                f"Inkompatibilne dimenzije za sabiranje: {self.dimension} vs {other.dimension}"
            )
        new_value = self.value + other.value
        new_uncertainty = math.sqrt(self.uncertainty**2 + other.uncertainty**2)
        return PhysicalQuantity(new_value, self.dimension, new_uncertainty)

    def __sub__(self, other: 'PhysicalQuantity') -> 'PhysicalQuantity':
        if self.dimension != other.dimension:
            raise ValueError(
                f"Inkompatibilne dimenzije za oduzimanje: {self.dimension} vs {other.dimension}"
            )
        new_value = self.value - other.value
        new_uncertainty = math.sqrt(self.uncertainty**2 + other.uncertainty**2)
        return PhysicalQuantity(new_value, self.dimension, new_uncertainty)

    def __mul__(self, other: 'PhysicalQuantity') -> 'PhysicalQuantity':
        new_value = self.value * other.value
        new_dimension = self.dimension * other.dimension

        rel1 = (self.uncertainty / abs(self.value)) if self.value != 0 else 0
        rel2 = (other.uncertainty / abs(other.value)) if other.value != 0 else 0
        new_uncertainty = abs(new_value) * math.sqrt(rel1**2 + rel2**2)

        return PhysicalQuantity(new_value, new_dimension, new_uncertainty)

    def __truediv__(self, other: 'PhysicalQuantity') -> 'PhysicalQuantity':
        if other.value == 0:
            raise ZeroDivisionError("Dijeljenje sa 0 nije dozvoljeno.")

        new_value = self.value / other.value
        new_dimension = self.dimension / other.dimension

        rel1 = (self.uncertainty / abs(self.value)) if self.value != 0 else 0
        rel2 = (other.uncertainty / abs(other.value)) if other.value != 0 else 0
        new_uncertainty = abs(new_value) * math.sqrt(rel1**2 + rel2**2)

        return PhysicalQuantity(new_value, new_dimension, new_uncertainty)

    def __repr__(self) -> str:
        return f"{self.value} ± {self.uncertainty} (Dim: {self.dimension})"
''',
    "tests/test_quantity.py": '''import pytest
import math
from lat_ces.core.dimensions import LENGTH, TIME, VELOCITY
from lat_ces.modules.quantity import PhysicalQuantity

def test_quantity_creation():
    d = PhysicalQuantity(value=10.0, dimension=LENGTH, uncertainty=0.1)
    assert d.value == 10.0
    assert d.dimension == LENGTH
    assert d.uncertainty == 0.1

def test_quantity_addition_success():
    d1 = PhysicalQuantity(10.0, LENGTH, 0.3)
    d2 = PhysicalQuantity(5.0, LENGTH, 0.4)
    res = d1 + d2
    assert res.value == 15.0
    assert res.dimension == LENGTH
    assert math.isclose(res.uncertainty, 0.5)

def test_quantity_addition_dimension_mismatch():
    d = PhysicalQuantity(10.0, LENGTH, 0.1)
    t = PhysicalQuantity(2.0, TIME, 0.05)
    with pytest.raises(ValueError):
        _ = d + t

def test_quantity_division_velocity():
    d = PhysicalQuantity(100.0, LENGTH, 2.0)
    t = PhysicalQuantity(10.0, TIME, 0.1)
    v = d / t
    assert v.value == 10.0
    assert v.dimension == VELOCITY
    expected_u = 10.0 * math.sqrt((2.0/100.0)**2 + (0.1/10.0)**2)
    assert math.isclose(v.uncertainty, expected_u)
'''
}

print("🚀 Kreiram fajlove za Modul 010...")
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
