# Priority A/B — TEST MATRIX → DEPENDENCY MAP

Target: `susnjarfahrudin-ai/LATSES`

Source examined: `fahrudinsusnjar-eng/LATSES@170ec750f9aaa4ecba227bf9401674919e8abd81`

## Priority A — Scientific model lifecycle / applicability

| File | Import dependency | Public API | Existing tests | Regression gate | Action |
|---|---|---|---|---|---|
| `lat_ces/scientific/models/metadata.py` | `lat_ces.scientific.dimensions.dimension.Dimension` | `ModelInput`, `ModelOutput`, `ScientificModelMetadata` | `tests/test_scientific_model_applicability.py`, `tests/test_scientific_model_registry.py` | metadata identity + required input/output invariants | ADAPT/MERGE |
| `lat_ces/scientific/models/contract.py` | `.metadata` | `ScientificModelContract`, `ContractIssue`, `validate()`, `is_valid` | applicability contract-invalid case | duplicate names / invalid dimensions block applicability | ADAPT/MERGE |
| `lat_ces/scientific/models/registry.py` | `.contract`, `.metadata` | `ModelRegistry`, `ModelRegistryEntry`, `ModelStatus` | registry tests | registry/model metadata identity must match | ADAPT/MERGE |
| `lat_ces/scientific/models/reason_codes.py` | stdlib `Enum` | `ApplicabilityReason` | applicability tests | stable reason codes for all gate outcomes | ADAPT/MERGE |
| `lat_ces/scientific/models/applicability.py` | `.reason_codes`, `.registry` | `ApplicabilityEvaluator`, request/result/status | applicability tests | contract gate → context gate → required-input gate | ADAPT/MERGE |
| `lat_ces/scientific/models/__init__.py` | all model submodules | canonical package exports | import smoke through tests | all public symbols import from one package | ADAPT/MERGE |
| `tests/test_scientific_model_applicability.py` | `lat_ces.scientific.models` | regression suite | existing | preserve all gate outcomes + invalid contract | KEEP/ADAPT |
| `tests/test_scientific_model_registry.py` | `lat_ces.scientific.models` | regression suite | existing | metadata.model_id mismatch rejected | KEEP/ADAPT |

## Priority B — Scientific fluid equation expansion

| File | Import dependency | Public API | Existing tests | Regression gate | Action |
|---|---|---|---|---|---|
| `lat_ces/scientific/equations/equation.py` | `Dimension`, canonical `PhysicalQuantity` shim | `PhysicalEquation.evaluate()` alias | fluid tests | `evaluate()` == `calculate()` behavior | ADAPT |
| `lat_ces/scientific/equations/fluids.py` | `PhysicalEquation`, `PhysicalQuantity`, `Unit`, dimensions | `MASS_FLOW`, `MassFlowEquation`, `VolumetricFlowEquation` | `tests/test_fluid_equations.py` | mass-flow calculation + uncertainty + alias | ADAPT |
| `tests/test_fluid_equations.py` | fluid equations + canonical quantity | equation regression suite | existing | volumetric alias and mass-flow result | KEEP/ADAPT |
| `tests/test_advanced_fluid_equations.py` | fluid equations + canonical quantity | Venturi/Bernoulli regression suite | existing | numerical values, uncertainty, domain/dimension checks | KEEP/ADAPT |

## Dependency map

```text
PhysicalQuantity canonical implementation
        ↑
legacy quantity.py compatibility shim
        ↑
PhysicalEquation
        ↑
fluids.py
   ├── ContinuityEquation → VolumetricFlowEquation alias
   ├── MassFlowEquation
   ├── DynamicPressureEquation
   ├── PlenumPressureDropEquation
   ├── VenturiFlowEquation
   └── BernoulliTotalPressureEquation

ScientificModelMetadata
        ↓
ScientificModelContract
        ↓
ModelRegistryEntry → ModelRegistry
        ↓
ApplicabilityEvaluator
        ↓
ApplicabilityResult / ApplicabilityReason
        ↓
tests/test_scientific_model_applicability.py
        tests/test_scientific_model_registry.py
```

## Controlled merge/adapt rules

1. No deletion of existing canonical files.
2. Preserve `lat_ces.scientific.quantity` as the compatibility import path; its implementation remains `lat_ces.scientific.quantities.quantity.PhysicalQuantity`.
3. Import Priority A model modules without coupling them to equation execution.
4. Add Priority B equations as additive API extensions; do not rename/remove existing equations.
5. Add regression tests before any cleanup/obsolete-file decision.
6. No cleanup or deletion is part of this branch.
