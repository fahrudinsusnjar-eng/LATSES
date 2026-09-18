# AILCS-SRC-008 — P1–P4 MAPPING v0.1

**SOURCE-ID:** `AILCS-SRC-008`  
**Original source:** `Cjelokupna arhitektura AILCS sistema.png`  
**Phase:** 2 — P1–P4 mapping  
**Project boundary:** AILCS only  
**Status:** MAPPING COMPLETE; CROSS-SOURCE VALIDATION PENDING

## P1–P4 control definitions

- **P1 — Izvor/identitet:** potvrđuje originalno postojanje stavke i njen SOURCE-ID/provenijenciju.
- **P2 — Zahtjev:** prenosi šta izvor stvarno navodi, bez dodavanja novog zahtjeva.
- **P3 — Usklađivanje:** određuje gdje stavka pripada u AILCS strukturi i s kojim komponentama je povezana. Ne koristi LAT/LATCES strukturu.
- **P4 — Verifikacija:** evidentira nivo potvrde; u ovoj fazi potvrda je samo source-level. Cross-source potvrda, konflikt, zamjena ili usvajanje ostaju za narednu fazu.

## Mapping register

| OR-ID | P1 — Izvor/identitet | P2 — Originalni zahtjev | P3 — AILCS usklađivanje | P4 — Verifikacija |
|---|---|---|---|---|
| OR-001 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | The source identifies AILCS and the M01–M11 architecture. | M01 + M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-002 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Users include citizens/participants, pupils/students, teachers/mentors, reviewers, examiners, employers, institutions and government analysts. | M01 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-003 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M02 Digital Channels include Web, Mobile, Teacher, Employer, Reviewer, Examiner, Institutional and Admin/Government portals. | M02 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-004 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Cross-cutting Security M03 includes authentication, authorization, MFA, RBAC/ABAC, access policies, encryption and audit. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-005 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | API Gateway M04 includes routing, rate limiting, validation, versions, logging and monitoring. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-006 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Observability includes monitoring, alerting, logging and tracing. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-007 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Identity Provider is shown as eIDAS-compatible with G2G/G2C and SSO. | M01 + M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-008 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Notification Service includes Email, SMS, In-App and Push. | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-009 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | File/Document Service supports document storage and versions. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-010 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Audit & Compliance includes an Audit Ledger and retention controls. | M03 + M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-011 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M01 is Identity, Users & Institutions. | M01 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-012 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M01 includes users, institutions/organizational units, roles/permissions, user–institution links and identity lifecycle. | M01 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-013 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M05 is Core Learning & Competency Services. | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-014 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M05 includes Competency, Learning, Assessment, Practical Training, Examination, Certification and Employer Feedback services. | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-015 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M06 is AI Intelligence Platform. | M06 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-016 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M06 includes AI Orchestrator, AI Tutor, AI Mentor, Adaptive Learning Engine, Retrieval/Knowledge Engine, Exercise Generator, AI Analytics and Model Abstraction Layer. | M06 + M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-017 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M07 is AI Safety & Human Oversight. | M07 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-018 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M07 includes risk classification, output validation, uncertainty/limitations, human escalation, unsafe-answer blocking and safety-decision audit. | M03 + M07 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-019 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M08 is Knowledge & Scientific Governance. | M08 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-020 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M08 includes source registration, scientific/professional/security review, licences/copyright, approval/versioning and Approved Knowledge Base. | M03 + M04 + M08 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-021 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M10 is Analytics, Labour Market & Policy Intelligence. | M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-022 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M10 includes competency/occupation analytics, shortage skills, program/institution performance, employability/outcomes, employer feedback, policy indicators, reports, predictions and trends. | M05 + M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-023 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M11 is Continuous Improvement & Calibration. | M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-024 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M11 compares AI/expert assessments and examinations/real outcomes. | M10 + M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-025 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M11 integrates employer feedback and detects deviation/drift. | M05 + M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-026 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M11 calibrates models/tests and supports program/standards review and change/version management. | M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-027 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M09 is Data & Evidence Platform. | M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-028 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | M09 includes Identity, Competency, Learning, Assessment, Certification, Knowledge, Vector DB, Object Storage and Immutable Audit Ledger stores. | M01 + M03 + M05 + M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-029 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Analytics Warehouse stores aggregated data, OLAP, reports and models. | M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-030 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Data Governance & Quality includes classification, ownership, quality, retention, backup/recovery, Privacy by Design and Data Lineage. | M03 + M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-031 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | External systems include education systems. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-032 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | External systems include labour-market systems. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-033 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | External systems include public registries/eID/qualifications. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-034 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | External systems include employer/HR systems and professional bodies. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-035 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | International integrations include EQF, Europass and e-Certificate. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-036 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Operational infrastructure includes Cloud/Data Center with high availability. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-037 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Infrastructure includes Docker/Kubernetes, CI/CD, monitoring/alerting, backup/DR and security operations/SOC. | M03 + M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-038 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Change & Release Management keeps changes under control. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-039 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Legal/governance framework includes BiH laws/regulations, policies/procedures, AI Governance Board, oversight/audit and responsible AI ethics. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-040 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | The source identifies nine main process flows. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-041 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Flow 1 is Registration & Identity (M01). | M01 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-042 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Flow 2 is Assessment & Profile (M05). | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-043 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Flow 3 is Learning & Interaction (M05 + M06). | M05 + M06 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-044 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Flow 4 is Assessment & Exam (M05). | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-045 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Flow 5 is Certification (M05). | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-046 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Flow 6 is Employment & Feedback (M05). | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-047 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Flow 7 is Analytics (M10). | M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-048 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Flow 8 is Calibration (M11). | M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-049 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Flow 9 is Program Improvement (M11 → M05/M06/M08). | M05 + M06 + M08 + M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-050 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Detailed process includes registration/identity, initial assessment/profile, personalized learning, assessment/exam, certification, employment confirmation, analytics, calibration and improvement. | M01 + M05 + M10 + M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-051 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Feedback loops connect later outcomes back to earlier stages. | M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-052 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | The legend distinguishes modules M01–M11, cross-cutting support, external integrations and the data layer. | M01 + M09 + M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-053 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | The legend distinguishes synchronous REST/HTTPS, asynchronous Event/Message and data flows. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-054 | AILCS-SRC-008 — Cjelokupna arhitektura AILCS sistema.png | Trust boundaries and security/database/service/user icons are explicitly represented. M01–M11 are recorded as source-visible architecture, not yet declared final canonical module definitions. P1–P4 mapping, conflict analysis and consolidation remain pending. LAT/LATCES/LATSES is strictly excluded. | M01 + M03 + M09 + M11 | SOURCE-EXTRACTED; cross-source verification pending |

## Phase-2 control result

- Original source provenance preserved: **YES**
- Original requirement wording preserved: **YES**
- AILCS structural mapping assigned: **YES**
- Cross-source duplicate/conflict resolution: **NOT YET**
- Status/action closure: **NOT YET**
- Reconstruction register closure: **NO**
- Final AILCS documentation: **NO**
