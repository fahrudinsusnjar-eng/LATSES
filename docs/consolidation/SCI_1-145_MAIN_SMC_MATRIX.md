# SCI 1–145 → MAIN → SMC Consolidation Matrix

**Status:** 55/55 legacy audit complete — execution baseline
**Branch:** `agent/sci-1-145-smc-consolidation`
**Governance:** SMC-001 → SMC-004

## Rule

This is the executable baseline for SCI/legacy 0001–0055. Decisions are based on real implementation paths, imports, tests and provenance. No deletion is implied by `MERGE`, `ADAPT` or `MOVE`.

**KEEP** = canonical owner remains.  
**MERGE** = responsibility converges on an existing canonical owner.  
**ADAPT** = implementation/API is retained but brought under SMC.  
**MOVE** = verification/governance responsibility moves to SMC.  
**RETIRE** = only after zero production imports + regression evidence + SMC-004 acceptance.  
**NEW** = capability genuinely absent; no NEW is authorized merely because an SCI number exists.

## 55/55 matrix

| # | Responsibility | Canonical owner | Real main path / evidence | Decision |
|---:|---|---|---|---|
| 0001 | Axioms | `lat_ces/scientific/core` | `lat_ces/core/axioms.py` + tests | KEEP + ADAPT |
| 0002 | SKO foundation | `lat_ces/scientific/core` | `lat_ces/core/sko.py` + tests | KEEP + ADAPT |
| 0003 | SKO identity | `lat_ces/scientific/core` | `lat_ces/core/sko.py` | MERGE |
| 0004 | SKO governance | `lat_ces/scientific/core` | `lat_ces/core/sko.py` | MERGE |
| 0005 | SKO verification | `lat_ces/scientific/core/verification` | core/SKO tests | MERGE |
| 0006 | Dimensions | `lat_ces/scientific/units/dimensions` | `lat_ces/core/dimensions.py` | MERGE + ADAPT |
| 0007 | Dimension algebra | `lat_ces/scientific/units/dimensions` | `lat_ces/core/dimensions.py` | MERGE |
| 0008 | SKO/unit bridge | `lat_ces/scientific/core` + units | core/SKO/dimensions | MERGE |
| 0009 | Core validation | `lat_ces/scientific/core/validation` | core validation/tests | MERGE |
| 0010 | Quantity legacy API | `lat_ces/scientific/quantity` | `modules/quantity.py` → `scientific/quantity/quantity.py` | MERGE |
| 0011 | Equation engine | `lat_ces/scientific/equations` | `modules/equation.py` + scientific equations | MERGE |
| 0012 | Plenum | `lat_ces/scientific/models/plenum` | legacy + scientific plenum paths | MERGE + ADAPT |
| 0013 | Acoustics | `lat_ces/scientific/models/acoustics` | legacy + scientific acoustics | MERGE + ADAPT |
| 0014 | Thermal | `lat_ces/scientific/models/thermal` | legacy + scientific thermal | MERGE + ADAPT |
| 0015 | Pressure/fan | `lat_ces/scientific/models/pressure` | legacy + pressure-drop/fan paths | MERGE + ADAPT |
| 0016 | Duct/friction | `lat_ces/scientific/models/duct` | legacy + friction/loss paths | MERGE + ADAPT |
| 0017 | Unit verification spec | `lat_ces/scientific/units/verification` | unit tests/evidence | MERGE |
| 0018 | Unit implementation | `lat_ces/scientific/units` | units implementation | ADAPT |
| 0019 | Unit verification execution | `lat_ces/scientific/units/verification` | unit tests/evidence | MERGE |
| 0020 | Registry governance | `lat_ces/scientific/units/registry` | registry/tests | MERGE |
| 0021 | Registry implementation | `lat_ces/scientific/units/registry.py` | actual registry.py | KEEP |
| 0022 | Registry verification | `lat_ces/scientific/units/verification` | registry tests | MERGE |
| 0023 | Registry verification execution | `lat_ces/scientific/units/verification` | registry evidence | KEEP |
| 0024 | Registry hardening spec | `lat_ces/scientific/units/integrity` | canonical identity/integrity tests | ADAPT |
| 0025 | Registry hardening | `lat_ces/scientific/units/registry.py` | actual registry.py | ADAPT |
| 0026 | Hardening verification | `lat_ces/scientific/units/verification` | hardening tests | MERGE |
| 0027 | Hardening evidence | `lat_ces/scientific/units/verification` | evidence/tests | KEEP |
| 0028 | Formal verification | `lat_ces/smc/verification` | formal verification artifacts | MOVE |
| 0029 | Derived units | `lat_ces/scientific/equations` + units | equation/dimension paths | MERGE |
| 0030 | Derived-unit implementation | `lat_ces/scientific/equations` | scientific equations | ADAPT |
| 0031 | Derived-unit verification | `lat_ces/scientific/equations/verification` | equation tests | MERGE |
| 0032 | Verification evidence | `lat_ces/scientific/equations/verification` | tests/evidence | KEEP |
| 0033 | Derived-unit hardening | `lat_ces/scientific/quantity/integrity` | integrity/tests | ADAPT |
| 0034 | Derived-unit hardening implementation | `lat_ces/scientific/quantity` + equations | quantity/equation paths | MERGE |
| 0035 | Hardening verification | `lat_ces/scientific/quantity/verification` | tests | MERGE |
| 0036 | Hardening evidence | `lat_ces/scientific/quantity/verification` | tests/evidence | KEEP |
| 0037 | Formal verification | `lat_ces/smc/verification` | formal invariants | MOVE |
| 0038 | Physical quantity engine | `lat_ces/scientific/quantity` | scientific quantity | MERGE |
| 0039 | Physical quantity implementation | `lat_ces/scientific/quantity/quantity.py` | actual `PhysicalQuantity` | ADAPT |
| 0040 | Quantity verification spec | `lat_ces/scientific/quantity/verification` | quantity tests | MERGE |
| 0041 | Quantity verification | `lat_ces/scientific/quantity/verification` | tests/evidence | KEEP |
| 0042 | Quantity hardening spec | `lat_ces/scientific/quantity/integrity` | integrity/audit | ADAPT |
| 0043 | Quantity hardening implementation | `lat_ces/scientific/quantity/quantity.py` | actual PhysicalQuantity | MERGE |
| 0044 | Hardening verification | `lat_ces/scientific/quantity/verification` | tests | MERGE |
| 0045 | Hardening evidence | `lat_ces/scientific/quantity/verification` | tests/evidence | KEEP |
| 0046 | Measurement engine | `lat_ces/scientific/measurement.py` | actual measurement + tests | MERGE |
| 0047 | Measurement implementation | `lat_ces/scientific/measurement.py` | actual measurement.py | KEEP + ADAPT |
| 0048 | Measurement verification | `lat_ces/scientific/measurement` verification | tests | MERGE |
| 0049 | Measurement evidence | `lat_ces/scientific/measurement` verification | tests/evidence | KEEP |
| 0050 | Measurement hardening | `lat_ces/scientific/measurement` integrity | measurement/integrity | ADAPT |
| 0051 | Measurement hardening implementation | `lat_ces/scientific/measurement.py` | actual measurement.py | ADAPT |
| 0052 | Hardening verification | `lat_ces/scientific/measurement` verification | tests | MERGE |
| 0053 | Hardening evidence | `lat_ces/scientific/measurement` verification | tests/evidence | KEEP |
| 0054 | Data provenance spec | `lat_ces/scientific/provenance` | `gov/provenance.py`, ledger, graph/lineage | MERGE |
| 0055 | Data provenance implementation | `lat_ces/scientific/provenance` | governance + lineage/evidence | MERGE + ADAPT |

## Canonical duplicate-resolution rules

### Quantity
`lat_ces/modules/quantity.py` is already a compatibility bridge to `lat_ces.scientific.quantity.quantity.PhysicalQuantity`. Do not create another Quantity implementation. Migrate callers, then retire only the bridge when unused.

### Units
`lat_ces/scientific/units/registry.py` is the canonical registry. `lat_ces/core/dimensions.py` remains a compatibility dependency during migration. Do not create another SI registry.

### Equations
Converge legacy equation callers on `lat_ces/scientific/equations`. Do not create SCI-number-specific equation engines.

### Provenance
`lat_ces/gov/provenance.py` and `data/provenance_ledger.jsonl` remain operational compatibility infrastructure. Wrap/adapt them behind one canonical Scientific Provenance contract; do not delete the ledger during consolidation.

## Execution gates

1. Freeze legacy APIs; no silent deletion.
2. Establish canonical imports and compatibility bridges.
3. Migrate imports subsystem-by-subsystem.
4. Run targeted tests after each subsystem.
5. Run full pytest and CI.
6. SMC-001 specification traceability.
7. SMC-002 legacy consolidation checks.
8. SMC-003 Scientific Model contract checks.
9. SMC-004 acceptance gate.
10. Only after acceptance: remove duplicate implementations with zero production imports.

## RETIRE gate

RETIRE is authorized only when production imports are zero, required tests no longer depend on the old path, identity/provenance continuity is demonstrated, canonical replacement passes regression tests, and SMC-004 accepts the migration.

## SCI 1–145
SCI 0001–0055 are the audited legacy sequence. SCI 0056–0145 use the canonical owners and SMC contracts established here. No SCI number by itself creates a new Python module.
