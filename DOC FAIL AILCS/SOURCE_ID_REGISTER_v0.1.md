# AILCS — SOURCE-ID REGISTER v0.1

**Status:** Working register — source inventory stage  
**Date:** 2026-09-11  
**Project boundary:** AILCS only

## 1. Purpose

This register assigns a stable `SOURCE-ID` to each AILCS source that has been identified and source-level verified in the available Library material.

The register is an evidence-control document. It does **not** create new requirements and does **not** treat reconstructed or proposed architecture as original requirements.

## 2. Project boundary

**AILCS ≠ LATCES/LATSES.**

Material belonging to LATCES/LATSES, including engineering, HVAC, Living Air Twin, or other LAT-specific documentation, is excluded unless independent evidence establishes that it is an AILCS source.

## 3. Source register

| SOURCE-ID | Original filename | Type | Source | Classification | Verification | Requirements extracted | P1–P4 mapping | Action |
|---|---|---|---|---|---|---|---|---|
| AILCS-SRC-001 | `Tehnička arhitektura AI obrazovne platforme.png` | IMAGE | Library | AILCS-SOURCE | VERIFIED | Pending detailed extraction | Pending | Extract source content |
| AILCS-SRC-002 | `AILCS: Tehnička arhitektura učenja i kompetencija.png` | IMAGE | Library | AILCS-SOURCE | VERIFIED | Pending detailed extraction | Pending | Extract source content |
| AILCS-SRC-003 | `Arhitektura BIH AI obrazovnog sistema.png` | IMAGE | Library | AILCS-SOURCE | VERIFIED | Pending detailed extraction | Pending | Extract source content |
| AILCS-SRC-004 | `Cjelokupna arhitektura AILCS sistema.png` | IMAGE | Library | AILCS-SOURCE | VERIFIED | Pending detailed extraction | Pending | Extract source content |
| AILCS-SRC-005 | `AILCS: Arhitektura državnog obrazovnog sistema.png` | IMAGE | Library | AILCS-SOURCE | VERIFIED | Pending detailed extraction | Pending | Extract source content |
| AILCS-SRC-006 | `Arhitektura AI obrazovnog sistema BiH.png` | IMAGE | Library | AILCS-SOURCE | VERIFIED | Pending detailed extraction | Pending | Extract source content |
| AILCS-SRC-007 | `Tehnička arhitektura BIH AI sistema učenja.png` | IMAGE | Library | AILCS-SOURCE | VERIFIED | Pending detailed extraction | Pending | Extract source content |
| AILCS-SRC-008 | `Tehnička arhitektura AI platforme za učenje(1).png` | IMAGE | Library | AILCS-SOURCE | VERIFIED | Pending detailed extraction | Pending | Extract source content |

## 4. Verification rules

`VERIFIED` means that the source has been identified as AILCS-specific based on the available source evidence. It does **not** mean that every statement visible in the source has already been validated as a formal requirement.

`Pending detailed extraction` means the source has not yet been converted into a complete requirement-by-requirement evidence record.

`Pending` P1–P4 mapping means no normative mapping is being asserted at this stage.

## 5. Exclusions / non-AILCS material

The following material encountered during Library searches is explicitly **not** entered as an AILCS source:

- `prilog.docx` — contains room geometry, air intake/exhaust, plenum and HVAC data; classified as LAT/HVAC material.
- `kompletna dokumentacija i ona koja nije zavrsena.docx` — begins with `LAT-01-000 PROJECT CHARTER Living Air Twin (LAT)`; classified as LAT material.
- `Pasted markdown.md` — LAT SMC architecture material; classified as LAT material.

These exclusions are recorded to prevent accidental cross-project contamination.

## 6. Register state

**Current identified AILCS sources:** 8  
**Verified as AILCS-specific:** 8  
**Detailed requirement extraction completed:** 0  
**P1–P4 mapping completed:** 0  
**Register closed:** NO

## 7. Next controlled step

For each `SOURCE-ID`, extract only what is actually present in the original source and create the **Original Requirements Register**. Any interpretation, normalization, consolidation, or newly proposed element must be explicitly marked as reconstructed/proposed rather than historical source content.

**Control rule:** No final AILCS document is to be treated as authoritative until the source inventory, original requirements, P1–P4 mapping, and status/action register have been closed.