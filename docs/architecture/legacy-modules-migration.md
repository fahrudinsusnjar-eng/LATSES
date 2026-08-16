# Legacy `lat_ces.modules` migration map

## Scope

`lat_ces.modules` is a legacy compatibility/integration zone. It is not the canonical scientific layer. Existing callers and tests remain supported while migration proceeds incrementally.

The canonical direction is:

```text
application / GUI / CLI
        |
        v
scientific + core
        ^
        |
legacy modules (migration zone only)
```

New production code MUST NOT introduce imports from `lat_ces.modules`.

## Module map

| Legacy module | Current role | Canonical target / migration destination | Disposition |
|---|---|---|---|
| `quantity.py` | compatibility wrapper | `lat_ces.scientific.quantity.PhysicalQuantity`; dimensions/units from `lat_ces.core.dimensions` | **ADAPT → KEEP as temporary facade** |
| `equation.py` | legacy equation abstraction | `lat_ces.scientific.quantity.equation.Equation` and the scientific equation layer | **ADAPT** |
| `plenum.py` | legacy plenum engine | `lat_ces.scientific.analysis.plenum.PlenumAnalysisEngine` plus the applicable scientific plenum models | **MIGRATE; no 1:1 drop-in assumption** |
| `pressure.py` | legacy pressure/drop calculations | canonical pressure/duct-loss models under `lat_ces.scientific` | **MIGRATE after API mapping** |
| `duct.py` | legacy duct calculations | canonical duct/friction/loss models under `lat_ces.scientific` | **MIGRATE after API mapping** |
| `fittings.py` | legacy fitting-loss calculations | canonical fittings/duct-loss scientific layer | **MIGRATE after API mapping** |
| `acoustics.py` | legacy acoustics engine | `lat_ces.scientific` acoustics models | **MIGRATE after API mapping** |
| `thermal.py` | legacy thermal engine | `lat_ces.scientific` thermal models | **MIGRATE after API mapping** |
| `psychrometrics.py` | legacy psychrometric helpers | canonical psychrometric/humidity scientific layer | **MIGRATE after API mapping** |
| `fan_laws.py` | fan-law implementation | canonical fan/curve scientific layer, if an equivalent is confirmed | **AUDIT; do not remove yet** |
| `pipeline.py` | legacy module pipeline | `lat_ces.application` for application orchestration and `lat_ces.master_pipeline` for system integration | **MIGRATE / RETIRE after callers move** |
| `pipeline_v3.py` | legacy network pipeline | canonical duct/network scientific models plus system/application orchestration | **MIGRATE / RETIRE after callers move** |

## Quantity migration completed

`lat_ces.modules.quantity.PhysicalQuantity` is already a compatibility import of the canonical implementation. The canonical implementation imports `Dimension` and `Unit` from `lat_ces.core.dimensions` and retains the legacy `Dimension` constructor form only for compatibility.

Therefore the first migration candidate is already at the **facade stage**. This P0 change adds regression protection rather than duplicating another quantity implementation.

## Guard policy

The migration guard is intentionally asymmetric:

- imports **inside** `lat_ces.modules` are allowed while the legacy zone exists;
- tests and migration tooling may inspect or exercise `lat_ces.modules`;
- new production code outside `lat_ces.modules` may **not** import `lat_ces.modules`;
- removal of a legacy module happens only after its callers and tests have migrated to the canonical target and CI is green.

This prevents the legacy boundary from growing while avoiding a risky all-at-once deletion.
