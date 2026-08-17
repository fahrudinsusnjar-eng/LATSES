"""Solver-neutral roof input and deterministic dead-load accounting.

This layer only uses user/manufacturer-declared properties. It never chooses
standards, design values, material suitability, or safety factors.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RoofLayer:
    name: str
    thickness_m: float = 0.0
    density_kg_m3: float | None = None
    mass_kg_m2: float | None = None
    source_ref: str | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Naziv sloja je obavezan")
        if self.thickness_m < 0:
            raise ValueError("Debljina sloja ne može biti negativna")
        if self.density_kg_m3 is not None and self.density_kg_m3 < 0:
            raise ValueError("Gustoća ne može biti negativna")
        if self.mass_kg_m2 is not None and self.mass_kg_m2 < 0:
            raise ValueError("Površinska masa ne može biti negativna")
        if self.density_kg_m3 is None and self.mass_kg_m2 is None:
            raise ValueError(
                f"Sloj '{self.name}' nema potvrđenu gustoću niti površinsku masu"
            )

    @property
    def dead_load_kg_m2(self) -> float:
        if self.mass_kg_m2 is not None:
            return self.mass_kg_m2
        assert self.density_kg_m3 is not None
        return self.density_kg_m3 * self.thickness_m

    @property
    def dead_load_kn_m2(self) -> float:
        return self.dead_load_kg_m2 * 9.80665 / 1000.0


@dataclass
class RoofSpec:
    shape: str
    support: str
    structural_system: str
    covering: str
    length_m: float
    width_m: float
    rise_m: float = 0.0
    layers: list[RoofLayer] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.shape.strip():
            raise ValueError("Oblik krova je obavezan")
        if not self.support.strip():
            raise ValueError("Oslonac krova je obavezan")
        if not self.structural_system.strip():
            raise ValueError("Noseća konstrukcija krova je obavezna")
        if not self.covering.strip():
            raise ValueError("Pokrov krova je obavezan")
        if self.length_m <= 0 or self.width_m <= 0:
            raise ValueError("Gabarit krova mora biti > 0")
        if self.rise_m < 0:
            raise ValueError("Uzdignuće krova ne može biti negativno")

    @property
    def footprint_area_m2(self) -> float:
        return self.length_m * self.width_m


@dataclass(frozen=True)
class RoofLoadResult:
    area_m2: float
    load_kg_m2: float
    load_kn_m2: float
    total_mass_kg: float
    complete: bool
    unresolved_layers: tuple[str, ...]


class RoofLoadModel:
    """Deterministic roof self-weight model from declared layer properties."""

    def evaluate(self, roof: RoofSpec) -> RoofLoadResult:
        unresolved: list[str] = []
        total_kg_m2 = 0.0
        for layer in roof.layers:
            try:
                total_kg_m2 += layer.dead_load_kg_m2
            except ValueError:
                unresolved.append(layer.name)
        area = roof.footprint_area_m2
        return RoofLoadResult(
            area_m2=area,
            load_kg_m2=total_kg_m2,
            load_kn_m2=total_kg_m2 * 9.80665 / 1000.0,
            total_mass_kg=total_kg_m2 * area,
            complete=not unresolved,
            unresolved_layers=tuple(unresolved),
        )
