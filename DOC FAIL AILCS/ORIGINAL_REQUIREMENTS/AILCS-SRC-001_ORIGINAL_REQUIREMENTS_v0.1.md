# AILCS-SRC-001 — ORIGINAL REQUIREMENTS v0.1

**Source-ID:** `AILCS-SRC-001`  
**Original source:** `Tehnička arhitektura AI obrazovne platforme.png`  
**Source type:** IMAGE  
**Source location:** ChatGPT Library  
**Evidence status:** SOURCE-EXTRACTED  
**Normative status:** NOT YET FORMALLY APPROVED  
**Project boundary:** AILCS only

## 1. Purpose

This document records requirements and architecture statements that can be directly extracted from the identified AILCS source image. It is an evidence reconstruction record, not a final specification.

Where the source gives an explicit component, actor, interface, flow, security principle, technology example, or service function, it is recorded below. No requirement is promoted to a final normative requirement merely because it appears in the diagram.

## 2. Actors and user-facing capabilities visible in the source

### OR-001 — Polaznici / učenici
The platform provides for learners/users:
- registration;
- learning and training;
- tests and assignments;
- progress tracking.

### OR-002 — Nastavnici / instruktori
The platform provides for teachers/instructors:
- content creation;
- learner monitoring;
- grading;
- communication.

### OR-003 — Stručni recenzenti
The platform supports:
- professional review;
- program validation;
- content approval.

### OR-004 — Naučni recenzenti
The platform supports:
- scientific validation;
- source verification;
- methodological verification.

### OR-005 — Poslodavci
The platform supports:
- competency review;
- employment-related use;
- employer assessment after three months;
- feedback.

### OR-006 — Ispitne institucije
The platform supports:
- final professional examination;
- certificate issuance;
- reporting.

### OR-007 — Administratori
The platform supports:
- system administration;
- management of users and roles;
- configuration.

### OR-008 — Državne institucije
The platform supports:
- oversight;
- reports and statistics;
- policies and standards.

## 3. Presentation layer

### OR-009 — User interface layer
The source defines a `PRESENTATION LAYER (Korisnički interfejsi)` as the user-facing layer of the platform.

## 4. API Gateway & Edge Layer

### OR-010 — API Gateway
The source defines an API Gateway providing:
- routing;
- rate limiting;
- throttling.

### OR-011 — Authentication and authorization
The source defines an Authentication & Authorization Service (IAM) with:
- OAuth2 / OpenID Connect;
- RBAC (Role Based Access Control);
- MFA.

### OR-012 — Request validation and edge protection
The source defines request validation controls including:
- schema validation;
- input sanitization;
- DDoS protection.

## 5. Application / Service Layer

### OR-013 — User and Role Service
The source defines a service for:
- user management;
- role management;
- organization management.

### OR-014 — Curriculum Service
The source defines curriculum functionality for:
- curricula;
- modules;
- programs;
- versions.

### OR-015 — Content Service
The source defines content handling for:
- text;
- video;
- files;
- simulations.

### OR-016 — Assessment Service
The source defines assessment functionality for:
- tests;
- assignments;
- rubrics;
- automated assessment.

### OR-017 — Certification Service
The source defines certification functionality for:
- certificates;
- badges;
- verification/validation.

### OR-018 — AI Tutor Service
The source defines AI tutoring functionality for:
- adaptive teaching;
- personalized recommendations.

### OR-019 — Competency Assessment Service
The source defines competency assessment functionality for:
- initial assessment;
- skills assessment;
- competency mapping.

### OR-020 — Learning Path Engine
The source defines generation of an individual learning path.

### OR-021 — Simulation & Lab Service
The source defines:
- simulations;
- virtual laboratories.

### OR-022 — Safety Gate Service
The source defines:
- risk assessment;
- safety rules;
- safety limitations/constraints.

### OR-023 — Analytics & Reporting Service
The source defines:
- reports;
- KPIs;
- statistics;
- dashboards.

### OR-024 — Employer Review Service
The source defines:
- employer assessment after three months;
- feedback.

### OR-025 — Review & Approval Service
The source defines a workflow for:
- review;
- content approval.

### OR-026 — Notification Service
The source defines notifications through:
- e-mail;
- SMS;
- in-app notifications;
- reminders.

### OR-027 — Audit & Trace Service
The source defines audit/trace functionality for:
- audit logs;
- activity traces;
- changes;
- versions.

### OR-028 — Workflow & Orchestration Engine
The source defines workflow orchestration for:
- learning;
- assessment;
- review;
- certification.

## 6. Integrations

### OR-029 — LMS / school-system integration
The source identifies integration with LMS / school systems and references:
- SCORM;
- LTI;
- xAPI.

### OR-030 — ERP / HR integration
The source identifies integration with ERP / HR systems for employer-related use.

### OR-031 — e-Government integration
The source identifies e-Government integration including:
- e-ID;
- electronic signatures;
- registries.

### OR-032 — Payment integration
The source identifies a Payment Gateway for online payment.

### OR-033 — Video conferencing integration
The source identifies video-conferencing integration and gives examples including Zoom, Jitsi and MS Teams.

### OR-034 — Email / SMS integration
The source identifies an Email / SMS Gateway.

### OR-035 — External AI service integration
The source identifies external AI services, including:
- LLM;
- NLP;
- speech services.

## 7. Data Layer

### OR-036 — User & Identity DB
The source defines a user and identity database and gives PostgreSQL as an example technology.

### OR-037 — Content DB
The source defines a content database and gives PostgreSQL as an example technology.

### OR-038 — Assessment DB
The source defines an assessment database and gives PostgreSQL as an example technology.

### OR-039 — Learning Analytics DB
The source defines a learning analytics database and gives TimescaleDB as an example technology.

### OR-040 — Document Storage
The source defines document/file storage and gives S3 / MinIO as examples.

### OR-041 — Audit Log DB
The source defines an audit-log database and gives Elasticsearch as an example.

### OR-042 — Cache
The source defines a cache layer and gives Redis as an example.

### OR-043 — Search Index
The source defines a search index and gives OpenSearch as an example.

### OR-044 — Data Warehouse
The source defines a data warehouse for analytics / BI.

## 8. Cross-cutting services

### OR-045 — Centralized logging
The source defines a Logging Service for centralized logs.

### OR-046 — Monitoring and alerting
The source defines Monitoring & Alerting and gives Prometheus and Grafana as examples.

### OR-047 — Backup and disaster recovery
The source defines Backup & Disaster Recovery including backup and replication.

### OR-048 — Configuration service
The source defines configuration handling including feature flags and configuration.

### OR-049 — CI/CD pipeline
The source defines a CI/CD pipeline and gives GitLab CI / Jenkins as examples.

### OR-050 — Secrets management
The source defines Secrets Management and gives Vault / KMS as examples.

## 9. AI / ML layer

### OR-051 — LLM service
The source defines an LLM Service for generation and explanations.

### OR-052 — NLP service
The source defines an NLP Service for language understanding.

### OR-053 — Recommendation engine
The source defines a Recommendation Engine for content recommendations.

### OR-054 — Model training pipeline
The source defines a Model Training Pipeline for model training and evaluation.

### OR-055 — Calibration engine
The source defines a Calibration Engine for calibration of AI assessments.

## 10. Data-flow example

### OR-056 — End-to-end learning-to-employment flow
The source shows the following example flow:

`Početna procjena → Personalizirani plan → Učenje & zadaci → Završna procjena (AI) → Stručni ispit (ljudski) → Zapošljavanje → Ocjena poslodavca → Povratna petlja`

The diagram also shows a feedback loop returning toward the learning process.

This is recorded as a source architecture flow; its final normative business-process definition remains pending.

## 11. Security principles visible in the source

### OR-057 — Encryption in transit
The source specifies encryption in transit using TLS 1.3.

### OR-058 — Encryption at rest
The source specifies encryption of stored data.

### OR-059 — Least privilege access control
The source specifies RBAC and least-privilege principles.

### OR-060 — Immutable audit trail
The source specifies an immutable audit trail.

### OR-061 — Regular security checks
The source specifies regular security checks.

### OR-062 — Regulatory / standards compliance
The source references compliance with GDPR and ISO 27001.

## 12. Technology stack examples

The source presents the following as an example technology stack, not as a formally frozen implementation decision:

- Frontend: React / Next.js
- Backend: Python (FastAPI) / Node.js
- DB: PostgreSQL, TimescaleDB
- Search: OpenSearch
- Cache: Redis
- Storage: S3 / MinIO
- AI: LLM, RAG, Vector DB (pgvector)
- Infrastructure: Docker, Kubernetes
- CI/CD: GitLab CI
- Monitoring: Prometheus + Grafana

These are therefore recorded as **technology examples from the source**, not yet as mandatory technology requirements.

## 13. Source-level architecture layers

The source identifies:

1. Presentation Layer
2. API Gateway & Edge Layer
3. Application / Service Layer
4. Data Layer
5. Cross-Cutting Services
6. AI / ML Layer

The AI / ML layer is shown as a distinct supporting layer associated with AI services and integrations.

## 14. Items deliberately NOT inferred

The following are not declared as original requirements from this source because the image alone does not establish them with sufficient specificity:

- exact legal status or institutional authority of each actor;
- final competency taxonomy;
- final certification legislation/procedure;
- exact API schemas;
- exact database schemas;
- exact data-retention periods;
- exact SLA/SLO targets;
- final cloud/on-premises deployment model;
- final choice among alternative technologies;
- detailed AI model governance policy;
- final P1–P4 classification;
- final module IDs M01–M11.

These may be developed later from other AILCS sources or as explicitly marked reconstruction/proposal items.

## 15. Extraction control

**Original source statements extracted:** 62 numbered records  
**Source-derived technology examples:** recorded separately  
**New requirements invented:** 0  
**P1–P4 mapping:** pending  
**Normative approval:** pending

## 16. Next step

Compare `AILCS-SRC-001` against `AILCS-SRC-002` and the remaining verified AILCS sources. Duplicate requirements should be consolidated only after preserving their individual SOURCE-ID provenance. Conflicts or differences between sources must be recorded rather than silently resolved.
