# AILCS — SOURCE-ID REGISTER v0.2

**Status:** Controlled source register — original-source extraction stage  
**Project boundary:** AILCS only  
**Last update:** 2026-09-18

## 1. Purpose

This register assigns a stable SOURCE-ID to each verified AILCS source and tracks whether original-source extraction has been completed.

**Control sequence:**
INVENTAR → SOURCE-ID → ORIGINALNI ZAHTJEVI → P1–P4 → STATUS → AKCIJA → register closure → final AILCS documentation.

## 2. Project boundary

**AILCS ≠ LATCES/LATSES.**

LATCES/LATSES, HVAC, Living Air Twin and other LAT material are excluded unless independently verified as AILCS source material.

## 3. Current verified source register

| SOURCE-ID | Original filename | Type | Classification | Verification | Original extraction | P1–P4 | Status | Action |
|---|---|---|---|---|---|---|---|---|
| AILCS-SRC-001 | Tehnička arhitektura AI obrazovne platforme.png | IMAGE | AILCS-SOURCE | VERIFIED | COMPLETE | PENDING | OPEN | P1–P4 later |
| AILCS-SRC-002 | AILCS: Tehnička arhitektura učenja i kompetencija.png | IMAGE | AILCS-SOURCE | VERIFIED | COMPLETE | PENDING | OPEN | P1–P4 later |
| AILCS-SRC-003 | Arhitektura BIH AI obrazovnog sistema.png | IMAGE | AILCS-SOURCE | VERIFIED | COMPLETE | PENDING | OPEN | P1–P4 later |
| AILCS-SRC-004 | Arhitektura AI obrazovnog sistema BiH.png | IMAGE | AILCS-SOURCE | VERIFIED | COMPLETE | PENDING | OPEN | P1–P4 later |
| AILCS-SRC-005 | AILCS: Arhitektura državnog obrazovnog sistema.png | IMAGE | AILCS-SOURCE | VERIFIED | COMPLETE | PENDING | OPEN | P1–P4 later |
| AILCS-SRC-006 | Tehnička arhitektura BIH AI sistema učenja.png | IMAGE | AILCS-SOURCE | VERIFIED | COMPLETE | PENDING | OPEN | P1–P4 later |
| AILCS-SRC-007 | Tehnička arhitektura AI platforme za učenje(1).png | IMAGE | AILCS-SOURCE | VERIFIED | COMPLETE | PENDING | OPEN | P1–P4 later |
| AILCS-SRC-008 | Cjelokupna arhitektura AILCS sistema.png | IMAGE | AILCS-SOURCE | VERIFIED | COMPLETE | PENDING | OPEN | P1–P4 later |

## 4. Current totals

- Identified AILCS architecture/source images: **8**
- Verified AILCS-specific: **8**
- Original-source extraction completed: **8**
- P1–P4 mapping completed: **0**
- Cross-source consolidation completed: **0**
- Register closed: **NO**

## 5. Extraction files

Each completed extraction is stored under:

`DOC FAIL AILCS/ORIGINAL_REQUIREMENTS/`

with the corresponding SOURCE-ID.

## 6. Explicit exclusions

The following Library material has been inspected and classified as NOT-AILCS:

- `prilog.docx` — LAT/HVAC room and ventilation material.
- `kompletna dokumentacija i ona koja nije zavrsena.docx` — LAT-01 / Living Air Twin documentation.
- `Pasted markdown.md` — LAT SMC architecture.
- `Dvije stvari koje bih još dodao.docx` — LAT engineering/Physics Engine discussion.

These exclusions are preserved to prevent cross-project contamination.

## 7. Control rule

The completion of source extraction does **not** authorize final architecture synthesis.

Next phase is:

**P1–P4 mapping → cross-source comparison/conflict register → status/action closure → reconstruction register closure → final AILCS documentation.**

No final AILCS document is authoritative before that sequence is closed.
