import importlib


def test_quantity_import_resolution_is_canonical():
    canonical_module = importlib.import_module("lat_ces.scientific.quantity")
    canonical_package = importlib.import_module("lat_ces.scientific.quantity.quantity")
    measurement = importlib.import_module("lat_ces.scientific.measurement")
    cli = importlib.import_module("lat_ces.scientific.cli")

    assert canonical_module.PhysicalQuantity is canonical_package.PhysicalQuantity
    assert measurement.PhysicalQuantity is canonical_package.PhysicalQuantity
    assert cli.PhysicalQuantity is canonical_package.PhysicalQuantity

    assert canonical_module.__file__.replace("\\", "/").endswith("/lat_ces/scientific/quantity/__init__.py")
