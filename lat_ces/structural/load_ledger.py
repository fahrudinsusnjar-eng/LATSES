"""Deterministic construction-layer mass and load ledger."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ConstructionLayer:
    name: str
    material_ref: str
    density_kg_m3: float | None = None
    thickness_m: float | None = None
    surface_mass_kg_m2: float | None = None

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.material_ref.strip():
            raise ValueError("layer name and material_ref are required")
        if (self.density_kg_m3 is None) == (self.surface_mass_kg_m2 is None):
            raise ValueError("provide exactly one mass input")
        if self.density_kg_m3 is not None:
            if self.density_kg_m3 <= 0 or self.thickness_m is None or self.thickness_m <= 0:
                raise ValueError("density and thickness must be > 0")
        if self.surface_mass_kg_m2 is not None and self.surface_mass_kg_m2 <= 0:
            raise ValueError("surface mass must be > 0")

    @property
    def mass_kg_m2(self) -> float:
        if self.surface_mass_kg_m2 is not None:
            return self.surface_mass_kg_m2
        assert self.density_kg_m3 is not None and self.thickness_m is not None
        return self.density_kg_m3 * self.thickness_m

    @property
    def load_kn_m2(self) -> float:
        return self.mass_kg_m2 * 9.81 / 1000.0


@dataclass(frozen=True)
class ConstructionAssembly:
    name: str
    area_m2: float
    layers: tuple[ConstructionLayer, ...] = ()

    def __post_init__(self) -> None:
        if self.area_m2 <= 0:
            raise ValueError("assembly area_m2 must be > 0")

    @property
    def mass_kg_m2(self) -> float:
        return sum(layer.mass_kg_m2 for layer in self.layers)

    @property
    def load_kn_m2(self) -> float:
        return sum(layer.load_kn_m2 for layer in self.layers)

    @property
    def total_mass_kg(self) -> float:
        return self.mass_kg_m2 * self.area_m2

    @property
    def total_weight_kn(self) -> float:
        return self.load_kn_m2 * self.area_m2


@dataclass
class LoadLedger:
    assemblies: list[ConstructionAssembly] = field(default_factory=list)

    def add(self, assembly: ConstructionAssembly) -> ConstructionAssembly:
        self.assemblies.append(assembly)
        return assembly

    @property
    def total_mass_kg(self) -> float:
        return sum(item.total_mass_kg for item in self.assemblies)

    @property
    def total_weight_kn(self) -> float:
        return sum(item.total_weight_kn for item in self.assemblies)

    def summary(self) -> dict[str, float]:
        return {"assemblies": float(len(self.assemblies)), "total_mass_kg": self.total_mass_kg, "total_weight_kn": self.total_weight_kn}
