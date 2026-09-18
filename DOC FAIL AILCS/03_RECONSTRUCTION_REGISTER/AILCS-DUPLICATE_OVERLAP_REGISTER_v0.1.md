# AILCS — PHASE 3 DUPLICATE / OVERLAP REGISTER v0.1

**Scope:** SRC-001 through SRC-008  
**Records reviewed:** 674  
**Rule:** screening findings only; source provenance is preserved.  
**LAT/LATCES:** excluded.

## Exact normalized overlap groups

| ID | Source records | Finding | Action | Status |
|---|---|---|---|---|
| OX-001 | SRC-005:OR-066; SRC-005:OR-181 | Both contain the same normalized learning/lesson concept, but occur in different architectural contexts. | Compare context; do not delete either source record. | OPEN |
| OX-002 | SRC-005:OR-117; SRC-005:OR-118 | Same normalized model-abstraction wording, although labels Model A and Model B differ. | Treat as related model slots; verify intended distinction. | OPEN |
| OX-003 | SRC-006:OR-032; SRC-007:OR-019 | NLP Engine. | MERGE candidate; preserve both SOURCE-IDs. | OPEN |
| OX-004 | SRC-006:OR-034; SRC-007:OR-021 | Assessment Engine with adaptive/knowledge-skill assessment. | MERGE/REFINE candidate; preserve both SOURCE-IDs. | OPEN |
| OX-005 | SRC-006:OR-037; SRC-007:OR-024 | Safety Gate checks risk, limitations and safety rules. | MERGE candidate; preserve both SOURCE-IDs. | OPEN |
| OX-006 | SRC-006:OR-042; SRC-007:OR-032 | TLS/AES-256, IAM, MFA, SSO, WAF, Firewall and IDS/IPS. | MERGE candidate; validate exact security baseline later. | OPEN |
| OX-007 | SRC-006:OR-043; SRC-007:OR-033 | GDPR, pseudonymization and retention policy. | MERGE candidate; validate legal implementation details later. | OPEN |

## High-similarity cross-source candidates

| ID | Similarity | Source A | Source B | Action |
|---|---:|---|---|---|
| OX-008 | 0.86 | SRC-006:OR-035 Predictive Analytics — success prediction/dropout risk | SRC-007:OR-022 same capability | MERGE/REFINE |
| OX-009 | 0.83 | SRC-006:OR-045 DevOps — Git, CI/CD, testing, deployment | SRC-007:OR-035 same capability | MERGE |
| OX-010 | 0.78 | SRC-002:OR-040 eID and digital signatures | SRC-005:OR-225 eIDAS, qualified signatures, identification | REFINE/VERIFY |
| OX-011 | 0.75 | SRC-001:OR-053 Recommendation engine | SRC-006:OR-033 Recommendation Engine | MERGE/REFINE |
| OX-012 | 0.75 | SRC-006:OR-013 API Gateway | SRC-007:OR-026 API Gateway in integration layer | MERGE |
| OX-013 | 0.75 | SRC-006:OR-041 Cloud/Hybrid, Docker, Kubernetes, Load Balancer, CDN | SRC-007:OR-031 Docker/Kubernetes, Load Balancer, CDN | REFINE |
| OX-014 | 0.67 | SRC-004:OR-001 AILCS identity | SRC-007:OR-001 AILCS identity | MERGE |
| OX-015 | 0.67 | SRC-007:OR-038 labour-market external systems | SRC-008:OR-032 labour-market systems | MERGE/REFINE |
| OX-016 | 0.63 | SRC-001:OR-022 Safety Gate Service | SRC-006:OR-037 Safety Gate | MERGE |
| OX-017 | 0.63 | SRC-001:OR-022 Safety Gate Service | SRC-007:OR-024 Safety Gate | MERGE |
| OX-018 | 0.63 | SRC-003:OR-001 System identity | SRC-007:OR-001 AILCS identity | MERGE |
| OX-019 | 0.60 | SRC-001:OR-024 Employer Review Service | SRC-006:OR-030 employer feedback after three months | REFINE |
| OX-020 | 0.60 | SRC-002:OR-033 Immutable audit ledger | SRC-005:OR-203 Immutable Audit Ledger | MERGE |
| OX-021 | 0.60 | SRC-005:OR-024 Web portal | SRC-006:OR-009 Web Portal | MERGE |
| OX-022 | 0.60 | SRC-005:OR-030 API Gateway | SRC-007:OR-026 API Gateway | MERGE |
| OX-023 | 0.60 | SRC-006:OR-036 AI calibration | SRC-007:OR-023 AI calibration | MERGE |
| OX-024 | 0.57 | SRC-001:OR-010 API Gateway | SRC-005:OR-033 Rate Limiting in API Gateway | REFINE |
| OX-025 | 0.57 | SRC-006:OR-010 mobile iOS/Android | SRC-007:OR-003 Android/iOS mobile | MERGE |
| OX-026 | 0.57 | SRC-006:OR-024 assessment types | SRC-007:OR-014 initial/adaptive assessment | REFINE |
| OX-027 | 0.57 | SRC-006:OR-034 Assessment Engine | SRC-007:OR-014 initial/adaptive assessment | REFINE |
| OX-028 | 0.57 | SRC-006:OR-038 data stores | SRC-007:OR-025 data stores | REFINE |

## Control rule

Similarity is a screening signal, not proof of identity. No record is removed. All final consolidation decisions belong to STATUS → AKCIJA.
