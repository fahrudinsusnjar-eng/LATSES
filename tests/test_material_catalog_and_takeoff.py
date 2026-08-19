from __future__ import annotations

import math

import pytest

from lat_ces.building.material_catalog import (
    GlazingSpec,
    MaterialCatalog,
    MaterialCategory,
    ProductDimensions,
    ProductSpec,
)
from lat_ces.building.quantity_takeoff import (
    block_count_for_wall,
    concrete_volume,
    insulation_volume,
    linear_quantity,
    timber_volume,
)


def test_catalog_supports_masonry_and_glazing() -> None:
    catalog = MaterialCatalog()
    block = catalog.add(
        ProductSpec(
            product_id="BLOCK-25",
            name="Masonry block 25",
            category=MaterialCategory.MASONRY_BLOCK,
            dimensions=ProductDimensions(length_m=0.25, width_m=0.25, height_m=0.238),
            unit="piece",
        )
    )
    window = catalog.add(
        ProductSpec(
            product_id="WINDOW-TRIPLE",
            name="Triple glazed window",
            category=MaterialCategory.WINDOW,
            glazing=GlazingSpec(pane_count=3, gas_fill="argon", low_e=True),
        )
    )
    assert catalog.get(block.product_id) is block
    assert window.glazing is not None
    assert window.glazing.pane_count == 3
    assert window.glazing.gas_fill == "argon"


def test_block_takeoff_excludes_openings_and_adds_waste() -> None:
    product = ProductSpec(
        product_id="BLOCK",
        name="Block",
        category=MaterialCategory.MASONRY_BLOCK,
        dimensions=ProductDimensions(length_m=0.50, width_m=0.25, height_m=0.20),
    )
    result = block_count_for_wall(product, 10.0, 2.5, opening_area_m2=5.0, waste_fraction=0.05)
    expected = math.ceil(20.0 / 0.10 * 1.05)
    assert result.quantity == expected
    assert "openings 5.0000 m²" in (result.notes or "")


def test_generic_quantities_for_insulation_timber_concrete_and_linear_elements() -> None:
    product = ProductSpec(
        product_id="GENERIC",
        name="Generic",
        category=MaterialCategory.BOARD,
    )
    assert insulation_volume(product, 100.0, 0.15).quantity == pytest.approx(15.0)
    assert linear_quantity(product, 20.0, waste_fraction=0.05).quantity == pytest.approx(21.0)
    assert timber_volume(0.08, 0.16, 4.0, 20) == pytest.approx(1.024)
    assert concrete_volume(100.0, 0.20) == pytest.approx(20.0)
