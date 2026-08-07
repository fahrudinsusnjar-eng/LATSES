"""
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