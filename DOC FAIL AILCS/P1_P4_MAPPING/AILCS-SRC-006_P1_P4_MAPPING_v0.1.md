# AILCS-SRC-006 — P1–P4 MAPPING v0.1

**SOURCE-ID:** `AILCS-SRC-006`  
**Original source:** `Tehnička arhitektura BIH AI sistema učenja.png`  
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
| OR-001 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | The architecture presents AILCS users and access channels. | M02 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-002 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Users include Učenici/Polaznici. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-003 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Users include Studenti. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-004 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Users include Radnici and Nezaposleni. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-005 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Users include Nastavnici/Mentori and Instruktori. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-006 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Users include Recenzenti and Ispitivači. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-007 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Users include Poslodavci. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-008 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Users include Institucije/Fakulteti and Administratori. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-009 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Access channels include Web Portal. | M02 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-010 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Access channels include mobile iOS/Android application. | M02 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-011 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Access channels include instructor and employer portals. | M02 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-012 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | API access for integrations is shown. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-013 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | API Gateway is part of the integration layer. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-014 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Authentication uses OIDC/OAuth2. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-015 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Authorization uses RBAC/ABAC. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-016 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Rate limiting, request validation, routing and API versioning are shown. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-017 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Monitoring and audit hooks are shown. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-018 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Integration adapters include eIDAS/IDDEEA. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-019 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Integration adapters include e-Dnevnik/ISS. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-020 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Registries, payment systems and national qualification registers are shown. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-021 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Core services include user management. | M01 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-022 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Core services include competency profiles. | M01 + M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-023 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Competency profiles contain competencies, skill levels, qualifications and evidence. | M01 + M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-024 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Assessment/testing includes initial, adaptive, formative and final assessment. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-025 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Learning/content includes courses, modules, lessons, exercises, tasks and simulations. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-026 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | AI Tutor & Mentor provides explanations, recommendations, personalization, learning help and Q&A. | M06 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-027 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Practical training includes virtual lab, simulators, CAD/CAM/CAE, industrial scenarios and practical tasks. | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-028 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Exams/certification include exams, results, verification and certificates. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-029 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Employment includes employer connection, offers and probationary work. | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-030 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Feedback includes employer feedback after three months, competency assessment and missing skills. | M05 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-031 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Analytics/reporting includes dashboards, KPI, reports and trends. | M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-032 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | AI/analytics layer includes NLP Engine. | M06 + M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-033 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Recommendation Engine supports content/resource recommendations. | M06 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-034 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Assessment Engine supports adaptive testing and knowledge/skill assessment. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-035 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Predictive Analytics includes success prediction and dropout risk. | M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-036 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | AI calibration aligns AI assessment with expert assessment. | M11 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-037 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Safety Gate checks risk, limitations and safety rules. | M07 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-038 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Data layer contains operational, knowledge, tests/tasks, learning-ledger and analytics stores. | M09 + M10 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-039 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Backup and archive are shown. | M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-040 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Integration layer includes REST/GraphQL API, synchronization/transformation services and Event Bus/Message Queue. | M04 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-041 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Infrastructure includes Cloud/Hybrid Cloud, Docker, Kubernetes, Load Balancer and CDN. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-042 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Security includes TLS/AES-256, IAM, MFA, SSO, WAF, Firewall and IDS/IPS. | M03 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-043 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Data governance includes GDPR, pseudonymization and retention policy. | M03 + M09 | SOURCE-EXTRACTED; cross-source verification pending |
| OR-044 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | Operations include monitoring, logging, alerting and health checks. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-045 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | DevOps includes Git repository, CI/CD, automated testing and deployment. | CROSS-CUTTING / TO VALIDATE | SOURCE-EXTRACTED; cross-source verification pending |
| OR-046 | AILCS-SRC-006 — Tehnička arhitektura BIH AI sistema učenja.png | External systems include education, government, labour-market, employers, examination institutions, eID, payments and qualification registers. | M01 | SOURCE-EXTRACTED; cross-source verification pending |

## Phase-2 control result

- Original source provenance preserved: **YES**
- Original requirement wording preserved: **YES**
- AILCS structural mapping assigned: **YES**
- Cross-source duplicate/conflict resolution: **NOT YET**
- Status/action closure: **NOT YET**
- Reconstruction register closure: **NO**
- Final AILCS documentation: **NO**
