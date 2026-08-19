from lat_ces.materials.building_catalog import BuildingMaterialCatalog


def test_parameterized_building_catalog_loads_from_package_data():
    catalog = BuildingMaterialCatalog.default()
    assert catalog.catalog_id == "LAT-CES-BUILDING-MATERIALS"
    assert len(catalog.items) >= 20
    assert catalog.by_id("masonry_block").requires_dimensions is True


def test_glazing_catalog_contains_requested_pane_options():
    catalog = BuildingMaterialCatalog.default()
    pane_counts = {option.panes for option in catalog.glazing_options}
    assert {1, 2, 3, 4}.issubset(pane_counts)


def test_catalog_search_is_deterministic():
    catalog = BuildingMaterialCatalog.default()
    results = catalog.search("izolacija")
    assert [item.item_id for item in results] == sorted(item.item_id for item in results)
    assert results
