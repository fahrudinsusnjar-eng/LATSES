# Dimension/Unit canonical import cleanup

## Scope

The canonical `Dimension` and `Unit` implementations live in `lat_ces.core.dimensions`.
Scientific-layer modules may remain as compatibility facades, but production quantity
implementations should import the canonical classes directly.

## Changes

- `lat_ces/scientific/quantities/quantity.py` now imports `Unit` and `UnitSKOError` from `lat_ces.core.dimensions`.
- `lat_ces/scientific/quantity/quantity.py` now imports `Dimension`, `Unit`, and `UnitSKOError` from `lat_ces.core.dimensions`.
- Existing compatibility facades under `scientific/dimensions` and `scientific/units` are retained.
- Canonical identity regression coverage now verifies that both quantity implementations use the same canonical `Unit` class.

## Deliberately not changed

- No scientific behavior or conversion formulas were changed.
- No compatibility facade was removed.
- No report/CLI/GUI behavior was changed.
- No broad repository-wide import rewrite was performed without evidence from consumers.

## Verification target

The PR must pass the existing CI suite before any further cleanup is attempted.
