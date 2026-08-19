"""Canonical catalog models for user-selected building materials/products.

The catalog stores declared manufacturer/design data. It never invents a
product dimension, density, coverage, or consumption value.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class MaterialCategory(StrEnum):
    MASONRY_BLOCK = "masonry_block"
    PARTITION_BLOCK = "partition_block"
    DRYWALL = "drywall"
    ROOF_TILE = "roof_tile"
    ROOF_COVERING = "roof_covering"
    ROOF_TIMBER = "roof_timber"
    BATTEN = "batten"
    INSULATION = "insulation"
    FACADE_SYSTEM = "facade_system"
    WINDOW = "window"
    EXTERIOR_DOOR = "exterior_door"
    INTERIOR_DOOR = "interior_door"
    FLOOR_FINISH = "floor_finish"
    WALL_FINISH = "wall_finish"
    CEILING_FINISH = "ceiling_finish"
    BOARD = "board"
    METAL_SHEET = "metal_sheet"
    GUTTER = "gutter"
    DOWNPIPE = "downpipe"
    RAILING = "railing"
    FASTENER = "fastener"
    BINDING = "binding"
    CONCRETE = "concrete"
    REINFORCEMENT_STEEL = "reinforcement_steel"


@dataclass(frozen=True)
class ProductDimensions:
    length_m: float | None = None
    width_m: float | None = None
    height_m: float | None = None
    thickness_m: float | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("length_m", self.length_m),
            ("width_m", self.width_m),
            ("height_m", self.height_m),
            ("thickness_m", self.thickness_m),
        ):
            if value is not None and value <= 0:
                raise ValueError(f"{name} must be > 0 when supplied")

    @property
    def face_area_m2(self) -> float | None:
        if self.length_m is None or self.height_m is None:
            return None
        return self.length_m * self.height_m

    @property
    def plan_area_m2(self) -> float | None:
        if self.length_m is None or self.width_m is None:
            return None
        return self.length_m * self.width_m

    @property
    def volume_m3(self) -> float | None:
        if None in (self.length_m, self.width_m, self.height_m):
            return None
        return self.length_m * self.width_m * self.height_m  # type: ignore[operator]


@dataclass(frozen=True)
class GlazingSpec:
    pane_count: int
    gas_fill: str | None = None
    low_e: bool | None = None
    spacer: str | None = None

    def __post_init__(self) -> None:
        if self.pane_count not in (1, 2, 3, 4):
            raise ValueError("pane_count must be between 1 and 4")


@dataclass(frozen=True)
class ProductSpec:
    product_id: str
    name: str
    category: MaterialCategory
    manufacturer: str | None = None
    dimensions: ProductDimensions = field(default_factory=ProductDimensions)
    density_kg_m3: float | None = None
    surface_mass_kg_m2: float | None = None
    coverage_m2_per_unit: float | None = None
    consumption_per_m2: float | None = None
    unit: str = "piece"
    notes: str | None = None
    glazing: GlazingSpec | None = None

    def __post_init__(self) -> None:
        if not self.product_id.strip() or not self.name.strip():
            raise ValueError("product_id and name are required")
        if self.density_kg_m3 is not None and self.density_kg_m3 <= 0:
            raise ValueError("density_kg_m3 must be > 0")
        if self.surface_mass_kg_m2 is not None and self.surface_mass_kg_m2 <= 0:
            raise ValueError("surface_mass_kg_m2 must be > 0")
        if self.coverage_m2_per_unit is not None and self.coverage_m2_per_unit <= 0:
            raise ValueError("coverage_m2_per_unit must be > 0")
        if self.consumption_per_m2 is not None and self.consumption_per_m2 <= 0:
            raise ValueError("consumption_per_m2 must be > 0")
        if not self.unit.strip():
            raise ValueError("unit must not be empty")


@dataclass
class MaterialCatalog:
    products: dict[str, ProductSpec] = field(default_factory=dict)

    def add(self, product: ProductSpec) -> ProductSpec:
        if product.product_id in self.products:
            raise ValueError(f"Duplicate product id: {product.product_id}")
        self.products[product.product_id] = product
        return product

    def upsert(self, product: ProductSpec) -> ProductSpec:
        self.products[product.product_id] = product
        return product

    def get(self, product_id: str) -> ProductSpec:
        try:
            return self.products[product_id]
        except KeyError as exc:
            raise KeyError(f"Unknown product: {product_id}") from exc

    def by_category(self, category: MaterialCategory) -> tuple[ProductSpec, ...]:
        return tuple(p for p in self.products.values() if p.category == category)


__all__ = [
    "GlazingSpec",
    "MaterialCatalog",
    "MaterialCategory",
    "ProductDimensions",
    "ProductSpec",
]
