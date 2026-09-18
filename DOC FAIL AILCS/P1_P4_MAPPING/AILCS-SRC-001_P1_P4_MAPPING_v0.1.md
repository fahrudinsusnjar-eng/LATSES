# AILCS-SRC-001 — P1–P4 MAPPING v0.1

**SOURCE-ID:** `AILCS-SRC-001`  
**Original source:** `Tehnička arhitektura AI obrazovne platforme.png`  
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
| OR-001 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Polaznici / učenici The platform provides for learners/users: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-002 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Nastavnici / instruktori The platform provides for teachers/instructors: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-003 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Stručni recenzenti The platform supports: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-004 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Naučni recenzenti The platform supports: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-005 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Poslodavci The platform supports: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-006 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Ispitne institucije The platform supports: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-007 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Administratori The platform supports: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-008 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Državne institucije The platform supports: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-009 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | User interface layer The source defines a `PRESENTATION LAYER (Korisnički interfejsi)` as the user-facing layer of the platform. | M02 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-010 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | API Gateway The source defines an API Gateway providing: | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-011 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Authentication and authorization The source defines an Authentication & Authorization Service (IAM) with: | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-012 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Request validation and edge protection The source defines request validation controls including: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-013 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | User and Role Service The source defines a service for: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-014 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Curriculum Service The source defines curriculum functionality for: | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-015 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Content Service The source defines content handling for: | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-016 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Assessment Service The source defines assessment functionality for: | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-017 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Certification Service The source defines certification functionality for: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-018 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | AI Tutor Service The source defines AI tutoring functionality for: | M06 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-019 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Competency Assessment Service The source defines competency assessment functionality for: | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-020 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Learning Path Engine The source defines generation of an individual learning path. | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-021 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Simulation & Lab Service The source defines: | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-022 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Safety Gate Service The source defines: | M07 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-023 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Analytics & Reporting Service The source defines: | M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-024 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Employer Review Service The source defines: | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-025 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Review & Approval Service The source defines a workflow for: | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-026 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Notification Service The source defines notifications through: | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-027 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Audit & Trace Service The source defines audit/trace functionality for: | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-028 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Workflow & Orchestration Engine The source defines workflow orchestration for: | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-029 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | LMS / school-system integration The source identifies integration with LMS / school systems and references: | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-030 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | ERP / HR integration The source identifies integration with ERP / HR systems for employer-related use. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-031 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | e-Government integration The source identifies e-Government integration including: | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-032 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Payment integration The source identifies a Payment Gateway for online payment. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-033 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Video conferencing integration The source identifies video-conferencing integration and gives examples including Zoom, Jitsi and MS Teams. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-034 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Email / SMS integration The source identifies an Email / SMS Gateway. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-035 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | External AI service integration The source identifies external AI services, including: | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-036 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | User & Identity DB The source defines a user and identity database and gives PostgreSQL as an example technology. | M01 + M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-037 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Content DB The source defines a content database and gives PostgreSQL as an example technology. | M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-038 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Assessment DB The source defines an assessment database and gives PostgreSQL as an example technology. | M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-039 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Learning Analytics DB The source defines a learning analytics database and gives TimescaleDB as an example technology. | M09 + M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-040 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Document Storage The source defines document/file storage and gives S3 / MinIO as examples. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-041 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Audit Log DB The source defines an audit-log database and gives Elasticsearch as an example. | M03 + M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-042 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Cache The source defines a cache layer and gives Redis as an example. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-043 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Search Index The source defines a search index and gives OpenSearch as an example. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-044 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Data Warehouse The source defines a data warehouse for analytics / BI. | M09 + M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-045 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Centralized logging The source defines a Logging Service for centralized logs. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-046 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Monitoring and alerting The source defines Monitoring & Alerting and gives Prometheus and Grafana as examples. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-047 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Backup and disaster recovery The source defines Backup & Disaster Recovery including backup and replication. | M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-048 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Configuration service The source defines configuration handling including feature flags and configuration. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-049 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | CI/CD pipeline The source defines a CI/CD pipeline and gives GitLab CI / Jenkins as examples. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-050 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Secrets management The source defines Secrets Management and gives Vault / KMS as examples. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-051 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | LLM service The source defines an LLM Service for generation and explanations. | M06 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-052 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | NLP service The source defines an NLP Service for language understanding. | M06 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-053 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Recommendation engine The source defines a Recommendation Engine for content recommendations. | M06 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-054 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Model training pipeline The source defines a Model Training Pipeline for model training and evaluation. | M06 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-055 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Calibration engine The source defines a Calibration Engine for calibration of AI assessments. | M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-056 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | End-to-end learning-to-employment flow The source shows the following example flow: The diagram also shows a feedback loop returning toward the learning process. | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-057 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Encryption in transit The source specifies encryption in transit using TLS 1.3. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-058 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Encryption at rest The source specifies encryption of stored data. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-059 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Least privilege access control The source specifies RBAC and least-privilege principles. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-060 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Immutable audit trail The source specifies an immutable audit trail. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-061 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Regular security checks The source specifies regular security checks. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-062 | AILCS-SRC-001 — Tehnička arhitektura AI obrazovne platforme.png | Regulatory / standards compliance The source references compliance with GDPR and ISO 27001. The source presents the following as an example technology stack, not as a formally frozen implementation decision: The source identifies: The AI / ML layer is shown as a distinct supporting layer associated with AI services and integrations. The following are not declared as original requirements from this source because the image alone does not establish them with sufficient specificity: | M03 | SOURCE-EXTRACTED; cross-source verification pending |

## Phase-2 control result

- Original source provenance preserved: **YES**
- Original requirement wording preserved: **YES**
- AILCS structural mapping assigned: **YES**
- Cross-source duplicate/conflict resolution: **NOT YET**
- Status/action closure: **NOT YET**
- Reconstruction register closure: **NO**
- Final AILCS documentation: **NO**
