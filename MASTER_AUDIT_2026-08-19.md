# LAT-CES Master Audit — 2026-08-19

## Reference state
The current `main` reference is `925bab6b4e458c83e8fa0d629564162fdee7a3bb`. Recent preliminary-structural and HeatingZone restore/revert PRs exist in history; this master branch therefore does not assume those reverted feature files are present on `main`.

## Architecture observations
- `lat_ces/building/` and `lat_ces/building_model/` are the BuildingModel domain layers.
- `lat_ces/core/`, `lat_ces/scientific/` and `lat_ces/modules/` are the canonical scientific calculation layers.
- `lat_ces/gui_complete.py` is the current `lat-ces-gui` entry point; specialized GUI entry points remain in `pyproject.toml` for compatibility.
- `data/material_catalog/` is a manufacturer-information contract and currently has no product records.
- `lat_ces/materials/catalog_reader.py` expects a different record shape from the current manufacturer schema; this is a concrete adapter/migration issue.

## GUI direction
Use one visual system: light neutral background, slate text, engineering blue for primary actions, green success, amber warning, red error and teal focus/selection. Buttons use Primary (calculate/apply/save), Secondary (open/edit/view) and Danger (delete/reset). Status must never rely on color alone.

## Material architecture
Keep two separate concepts:

1. **Parameterized Building Material / Element Catalog** — generic construction families, editable dimensions, units and quantity-takeoff basis.
2. **Manufacturer Material Catalog** — source-linked manufacturer-declared facts only.

The parameterized catalog must not pretend to contain verified commercial product dimensions or normative design values.

## Target engineering sequence
1. Catalog GUI + BuildingModel selector.
2. Geometry-driven quantity take-off.
3. Structural model reconstruction on current `main` with load-path, RC design and detailing separated.
4. Envelope/thermal calculations using selected layer stacks.
5. Windows/glazing: wood/PVC/aluminium, 1/2/3/4 panes, gas fill, Low-E, spacer.
6. Roof timber, covering, sheet metal, gutters/downpipes and railings.
7. Electrical and plumbing objects under BuildingModel ownership.
8. Unified Building Engineering Report with quantities and engineering results plus provenance.

## Cleanup rule
Generated caches and temporary markers are safe cleanup candidates. Legacy GUIs/engines are not deleted solely because they look old; import/runtime evidence is required.

## Release gate
Verification GREEN + Windows Installer GREEN + persistence round-trip + package discovery + no tracked generated artifacts or patch/diff fragments.
