# GitHub Reconstruction Inventory v0.1

**System:** LAT-CES / LATSES  
**Repository:** `fahrudinsusnjar-eng/LATSES`  
**Canonical snapshot:** `main`  
**Snapshot commit:** `170ec750f9aaa4ecba227bf9401674919e8abd81`  
**Purpose:** Preserve and classify the existing implementation before final AILCS/LAT-CES documentation is reconstructed.

## 0. Reconstruction rule

This inventory is an evidence register, not a final specification. No requirement is inferred merely because a file exists. The authoritative chain is:

`SOURCE-ID -> original requirement -> implementation/evidence -> P1-P4 -> status -> action`

For this v0.1 pass, `original requirement` remains **PENDING EXTRACTION** unless it is explicitly present in a source artifact already inspected. P1-P4 are provisional reconstruction priorities.

### Priority meaning

- **P1** — constitutional identity, authority, provenance, canonicality, scientific validity, safety boundary, or integrity issue that must be closed before finalization.
- **P2** — architectural consolidation/integration issue; important for a canonical implementation but not necessarily a constitutional defect.
- **P3** — documentation, testing, evidence, reporting, or validation completion.
- **P4** — future/experimental/extension capability; must not be represented as completed core capability without evidence.

## 1. Repository baseline

| Field | Evidence / value | Status | Priority |
|---|---|---|---|
| Repository | `fahrudinsusnjar-eng/LATSES` | VERIFIED | P1 |
| Canonical branch for this inventory | `main` | VERIFIED | P1 |
| Snapshot commit | `170ec750f9aaa4ecba227bf9401674919e8abd81` | VERIFIED | P1 |
| Named branch `susnjarfahrudinai` | Not present in connected repository branch set | VERIFY EXTERNAL | P1 |
| Reconstruction inventory | This file | CREATED | P1 |
| Existing main documentation | `SCI 1-145 LAT SES.docx` | PRESENT | P1/P3 |

## 2. Constitutional / core layer

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-COR-001 | `lat_ces/core/axioms.py` | Constitutional axioms | P1 | IMPLEMENTED | Extract exact axioms and map to canonical hierarchy |
| GH-COR-002 | `lat_ces/core/sko.py` | Scientific Knowledge Object | P1 | IMPLEMENTED | Map identity/integrity requirements to source requirements |
| GH-COR-003 | `lat_ces/core/dimensions.py` | Dimension engine | P1/P3 | IMPLEMENTED | Validate canonical dimensional rules and tests |
| GH-COR-004 | `lat_ces/core/__init__.py` | Core package boundary | P2 | SUPPORT | Keep as package metadata |
| GH-GOV-001 | `lat_ces/gov/axiom.py` | Governance axiom abstraction | P1 | IMPLEMENTED | Reconcile with constitutional engine |
| GH-GOV-002 | `lat_ces/gov/provenance.py` | Provenance ledger | P1 | PARTIAL | Add/verify cryptographic provenance requirements |
| GH-GOV-003 | `lat_ces/gov/__init__.py` | Governance package boundary | P2 | SUPPORT | Retain |
| GH-GOV-T01 | `lat_ces/gov/tests/test_axiom.py` | Governance axiom tests | P3 | IMPLEMENTED | Map tests to requirements |
| GH-GOV-T02 | `lat_ces/gov/tests/test_provenance.py` | Provenance tests | P1/P3 | IMPLEMENTED | Expand to integrity/hash-chain requirements |
| GH-TST-AX | `tests/test_axioms.py` | Constitutional regression tests | P1/P3 | IMPLEMENTED | Link each assertion to source requirement |
| GH-TST-SKO | `tests/test_sko.py` | SKO regression tests | P1/P3 | IMPLEMENTED | Link identity/immutability assertions |

## 3. Mathematical and physical foundation

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-MTH-001 | `lat_ces/math/vector.py` | Vector operations | P2/P3 | IMPLEMENTED | Validate against state/control contracts |
| GH-MTH-002 | `lat_ces/math/field.py` | Field representation | P2/P3 | IMPLEMENTED | Confirm scientific scope |
| GH-MTH-003 | `lat_ces/math/state_space.py` | State-space mathematics | P2/P3 | IMPLEMENTED | Link to observer/control model contracts |
| GH-MTH-T01 | `lat_ces/math/tests/test_vector.py` | Vector tests | P3 | IMPLEMENTED | Map evidence |
| GH-MTH-T02 | `lat_ces/math/tests/test_field.py` | Field tests | P3 | IMPLEMENTED | Map evidence |
| GH-MTH-T03 | `lat_ces/math/tests/test_state_space.py` | State-space tests | P3 | IMPLEMENTED | Map evidence |
| GH-SCIQ-001 | `lat_ces/scientific/quantities/quantity.py` | Scientific quantity model | P1/P3 | IMPLEMENTED | Reconcile with core quantity model |
| GH-SCIU-001 | `lat_ces/scientific/units/unit.py` | Unit model | P1/P3 | IMPLEMENTED | Canonicalize unit authority |
| GH-SCIU-002 | `lat_ces/scientific/units/units.py` | Unit exports | P2 | SUPPORT | Retain |
| GH-SCIU-003 | `lat_ces/scientific/units/dimension.py` | Scientific dimension wrapper | P1/P2 | IMPLEMENTED | Reconcile duplicate dimension implementations |
| GH-SCIU-004 | `lat_ces/scientific/units/derived_units.py` | Derived SI units | P1/P3 | IMPLEMENTED | Validate canonical unit registry |
| GH-SCIU-T01 | `lat_ces/scientific/units/tests/test_conversion.py` | Conversion tests | P3 | IMPLEMENTED | Map evidence |
| GH-SCIU-T02 | `lat_ces/scientific/units/tests/test_quantity.py` | Quantity tests | P3 | IMPLEMENTED | Map evidence |
| GH-SCIU-T03 | `lat_ces/scientific/units/tests/test_registry.py` | Unit registry test | P3 | PRESENT | Inspect coverage |
| GH-SCIU-T04 | `lat_ces/scientific/units/tests/test_si_units.py` | SI unit tests | P3 | IMPLEMENTED | Map evidence |
| GH-SCIU-T05 | `lat_ces/scientific/units/tests/test_unit.py` | Unit tests | P3 | IMPLEMENTED | Map evidence |
| GH-SCIU-T06 | `lat_ces/scientific/units/tests/test_unit_conversion.py` | Conversion tests | P3 | IMPLEMENTED | Map evidence |
| GH-SCIU-T07 | `lat_ces/scientific/units/tests/test_units.py` | Units tests | P3 | IMPLEMENTED | Map evidence |

## 4. Scientific equation and engineering modules

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-EQ-001 | `lat_ces/modules/equation.py` | Physical equation engine | P1/P3 | IMPLEMENTED | Map equation identity/contract |
| GH-EQ-002 | `lat_ces/scientific/equation.py` | Scientific equation facade | P2 | IMPLEMENTED | Reconcile duplicate equation layers |
| GH-EQ-003 | `lat_ces/scientific/equations/equation.py` | Equation implementation | P1/P3 | IMPLEMENTED | Canonicalize |
| GH-EQ-004 | `lat_ces/scientific/equations/engine.py` | Equation engine facade | P2 | IMPLEMENTED | Reconcile with module engine |
| GH-EQ-005 | `lat_ces/scientific/equations/fluids.py` | Fluid equations | P1/P3 | IMPLEMENTED | Scientific validation and applicability mapping |
| GH-EQ-T01 | `tests/test_equation.py` | Equation tests | P3 | IMPLEMENTED | Map evidence |
| GH-EQ-T02 | `tests/test_scientific_equation.py` | Scientific equation tests | P3 | IMPLEMENTED | Map evidence |
| GH-EQ-T03 | `tests/test_fluid_equations.py` | Fluid equation tests | P3 | IMPLEMENTED | Map evidence |
| GH-EQ-T04 | `tests/test_advanced_fluid_equations.py` | Advanced fluid equation tests | P3/P4 | PRESENT | Determine validated scope |
| GH-EQ-T05 | `tests/test_venturi_bernoulli_equations.py` | Bernoulli/Venturi tests | P3 | IMPLEMENTED | Map evidence |
| GH-QTY-001 | `lat_ces/modules/quantity.py` | Physical quantity + uncertainty | P1/P3 | IMPLEMENTED | Reconcile with scientific quantity stack |
| GH-QTY-T01 | `tests/test_quantity.py` | Quantity tests | P3 | IMPLEMENTED | Map evidence |
| GH-QTY-T02 | `tests/test_physical_quantity.py` | Physical quantity tests | P3 | IMPLEMENTED | Map evidence |
| GH-QTY-T03 | `tests/test_unit_hardening.py` | Unit hardening tests | P1/P3 | IMPLEMENTED | Promote to normative evidence |

## 5. LAT-CES Module 010-020 lineage

| SOURCE-ID | Path | Declared module | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-M010 | `lat_ces/modules/quantity.py` | LAT-SCI-MOD-0010 | P1/P3 | IMPLEMENTED | Preserve as historical/module evidence |
| GH-M011 | `lat_ces/modules/equation.py` | LAT-SCI-MOD-0011 | P1/P3 | IMPLEMENTED | Preserve and map |
| GH-M012 | `lat_ces/modules/plenum.py` | LAT-SCI-MOD-0012 | P1/P3 | IMPLEMENTED | Validate model applicability |
| GH-M013 | `lat_ces/modules/acoustics.py` | LAT-SCI-MOD-0013 | P2/P3 | IMPLEMENTED | Validate acoustic domain |
| GH-M014 | `lat_ces/modules/thermal.py` | LAT-SCI-MOD-0014 | P1/P3 | IMPLEMENTED | Validate thermodynamic scope |
| GH-M015 | `lat_ces/modules/pressure.py` | LAT-SCI-MOD-0015 | P1/P3 | IMPLEMENTED | Validate pressure/power equations |
| GH-M016 | `lat_ces/modules/duct.py` | LAT-SCI-MOD-0016 | P2/P3 | IMPLEMENTED | Reconcile with scientific duct models |
| GH-M017 | `lat_ces/modules/fittings.py` | LAT-SCI-MOD-0017 | P2/P3 | IMPLEMENTED | Validate loss coefficients |
| GH-M018 | `lat_ces/modules/fan_laws.py` | LAT-SCI-MOD-0018 | P2/P3 | IMPLEMENTED | Validate affinity laws |
| GH-M019 | `lat_ces/modules/psychrometrics.py` | LAT-SCI-MOD-0019 | P1/P3 | IMPLEMENTED | Validate psychrometric domain |
| GH-M020 | `lat_ces/modules/pipeline_v3.py` | LAT-SCI-MOD-0020 | P2 | IMPLEMENTED | Establish canonical pipeline version |
| GH-M021 | `lat_ces/modules/pipeline.py` | Earlier pipeline | P2 | HISTORICAL/ACTIVE | Compare against v3 |

## 6. Scientific HVAC / building model inventory

| SOURCE-ID | Path | Domain | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-SCI-001 | `lat_ces/scientific/acoustics.py` | Acoustics | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-002 | `lat_ces/scientific/air_filtration.py` | Air filtration | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-003 | `lat_ces/scientific/boiler.py` | Boiler | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-004 | `lat_ces/scientific/chiller.py` | Chiller | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-005 | `lat_ces/scientific/coil_performance.py` | Coil performance | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-006 | `lat_ces/scientific/condensation.py` | Condensation | P1/P3 | IMPLEMENTED | Applicability/validation |
| GH-SCI-007 | `lat_ces/scientific/damper_authority.py` | Damper authority | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-008 | `lat_ces/scientific/duct_friction.py` | Duct friction | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-009 | `lat_ces/scientific/duct_leakage.py` | Duct leakage | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-010 | `lat_ces/scientific/duct_loss.py` | Duct loss | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-011 | `lat_ces/scientific/energy.py` | Energy | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-012 | `lat_ces/scientific/energy_cost.py` | Energy cost | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-013 | `lat_ces/scientific/fan_affinity.py` | Fan affinity | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-014 | `lat_ces/scientific/fan_curve.py` | Fan curve | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-015 | `lat_ces/scientific/filter_degradation.py` | Filter degradation | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-016 | `lat_ces/scientific/heat_exchanger.py` | Heat exchanger | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-017 | `lat_ces/scientific/heat_recovery.py` | Heat recovery | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-018 | `lat_ces/scientific/humidity.py` | Humidity | P1/P3 | IMPLEMENTED | Validate |
| GH-SCI-019 | `lat_ces/scientific/hydronic_pump.py` | Hydronic pump | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-020 | `lat_ces/scientific/iaq.py` | Indoor air quality | P1/P3 | IMPLEMENTED | Define normative IAQ requirements |
| GH-SCI-021 | `lat_ces/scientific/internal_gains.py` | Internal gains | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-022 | `lat_ces/scientific/mass_balance.py` | Mass balance | P1/P3 | IMPLEMENTED | Validate conservation requirement |
| GH-SCI-023 | `lat_ces/scientific/measurement.py` | Measurement model | P1 | IMPLEMENTED | Link measurement authority to constitution |
| GH-SCI-024 | `lat_ces/scientific/plenum.py` | Plenum | P1/P3 | IMPLEMENTED | Validate against physical tests |
| GH-SCI-025 | `lat_ces/scientific/pressure_drop.py` | Pressure drop | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-026 | `lat_ces/scientific/psychrometrics.py` | Psychrometrics | P1/P3 | IMPLEMENTED | Validate |
| GH-SCI-027 | `lat_ces/scientific/room_dynamics.py` | Room dynamics | P1/P3 | IMPLEMENTED | Validate against room measurements |
| GH-SCI-028 | `lat_ces/scientific/solar_gain.py` | Solar gain | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-029 | `lat_ces/scientific/stack_effect.py` | Stack effect | P1/P3 | IMPLEMENTED | Validate applicability |
| GH-SCI-030 | `lat_ces/scientific/thermal.py` | Thermal model | P1/P3 | IMPLEMENTED | Validate |
| GH-SCI-031 | `lat_ces/scientific/thermal_bridge.py` | Thermal bridge | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-032 | `lat_ces/scientific/thermal_comfort.py` | Thermal comfort | P1/P3 | IMPLEMENTED | Define validation criteria |
| GH-SCI-033 | `lat_ces/scientific/vav_damper.py` | VAV damper | P2/P3 | IMPLEMENTED | Validate |
| GH-SCI-034 | `lat_ces/scientific/vav_terminal.py` | VAV terminal | P2/P3 | IMPLEMENTED | Validate |

## 7. Scientific model governance / lifecycle

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-SMC-001 | `lat_ces/scientific/models/metadata.py` | Model metadata | P1 | IMPLEMENTED | Map to canonical model identity |
| GH-SMC-002 | `lat_ces/scientific/models/contract.py` | Model I/O contract | P1 | IMPLEMENTED | Make normative |
| GH-SMC-003 | `lat_ces/scientific/models/registry.py` | Scientific model registry | P1 | IMPLEMENTED | Verify identity and uniqueness |
| GH-SMC-004 | `lat_ces/scientific/models/applicability.py` | Model applicability | P1 | IMPLEMENTED | Complete domain/assumption rules |
| GH-SMC-005 | `lat_ces/scientific/models/reason_codes.py` | Applicability reason codes | P1/P3 | IMPLEMENTED | Map to decision evidence |
| GH-SMC-006 | `lat_ces/scientific/registry/constants.py` | Registry constants | P1/P2 | IMPLEMENTED | Reconcile registries |
| GH-SMC-007 | `lat_ces/scientific/registry/registry.py` | Registry implementation | P1/P2 | IMPLEMENTED | Establish canonical registry |
| GH-SMC-T01 | `tests/test_scientific_model_metadata.py` | Metadata regression | P1/P3 | IMPLEMENTED | Link evidence |
| GH-SMC-T02 | `tests/test_scientific_model_contract.py` | Contract regression | P1/P3 | IMPLEMENTED | Link evidence |
| GH-SMC-T03 | `tests/test_scientific_model_registry.py` | Registry regression | P1/P3 | IMPLEMENTED | Link identity evidence |
| GH-SMC-T04 | `tests/test_scientific_model_applicability.py` | Applicability regression | P1/P3 | IMPLEMENTED | Link applicability evidence |
| GH-SMC-T05 | `lat_ces/scientific/registry/tests/test_registry.py` | Registry tests | P1/P3 | IMPLEMENTED | Consolidate with model registry tests |

## 8. Scientific uncertainty / reporting / analysis

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-UNC-001 | `lat_ces/scientific/uncertainty/engine.py` | Uncertainty engine | P1/P3 | IMPLEMENTED | Define uncertainty propagation requirements |
| GH-UNC-T01 | `lat_ces/scientific/uncertainty/tests/test_uncertainty.py` | Uncertainty tests | P3 | IMPLEMENTED | Map evidence |
| GH-ANA-001 | `lat_ces/scientific/analysis/plenum.py` | Plenum analysis | P2/P3 | IMPLEMENTED | Link analysis to canonical model |
| GH-ANA-002 | `lat_ces/scientific/analysis/reporting.py` | Analysis reporting | P3 | IMPLEMENTED | Define evidence/report contract |
| GH-RPT-001 | `lat_ces/scientific/reports/pdf.py` | PDF report generation | P3 | IMPLEMENTED | Validate output as evidence |
| GH-RPT-002 | `lat_ces/scientific/reports/exporter.py` | Report exporter | P3 | PRESENT | Inspect completeness |
| GH-RPT-003 | `lat_ces/scientific/reports/pdf_generator.py` | PDF generator facade | P3 | PRESENT | Reconcile with PDF implementation |
| GH-RPT-T01 | `tests/test_reporting.py` | Reporting tests | P3 | IMPLEMENTED | Map evidence |
| GH-RPT-T02 | `tests/test_report_exporter.py` | Export tests | P3 | IMPLEMENTED | Map evidence |
| GH-RPT-T03 | `tests/test_pdf_generator.py` | PDF tests | P3 | IMPLEMENTED | Map evidence |

## 9. Digital Twin / telemetry / control / safety

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-TWN-001 | `lat_ces/twin/telemetry.py` | Telemetry packet/model | P1 | IMPLEMENTED | Define measurement authority and provenance |
| GH-TWN-002 | `lat_ces/twin/observer.py` | Luenberger observer | P1/P3 | IMPLEMENTED | Validate observability/estimation assumptions |
| GH-TWN-003 | `lat_ces/twin/drift.py` | Drift detection | P1/P3 | IMPLEMENTED | Define thresholds and validation |
| GH-CTL-001 | `lat_ces/control/lqr.py` | LQR controller | P1/P3 | IMPLEMENTED | Define control contract and stability evidence |
| GH-CTL-002 | `lat_ces/control/barrier.py` | Safety barrier | P1 | IMPLEMENTED | Make safety limits constitutionally authoritative |
| GH-COM-001 | `lat_ces/com/bus.py` | Communication bus | P1/P2 | IMPLEMENTED | Define interface/security contract |
| GH-COM-002 | `lat_ces/com/gateway.py` | Secure gateway | P1/P2 | IMPLEMENTED | Define security boundary |
| GH-DAT-001 | `lat_ces/data/snapshot.py` | Data snapshot | P2/P3 | IMPLEMENTED | Link snapshot identity to provenance |
| GH-DAT-002 | `lat_ces/data/timeseries.py` | Time series | P2/P3 | IMPLEMENTED | Define retention/integrity semantics |
| GH-SIM-001 | `lat_ces/sim/hil.py` | Hardware-in-the-loop scaffold | P4 | PRESENT | Do not classify as validated HIL without evidence |
| GH-SIM-002 | `lat_ces/sim/monte_carlo.py` | Monte Carlo simulation | P3/P4 | IMPLEMENTED | Define statistical validation scope |
| GH-TWN-T01 | `lat_ces/twin/tests/test_telemetry.py` | Telemetry tests | P3 | IMPLEMENTED | Map evidence |
| GH-TWN-T02 | `lat_ces/twin/tests/test_observer.py` | Observer tests | P3 | IMPLEMENTED | Map evidence |
| GH-TWN-T03 | `lat_ces/twin/tests/test_drift.py` | Drift tests | P3 | IMPLEMENTED | Map evidence |
| GH-CTL-T01 | `lat_ces/control/tests/test_lqr.py` | LQR tests | P3 | IMPLEMENTED | Map evidence |
| GH-CTL-T02 | `lat_ces/control/tests/test_barrier.py` | Barrier tests | P1/P3 | IMPLEMENTED | Promote safety tests to normative evidence |
| GH-COM-T01 | `lat_ces/com/tests/test_bus.py` | Bus tests | P3 | IMPLEMENTED | Map evidence |
| GH-COM-T02 | `lat_ces/com/tests/test_gateway.py` | Gateway tests | P1/P3 | IMPLEMENTED | Map security evidence |
| GH-DAT-T01 | `lat_ces/data/tests/test_snapshot.py` | Snapshot tests | P3 | IMPLEMENTED | Map evidence |
| GH-DAT-T02 | `lat_ces/data/tests/test_timeseries.py` | Time-series tests | P3 | IMPLEMENTED | Map evidence |
| GH-SIM-T01 | `lat_ces/sim/tests/test_hil.py` | HIL tests | P4/P3 | PRESENT | Determine whether this is scaffold or validation |
| GH-SIM-T02 | `lat_ces/sim/tests/test_monte_carlo.py` | Monte Carlo tests | P3 | IMPLEMENTED | Map evidence |

## 10. Master integration / runtime

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-PIPE-001 | `lat_ces/master_pipeline.py` | Master LAT-CES runtime | P1/P2 | IMPLEMENTED | Establish canonical runtime path |
| GH-PIPE-002 | `lat_ces/modules/pipeline.py` | Earlier network pipeline | P2 | HISTORICAL/ACTIVE | Compare and classify |
| GH-PIPE-003 | `lat_ces/modules/pipeline_v3.py` | Duct network integration v3 | P2 | IMPLEMENTED | Determine canonical role |
| GH-PIPE-004 | `build_pipeline.py` | Pipeline builder | P2/P3 | BUILD ARTIFACT | Determine whether reproducible build source |
| GH-PIPE-005 | `build_pipeline_v2.py` | Pipeline builder v2 | P2/P3 | BUILD ARTIFACT | Compare with canonical |
| GH-PIPE-T01 | `lat_ces/tests/test_master_pipeline.py` | Master runtime tests | P1/P3 | IMPLEMENTED | Link runtime assertions to requirements |
| GH-PIPE-T02 | `tests/test_pipeline.py` | Pipeline tests | P3 | IMPLEMENTED | Map evidence |
| GH-PIPE-T03 | `tests/test_pipeline_v2.py` | Pipeline v2 tests | P2/P3 | IMPLEMENTED | Classify historical/current |
| GH-PIPE-T04 | `tests/test_pipeline_v3.py` | Pipeline v3 tests | P2/P3 | IMPLEMENTED | Classify canonical status |

## 11. Build scripts and generated-source history

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-BLD-001 | `build_mod10.py` | Module 010 builder | P2/P3 | BUILD ARTIFACT | Preserve provenance of generated module |
| GH-BLD-002 | `build_mod11.py` | Module 011 builder | P2/P3 | BUILD ARTIFACT | Preserve provenance |
| GH-BLD-003 | `build_mod12.py` | Module 012 builder | P2/P3 | BUILD ARTIFACT | Preserve provenance |
| GH-BLD-004 | `build_mod13.py` | Module 013 builder | P2/P3 | BUILD ARTIFACT | Preserve provenance |
| GH-BLD-005 | `build_mod14.py` | Module 014 builder | P2/P3 | BUILD ARTIFACT | Preserve provenance |
| GH-BLD-006 | `build_mod15.py` | Module 015 builder | P2/P3 | BUILD ARTIFACT | Preserve provenance |
| GH-BLD-007 | `build_mod16.py` | Module 016 builder | P2/P3 | BUILD ARTIFACT | Preserve provenance |
| GH-BLD-008 | `build_block3.py` | Block 3 builder | P2/P3 | BUILD ARTIFACT | Identify generated outputs |
| GH-BLD-009 | `run_latces.py` | Runtime launcher | P2/P3 | IMPLEMENTED | Establish supported entrypoint |
| GH-BLD-010 | `init_git.sh` | Repository initialization | P3 | HISTORICAL | Preserve only as historical evidence |

## 12. Tests: repository-level evidence

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-TST-001 | `tests/test_acoustics.py` | Acoustic tests | P3 | IMPLEMENTED | Map |
| GH-TST-002 | `tests/test_dimensions.py` | Dimension tests | P1/P3 | IMPLEMENTED | Map |
| GH-TST-003 | `tests/test_duct.py` | Duct tests | P3 | IMPLEMENTED | Map |
| GH-TST-004 | `tests/test_fan_laws.py` | Fan-law tests | P3 | IMPLEMENTED | Map |
| GH-TST-005 | `tests/test_fittings.py` | Fitting tests | P3 | IMPLEMENTED | Map |
| GH-TST-006 | `tests/test_measurement.py` | Measurement tests | P1/P3 | IMPLEMENTED | Map measurement authority |
| GH-TST-007 | `tests/test_plenum.py` | Plenum tests | P1/P3 | IMPLEMENTED | Map |
| GH-TST-008 | `tests/test_plenum_analysis.py` | Plenum analysis tests | P3 | IMPLEMENTED | Map |
| GH-TST-009 | `tests/test_plenum_pressure_drop_equation.py` | Plenum pressure equation tests | P1/P3 | IMPLEMENTED | Map |
| GH-TST-010 | `tests/test_plenum_safety.py` | Plenum safety tests | P1 | IMPLEMENTED | Promote to safety evidence |
| GH-TST-011 | `tests/test_pressure.py` | Pressure tests | P3 | IMPLEMENTED | Map |
| GH-TST-012 | `tests/test_psychrometrics.py` | Psychrometric tests | P3 | IMPLEMENTED | Map |
| GH-TST-013 | `tests/test_thermal.py` | Thermal tests | P1/P3 | IMPLEMENTED | Map |
| GH-TST-014 | `tests/test_scientific_cli.py` | Scientific CLI tests | P3 | IMPLEMENTED | Map |
| GH-TST-015 | `tests/test_scientific_units.py` | Scientific units tests | P1/P3 | IMPLEMENTED | Map |
| GH-TST-016 | `tests/test_agent.py` | Agent tests | P2/P3 | IMPLEMENTED | Define agent boundary |

## 13. Documentation / reports / examples / evidence artifacts

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-DOC-001 | `SCI 1-145 LAT SES.docx` | Main scientific/system document | P1/P3 | PRESENT | Extract original requirements before rewriting |
| GH-DOC-002 | `README.md` | Repository architecture overview | P2/P3 | PRESENT | Reconcile with canonical architecture |
| GH-DOC-003 | `AGENTS.md` | Development/verification rules | P2/P3 | PRESENT | Treat as process evidence, not system requirement |
| GH-DOC-004 | `docs/architecture/LAT-ROM-SMC-001.md` | Scientific model architecture | P1/P2 | PRESENT | Map to SMC requirements |
| GH-DOC-005 | `docs/architecture/SMC-004-SMC-Architectural-Review.md` | SMC architectural review | P1/P2 | PRESENT | Extract decisions/constraints |
| GH-DOC-006 | `certifikat.md` | Certificate artifact | P3 | PRESENT | Verify meaning and evidentiary status |
| GH-DOC-007 | `certifikat.pdf` | Certificate artifact | P3 | PRESENT | Verify meaning and evidentiary status |
| GH-EX-001 | `examples/demo_plenum_workflow.py` | Plenum example | P3 | PRESENT | Use as reproducibility evidence only |
| GH-EX-002 | `examples/plenum_input.json` | Plenum input | P3 | PRESENT | Link to example evidence |
| GH-EX-003 | `examples/plenum_integration_demo.py` | Integration demo | P2/P3 | PRESENT | Map integration evidence |
| GH-EX-004 | `examples/plenum_north_config.json` | North plenum config | P3 | PRESENT | Map |
| GH-EX-005 | `examples/plenum_north_report.json` | North plenum report | P3 | PRESENT | Map |
| GH-EX-006 | `examples/demo_report_weasyprint.py` | Report example | P3 | PRESENT | Map |
| GH-RUN-001 | `demo_report.md` | Demo report | P3 | PRESENT | Evidence classification |
| GH-RUN-002 | `demo_report.json` | Demo report data | P3 | PRESENT | Evidence classification |
| GH-RUN-003 | `demo_report.pdf` | Demo report PDF | P3 | PRESENT | Evidence classification |
| GH-RUN-004 | `filter_degradation_report.py` | Filter report generator | P3 | PRESENT | Map |
| GH-RUN-005 | `reports/generate_filter_report.py` | Filter report generator | P3 | PRESENT | Reconcile duplicate reporting path |
| GH-RUN-006 | `filter_degradation_report.png` | Generated report image | P3 | PRESENT | Preserve as output evidence |
| GH-RUN-007 | `filter_degradation_longterm.png` | Long-term degradation result | P3/P4 | PRESENT | Validate before normative use |

## 14. Packaging / CI / repository controls

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-CI-001 | `.github/workflows/ci.yml` | Main CI workflow | P1/P3 | PRESENT | Verify active workflow and tests |
| GH-CI-002 | `.github/workflows/GitHub Actions CI Pipeline (.github/workflows/ci.yml)` | Historical/duplicated CI path | P2 | PRESENT | Classify duplicate artifact |
| GH-CI-003 | `pytest.ini` | Test configuration | P3 | PRESENT | Preserve as test policy evidence |
| GH-CI-004 | `.gitignore` | Repository hygiene | P3 | PRESENT | Retain |
| GH-CI-005 | `.devcontainer/devcontainer.json` | Development environment | P3 | PRESENT | Verify reproducibility |
| GH-PKG-001 | `pyproject.toml` | Python package/build metadata | P2/P3 | PRESENT | Verify supported package entrypoints |
| GH-PKG-002 | `lat_ces/cli.py` | LAT-CES CLI | P2/P3 | PRESENT | Define supported interface |
| GH-PKG-003 | `lat_ses/agent.py` | LAT-SES agent | P2 | IMPLEMENTED | Define relationship to LAT-CES |
| GH-PKG-004 | `lat_ses/__init__.py` | LAT-SES package | P2 | SUPPORT | Retain |

## 15. Data / ledger

| SOURCE-ID | Path | Role | P1-P4 | Status | Action |
|---|---|---|---|---|---|
| GH-LED-001 | `data/provenance_ledger.jsonl` | Existing provenance data | P1 | PRESENT/PARTIAL | Inspect schema; reconcile with constitutional provenance requirement |
| GH-LED-002 | `lat_ces/data/snapshot.py` | Snapshot persistence model | P2/P3 | IMPLEMENTED | Link snapshot identity to ledger |
| GH-LED-003 | `lat_ces/data/timeseries.py` | Time-series persistence | P2/P3 | IMPLEMENTED | Define integrity/retention semantics |

## 16. Known duplicate / lineage zones requiring explicit reconstruction

1. `lat_ces/core/*` versus `lat_ces/scientific/*` — determine canonical foundation versus scientific facade.
2. `lat_ces/modules/*` versus `lat_ces/scientific/*` — determine which layer is normative and which is compatibility/historical.
3. `pipeline.py` / `pipeline_v3.py` / `master_pipeline.py` / `build_pipeline*.py` — determine canonical runtime and historical builders.
4. `lat_ces/scientific/registry/*` versus `lat_ces/scientific/models/registry.py` — determine whether one is a lower-level registry and one a model registry, or whether consolidation is required.
5. `lat_ces/scientific/units/*` versus `lat_ces/core/dimensions.py` and `lat_ces/modules/quantity.py` — define authoritative physical quantity/unit path.
6. `docs/architecture/*` versus `SCI 1-145 LAT SES.docx` — extract original requirements first; do not rewrite either source prematurely.
7. CI workflow paths — classify active versus historical/duplicated workflow artifacts.

## 17. Key commit evidence to preserve

| COMMIT-ID | SHA | Message / significance | P1-P4 |
|---|---|---|---|
| GH-CMT-001 | `b774cd70d190742d9ceac7c50936bf66ba952a91f` | `SMN-001: Add Reynolds number model` | P3 |
| GH-CMT-002 | `fff0d7cdd9b57cebd090f733523cfb44165384be` | `SMN-002: Add Mach number model` | P3 |
| GH-CMT-003 | `34aaa192375f9ece4b552410b3d32e885c93975a` | `SMN-003: Add Prandtl number model` | P3 |
| GH-CMT-004 | `26432c503746630eea3ee7da109d74cc52caf99f` | `SMN-004: Add Nusselt number model` | P3 |
| GH-CMT-005 | `80aa50c987849a35d29eed13d5386bd130a2b30c` | `SMN-005: Add Biot number model` | P3 |
| GH-CMT-006 | `554b19f28c45ce4d4feb2711069a217c4e1f1e2c` | `SMN-006: Add Fourier number model` | P3 |
| GH-CMT-007 | `d4162512178687a6bdae31312dae657aff07011f` | `SMC-001: Add scientific model metadata` | P1 |
| GH-CMT-008 | `244830d8b6fff1150e9f4a13d5c8288a50cabb41` | `SMC-002: Add scientific model input output contract` | P1 |
| GH-CMT-009 | `f79653d185835f2cb28286bb010922d4227e764b` | `SMC-003: Add scientific model registry` | P1 |
| GH-CMT-010 | `164a91e9aa1514b0de4da8d5d4728c0d4cda9463` | `SMC-004: Add scientific model applicability` | P1 |
| GH-CMT-011 | `5b7a4a3aadae6dca0011c54674d5901834a89010` | `Add SMC constitutional boundary and architectural review` | P1 |
| GH-CMT-012 | `e1e6c2f1ab34ba252e2ede0d12715162465eb4a4` | `Consolidate scientific model lifecycle and applicability` | P1/P2 |
| GH-CMT-013 | `cdbef0fa497b2b2ea71ceabb6eee1ad373694e04` | `Add applicability regression for missing required input` | P1/P3 |
| GH-CMT-014 | `86aa38fd886079928689f70ffeb6d92520f074a9` | `Fix GitHub Actions CI pipeline` | P3 |
| GH-CMT-015 | `170ec750f9aaa4ecba227bf9401674919e8abd81` | `Add registry identity integrity regression test` — current main snapshot | P1 |

## 18. Reconstruction status at v0.1

### P1 — immediate closure register

- Canonical source identity / SOURCE-ID scheme.
- Constitutional hierarchy and authority mapping.
- Cryptographic provenance versus current ledger implementation.
- Scientific model identity, contract, registry and applicability.
- Canonical physical quantity / dimension / unit authority.
- Canonical runtime path and safety authority.
- Measurement authority and reality-supremacy traceability.

### P2 — consolidation register

- Duplicate module/scientific layers.
- Multiple pipeline generations.
- Multiple registry layers.
- Multiple reporting/build paths.
- LAT-CES versus LAT-SES boundary.

### P3 — evidence register

- Map all existing tests to requirements.
- Map reports/examples to reproducible evidence.
- Extract original requirements from `SCI 1-145 LAT SES.docx`.
- Verify CI coverage and reproducibility.

### P4 — future/experimental register

- HIL beyond scaffold-level evidence.
- Advanced validation and deployment extensions.
- Any capability present only as a prototype without validated evidence.

## 19. Next reconstruction action

**Do not write final AILCS/LAT-CES normative documents yet.**

Next pass must take this GitHub inventory and join it with the Library/document inventory:

`GitHub SOURCE-ID + Library SOURCE-ID -> original requirement -> implementation -> test/evidence -> P1-P4 -> status -> action`

Only after this combined register is closed should the final AILCS/LAT-CES documentation be generated.

---

**Inventory version:** v0.1  
**Snapshot:** `main@170ec750f9aaa4ecba227bf9401674919e8abd81`  
**Classification:** Reconstruction control artifact; not yet a final normative specification.
