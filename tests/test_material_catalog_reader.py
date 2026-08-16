from pathlib import Path

from lat_ces.materials import MaterialCatalog, MaterialRecord


def test_material_catalog_is_read_only_and_preserves_manufacturer_data(tmp_path: Path) -> None:
    root = tmp_path / "catalog"
    materials = root / "materials"
    materials.mkdir(parents=True)
    (materials / "example.json").write_text(
        '{\n'
        '  "material_id": "manufacturer.example.insulation.001",\n'
        '  "name": "Example Insulation",\n'
        '  "manufacturer": "Example Manufacturer",\n'
        '  "product_url": "https://manufacturer.example/product",\n'
        '  "technical_data": {"lambda_W_mK": 0.035, "density_kg_m3": 30},\n'
        '  "source_documents": ["https://manufacturer.example/datasheet.pdf"],\n'
        '  "informational_only": true\n'
        '}\n',
        encoding="utf-8",
    )

    catalog = MaterialCatalog(root)
    records = catalog.records()
    assert len(records) == 1
    assert isinstance(records[0], MaterialRecord)
    assert records[0].technical_data["lambda_W_mK"] == 0.035
    assert records[0].informational_only is True
    assert catalog.by_id("manufacturer.example.insulation.001").manufacturer == "Example Manufacturer"


def test_reader_exposes_no_write_api() -> None:
    public_names = {name for name in dir(MaterialCatalog) if not name.startswith("_")}
    assert "write" not in public_names
    assert "save" not in public_names
    assert "update" not in public_names
    assert "approve" not in public_names
    assert "select_for_design" not in public_names
