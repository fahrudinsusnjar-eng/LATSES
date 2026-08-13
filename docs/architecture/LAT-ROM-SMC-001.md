# LAT-ROM-SMC-001 — SMC Constitutional Boundary & Replacement Contract

**Status:** Proposed
**Revision:** Rev A
**System:** LAT
**Subsystem:** LAT-ROM / SMC

---

## 1. Purpose

This contract defines the constitutional boundary between LAT-ROM, SMC-ROM, and individual SMC scientific models.

SMC-ROM is a selector and coordinator of scientific models.

SMC-ROM does not constitute a source of constitutional truth and does not replace human decision authority.

---

## 2. Fundamental Principle

> **LAT does not need to always be correct in order to be responsible. It must be able to demonstrate why a decision was made at a particular time and why that decision was later changed.**

> **LAT does not represent itself as a fact; LAT represents its analysis of facts.**

Scientific models analyse the verified knowledge available within the applicable time and execution context.

The human remains the final decision-maker.

---

## 3. Constitutional Hierarchy

The architectural relationship is:

LAT Constitution
      |
      v
   LAT-ROM
      |
      v
   SMC-ROM
      |
      v
 SMC scientific models

Each lower layer operates only within the authority granted by the layer above it.

No SMC model may override the LAT Constitution or LAT-ROM.

---

## 4. Information Isolation

### 4.1 Individual SMC Model

An individual SMC model:
- does not need to know that SMC-ROM exists;
- does not need to know that LAT-ROM exists;
- receives only permitted execution context;
- returns only contractually permitted results.

### 4.2 SMC-ROM

SMC-ROM:
- does not need to know LAT-ROM internal decisions;
- receives only the authority required for selection and coordination;
- cannot inspect LAT-ROM private decision records.

### 4.3 LAT-ROM

LAT-ROM:
- supervises SMC-ROM;
- may read the independent SMC-ROM decision history;
- may determine whether SMC-ROM violated its contract;
- may replace SMC-ROM when required.

LAT-ROM internal decisions remain private to LAT-ROM.

---

## 5. SMC-ROM Role

SMC-ROM is the selector.

Its responsibilities include:

1. selecting applicable SMC models;
2. rejecting models that fail applicability or contract requirements;
3. removing models from active execution;
4. replacing models when permitted;
5. maintaining bounded operational state;
6. preserving decision provenance;
7. reconstructing operational state after application restart.

SMC-ROM shall not:

- redefine scientific truth;
- modify constitutional axioms;
- override LAT-ROM;
- erase historical evidence;
- represent its analysis as unquestionable fact;
- bypass the human decision-maker.

---

## 6. Model Lifecycle

An SMC model may have operational states such as:

ACTIVE
INACTIVE
BENCHED
RETIRED
INVALID
SUPERSEDED

These states describe operational applicability and lifecycle.

They do not independently establish whether a scientific proposition is true or false.

---

## 7. Model Rejection and Replacement

A model may be removed from active execution when:

- its contract is invalid;
- applicability conditions are not satisfied;
- required inputs are missing;
- the required model version is unavailable;
- it has been superseded;
- continuation is not permitted by SMC-ROM.

Removal from active execution shall not delete historical records.

A model may have been valid for the knowledge and execution context available at an earlier time.

---

## 8. Decision Provenance

Every significant SMC-ROM selection, rejection, replacement, retirement, or supersession decision shall create a decision record.

Where applicable, the record contains:

- decision identifier;
- timestamp;
- application session identifier;
- model identifier;
- model version;
- previous state;
- resulting state;
- reason code;
- evidence references;
- applicability result;
- contract result;
- supersession relationship;
- selector version.

The purpose of provenance is traceability and accountability.

---

## 9. Supersession

Supersession records why a later model, decision, or version replaced an earlier one.

A supersession record shall preserve:

- the superseded model or decision;
- the superseding model or decision;
- the time of supersession;
- the reason for supersession;
- the evidence supporting the change;
- the applicable knowledge or execution context;
- the authority that permitted the replacement.

Supersession does not imply that the previous decision was irrational or invalid at the time it was made.

It establishes that the later state is the currently applicable state under a changed context, evidence base, contract, or scientific understanding.

---

## 10. Operational State vs Historical Record

Operational state and historical state are distinct.

Operational state:

- ACTIVE;
- BENCHED;
- RETIRED;
- INVALID;
- SUPERSEDED.

Historical record:

- decision;
- rationale;
- evidence;
- timestamp;
- provenance;
- supersession.

Operational cleanup shall never imply historical deletion.

---

## 11. Bounded Operational Bench

SMC-ROM shall maintain a bounded operational bench.

BENCH_CAPACITY = 10

The bench contains candidates that are not currently active but remain eligible for possible future selection.

The bench must never grow without bound.

---

## 12. Bench Eviction

When a new candidate must be added while the bench is full, the oldest operational bench entry shall be removed.

The eviction policy is:

FIFO — First In, First Out

Example:

B1 B2 B3 B4 B5 B6 B7 B8 B9 B10

After adding B11:

B2 B3 B4 B5 B6 B7 B8 B9 B10 B11

B1 is evicted from operational bench state.

---

## 13. Bench Eviction Does Not Delete History

Eviction from the operational bench shall never delete the historical decision record.

Therefore:

The bench is bounded; history is preserved.

The limit of ten applies only to active operational bench state.

It does not limit provenance, evidence, or decision history.

---

## 14. Restart and State Reconstruction

Application restart shall not erase SMC-ROM historical records.

After restart, SMC-ROM shall reconstruct operational state from the preserved authoritative records available to it.

A model that was previously rejected, invalidated, superseded, or retired shall not automatically become active solely because the application restarted.

If a model cannot be validated after restart, SMC-ROM shall mark it as INVALID or otherwise non-active according to the applicable contract.

The human-facing interface shall not expose internal selector or constitutional details.

---

## 15. SMC-ROM Oversight and Replacement

SMC-ROM operates under LAT-ROM authority.

LAT-ROM may inspect the independent SMC-ROM decision history when required for constitutional or contractual oversight.

SMC-ROM shall not receive or infer LAT-ROM private decision records.

If LAT-ROM determines that SMC-ROM has violated its constitutional or contractual boundaries, LAT-ROM may suspend, replace, or otherwise restrict SMC-ROM.

Replacement shall not erase the historical record of the previous SMC-ROM.

The replacement SMC-ROM shall begin from the authoritative state permitted by LAT-ROM and the preserved records available to it.

---

## 16. Independent Decision Record

SMC-ROM shall write decision records to an independent, append-oriented record store.

The record store shall be logically separated from SMC-ROM operational state.

SMC-ROM shall not be permitted to delete or rewrite historical decision records through normal operational execution.

LAT-ROM shall have read-only access to the SMC-ROM decision record store for oversight purposes.

The record store shall preserve sufficient information to reconstruct the sequence of SMC-ROM operational decisions.

---

## 17. Reason Codes

Every consequential SMC-ROM operational decision shall use a deterministic reason code.

Reason codes shall describe the operational cause of the decision.

Reason codes shall not be used to redefine scientific truth.

A reason code shall be traceable to the applicable contract, applicability evaluation, evidence, or lifecycle rule.

The reason-code catalogue shall be versioned independently from individual model results.

---

## 18. Individual SMC Model Boundary

An individual SMC model is responsible only for the scientific analysis defined by its contract.

An individual SMC model shall:

- evaluate its permitted inputs;
- produce its permitted outputs;
- expose applicability information required by its contract;
- identify uncertainty or limitations when required;
- remain within its declared scientific domain.

An individual SMC model shall not:

- select itself as the active model;
- select another SMC model;
- modify SMC-ROM state;
- access LAT-ROM records;
- access another models private operational state;
- modify constitutional axioms.

---

## 19. Direction of Authority

Authority flows downward through the architectural hierarchy:

LAT-ROM -> SMC-ROM -> individual SMC models.

Operational information required for execution may flow upward only through defined interfaces and recorded results.

No lower layer may grant authority to itself or to a higher layer.

No individual SMC model may establish, modify, or revoke the authority of SMC-ROM.

No SMC-ROM decision may modify the authority of LAT-ROM.

Constitutional authority originates above the scientific-model execution layer and is not delegated upward by model output.

---

## 20. Human Decision Boundary

SMC-ROM may provide model-selection and applicability decisions to the LAT execution layer.

SMC-ROM shall not represent an operational selection as a command binding the human decision-maker.

The human decision-maker remains the final authority for decisions requiring human judgement.

Internal selector identity, LAT-ROM oversight mechanisms, constitutional records, and private supervisory decisions shall not be exposed through the normal human-facing interface.

---

## 21. SMC-005 Boundary

SMC-005 shall operate only on information explicitly exposed through its authorized interface.

SMC-005 may consume:

- validated model metadata;

- applicability results;

- contract validation results;

- deterministic reason codes;

- permitted evidence references;

- permitted model lifecycle state;

- authorized execution context.

SMC-005 shall not consume:

- LAT-ROM private decision records;

- SMC-ROM private selector identity;

- constitutional supervisory records;

- hidden model state belonging to another SMC;

- information obtained by bypassing an authorized interface.

---

## 22. SMC-005 Output Boundary

SMC-005 shall return only structured results defined by its authorized contract.

Permitted outputs may include:

- applicability status;

- applicability reason code;

- validated model identifier;

- validated model version;

- contract status;

- evidence references permitted by the interface;

- explicit limitations or uncertainty indicators;

- provenance identifiers required for traceability.

SMC-005 shall not return:

- constitutional decisions;

- LAT-ROM private decisions;

- SMC-ROM private selector identity;

- authority grants or revocations;

- instructions to modify another subsystems authority;

- claims that its scientific analysis constitutes unquestionable fact.

---

## 23. Failure and Safe Non-Execution

If SMC-005 cannot establish a valid result under its authorized contract, it shall not fabricate, infer, or silently substitute a result.

Failure to establish applicability shall result in a non-active outcome.

A non-active outcome shall not be interpreted as proof that the underlying scientific proposition is false.

The failure shall be recorded with an applicable deterministic reason code and provenance information.

The LAT execution layer shall determine the appropriate operational response according to its governing contract.

SMC-005 shall not bypass failure handling by selecting an unauthorized model or accessing unauthorized state.

SMC-ROM shall reconstruct its operational state only from records within its authorized information boundary.

LAT-ROM private decisions shall not form part of SMC-ROM state reconstruction.

If the preserved records are insufficient to establish a valid operational state, SMC-ROM shall enter a non-active or otherwise safe state defined by its governing contract.

---

## 24. Constitutional Violation and SMC-ROM Replacement

If LAT-ROM determines that SMC-ROM has violated a constitutional, architectural, or contractual boundary, LAT-ROM may suspend, restrict, replace, or otherwise remove SMC-ROM from operational authority.

Such action shall not delete, rewrite, or conceal the historical records produced by the previous SMC-ROM.

The determination to replace SMC-ROM shall remain an internal LAT-ROM decision and shall not be delegated to an individual SMC model.

A replacement SMC-ROM shall operate only within the authority granted by LAT-ROM and shall inherit only the authoritative operational state and historical information explicitly permitted by its contract.

Replacement shall preserve continuity of provenance and shall establish a traceable relationship between the previous SMC-ROM and its replacement.

---

## 25. Architectural Invariants and Final Boundary

The following invariants are mandatory:

1. Constitutional authority originates above the scientific-model execution layer.
2. LAT-ROM remains above SMC-ROM in the authority hierarchy.
3. SMC-ROM remains above individual SMC models in the operational selection hierarchy.
4. No individual SMC model may select, replace, or govern SMC-ROM.
5. No SMC-ROM decision may modify the authority of LAT-ROM.
6. No scientific-model result may modify constitutional authority.
7. Historical records shall not be deleted as part of normal operational cleanup.
8. Operational state and historical record shall remain conceptually distinct.
9. Restart shall not automatically reactivate an invalid, retired, superseded, or rejected model.
10. Failure to establish a valid result shall result in safe non-execution rather than fabricated certainty.
11. The operational bench may be bounded, but provenance and historical records shall remain preserved.
12. SMC-005 shall operate only within its authorized information and output boundaries.
13. Internal selector identity and private supervisory mechanisms shall not be exposed through the normal human-facing interface.
14. The human decision-maker remains the final authority where human judgement is required.
15. No lower layer may grant authority to itself or to a higher layer.

These invariants constitute the final architectural boundary of this contract.

Any future extension, implementation, or replacement of SMC-ROM or an individual SMC model shall remain compatible with these invariants or shall require an explicit revision of this contract and the applicable constitutional governance process.
