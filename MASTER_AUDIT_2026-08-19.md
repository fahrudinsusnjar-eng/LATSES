# LAT-CES Master Audit — 2026-08-19

## Scope

This audit is based on the current `main` tree and the currently merged PR history. It is intentionally **read-only in its conclusions**: legacy code is not deleted merely because it looks old. Deletion requires an import/runtime dependency proof.

## 1. Current architecture

### Canonical building layer

`lat_ces/building/` and `lat_ces/building_model/` contain the BuildingModel foundation and MEP domain objects. `BuildingModel` owns levels, rooms, materials, roof and orientation.

### Scientific layer

`lat_ces/core/`, `lat_ces/scientific/` and `lat_ces/modules/` contain the existing dimensional, quantity, equation and HVAC/engineering engines. The repository guidance explicitly requires new work to prefer canonical abstractions over parallel implementations.

### GUI layer

`lat_ces/gui_complete.py` is the current `lat-ces-gui` entry point. It already exposes Model/Pogledi, Omotač/Fasada, Konstrukcija/Statika, Proračuni, MEP and Fasade tabs. Additional legacy/specialized GUI entry points remain in `pyproject.toml` for compatibility.

### Material information layer

`data/material_catalog/` defines a manufacturer-information contract, but currently contains only schema/index/template files and **no product records**. The existing `lat_ces/materials/catalog_reader.py` expects a different legacy record shape (`material_id`, `name`, `manufacturer`, etc.) than the current manufacturer schema (`record_id`, nested manufacturer/product/source/technical_data). This is a real architectural mismatch that should be resolved separately from the new generic Building Material Catalog.

## 2. Important current-state finding

The current `main` is **not** the same state as the earlier preliminary structural branch. PR #96 and the subsequent restore/revert sequence exist in history, while `main` currently points to `925bab6b...`. The master branch therefore must not assume that the reverted preliminary structural solver is available.

The consequence is important: future structural work must be rebuilt from the current canonical `main` deliberately, with tests and CI at each boundary, rather than relying on files that were present only on the reverted feature branch.

## 3. GUI design direction

Use one visual system across the desktop application:

- background: light neutral (`#F5F7FA`)
- primary text: slate (`#0F172A`)
- secondary text: (`#475569`)
- primary action: engineering blue (`#2563EB`)
- success: (`#16A34A`)
- warning: (`#D97706`)
- error: (`#DC2626`)
- selection/focus: (`#0EA5A4`)

Buttons should follow three levels: **Primary** (calculate/apply/save), **Secondary** (open/edit/view), and **Danger** (delete/reset). Calculation results should use status badges instead of relying on colour alone.

## 4. Building Material Catalog direction

Do not mix two different concepts:

1. **Building Material / Element Catalog** — parameterized generic templates used to construct the BuildingModel and quantity take-off.
2. **Manufacturer Material Catalog** — factual, source-linked manufacturer records used only as informational inputs.

The first can safely ship with categories and editable dimensions/units. The second must only contain verified manufacturer-declared facts with source provenance.

## 5. Required next engineering layers

1. Building Material / Element Catalog and GUI selector.
2. Quantity take-off from actual BuildingModel geometry.
3. Structural model reconstruction on the current `main` with load-path, RC design and detailing as separate layers.
4. Thermal/envelope solver using the selected material layer stack.
5. Window/glazing model with frame material, pane count, gas fill, Low-E and spacer.
6. Roof timber/covering geometry and metal/gutter/downpipe quantities.
7. Electrical and plumbing domain objects in the same BuildingModel ownership pattern.
8. One final Building Engineering Report that combines quantities and engineering results while preserving provenance.

## 6. Deletion policy

Safe immediate cleanup candidates are generated Python cache artifacts and temporary marker files. Legacy GUI/engine files are **not** automatically deleted until import/reference evidence proves they are unused.

## 7. Release gate

No feature is considered release-ready until:

- full Verification is GREEN;
- Windows Installer is GREEN;
- the built installer contains the current canonical GUI entry point;
- the affected model state round-trips through persistence;
- no patch/diff fragments or generated artifacts are present in tracked source.
