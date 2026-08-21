# LAT-CES Project State / Working Checkpoint

**Purpose:** This file is the persistent hand-off point for the LAT-CES engineering work. It prevents restarting analysis from zero on the next session.

## Current working line

- **Repository:** `susnjarfahrudin-ai/LATSES`
- **Default integration branch:** `main`
- **Active engineering branch:** `agent/building-engineering-completion`
- **Active PR:** `#125 — feat: complete Building Engineering integration over canonical BuildingModel`
- **PR base:** `main`
- **Last active branch commit before checkpoint fixes:** `306d73620137342507ba60e63245074e1db097a5`
- **Checkpoint commits added:** `d44f796c74cc56c2f08231d151b32690d68bf78c`, `99ad8acfa45437c7509b0841d2ee7cfe667a2496`

## Architectural decision already made

`BuildingModel` is the single source of truth. The GUI must not become the owner of engineering formulas. Catalog data is informational and must not inject hidden engineering assumptions. Structural results are preliminary transparent load take-offs, not final code-compliance verification. Missing engineering inputs must remain explicit `INPUT_REQUIRED` / `CHECK` states.

## What was already completed before this checkpoint

PR #125 is the current continuation of the Building Engineering work built on the existing reference-house/catalog/workspace line. It contains the completed integration layer for:

- geometry-driven QTO including openings, envelope areas, roof surface/perimeter, gutters, railings and roof/timber counts;
- canonical envelope thermal take-off with refusal to invent missing lambda values;
- canonical electrical design-intent registry and reporting;
- unified Building Engineering Report aggregating MEP, QTO, structural, thermal and electrical domains from one BuildingModel;
- regression coverage for the cross-domain contract.

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

## Current CI interpretation

The previous PR #126 reproduced two already-solved historical issues because it was based on the stale reference-house test contract. Its current failing verification/installer result is **not a new architecture problem**.

The correct repair has now been applied to `agent/building-engineering-completion`:

1. restore canonical reference-house area semantics and portable resource loading;
2. replace stale `>350`/broad threshold showcase assertions with deterministic canonical values;
3. keep this work on PR #125, not in a new parallel hotfix branch.

## PR hygiene decision

PR #126 (`fix/reference-house-resource-loading`) is a duplicate/stale path and should be closed rather than continued. The active work belongs to PR #125.

## Next technical gate

Run CI on the updated `agent/building-engineering-completion` branch and verify:

1. Verification pipeline is green;
2. Windows Installer workflow is green;
3. installer/EXE artifact is produced;
4. resulting artifact is tested before declaring a release-ready build.

Only after those gates pass should PR #125 be considered for approval/merge.

## What NOT to do tomorrow

Do **not** restart the 338 m² analysis.

Do **not** create another `reference-house` hotfix branch for the same issue.

Do **not** change the model geometry merely to satisfy the obsolete `>350 m²` assertion.

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

### 2026-08-21

**Starting point:** PR #125 active; PR #126 was opened against the same `main` base and reintroduced the stale `338 > 350` test failure.

**Recovered truth:** PR #114 already contained the correct canonical area semantics and acceptance contract; it was closed without merge.

**Action taken:** carried the PR #114 implementation forward onto `agent/building-engineering-completion` and added this state file.

**Current next action:** run the updated branch through Verification + Windows Installer, then record the exact CI/installer result here before any merge/review decision.
