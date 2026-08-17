"""Solver-neutral construction inputs for slabs, walls and floor assemblies."""
from __future__ import annotations

from dataclasses import dataclass

from .load_ledger import ConstructionAssembly, ConstructionLayer, LoadLedger


@dataclass(frozen=True)
class SlabInput:
    name: str
    area_m2: float
    layers: tuple[ConstructionLayer, ...]

    def assembly(self) -> ConstructionAssembly:
        return ConstructionAssembly(self.name, self.area_m2, self.layers)


@dataclass(frozen=True)
class WallInput:
    name: str
    area_m2: float
    layers: tuple[ConstructionLayer, ...]

    def assembly(self) -> ConstructionAssembly:
        return ConstructionAssembly(self.name, self.area_m2, self.layers)


@dataclass(frozen=True)
class FloorInput:
    name: str
    area_m2: float
    layers: tuple[ConstructionLayer, ...]

    def assembly(self) -> ConstructionAssembly:
        return ConstructionAssembly(self.name, self.area_m2, self.layers)


def build_permanent_load_ledger(
    slabs: tuple[SlabInput, ...] = (),
    walls: tuple[WallInput, ...] = (),
    floors: tuple[FloorInput, ...] = (),
) -> LoadLedger:
    """Build a permanent-load ledger without choosing design values."""
    ledger = LoadLedger()
    for item in (*slabs, *walls, *floors):
        ledger.add(item.assembly())
    return ledger
