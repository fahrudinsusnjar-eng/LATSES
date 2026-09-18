# AILCS-SRC-007 — P1–P4 MAPPING v0.1

**SOURCE-ID:** `AILCS-SRC-007`  
**Original source:** `Tehnička arhitektura AI platforme za učenje(1).png`  
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
| OR-001 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | The source identifies the BIH AI LEARNING & COMPETENCY SYSTEM (AILCS). | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-002 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Presentation layer includes responsive Web Portal. | M02 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-003 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Presentation layer includes Android/iOS mobile application. | M02 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-004 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Instructor, employer and admin portals are shown. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-005 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | API Portal/Developer Console is shown. | M02 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-006 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Learners include secondary-school students, university students, adults, unemployed and employees in further training. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-007 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Teachers/instructors support planning, progress monitoring, assessment and communication. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-008 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Professional reviewers support program/content/test review and source validation. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-009 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Scientific reviewers support scientific review, quality and methodology. | M08 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-010 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Employers support needs definition, three-month assessment, employee feedback and candidate access. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-011 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Examination institutions support professional exams, practical checks and certification. | M01 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-012 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Administrators support system management, users/roles, security/settings and reports. | M01 + M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-013 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Application layer includes competency assessment. | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-014 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Initial knowledge assessment and adaptive testing are shown. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-015 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Personalized learning includes learning paths, content recommendations and microlearning. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-016 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Learning Ledger records activities, grades, sources, versions and audit trace. | M03 + M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-017 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | AI Tutor/Mentor provides explanations, assistance, conversation and simulations. | M06 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-018 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Communication/collaboration includes forums, messages, groups and notifications. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-019 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | AI/analytics layer includes NLP Engine. | M06 + M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-020 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Recommender supports content, next-lesson and resource recommendations. | M06 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-021 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Assessment Engine supports adaptive testing and knowledge/skill assessment. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-022 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Predictive Analytics supports success prediction and dropout-risk analysis. | M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-023 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | AI calibration aligns AI assessments with expert assessments. | M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-024 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Safety Gate checks risk, limitations and safety rules. | M07 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-025 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Data layer includes operational DB, Knowledge Base DB, tests/tasks DB, Learning Ledger DB, analytics warehouse and backup/archive. | M05 + M09 + M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-026 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Integration layer includes API Gateway. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-027 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | API Gateway shows REST/GraphQL, throttling and authentication. | M03 + M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-028 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Integration services perform synchronization and transformations. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-029 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Event Bus/Message Queue supports asynchronous messages, events and notifications. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-030 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Infrastructure includes Cloud/Hybrid Cloud. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-031 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Infrastructure includes Docker/Kubernetes, Load Balancer and CDN. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-032 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Security includes TLS/AES-256, IAM, MFA, SSO, WAF, Firewall and IDS/IPS. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-033 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Data governance includes GDPR, pseudonymization and retention policy. | M03 + M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-034 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | Monitoring includes Prometheus, logging includes ELK/EFK, plus alerting and health checks. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-035 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | DevOps includes Git, CI/CD, automated testing and deployment. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-036 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | External systems include education institutions and LMS/SIS. | M01 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-037 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | External systems include government institutions and registries. | M01 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-038 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | External systems include labour-market services and employers. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-039 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | External systems include examination institutions, eID/digital signatures, payment systems and qualification registers. | M01 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-040 | AILCS-SRC-007 — Tehnička arhitektura AI platforme za učenje(1).png | External-system relationships are represented through integration arrows. | M04 | SOURCE-EXTRACTED; cross-source verification pending |

## Phase-2 control result

- Original source provenance preserved: **YES**
- Original requirement wording preserved: **YES**
- AILCS structural mapping assigned: **YES**
- Cross-source duplicate/conflict resolution: **NOT YET**
- Status/action closure: **NOT YET**
- Reconstruction register closure: **NO**
- Final AILCS documentation: **NO**
