# AILCS-SRC-002 — ORIGINAL REQUIREMENTS v0.1

**Original source:** `AILCS: Tehnička arhitektura učenja i kompetencija.png`  
**Source-ID:** `AILCS-SRC-002`  
**Source type:** IMAGE  
**Source location:** ChatGPT Library  
**Evidence status:** SOURCE-EXTRACTED  
**Normative status:** NOT YET VALIDATED  

## 1. Control statement

This document records content visibly represented in the original source image. It is an evidence extraction, not a final specification. No item below is promoted to a mandatory system requirement merely because it appears in the diagram.

`AILCS-SRC-002` is AILCS material and is kept separate from LATCES/LATSES engineering material.

## 2. System identity and stated principles

The source identifies the system as:

- `AILCS – AI LEARNING & COMPETENCY SYSTEM`
- `DRŽAVNI IT SISTEM – TEHNIČKA ARHITEKTURA`
- Integrated AI platform for development of knowledge, competency assessment, and connection of education with the labour market.

The source lists these system principles:

- Čovjek u centru
- Transparentnost i sljedivost
- Sigurnost i privatnost
- Interoperabilnost i otvoreni standardi
- Naučna i stručna validacija
- Kontinuirano poboljšanje

## 3. Original source records

### SRC-002-OR-001 — Institutional ecosystem

The source depicts:

- Bosnia and Herzegovina
- Federation BiH
- Republika Srpska
- Brčko Distrikt BiH
- ministries, institutes and agencies
- faculties, institutes, schools and employers

**Evidence class:** source content.

### SRC-002-OR-002 — Users and access channels

The source identifies the following users/actors:

- Učenik / Polaznik
- Student
- Radnik
- Nezaposleni
- Nastavnik / Mentor
- Instruktor
- Recenzent (naučni/stručni)
- Ispitivač
- Poslodavac
- Institucija / Fakultet / Institut
- Administrator sistema

Access channels shown:

- Web Portal
- Mobilna aplikacija (iOS/Android)
- Instructorski portal
- Poslodavac portal
- API pristup (integracije)

### SRC-002-OR-003 — API Gateway and security layer

The source identifies:

- Autentifikacija (OIDC/OAuth2)
- Autorizacija (RBAC/ABAC)
- Rate Limiting
- Validacija zahtjeva
- Rutiranje
- Verzioniranje API-a
- Monitoring
- Audit Hooks
- WAF / DDoS zaštita

Security services shown:

- Enkripcija (TLS 1.3)
- Upravljanje ključevima
- MFA
- SIEM integracija

### SRC-002-OR-004 — Core service: user management

`3.1 Upravljanje korisnicima` contains:

- Profili
- Organizacije
- Uloge i prava
- Postavke naloga
- Konsent menadžment

### SRC-002-OR-005 — Core service: competency profiles

`3.2 Kompetencijski profili` contains:

- Kompetencije
- Nivoi vještina
- Kvalifikacije
- Portfolio dokaza
- Prethodno iskustvo

### SRC-002-OR-006 — Core service: assessments

`3.3 Procjena (Assessments)` contains:

- Početna procjena
- Dijagnostički test
- Adaptivni test
- Formativna procjena
- Završna procjena

### SRC-002-OR-007 — Core service: learning and content

`3.4 Učenje i sadržaj` contains:

- Kursevi i moduli
- Lekcije
- Vježbe i zadaci
- Simulacije
- Multimedija

### SRC-002-OR-008 — Core service: AI Tutor and Mentor

`3.5 AI Tutor & Mentor` contains:

- Objašnjenja
- Preporuke
- Personalizacija
- Pomoć u učenju
- Razgovor / Q&A

### SRC-002-OR-009 — Core service: practical training

`3.6 Praktične obuke` contains:

- Virtual lab
- Simulacije
- CAD/CAM/CAE
- Industrijski scenariji
- Praktični zadaci

### SRC-002-OR-010 — Core service: examinations and certification

`3.7 Ispiti i certifikacija` contains:

- Stručni ispit
- Praktični ispit
- Rezultati
- Verifikacija
- Certifikati

### SRC-002-OR-011 — Core service: employment

`3.8 Zapošljavanje` contains:

- Povezivanje sa poslodavcima
- Ponude
- Probni rad
- Evidencija
- Ugovori

### SRC-002-OR-012 — Core service: feedback

`3.9 Povratne informacije` contains:

- Od poslodavca (3 mjeseca)
- Ocjena kompetencija
- Nedostajuće vještine
- Sigurnost na radu

### SRC-002-OR-013 — Core service: analytics and reporting

`3.10 Analitika & izvještavanje` contains:

- Dashboardi
- KPI
- Trendovi
- Predikcije
- Izvještaji

### SRC-002-OR-014 — AI orchestrator

`4.1 AI Orkestrator` contains:

- Upravljanje zahtjevima
- Kontekst i memorija
- Politike i pravila
- Planiranje akcija

### SRC-002-OR-015 — AI Safety Gate

`4.2 AI Safety Gate` contains:

- Klasifikacija rizika
- Provjera kompetencija
- Pravila sigurnosti
- Dozvola / Blokada
- Eskalacija čovjeku

### SRC-002-OR-016 — AI Model Abstraction Layer

`4.3 AI Model Abstraction Layer` depicts:

- Model A (LLM)
- Model B (LLM)
- Open Source Model
- Specijalizirani modeli (simulacije)

The source also identifies Model Management functions:

- verzije
- evaluacija
- fine-tuning
- prompt biblioteka

### SRC-002-OR-017 — AI services

`4.4 AI Servisi` contains:

- AI Tutor
- AI Mentor
- Generator pitanja
- Analiza odgovora
- Preporuke sadržaja
- Sažeci i objašnjenja

### SRC-002-OR-018 — Output Validator

`4.5 Output Validator` contains:

- Provjera tačnosti
- Provjera izvora
- Provjera sigurnosti
- Format i jezik

### SRC-002-OR-019 — Analytics Engine

`4.6 Analytics Engine` contains:

- Učenje analitika
- AI kalibracija
- Predikcije ishoda
- Uspješnost programa

### SRC-002-OR-020 — Knowledge Governance ingestion

`5.1 Ingestion` contains:

- Uvoz sadržaja
- Struktura
- Metapodaci

### SRC-002-OR-021 — Scientific review

`5.2 Naučna recenzija` contains:

- Naučni recenzenti
- Validacija sadržaja
- Kvalitet i tačnost

### SRC-002-OR-022 — Professional review

`5.3 Stručna recenzija` contains:

- Stručnjaci iz prakse
- Primjenjivost
- Standardi struke

### SRC-002-OR-023 — Safety review

`5.4 Sigurnosna recenzija` contains:

- Sigurnosni eksperti
- Procjena rizika
- Pravila sigurnog učenja

### SRC-002-OR-024 — Copyright and licences

`5.5 Copyright & Licence` contains:

- Provjera licence
- Uslovi korištenja
- Evidencija licenci

### SRC-002-OR-025 — Approved knowledge

`5.6 Odobreno znanje` contains:

- Verzije izvora
- Status odobrenja
- Povezani izvori

### SRC-002-OR-026 — Users database

`6.1 Users DB` contains:

- Korisnici
- Uloge
- Organizacije
- Sesije

### SRC-002-OR-027 — Competency database

`6.2 Competency DB` contains:

- Kompetencije
- Vještine
- Nivoi
- Dokazi

### SRC-002-OR-028 — Learning database

`6.3 Learning DB` contains:

- Kursevi
- Moduli
- Lekcije
- Putanje učenja

### SRC-002-OR-029 — Assessment database

`6.4 Assessment DB` contains:

- Testovi
- Pitanja
- Odgovori
- Rezultati

### SRC-002-OR-030 — Content / knowledge-base database

`6.5 Content/KB DB` contains:

- Izvori
- Dokumenti
- Metapodaci
- Verzije

### SRC-002-OR-031 — Vector database

`6.6 Vector DB` contains:

- Embeddings
- Semantičko pretraživanje
- RAG indeks

### SRC-002-OR-032 — Files / object storage

`6.7 Files / Object Storage` contains:

- Dokumenti
- Slike
- Video
- Certifikati

### SRC-002-OR-033 — Immutable audit ledger

`6.8 Audit Ledger (Immutable)` contains:

- Svi događaji
- AI tragovi
- Procjene
- Odluke

### SRC-002-OR-034 — Data protection functions

The source lists:

- Backups
- Replication
- Encryption at rest
- Data Retention Policy
- Disaster Recovery

### SRC-002-OR-035 — External educational systems

The source identifies:

- Obrazovne ustanove
- Škole, fakulteti, centri za obuku (LMS, SIS)

### SRC-002-OR-036 — Government institutions

The source identifies:

- Institucije vlasti
- Ministarstva, zavodi, agencije
- Registri, MUP, Poreska uprava...

### SRC-002-OR-037 — Labour market and employment services

The source identifies:

- Tržište rada / Zavodi za zapošljavanje
- Podaci o potražnji
- Deficitarna zanimanja

### SRC-002-OR-038 — Employers and companies

The source identifies:

- Poslodavci / Kompanije
- Povratne ocjene
- Kompetencije
- Zapošljavanje

### SRC-002-OR-039 — Examination institutions

The source identifies:

- Ispitne institucije
- Termini ispita
- Rezultati
- Certifikati

### SRC-002-OR-040 — eID and digital signatures

The source identifies:

- eID / Digitalni potpisi
- eIDAS
- kvalifikovani potpisi
- identifikacija

### SRC-002-OR-041 — Payment systems

The source identifies:

- Platni sistemi
- Uplate
- Refundacije
- finansijski moduli

### SRC-002-OR-042 — National qualifications register

The source identifies:

- Nacionalni registar kvalifikacija
- SOK / EQF / NQF standardi kvalifikacija

### SRC-002-OR-043 — End-to-end learning process

The source depicts this process:

`Početna procjena → Personalizirani plan → Učenje / Lekcije → Vježbe / Simulacije → Procjena → Praktična obuka → Završna procjena → Stručni ispit → Certifikat → Zapošljavanje → 3 mj. review → Povratna informacija`

A dashed feedback loop is labelled:

`Kontinuirano poboljšanje (Feedback Loop)`

### SRC-002-OR-044 — Security and compliance

The source lists:

- GDPR / ZKP usklađenost
- Enkripcija (TLS, AES-256)
- Penetraciona testiranja
- Monitoring i SOC
- Disaster Recovery

### SRC-002-OR-045 — Communication and data-flow legend

The legend distinguishes:

- Sinhrona komunikacija (API)
- Asinhrona komunikacija
- Tok podataka
- Povratna petlja / Feedback

It also distinguishes categories:

- Korisnici i kanali
- Sigurnosni sloj
- Poslovni servisi
- AI sloj
- Znanje i recenzija
- Podatkovni sloj
- Integracije & ekosistem

### SRC-002-OR-046 — Source version/date

The image footer states:

- Verzija: `1.0`
- Datum: `19.05.2026.`

## 4. Explicit non-inferences

The following are **not** established as final requirements by this source alone:

- final legal competences of BiH institutions;
- final P1–P4 classification;
- final API contracts;
- final database schemas;
- final security control catalogue;
- final service boundaries;
- final M01–M11 module numbering;
- final technology selection;
- final procurement or implementation architecture;
- final certification legislation;
- final data-retention periods;
- final AI model-selection policy.

These may be developed later, but must be labelled `RECONSTRUCTED` or `PROPOSED` unless supported by another original source.

## 5. Source extraction status

**Source-ID:** AILCS-SRC-002  
**Original source inspected:** YES  
**Original content extracted:** YES  
**Requirement validation:** PENDING  
**P1–P4 mapping:** PENDING  
**Cross-source consolidation:** PENDING  
**Register closure:** NO

## 6. Evidence reference

Library source record: `AILCS: Tehnička arhitektura učenja i kompetencija.png` — image source identified in the AILCS Library. fileciteturn54file0 fileciteturn54file1 fileciteturn54file2 fileciteturn54file3 fileciteturn54file4

**Control conclusion:** This document is an extraction of `AILCS-SRC-002`; it is not a final AILCS specification.