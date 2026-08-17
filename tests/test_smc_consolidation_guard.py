"""Final SMC consolidation guards for canonical import ownership."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEGACY_IMPORTS = (
    "lat_ces.modules.quantity",
    "lat_ces.modules.equation",
    "lat_ces.scientific.units.unit",
    "lat_ces.scientific.units.quantity",
)

EXCLUDED_DIRS = {".git", ".pytest_cache", "build", "dist", "__pycache__"}


def _source_files():
    for path in ROOT.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path


def test_no_retired_quantity_or_equation_imports_remain():
    offenders = []
    for path in _source_files():
        text = path.read_text(encoding="utf-8")
        for legacy in LEGACY_IMPORTS[:2]:
            if legacy in text and path.as_posix() != "tests/test_smc_consolidation_guard.py":
                offenders.append(f"{path}: {legacy}")
    assert not offenders, "Retired legacy imports remain:\n" + "\n".join(offenders)


def test_scientific_units_are_compatibility_facades_only():
    units_unit = ROOT / "lat_ces" / "scientific" / "units" / "unit.py"
    units_quantity = ROOT / "lat_ces" / "scientific" / "units" / "quantity.py"
    for path in (units_unit, units_quantity):
        if path.exists():
            text = path.read_text(encoding="utf-8")
            assert "Compatibility facade" in text or "compatibility facade" in text


def test_canonical_scientific_quantity_exists():
    canonical = ROOT / "lat_ces" / "scientific" / "quantity" / "quantity.py"
    assert canonical.exists()


def test_smc_contract_and_registry_exist():
    assert (ROOT / "lat_ces" / "scientific" / "smc" / "contracts.py").exists()
    assert (ROOT / "lat_ces" / "scientific" / "smc" / "registry.py").exists()
