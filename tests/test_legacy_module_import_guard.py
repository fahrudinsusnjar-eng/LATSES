import ast
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_ROOT = REPO_ROOT / "lat_ces"
LEGACY_ROOT = PRODUCTION_ROOT / "modules"


def _module_name_from_import(node: ast.AST) -> str:
    if isinstance(node, ast.Import):
        return node.names[0].name
    if isinstance(node, ast.ImportFrom):
        if node.level:
            return ""
        return node.module or ""
    return ""


def test_production_code_does_not_introduce_legacy_module_imports():
    violations = []

    for path in PRODUCTION_ROOT.rglob("*.py"):
        if LEGACY_ROOT in path.parents:
            continue
        if "tests" in path.parts:
            continue

        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            module_name = _module_name_from_import(node)
            if module_name == "lat_ces.modules" or module_name.startswith("lat_ces.modules."):
                violations.append(f"{path.relative_to(REPO_ROOT)}:{node.lineno}: {module_name}")

    assert not violations, "Production code must not introduce legacy imports:\n" + "\n".join(violations)


def test_legacy_quantity_is_the_canonical_physical_quantity_facade():
    from lat_ces.modules.quantity import PhysicalQuantity as LegacyPhysicalQuantity
    from lat_ces.scientific.quantity import PhysicalQuantity as CanonicalPhysicalQuantity

    assert LegacyPhysicalQuantity is CanonicalPhysicalQuantity
