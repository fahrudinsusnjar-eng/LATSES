
# AILCS-SRC-008 — ORIGINAL REQUIREMENTS v0.1

**SOURCE-ID:** AILCS-SRC-008  
**Source:** `Cjelokupna arhitektura AILCS sistema.png`  
**Source type:** complete AILCS M01–M11 architecture  
**Library file:** `file_0000000086908210ba03dd4c4a0f06e3`  
**Status:** SOURCE EXTRACTED; P1–P4 PENDING; REGISTER OPEN

## Original source records

- OR-001 — The source identifies AILCS and the M01–M11 architecture.
- OR-002 — Users include citizens/participants, pupils/students, teachers/mentors, reviewers, examiners, employers, institutions and government analysts.
- OR-003 — M02 Digital Channels include Web, Mobile, Teacher, Employer, Reviewer, Examiner, Institutional and Admin/Government portals.
- OR-004 — Cross-cutting Security M03 includes authentication, authorization, MFA, RBAC/ABAC, access policies, encryption and audit.
- OR-005 — API Gateway M04 includes routing, rate limiting, validation, versions, logging and monitoring.
- OR-006 — Observability includes monitoring, alerting, logging and tracing.
- OR-007 — Identity Provider is shown as eIDAS-compatible with G2G/G2C and SSO.
- OR-008 — Notification Service includes Email, SMS, In-App and Push.
- OR-009 — File/Document Service supports document storage and versions.
- OR-010 — Audit & Compliance includes an Audit Ledger and retention controls.
- OR-011 — M01 is Identity, Users & Institutions.
- OR-012 — M01 includes users, institutions/organizational units, roles/permissions, user–institution links and identity lifecycle.
- OR-013 — M05 is Core Learning & Competency Services.
- OR-014 — M05 includes Competency, Learning, Assessment, Practical Training, Examination, Certification and Employer Feedback services.
- OR-015 — M06 is AI Intelligence Platform.
- OR-016 — M06 includes AI Orchestrator, AI Tutor, AI Mentor, Adaptive Learning Engine, Retrieval/Knowledge Engine, Exercise Generator, AI Analytics and Model Abstraction Layer.
- OR-017 — M07 is AI Safety & Human Oversight.
- OR-018 — M07 includes risk classification, output validation, uncertainty/limitations, human escalation, unsafe-answer blocking and safety-decision audit.
- OR-019 — M08 is Knowledge & Scientific Governance.
- OR-020 — M08 includes source registration, scientific/professional/security review, licences/copyright, approval/versioning and Approved Knowledge Base.
- OR-021 — M10 is Analytics, Labour Market & Policy Intelligence.
- OR-022 — M10 includes competency/occupation analytics, shortage skills, program/institution performance, employability/outcomes, employer feedback, policy indicators, reports, predictions and trends.
- OR-023 — M11 is Continuous Improvement & Calibration.
- OR-024 — M11 compares AI/expert assessments and examinations/real outcomes.
- OR-025 — M11 integrates employer feedback and detects deviation/drift.
- OR-026 — M11 calibrates models/tests and supports program/standards review and change/version management.
- OR-027 — M09 is Data & Evidence Platform.
- OR-028 — M09 includes Identity, Competency, Learning, Assessment, Certification, Knowledge, Vector DB, Object Storage and Immutable Audit Ledger stores.
- OR-029 — Analytics Warehouse stores aggregated data, OLAP, reports and models.
- OR-030 — Data Governance & Quality includes classification, ownership, quality, retention, backup/recovery, Privacy by Design and Data Lineage.
- OR-031 — External systems include education systems.
- OR-032 — External systems include labour-market systems.
- OR-033 — External systems include public registries/eID/qualifications.
- OR-034 — External systems include employer/HR systems and professional bodies.
- OR-035 — International integrations include EQF, Europass and e-Certificate.
- OR-036 — Operational infrastructure includes Cloud/Data Center with high availability.
- OR-037 — Infrastructure includes Docker/Kubernetes, CI/CD, monitoring/alerting, backup/DR and security operations/SOC.
- OR-038 — Change & Release Management keeps changes under control.
- OR-039 — Legal/governance framework includes BiH laws/regulations, policies/procedures, AI Governance Board, oversight/audit and responsible AI ethics.
- OR-040 — The source identifies nine main process flows.
- OR-041 — Flow 1 is Registration & Identity (M01).
- OR-042 — Flow 2 is Assessment & Profile (M05).
- OR-043 — Flow 3 is Learning & Interaction (M05 + M06).
- OR-044 — Flow 4 is Assessment & Exam (M05).
- OR-045 — Flow 5 is Certification (M05).
- OR-046 — Flow 6 is Employment & Feedback (M05).
- OR-047 — Flow 7 is Analytics (M10).
- OR-048 — Flow 8 is Calibration (M11).
- OR-049 — Flow 9 is Program Improvement (M11 → M05/M06/M08).
- OR-050 — Detailed process includes registration/identity, initial assessment/profile, personalized learning, assessment/exam, certification, employment confirmation, analytics, calibration and improvement.
- OR-051 — Feedback loops connect later outcomes back to earlier stages.
- OR-052 — The legend distinguishes modules M01–M11, cross-cutting support, external integrations and the data layer.
- OR-053 — The legend distinguishes synchronous REST/HTTPS, asynchronous Event/Message and data flows.
- OR-054 — Trust boundaries and security/database/service/user icons are explicitly represented.

## Boundary
M01–M11 are recorded as source-visible architecture, not yet declared final canonical module definitions. P1–P4 mapping, conflict analysis and consolidation remain pending. LAT/LATCES/LATSES is strictly excluded.
