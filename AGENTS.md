# LATSES Agent Instructions

## Project Shape

- LATSES is a Python 3.9+ scientific engineering codebase for dimensional quantities and HVAC/air-distribution calculations.
- `lat_ces/core/` owns shared dimensional algebra, constitutional axioms, and Scientific Knowledge Object (SKO) behavior.
- `lat_ces/modules/` contains domain engines such as quantities, equations, plenums, pressure, acoustics, thermal calculations, ducts, fittings, and pipelines.
- `lat_ces/scientific/` provides the scientific dimensions, quantities, and units-facing API; check whether a change belongs in this layer or the legacy/core layer before editing.
- `lat_ses/` is the small agent package and is separate from the calculation library.
- `tests/` mirrors the major core and module surfaces. Root `build_*.py` files are repository build/generation scripts, not the primary package API.

## Verification

- Run the full suite with `python -m pytest` from the repository root. Pytest is configured by [pytest.ini](pytest.ini) with strict markers and `tests/` as the test path.
- For a focused change, run the closest test first, for example `python -m pytest tests/test_dimensions.py` or `python -m pytest tests/test_unit_hardening.py`.
- The project declares Python `>=3.9` and no runtime dependencies in [pyproject.toml](pyproject.toml). Use the repository virtual environment when available.
- After changing a build script, run that script and then the affected focused tests; inspect the generated diff before touching unrelated files.

## Scientific Invariants

- Preserve dimensional correctness: addition and subtraction require equal dimensions; multiplication, division, and powers must transform dimensions consistently.
- Treat uncertainty as non-negative and propagate it according to the surrounding `PhysicalQuantity` implementation and tests.
- Unit arithmetic must reject affine-offset units (for example, temperature units with offsets) until they are converted appropriately.
- Derived units start in `DRAFT` with their own identity. A `RELEASED` unit is immutable; preserve these status and mutation protections.
- Prefer the existing `Dimension`, `PhysicalQuantity`, `Unit`, equation, and domain-engine abstractions over parallel implementations. Keep public names and backward-compatible pipeline wrappers unless the task explicitly changes the API.

## Change Conventions

- Keep edits narrow and match the existing module/test organization. Add or update a focused test for behavioral changes, especially arithmetic, unit conversion, status transitions, and dimension validation.
- Preserve the existing documentation language and terminology in touched modules; comments should explain only non-obvious scientific or lifecycle rules.
- Do not commit, tag, push, or rewrite unrelated work unless explicitly requested.
- When packaging or installation behavior is involved, verify the explicit package list in [pyproject.toml](pyproject.toml); source-tree imports can succeed even when a subpackage is omitted from the built distribution.