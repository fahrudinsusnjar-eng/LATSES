# LAT-CES / LATSES RECONSTRUCTION — SECOND LIBRARY PASS v0.1

**Date:** 2026-09-10  
**Repository baseline:** `main@170ec750f9aaa4ecba227bf9401674919e8abd81`  
**Purpose:** Second document-by-document Library pass to extract original requirements not sufficiently represented in `RECONSTRUCTION_REGISTER_v0.2`.  
**Control rule:** This is reconstruction evidence, not final normative documentation. Final AILCS/LAT-CES documentation remains blocked until the reconstruction register is closed.

## 1. Extraction rule

Only requirements that are explicitly stated or directly structured as mandatory obligations in the Library sources are recorded. Editorial comments, recommendations, examples and future ideas are not converted into requirements unless the source gives them normative force.

Where a requirement already exists in v0.2, it is marked **DUPLICATE / REFINED** rather than silently creating a second requirement.

Status is reconstruction status only:

- **EXTRACTED** — original requirement located in Library.
- **REFINED** — requirement already exists in v0.2 but this pass adds an atomic constraint or acceptance detail.
- **CONFLICT/REVISION** — same subject appears with materially different revision/status wording and requires reconciliation.
- **PENDING IMPLEMENTATION MAP** — source requirement extracted; GitHub mapping not yet closed.

---

# 2. LIB-LCP-001 — LAT Constitutional Principles Rev D1.2

Source: `LIB-LCP-001` / Library file `LAT LCP Constitutional Principles Rev D1.2.docx`.

### REQ-LCP-011 — Multiple hypotheses before confidence
LAT shall actively evaluate multiple plausible explanations and search for competing explanations before increasing confidence in one hypothesis.  
**P1** — EXTRACTED/REFINED.  
**Action:** Map to analysis/recommendation logic; do not assume ordinary model comparison satisfies constitutional independence.

### REQ-LCP-012 — Disconfirmation search
LAT shall actively seek evidence capable of disproving the currently preferred hypothesis whenever reasonably achievable. Failure to identify an alternative shall not be treated as proof that none exists.  
**P1** — EXTRACTED.  
**Action:** Define test/evidence mapping.

### REQ-LCP-013 — Reality-before-model evaluation sequence
Constitutional evaluation shall follow: Physical Reality -> Raw Data Acquisition -> Source Integrity Assessment -> Measurement Quality Assessment -> Evidence Evaluation -> Model Evaluation -> Constitutional Review.  
**P1** — EXTRACTED/REFINED.  
**Action:** Compare with runtime and validation architecture.

### REQ-LCP-014 — Uncertainty at every evaluation stage
Each stage of the constitutional evaluation sequence shall acknowledge associated uncertainty; increasing uncertainty shall reduce constitutional confidence accordingly.  
**P1** — EXTRACTED.  
**Action:** Map to confidence/provenance implementation.

### REQ-LCP-015 — Model/reality disagreement escalation
Validated significant disagreement between physical reality and an engineering model shall trigger constitutional review.  
**P1** — EXTRACTED.  
**Action:** Identify executable trigger or mark implementation gap.

### REQ-LCP-016 — Balanced optimization criteria
Engineering recommendations shall, where applicable, consider safety, benefit, adverse consequences, environmental impact, energy, resources, cost, maintainability, reliability and long-term sustainability rather than effectiveness alone.  
**P1** — EXTRACTED.  
**Action:** Map to optimization/recommendation layer.

### REQ-LCP-017 — Lowest constitutional risk among viable alternatives
When multiple alternatives satisfy the intended objective, LAT shall prefer the alternative with the lowest overall constitutional risk while preserving greatest long-term benefit.  
**P1** — EXTRACTED.  
**Action:** Formalize decision criterion; implementation mapping pending.

### REQ-LCP-018 — Safe Operating State on insufficient confidence
When confidence is insufficient for autonomous operation, the affected system shall transition to a constitutionally defined Safe Operating State until reliable evaluation becomes possible.  
**P1** — EXTRACTED/REFINED.  
**Action:** Map to safety barrier/control and identify system-specific safe-state definitions.

### REQ-LCP-019 — Constitutional review before official assembly
Each LCP Part shall pass Technical, Constitutional, Terminology, LCDF Compliance, Cross-Reference, Amendment Verification and Draft Approval review before the official constitutional edition is assembled.  
**P1/P3** — EXTRACTED.  
**Action:** Preserve as document-governance requirement, not runtime requirement.

### REQ-LCP-020 — Constitutional ratification is bounded
Ratification confirms constitutional validity of document structure, authority and governance at adoption time; it does not permanently certify engineering, scientific or implementation correctness.  
**P1** — EXTRACTED.  
**Action:** Ensure status semantics distinguish document ratification from scientific validity.

### REQ-LCP-021 — Constitutional amendment package traceability
Every integrated constitutional amendment shall retain its amendment identifier and remain traceable through the constitutional revision history.  
**P1/P3** — EXTRACTED.  
**Action:** Map CAP/CA records.

### REQ-LCP-022 — Right to abstain
The constitutional framework shall permit LAT to abstain from producing a recommendation when evidence, applicability or confidence is insufficient, rather than manufacture certainty.  
**P1** — EXTRACTED from CP-13 introduction; implementation mapping pending.

### REQ-LCP-023 — Constitutional integrity preservation
Constitutional integrity shall be treated as an independent constitutional obligation, not merely as a software correctness property.  
**P1** — EXTRACTED; overlaps CIS/CCR but remains LCP authority.

---

# 3. LIB-CON-001 / LIB-CON-004 — Constitution and Living Constitution

### REQ-CON-008 — Model identification on every calculated result
Every calculated result shall identify the model from which it originated and distinguish measured, estimated and predicted values. Predictions shall never be presented as observations.  
**P1** — REFINED from v0.2 traceability requirement.

### REQ-CON-009 — Assumption disclosure
Every engineering conclusion shall declare relevant assumptions, their validity range and the impact if they fail. Hidden assumptions are prohibited.  
**P1** — REFINED.

### REQ-CON-010 — Boundary respect / extrapolation control
Models shall not be applied outside validated boundaries without increased uncertainty, additional verification or refusal of recommendation. Extrapolation without declared uncertainty is forbidden.  
**P1** — REFINED.

### REQ-CON-011 — Causality protection
A causal conclusion shall identify the proposed cause, supporting evidence and alternative explanations considered. Statistical relationship alone is insufficient proof of causation.  
**P1** — NEW atomic requirement.

### REQ-CON-012 — Confidence reporting
Every significant recommendation shall include confidence information reflecting evidence quality, model validity and uncertainty; artificial certainty is prohibited.  
**P1** — REFINED.

### REQ-CON-013 — Independent verification for critical conclusions
Critical conclusions shall use independent verification whenever possible; a single unverified pathway shall not determine critical decisions.  
**P1** — REFINED.

### REQ-CON-014 — Conflict handling
When information sources disagree, LAT shall detect the conflict, identify possible causes, perform additional verification and report remaining uncertainty; contradictions shall not be silently removed.  
**P1** — NEW atomic requirement.

### REQ-CON-015 — Historical continuity of changes
Every knowledge change shall preserve previous state, reason/evidence supporting the change and responsible revision. Previous knowledge states shall not be deleted or rewritten.  
**P1** — REFINED.

### REQ-CON-016 — Data authenticity
Recorded information shall preserve origin, timestamps, modification history and verification status; historical records shall not be modified to fit new conclusions.  
**P1** — REFINED; cryptographic mechanism remains separate P1-03 closure.

### REQ-CON-017 — Temporal validity
LAT shall evaluate information relevance according to age, environmental changes and sensor condition; expired information shall not be treated as current reality.  
**P1** — NEW atomic requirement.

### REQ-CON-018 — Degradation awareness
LAT shall account for sensor ageing, calibration changes and data deterioration; past performance shall not automatically represent present capability.  
**P1** — NEW atomic requirement.

### REQ-CON-019 — Anomaly evaluation
Unexpected values shall trigger evaluation rather than immediate rejection; anomaly handling shall consider noise, model limitations and real physical events.  
**P1** — NEW atomic requirement.

### REQ-CON-020 — Safe recommendation
Before issuing recommendations LAT shall consider safety impact, uncertainty and possible failure modes; optimization shall never override safety.  
**P1** — REFINED.

### REQ-CON-021 — Human-readable recommendation
Significant recommendations shall communicate what is suggested, why, confidence/uncertainty and possible risks in a form understandable to responsible humans. LAT shall not require blind trust.  
**P1** — NEW atomic requirement.

### REQ-CON-022 — Controlled failure behaviour
Subsystem failure shall not result in uncontrolled behaviour. When confidence falls below acceptable limits, LAT shall reduce activity, enter an appropriate safe state, preserve information and notify responsible entities.  
**P1** — REFINED; runtime mapping pending.

### REQ-CON-023 — Technology-independent constitutional rules
Operational rules shall remain valid across classical, distributed and future architectures; no technology may redefine constitutional principles.  
**P1/P2** — REFINED.

### REQ-CON-024 — Direction preservation
LAT's primary direction shall remain reality -> evidence/knowledge -> responsible engineering decision; increased computational power shall not automatically increase authority.  
**P1** — REFINED.

---

# 4. LIB-COM / LIB-UJ — Constitutional Object Meta-Model

Source: `LIB-CES-001` embedded constitutional core and `LAT USTAVNA JEZGRA A1 KOMPLET.docx`.

### REQ-COM-001 — Common constitutional meta-model
Every Constitutional Object shall conform to one common constitutional meta-model.  
**P1** — EXTRACTED.

### REQ-COM-002 — Permanent non-reassigned identity
Every Constitutional Object shall possess a permanent identifier that is never reassigned; versions do not change identity.  
**P1** — REFINED.

### REQ-COM-003 — Explicit constitutional ownership
Every Constitutional Object shall identify constitutional authority, responsible authority and constitutional owner.  
**P1** — NEW atomic requirement.

### REQ-COM-004 — Complete lifecycle metadata
Every Constitutional Object shall preserve current status, previous status and lifecycle history.  
**P1** — NEW atomic requirement.

### REQ-COM-005 — Validity interval
Constitutional Objects shall support validity information including valid-from/valid-until and creation/modification/ratification timestamps where applicable.  
**P1** — NEW atomic requirement.

### REQ-COM-006 — Explicit object relationships
Every constitutional relationship shall be explicit, typed, uniquely identifiable, machine-referenceable and constitutionally meaningful.  
**P1** — REFINED.

### REQ-COM-007 — Generic lifecycle
Constitutional Objects shall follow the generic lifecycle Draft -> Reviewed -> Validated -> Active -> Revised -> Archived unless a constitutionally authorized specialization applies.  
**P1** — REFINED.

### REQ-COM-008 — Backward-compatible extensions
Extensions to COM shall remain backward compatible, shall not redefine inherited properties and shall remain constitutionally traceable.  
**P2** — NEW atomic requirement.

### REQ-COM-009 — Machine-referenceability as compliance criterion
A Constitutional Object is compliant only if it has permanent identity, lifecycle compliance, authority identification, traceability, historical revision preservation and machine referenceability.  
**P1** — EXTRACTED.

---

# 5. LIB-CEC-001 — Constitutional Evidence Chain

### REQ-CEC-001 — No constitutionally valid conclusion before evidence evaluation
Engineering conclusions shall not precede constitutional evaluation of supporting evidence; recommendations require constitutionally sufficient evidence.  
**P1** — REFINED.

### REQ-CEC-002 — Evidence cannot be an undocumented dependency
Every constitutional evidence object shall remain identifiable, reviewable and traceable.  
**P1** — NEW atomic requirement.

### REQ-CEC-003 — Evidence quality before quantity
Evidence value shall depend on demonstrated quality, assessed against defined criteria, rather than evidence count.  
**P1** — NEW atomic requirement.

### REQ-CEC-004 — Evidence independence
Where reasonably achievable, conclusions shall rely on multiple independent lines of evidence; independence shall be demonstrated or explicitly assessed.  
**P1** — REFINED.

### REQ-CEC-005 — Evidence sufficiency is conclusion-specific
Evidence shall be assessed according to its ability to support the specific conclusion; only constitutionally relevant evidence contributes to constitutional confidence.  
**P1** — NEW atomic requirement.

### REQ-CEC-006 — Evidence identity survives modification
Evidence shall preserve constitutional identity throughout its lifecycle; modification shall not destroy historical traceability.  
**P1** — REFINED.

### REQ-CEC-007 — Absence of evidence handling
Absence of evidence shall not be interpreted as evidence of absence; unavailable evidence and uncertainty shall remain explicitly visible.  
**P1** — NEW atomic requirement.

### REQ-CEC-008 — Evidence validity independent of institutional authority
Evidence validity shall not depend on vendor, database, language, organization, hardware platform or individual contributor. Institutional authority may strengthen confidence but cannot replace evidence evaluation.  
**P1** — NEW atomic requirement.

### REQ-CEC-009 — Evidence lifecycle preservation
Evidence shall pass the defined lifecycle: source -> registration -> quality assessment -> classification -> usage -> traceability -> preservation -> review -> evolution, while preserving historical states.  
**P1/P3** — EXTRACTED.

---

# 6. LIB-CFR-001 — Constitutional Flow Registry

### REQ-CFR-001 — Authorized information flows only
Information may move only through constitutionally defined and authorized flows; unauthorized flows are prohibited.  
**P1** — NEW atomic requirement.

### REQ-CFR-002 — Constitutional Gate enforcement
Every constitutional information flow shall pass through Constitutional Gate checks for sender identity, receiver identity, permitted flow, authorization level and event recording. No flow may bypass the Gate.  
**P1** — NEW atomic requirement.

### REQ-CFR-003 — Flow reconstructability
Every flow shall permit reconstruction of source, destination, time, exchange reason and constitutional rules used.  
**P1** — REFINED.

### REQ-CFR-004 — Minimum necessary information
A flow shall carry only information necessary to perform the authorized constitutional responsibility; modules shall see only constitutionally permitted information.  
**P1** — NEW atomic requirement.

### REQ-CFR-005 — Semantic integrity through transfer
Information transfer shall not change information meaning; every modification shall constitute a new constitutional event.  
**P1** — REFINED.

### REQ-CFR-006 — Flow explainability
Every flow shall be explainable in terms of why it exists, which constitutional principle permits it, what function it serves and what consequences it has.  
**P1** — NEW atomic requirement.

### REQ-CFR-007 — Controlled flow evolution
New flows may be introduced only through a constitutional process; replaced flows retain permanent history.  
**P1/P2** — NEW atomic requirement.

### REQ-CFR-008 — Flow lifecycle and state control
Flows shall pass Proposal -> Constitutional Review -> Approval -> Registration -> Operational Use -> Monitoring -> Audit -> Evolution/Retirement and use controlled states such as Proposed, Under Review, Approved, Active, Suspended, Superseded, Retired and Archived.  
**P1/P3** — EXTRACTED.

---

# 7. LIB-CDR-001 — Constitutional Directory Registry

### REQ-CDR-001 — Constitutional directory identity
Every constitutional directory shall have a unique identifier, name, constitutional purpose, responsible constitutional unit and defined usage rules.  
**P1** — NEW atomic requirement.

### REQ-CDR-002 — Single primary responsibility
Each directory shall have one primary constitutional responsibility even if multiple modules consume its information.  
**P1** — NEW atomic requirement.

### REQ-CDR-003 — Directory classification
Every directory shall belong to a constitutionally defined category; detailed classification is delegated to derived documents.  
**P2** — EXTRACTED.

### REQ-CDR-004 — Information origin and history
For every information object it shall be possible to determine source, creation time, originating constitutional directory and change history.  
**P1** — REFINED.

### REQ-CDR-005 — Directory access is externally governed
Directories shall not define their own access rules; access shall be determined by constitutional rules through Constitutional Gate.  
**P1** — NEW atomic requirement.

### REQ-CDR-006 — Directory relationships are documented
All constitutional relationships between directories shall be explicitly documented and traceable.  
**P1/P2** — NEW atomic requirement.

### REQ-CDR-007 — Directory deletion prohibition
Directories shall not be deleted; they may be superseded while history is permanently preserved.  
**P1** — NEW atomic requirement.

### REQ-CDR-008 — Directory lifecycle
Directory lifecycle shall follow Proposal -> Review -> Approval -> Registration -> Operational Use -> Monitoring -> Constitutional Revision -> Superseded/Active Archive.  
**P2/P3** — EXTRACTED.

---

# 8. LIB-CIT-001 — Constitutional Information Topology / Traceability

### REQ-CIT-001 — Closed constitutional information loop
The official flow shall close the loop from Physical Reality through Observation, Evidence, Assumptions, Model Evaluation, Engineering Conclusion, Recommendation, Explanation, Decision, Implementation, Observed Reality and Constitutional Audit back to Observation.  
**P1** — REFINED; implementation mapping pending.

### REQ-CIT-002 — Mandatory constitutional information-object metadata
Every constitutional information object shall include Constitutional Identifier, Global UUID, Semantic Identifier, Version, Status, Provenance, Responsible Authority, related objects, timestamp, validity interval, confidence where applicable and references.  
**P1** — NEW atomic requirement.

### REQ-CIT-003 — Relationship semantic uniqueness
Every constitutional relationship shall have one explicit semantic meaning; additional relationship types require COO-controlled introduction.  
**P1** — REFINED.

### REQ-CIT-004 — Transformation record completeness
Every Constitutional Transformation shall identify transformation ID, source objects, target objects, transformation type, responsible authority, reasoning method, timestamp, version and traceability reference.  
**P1** — NEW atomic requirement.

### REQ-CIT-005 — Confidence reconstructability
Whenever confidence is assigned, CIT shall preserve confidence value, method, source, version and supporting constitutional objects so confidence can be independently reconstructed.  
**P1** — REFINED.

### REQ-CIT-006 — Explanation completeness
A constitutional explanation shall reference supporting evidence, assumptions, engineering conclusions, recommendations, decisions and constitutional transformations; failure to produce required explanation shall reduce confidence and be explicitly reported.  
**P1** — REFINED.

### REQ-CIT-007 — Integrity violation criteria
Loss of traceability, unknown provenance, missing transformations, missing mandatory relationships or inability to reconstruct constitutional reasoning constitute Constitutional Integrity Violations with defined severity levels.  
**P1** — NEW atomic requirement.

### REQ-CIT-008 — Separation of ownership
CIT exclusively owns constitutional traceability, reconstructability, explainability, information relationships, transformations and information integrity; it shall not redefine evidence, assumptions, COM, COO, consistency rules or decisions owned by other constitutional documents.  
**P1/P2** — NEW boundary requirement.

---

# 9. LIB-CCR-001 — Constitutional Consistency Rules

### REQ-CCR-001 — Universal consistency
Every Constitutional Object shall remain internally and externally consistent with all applicable constitutional documents.  
**P1** — REFINED.

### REQ-CCR-002 — Referential integrity
Every mandatory constitutional reference shall resolve to one valid Constitutional Object; broken or missing mandatory references are prohibited.  
**P1** — NEW atomic requirement.

### REQ-CCR-003 — Machine-verifiable consistency
Every constitutional consistency rule shall be machine-verifiable and constitutionally traceable.  
**P1** — NEW atomic requirement.

### REQ-CCR-004 — Recommendation/evidence/dependency chain
Recommendations shall reference CECN and explanation; CECN shall reference required evidence, assumptions and models; assumptions shall be registered in CAR; evidence shall be registered in CEC; decisions shall reference recommendations.  
**P1** — REFINED.

### REQ-CCR-005 — One active version
Only one Active version of the same Constitutional Object may exist simultaneously.  
**P1** — NEW atomic requirement.

### REQ-CCR-006 — Archived/revision integrity
Archived objects shall not directly return to Draft; historical revisions remain immutable; superseded versions remain traceable.  
**P1** — NEW atomic requirement.

### REQ-CCR-007 — Explicit dependencies
Required dependencies must resolve; supporting dependencies cannot replace required dependencies; implicit dependency inheritance is prohibited; circular dependencies require explicit constitutional approval.  
**P1** — NEW atomic requirement.

### REQ-CCR-008 — Confidence bounded by weakest indispensable dependency
Engineering confidence shall not exceed the constitutionally justified confidence supported by its weakest indispensable dependency unless additional independent evidence demonstrably increases overall confidence.  
**P1** — REFINED.

### REQ-CCR-009 — Reproducible confidence
Confidence propagation, sources and calculations shall remain traceable and reproducible.  
**P1** — NEW atomic requirement.

### REQ-CCR-010 — Integrity violation definition
Missing mandatory objects/references, lifecycle violations, ambiguity, semantic conflict, historical modification or incomplete traceability shall constitute a Constitutional Integrity Violation.  
**P1** — NEW atomic requirement.

---

# 10. LIB-CIS-001 — Constitutional Immune System

### REQ-CIS-001 — Integrity before availability
Constitutional integrity shall always take precedence over system availability.  
**P1** — NEW atomic requirement.

### REQ-CIS-002 — Safe Constitutional Mode
If constitutional integrity cannot be verified, LAT shall immediately enter Safe Constitutional Mode.  
**P1** — NEW atomic requirement.

### REQ-CIS-003 — Verified recovery before resumption
Recovery shall restore verified constitutional integrity before normal operation resumes. No state transition may bypass recovery.  
**P1** — NEW atomic requirement.

### REQ-CIS-004 — Immune-action traceability
Every immune action shall remain constitutionally traceable through CIT.  
**P1** — NEW atomic requirement.

### REQ-CIS-005 — Permanent reserve cell
A verified Reserve Cell shall always exist before failure and shall not be created only after failure.  
**P1/P4** — EXTRACTED; implementation architecture pending.

### REQ-CIS-006 — Immutable constitutional memory
Memory Cell shall preserve historical integrity, immune events, recovery history and constitutional evidence without historical mutation.  
**P1** — NEW atomic requirement.

### REQ-CIS-007 — Sentinel state restriction
Constitutional Sentinel output shall be limited to VERIFIED, DEGRADED, FAILED and UNKNOWN states.  
**P1** — EXTRACTED; implementation mapping pending.

### REQ-CIS-008 — Immune response sequence
On constitutional anomaly: Detect -> Isolate -> Preserve Evidence -> Activate Reserve Cell -> Validate -> Resume only if VERIFIED.  
**P1** — NEW atomic requirement.

### REQ-CIS-009 — Constitutional homeostasis
Continuous integrity monitoring shall cover identity consistency, traceability completeness, semantic consistency, lifecycle correctness, dependency integrity and confidence consistency; loss of equilibrium initiates immune response.  
**P1** — NEW atomic requirement.

### REQ-CIS-010 — No self-authorized constitutional mutation
CIS shall never modify COM, redefine COO, override CCR, bypass CTM, create constitutional evidence/assumptions/decisions or alter their authority.  
**P1** — NEW boundary requirement.

### REQ-CIS-011 — Deterministic immune behaviour
Every immune action shall be deterministic, traceable, reproducible, machine-verifiable and constitutionally explainable.  
**P1** — NEW atomic requirement.

### REQ-CIS-012 — Recovery uses only verified prior state
Recovery shall never reconstruct unknown constitutional state; it may activate only previously verified constitutional state.  
**P1** — NEW atomic requirement.

---

# 11. LIB-SMC-001 — SMC Constitutional Boundary & Replacement Contract

### REQ-SMC-005 — Decision provenance completeness
Every significant SMC-ROM selection, rejection, replacement, retirement or supersession shall create a decision record containing applicable identity, session, model/version, previous/resulting state, reason, evidence, applicability, contract, supersession and selector-version information.  
**P1** — REFINED.

### REQ-SMC-006 — Independent selector decision store
SMC-ROM decision history shall be independent from active execution state, append-oriented, historically preservative, readable by LAT-ROM, inaccessible to individual SMC models and protected from silent modification.  
**P1** — NEW atomic requirement.

### REQ-SMC-007 — Operational state/history separation
Operational cleanup or bench eviction shall never imply historical deletion; operational state and historical record are distinct.  
**P1** — REFINED.

### REQ-SMC-008 — Bounded bench
SMC-ROM shall maintain a bounded operational bench; current source explicitly specifies `BENCH_CAPACITY = 10`.  
**P2** — EXTRACTED.  
**Action:** Verify whether this is architectural requirement or implementation-specific parameter.

### REQ-SMC-009 — FIFO bench eviction
When the operational bench is full, oldest operational bench entry is evicted using FIFO; eviction does not delete provenance/history.  
**P2** — EXTRACTED.

### REQ-SMC-010 — Invalid model cannot continue effective execution
A model invalid for the current execution context shall not continue producing effective downstream results.  
**P1** — NEW atomic requirement.

### REQ-SMC-011 — Restart semantics
Model invalidation shall not silently restart the application. After a human-directed restart, SMC-ROM reconstructs permitted operational state using preserved history, current registry/applicability/contracts/evidence/versions.  
**P2** — NEW atomic requirement.

### REQ-SMC-012 — Selector replacement authority does not inherit automatically
Replacement of SMC-ROM shall preserve predecessor history, but the replacement selector does not receive authority merely because the previous selector possessed it; authority derives from the constitutional contract.  
**P1** — NEW boundary requirement.

### REQ-SMC-013 — Historical validity != current applicability != scientific truth
Replacement/rejection/supersession shall not be interpreted automatically as proof that the historical model or decision was scientifically wrong.  
**P1** — REFINED.

### REQ-SMC-014 — SMC authority boundary
No SMC component may modify constitutional axioms, redefine LAT-ROM authority, erase evidence, hide violations, declare its own analysis unquestionable, bypass human authority or silently expand authority.  
**P1** — REFINED.

### REQ-SMC-015 — SMC-ROM selection boundary
SMC-ROM may select/reject/replace applicable scientific models and maintain bounded state, but shall not redefine scientific truth, constitutional axioms, LAT-ROM authority or human decision authority.  
**P1/P2** — NEW atomic boundary.

---

# 12. LIB-LCDF / constitutional document framework

### REQ-LCDF-001 — Mandatory document identity header
Every constitutional document shall contain mandatory identity/authority metadata including identifier, title, abbreviation, revision, status, classification, layer, authority, effective/ratification dates, supersession, related documents, compatibility, language, owner and maintaining authority.  
**P1/P3** — REFINED.

### REQ-LCDF-002 — One primary constitutional purpose
Every constitutional document shall define one primary constitutional purpose and one primary responsibility unless a justified document-specific exception applies.  
**P1/P2** — NEW atomic requirement.

### REQ-LCDF-003 — Standard constitutional document structure
Constitutional documents shall follow the standard sequence: Header, Purpose, Responsibility, Scope, Definitions, Principles, Object Definitions, Lifecycle, Rules, Dependencies, Traceability, Governance, Review and Ratification, with justified exceptions only.  
**P2/P3** — EXTRACTED.

### REQ-LCDF-004 — Constitutional document quality
Every document shall be complete, consistent, unambiguous, traceable, version controlled, machine-referenceable, human readable and constitutionally reviewable.  
**P1/P3** — NEW atomic requirement.

### REQ-LCDF-005 — No ratification without constitutional compliance
A constitutional document shall not be ratifiable unless it demonstrably conforms to LCP, COM, COO, CCR and LCDF requirements.  
**P1/P3** — REFINED.

### REQ-LCDF-006 — Amendment history preservation
LCDF changes shall follow LCP amendment procedures, classify change type and preserve complete revision history.  
**P1/P3** — NEW atomic requirement.

### REQ-LCDF-007 — Ratification record completeness
Ratification records shall include identifier, designation, revision, ratification findings, effective date, supersession, authority and future digital-signature field where applicable.  
**P3/P4** — EXTRACTED; digital signature is future implementation, not current capability.

---

# 13. Cross-document constitutional architecture requirements

### REQ-XARCH-001 — Separation of constitutional responsibilities
LCP, COM, COO, CCR, CEC, CAR, CIT, CDR, CFR, CDR-directory and CIS responsibilities shall remain distinct; one document shall not silently redefine another document's owned semantics or authority.  
**P1/P2** — REFINED.

### REQ-XARCH-002 — Constitutional objects follow the same identity foundation
Evidence, assumptions, conclusions, recommendations, explanations and decisions shall inherit the common constitutional object foundation rather than invent independent identity/lifecycle semantics.  
**P1** — REFINED.

### REQ-XARCH-003 — Constitutional loop must be reconstructable
A recommendation and subsequent decision must be reconstructable from reality/observation through evidence, assumptions, model evaluation, conclusion, explanation and implementation/audit feedback.  
**P1** — REFINED.

### REQ-XARCH-004 — Lower layers cannot bypass constitutional gates
Engineering, scientific, software and implementation layers may implement constitutional obligations but cannot bypass constitutional identity, evidence, authority, traceability, consistency or safety controls.  
**P1** — REFINED.

### REQ-XARCH-005 — Constitutional evolution must preserve history
Future scientific, software and architectural evolution is permitted only through constitutionally defined change processes and shall preserve previous states, decisions and evidence.  
**P1/P2** — REFINED.

---

# 14. Revision/conflict observations discovered in second pass

1. **LCP revision divergence:** Library contains LCP Rev A1.0 / earlier constitutional material, `LAT LCP Constitutional Principles Rev D1.2`, and CAP-001 amendments. These are not to be merged by assumption. The register must preserve revision lineage and identify the authoritative target revision.
2. **CIT naming divergence:** Some sources call the function `Constitutional Information Traceability`, others `Constitutional Information Topology`. The underlying responsibility is similar, but identity must be reconciled before final documentation.
3. **CDR naming collision:** `Constitutional Directory Registry (CDR)` and `Constitutional Decision Record (CDR)` appear in different Library sources using the same abbreviation. This is a **P1 identity conflict** and must not be silently resolved by renaming during reconstruction.
4. **CFR/CIT/CEC derived-document references:** Several derived specifications are explicitly marked `Reserved` and therefore must not be represented as implemented documents merely because their parent framework defines them.
5. **CIS status:** CIS is explicitly a Constitutional Draft in the located source. Its required behaviour is therefore an extracted constitutional requirement, not evidence that the current GitHub runtime implements a CIS.
6. **SMC bench capacity:** `BENCH_CAPACITY = 10` is explicitly stated in the SMC contract. It must be classified as a normative architectural parameter versus an implementation detail before closure.
7. **Ratified vs scientifically valid:** Several constitutional documents explicitly distinguish document ratification from permanent correctness of engineering/scientific implementations. The reconstruction register must preserve that distinction.
8. **Constitutional hierarchy wording:** Some older sources use Reality -> Evidence -> Knowledge -> Principles -> Models -> Recommendations -> Human Decisions, while other baseline material uses Identity -> Reality -> Nature -> Measurement -> Time -> Knowledge -> Evidence -> Causality -> Boundaries -> Balance -> Direction -> Recommendation -> Human Responsibility -> Uncertainty -> Falsifiability -> Traceability -> Safety -> Integrity. This is a **P1 hierarchy reconciliation item**, not an invitation to choose one by preference.

---

# 15. Second-pass closure status

**Second pass result:** substantial additional original requirements extracted.

**Not closed:**
- source/revision authority;
- abbreviation collisions;
- complete Library inventory;
- requirement-to-GitHub implementation mapping;
- requirement-to-test mapping;
- constitutional hierarchy reconciliation;
- provenance/cryptographic integrity implementation comparison;
- runtime execution authority;
- final P1-P4 closure.

**Next mandatory step:** merge these second-pass requirement records into the master `RECONSTRUCTION_REGISTER`, deduplicate/refine IDs, then perform **REQ -> IMPL -> TEST -> COMMIT -> STATUS -> ACTION** mapping against the canonical GitHub snapshot.

**Final AILCS documentation remains BLOCKED until the register is closed.**
