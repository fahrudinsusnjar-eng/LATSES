"""Deterministic quantity takeoff helpers for the canonical BuildingModel.

All product dimensions and coverage/consumption values come from ProductSpec;
geometry comes from the building model or explicitly supplied measured areas.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil

from lat_ces.building.material_catalog import ProductSpec


@dataclass(frozen=True)
class QuantityResult:
    product_id: str
    description: str
    quantity: float
    unit: str
    basis: str
    notes: str | None = None


def area_coverage(product: ProductSpec, area_m2: float, *, waste_fraction: float = 0.0) -> QuantityResult:
    """Calculate units from declared coverage per unit or product face area."""
    if area_m2 < 0:
        raise ValueError("area_m2 must be >= 0")
    if not 0 <= waste_fraction < 1:
        raise ValueError("waste_fraction must be in [0, 1)")
    coverage = product.coverage_m2_per_unit or product.dimensions.face_area_m2
    if coverage is None or coverage <= 0:
        raise ValueError(f"Product {product.product_id} has no usable coverage/face area")
    quantity = area_m2 / coverage * (1.0 + waste_fraction)
    return QuantityResult(
        product_id=product.product_id,
        description=product.name,
        quantity=quantity,
        unit=product.unit,
        basis=f"area {area_m2:.4f} m² / coverage {coverage:.6f} m² per {product.unit}",
    )


def block_count_for_wall(
    product: ProductSpec,
    wall_length_m: float,
    wall_height_m: float,
    *,
    opening_area_m2: float = 0.0,
    waste_fraction: float = 0.05,
) -> QuantityResult:
    """Calculate masonry-unit count from external wall geometry and openings."""
    if wall_length_m <= 0 or wall_height_m <= 0:
        raise ValueError("wall dimensions must be > 0")
    gross = wall_length_m * wall_height_m
    net = gross - opening_area_m2
    if net < 0:
        raise ValueError("opening area cannot exceed gross wall area")
    result = area_coverage(product, net, waste_fraction=waste_fraction)
    return QuantityResult(
        product_id=result.product_id,
        description=result.description,
        quantity=float(ceil(result.quantity)),
        unit=result.unit,
        basis=f"net wall area {net:.4f} m²",
        notes=f"gross {gross:.4f} m²; openings {opening_area_m2:.4f} m²; waste {waste_fraction:.1%}",
    )


def roof_covering_count(product: ProductSpec, roof_area_m2: float, *, waste_fraction: float = 0.08) -> QuantityResult:
    """Calculate roofing-unit quantity from declared coverage per unit."""
    return area_coverage(product, roof_area_m2, waste_fraction=waste_fraction)


def insulation_volume(product: ProductSpec, area_m2: float, thickness_m: float) -> QuantityResult:
    """Calculate insulation volume in m³ from selected layer thickness."""
    if area_m2 < 0 or thickness_m <= 0:
        raise ValueError("area_m2 must be >= 0 and thickness_m must be > 0")
    volume = area_m2 * thickness_m
    return QuantityResult(
        product_id=product.product_id,
        description=product.name,
        quantity=volume,
        unit="m³",
        basis=f"area {area_m2:.4f} m² × thickness {thickness_m:.4f} m",
    )


def linear_quantity(product: ProductSpec, length_m: float, *, waste_fraction: float = 0.05) -> QuantityResult:
    """Calculate linear metres for gutters, rails, battens, profiles, etc."""
    if length_m < 0:
        raise ValueError("length_m must be >= 0")
    return QuantityResult(
        product_id=product.product_id,
        description=product.name,
        quantity=length_m * (1.0 + waste_fraction),
        unit="m",
        basis=f"measured length {length_m:.4f} m",
        notes=f"waste {waste_fraction:.1%}",
    )


def sheet_area(area_m2: float, *, waste_fraction: float = 0.08) -> float:
    """Return required sheet area with waste."""
    if area_m2 < 0 or not 0 <= waste_fraction < 1:
        raise ValueError("invalid area or waste_fraction")
    return area_m2 * (1.0 + waste_fraction)


def timber_volume(length_m: float, width_m: float, height_m: float, quantity: int) -> float:
    """Return nominal timber volume from selected cross-section and count."""
    if min(length_m, width_m, height_m) <= 0 or quantity <= 0:
        raise ValueError("timber dimensions and quantity must be > 0")
    return length_m * width_m * height_m * quantity


def concrete_volume(area_m2: float, thickness_m: float) -> float:
    """Return concrete volume for slabs/walls of uniform thickness."""
    if area_m2 <= 0 or thickness_m <= 0:
        raise ValueError("area_m2 and thickness_m must be > 0")
    return area_m2 * thickness_m


__all__ = [
    "QuantityResult",
    "area_coverage",
    "block_count_for_wall",
    "concrete_volume",
    "insulation_volume",
    "linear_quantity",
    "roof_covering_count",
    "sheet_area",
    "timber_volume",
]
