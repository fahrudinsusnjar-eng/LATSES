"""Read-only engineering access to manufacturer-declared material data."""

from .catalog_reader import MaterialCatalog, MaterialRecord

__all__ = ["MaterialCatalog", "MaterialRecord"]
