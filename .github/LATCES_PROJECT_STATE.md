# LAT-CES Project State / Working Checkpoint

**Purpose:** This file is the persistent hand-off point for the LAT-CES engineering work. It prevents restarting analysis from zero on the next session.

## Current working line

- **Repository:** `susnjarfahrudin-ai/LATSES`
- **Default integration branch:** `main`
- **Active engineering branch:** `agent/building-engineering-completion`
- **Active PR:** `#125 — feat: complete Building Engineering integration over canonical BuildingModel`
- **PR base:** `main`
- **Current latest branch commit:** `6bcac7229a42c49a946c084511ba38896515dcf`
- **Latest functional GUI repair commit:** `7c64b75ad4f53611169eda27e7d0fe124e4b6581`

## Architectural decision already made

`BuildingModel` is the single source of truth. The GUI must not become the owner of engineering formulas. Catalog data is informational and must not inject hidden engineering assumptions. Structural results are preliminary transparent load take-offs, not final code-compliance verification. Missing engineering inputs must remain explicit `INPUT_REQUIRED` / `CHECK` states.

## What was already completed before this checkpoint

PR #125 is the current continuation of the Building Engineering work built on the existing reference-house/catalog/workspace line. It contains the completed integration layer for:

- geometry-driven QTO including openings, envelope areas, roof surface/perimeter, gutters, railings and roof/timber counts;
- canonical envelope thermal take-off with refusal to invent missing lambda values;
- canonical electrical design-intent registry and reporting;
- unified Building Engineering Report aggregating MEP, QTO, structural, thermal and electrical domains from one BuildingModel;
- reference-house workflow that materializes the showcase/test house into the canonical BuildingModel and populates structural, MEP, heating and electrical test inputs;
- master GUI shell with Tlocrt / Presjek / 3D / Provjera / Izvještaj / Reference House commands.

## Important historical decision — DO NOT RE-OPEN

The `338 m²` reference-house area issue was already analysed on 2026-08-19.

Canonical semantics:

- **gross floor area:** `12 m × 10 m × 3 levels = 360 m²`
- **conditioned floor area:** explicitly modelled rooms = `338 m²`
- `floor_area_m2` remains the backward-compatible alias for conditioned floor area.

The old showcase assertion `summary.floor_area_m2 > 350` was stale and must not be restored. The accepted contract is deterministic exact-value checking for the canonical geometry/engineering outputs.

This decision and implementation were captured in PR #114, which was closed without merge. The implementation has now been carried forward directly onto the active PR #125 branch so this work is not lost.

## Resource-loading decision — DO NOT RE-OPEN

`importlib.resources.files("lat_ces")` caused the Python 3.10 namespace-package `MultiplexedPath` failure in CI/installer contexts. The accepted implementation loads `reference_house_model.json` adjacent to `lat_ces/reference_house.py` via `Path(__file__).with_name(...)`.

Do not create another reference-house resource-loader hotfix unless a new, reproducible failure proves this implementation insufficient.

## Master GUI regression found 2026-08-21 — FIXED, DO NOT LOSE

The Windows installer built from commit `5b3357b6bb495f85a580f33746ac46f809327088` started but crashed during `_install_master_layout` with:

`AttributeError: '_tkinter.tkapp' object has no attribute '_load_reference_house'`

Root cause: `lat_ces/gui_master.py` bound four callbacks in the master command panel (`_load_reference_house`, `_show_view`, `_run_master_validation`, `_show_engineering_report`) without defining them in the final class. CI previously missed this because it only imported/launched the application and did not exercise these callback bindings.

Repair committed:

- `7c64b75ad4f53611169eda27e7d0fe124e4b6581` — restored all four callbacks;
- `_load_reference_house()` now enters the canonical `build_reference_house_workflow()` into the active workspace and refreshes model/metrics/levels;
- `_show_view()` routes `plan/section/3d` to canonical view steps;
- `_run_master_validation()` calls the canonical `validate_model()`;
- `_show_engineering_report()` calls the canonical Building Engineering Report path;
- `6bcac7229a42c49a946c084511ba38896515dcf` adds `tests/test_gui_master_contract.py` to lock the callback contract so the exact regression cannot silently return.

The next Windows build must be tested by actually exercising the Reference House command, not merely importing or starting the executable.

## Current CI interpretation

Before the GUI callback repair, commit `5b3357b6...` had:

- Verification #685 — SUCCESS;
- Windows Installer #539 — SUCCESS;
- installer artifact existed, but the packaged GUI still contained the untested callback regression above.

Therefore those green checks are **not sufficient release evidence** for the master GUI. The corrected commits must produce a new CI/installer build and the executable must receive a real startup + master-command smoke test.

## PR hygiene decision

PR #126 (`fix/reference-house-resource-loading`) is a duplicate/stale path and is closed. The active work belongs to PR #125.

## Next technical gate — CURRENT

Run CI on the latest `agent/building-engineering-completion` commit and verify:

1. Verification pipeline is green;
2. Windows Installer workflow is green;
3. the packaged executable starts;
4. the Reference House command can be invoked without `AttributeError`;
5. Tlocrt / Presjek / 3D / Provjera / Izvještaj callbacks resolve and execute;
6. the installer artifact is then accepted as release candidate.

Only after those gates pass should PR #125 be considered for approval/merge.

## What NOT to do tomorrow

Do **not** restart the 338 m² analysis.

Do **not** create another `reference-house` hotfix branch for the same solved resource/area issues.

Do **not** assume a green import-only smoke test proves the master GUI is functional.

Do **not** merge PR #126 as a substitute for PR #125.

Do **not** move the active work away from `agent/building-engineering-completion` unless a new architectural reason is recorded here first.

## Checkpoint update protocol

After every meaningful work session, update this file with:

- date/time;
- active branch and PR;
- last known good/failed commit;
- what was completed;
- current blocker;
- exact next action;
- historical decisions that must not be repeated.

This file is the canonical session hand-off record for LAT-CES work.

## Session checkpoints

### 2026-08-21 — reference-house contract + master GUI recovery

**Recovered truth:** PR #114 already contained the correct `360 gross / 338 conditioned` area semantics, and PR #126 was a duplicate path. Those decisions are retained on #125.

**New regression found from user-installed artifact:** `gui_master.py` referenced missing master callbacks and crashed at startup.

**Action taken:** implemented missing callback methods on `agent/building-engineering-completion`, added regression coverage, and updated this checkpoint before proceeding.

**Current exact next action:** run the corrected commit through Verification + Windows Installer, then exercise the packaged GUI command path and record the result here.
