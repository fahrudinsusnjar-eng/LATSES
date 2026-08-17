# SCI 1–145 → main → SMC consolidation matrix

Source: `SCI 1-145 LAT SES.docx` (Library v1). The source contains 145 LAT-SCI specifications/records. The matrix below maps every sequence into the canonical implementation layer. `MAPPED_NOT_YET_ACCEPTED` is deliberate: documentation is not treated as implementation until code + tests + traceability pass SMC-004.

Decision vocabulary: KEEP / MERGE / ADAPT / MOVE / RETIRE / NEW.

| # | SCI ID | Canonical target | Decision | Status |
|---:|---|---|---|---|
| 1 | LAT-SCI-0001 | `lat_ces/scientific/core` + units/dimensions | ADAPT | MAPPED_NOT_YET_ACCEPTED |
| 2–9 | LAT-SCI-CORE-0002…0009 | `lat_ces/scientific/core` | ADAPT | MAPPED_NOT_YET_ACCEPTED |
| 10–37 | LAT-SCI-CORE-0010…0037 | `lat_ces/scientific/units` + `dimensions` | MERGE | MAPPED_NOT_YET_ACCEPTED |
| 38–53 | LAT-SCI-CORE-0038…0053 | `lat_ces/scientific/quantity` + measurement | ADAPT | MAPPED_NOT_YET_ACCEPTED |
| 54–61 | LAT-SCI-CORE-0054…0061 | provenance + validation | ADAPT | MAPPED_NOT_YET_ACCEPTED |
| 62–77 | LAT-SCI-CORE-0062…0077 | models + reasoning/synthesis interfaces | ADAPT | MAPPED_NOT_YET_ACCEPTED |
| 78–93 | LAT-SCI-CORE-0078…0093 | evidence + trust + assurance | ADAPT | MAPPED_NOT_YET_ACCEPTED |
| 94–101 | LAT-SCI-CORE-0094…0101 | lifecycle + ecosystem management | ADAPT | MAPPED_NOT_YET_ACCEPTED |
| 102–125 | LAT-SCI-CORE-0102…0125 | intelligence + governance/evolution/integration | ADAPT | MAPPED_NOT_YET_ACCEPTED |
| 126–129 | LAT-SCI-CORE-0126…0129 | federation + verification | ADAPT | MAPPED_NOT_YET_ACCEPTED |
| 130–137 | LAT-SCI-CORE-0130…0137 | security architecture + hardening | ADAPT | MAPPED_NOT_YET_ACCEPTED |
| 138–141 | LAT-SCI-CORE-0138…0141 | security hardening governance | ADAPT | MAPPED_NOT_YET_ACCEPTED |
| 142–145 | LAT-SCI-CORE-0142…0145 | adaptive security governance | ADAPT | MAPPED_NOT_YET_ACCEPTED |

## Direct main evidence already present

`main` contains substantial candidate implementations: `lat_ces/scientific/models`, `lat_ces/scientific/units`, `lat_ces/scientific/quantity`, `lat_ces/scientific/quantities`, `lat_ces/scientific/registry`, `lat_ces/scientific/uncertainty`, `lat_ces/scientific/equations`, measurement/scientific models, `lat_ces/gov`, `lat_ces/evidence`, `lat_ces/graph`, `lat_ces/twin`, and engineering/domain infrastructure. These are candidates for ADAPT/MERGE, not automatic acceptance.

## Legacy 0001–0055 rule

The old numbered modules remain on `main`. They are protected by SMC-002: no silent deletion. Each legacy module must be assigned KEEP/MERGE/ADAPT/MOVE/RETIRE/NEW from its actual file, imports, tests and provenance. A number alone is never used to infer scientific responsibility.

## SMC linkage

- SMC-001 binds specification → canonical implementation target.
- SMC-002 controls legacy 0001–0055 consolidation.
- SMC-003 defines the Scientific Model contract.
- SMC-004 is the acceptance gate before merge/release.
