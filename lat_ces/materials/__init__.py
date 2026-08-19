"""Read-only engineering access to material information and catalogs."""

from .building_catalog import BuildingCatalogItem, BuildingMaterialCatalog, GlazingOption
from .catalog_reader import MaterialCatalog, MaterialRecord

__all__ = [
    "BuildingCatalogItem",
    "BuildingMaterialCatalog",
    "GlazingOption",
    "MaterialCatalog",
    "MaterialRecord",
]
