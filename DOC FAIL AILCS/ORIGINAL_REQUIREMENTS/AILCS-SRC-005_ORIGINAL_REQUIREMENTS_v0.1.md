# AILCS-SRC-005 — ORIGINAL REQUIREMENTS v0.1

**SOURCE-ID:** AILCS-SRC-005  
**Original source:** `AILCS: Arhitektura državnog obrazovnog sistema.png`  
**Source type:** AILCS architecture diagram / high-level system architecture  
**Library file:** `file_000000009d18824692a7ce76a663597a`  
**Version visible in source:** 1.0  
**Date visible in source:** 19.05.2026.  
**Extraction status:** ORIGINAL SOURCE EXTRACTED  
**P1–P4 mapping:** PENDING  
**Cross-source consolidation:** PENDING  
**Register closure:** OPEN

## 0. Extraction rule

This document records only content visibly represented in the named source image. It does not convert the diagram into final normative requirements, final legal competences, final technical specifications, final API contracts, database schemas, technology choices, procurement specifications, or implementation commitments.

No LAT/LATCES/LATSES material has been used as AILCS source material.

---

## 1. System identity and institutional framing

**OR-001** — The system is titled **AILCS – AI LEARNING & COMPETENCY SYSTEM**.

**OR-002** — The source describes AILCS as a **DRŽAVNI INFORMACIONI SISTEM**.

**OR-003** — The source describes the presented architecture as a **ARHITEKTURA SISTEMA VISOKOG NIVOA**.

**OR-004** — The institutional header identifies **Bosna i Hercegovina**.

**OR-005** — The header visibly references the **Vijeće ministara BiH**.

**OR-006** — The header visibly references the **Ministarstvo civilnih poslova**.

**OR-007** — The header visibly references the **Agencija za razvoj visokog obrazovanja i osiguranje kvaliteta**.

**OR-008** — The header visibly references the **Zavod za zapošljavanje / Entitetska ministarstva obrazovanja**.

**OR-009** — The system architecture is presented as a national/state-level information-system concept for learning and competency development.

---

## 2. Users and access channels

**OR-010** — The architecture defines a user/actor layer titled **1. KORISNICI I KANALI PRISTUPA**.

**OR-011** — The user/actor layer includes **Učenik / Polaznik**.

**OR-012** — The user/actor layer includes **Student**.

**OR-013** — The user/actor layer includes **Radnik**.

**OR-014** — The user/actor layer includes **Nezaposleni**.

**OR-015** — The user/actor layer includes **Nastavnik / Mentor**.

**OR-016** — The user/actor layer includes **Instruktor**.

**OR-017** — The user/actor layer includes **Recenzent (naučni/stručni)**.

**OR-018** — The user/actor layer includes **Ispitivač**.

**OR-019** — The user/actor layer includes **Poslodavac**.

**OR-020** — The user/actor layer includes **Institucija / Fakultet / Institut**.

**OR-021** — The user/actor layer includes **Institucija sistema**.

**OR-022** — The user/actor layer includes **Administrator**.

**OR-023** — The architecture defines a separate **KANALI PRISTUPA** area.

**OR-024** — A **Web portal** is shown as an access channel.

**OR-025** — A **Mobilna aplikacija (iOS/Android)** is shown as an access channel.

**OR-026** — An **Instruktorski portal** is shown as an access channel.

**OR-027** — A **Poslodavac portal** is shown as an access channel.

**OR-028** — **API pristup (integracije)** is shown as an access channel.

---

## 3. Security and integration layer

**OR-029** — The architecture defines **2. SIGURNOSNI I INTEGRACIONI SLOJ**.

**OR-030** — The security/integration layer contains an **API GATEWAY**.

**OR-031** — API Gateway includes **Autentifikacija (OIDC/OAuth2)**.

**OR-032** — API Gateway includes **Autorizacija (RBAC/ABAC)**.

**OR-033** — API Gateway includes **Rate Limiting**.

**OR-034** — API Gateway includes **Validacija zahtjeva**.

**OR-035** — API Gateway includes **Rutiranje**.

**OR-036** — API Gateway includes **Verzioniranje API-a**.

**OR-037** — API Gateway includes **Monitoring**.

**OR-038** — API Gateway includes **Audit Hooks**.

**OR-039** — The security layer contains a **SIGURNOSNI SERVISI** area.

**OR-040** — Security services include **Enkripcija (TLS 1.3)**.

**OR-041** — Security services include **WAF / DDoS zaštita**.

**OR-042** — Security services include **Upravljanje ključevima**.

**OR-043** — Security services include **MFA**.

**OR-044** — Security services include **Sigurnosni logovi**.

---

## 4. Business / core services

**OR-045** — The architecture defines **3. POSLOVNI (CORE) SERVISI**.

**OR-046** — Core services include **3.1 Upravljanje korisnicima**.

**OR-047** — User management includes **Profili korisnika**.

**OR-048** — User management includes **Organizacije**.

**OR-049** — User management includes **Uloge i prava**.

**OR-050** — User management includes **Postavke naloga**.

**OR-051** — User management includes **Pristanak**.

**OR-052** — Core services include **3.2 Kompetencijski profili**.

**OR-053** — Competency profiles include **Kompetencije**.

**OR-054** — Competency profiles include **Nivoi vještina**.

**OR-055** — Competency profiles include **Kvalifikacije**.

**OR-056** — Competency profiles include **Portfolio dokaza**.

**OR-057** — Competency profiles include **Iskustvo**.

**OR-058** — Core services include **3.3 Procjena i testiranje**.

**OR-059** — Assessment/testing includes **Početna procjena**.

**OR-060** — Assessment/testing includes **Dijagnostički test**.

**OR-061** — Assessment/testing includes **Adaptivni test**.

**OR-062** — Assessment/testing includes **Formativna procjena**.

**OR-063** — Assessment/testing includes **Završna procjena**.

**OR-064** — Core services include **3.4 Učenje i sadržaj**.

**OR-065** — Learning/content includes **Kursevi i moduli**.

**OR-066** — Learning/content includes **Lekcije**.

**OR-067** — Learning/content includes **Vježbe i zadaci**.

**OR-068** — Learning/content includes **Simulacije**.

**OR-069** — Learning/content includes **Multimedija**.

**OR-070** — Core services include **3.5 AI Tutor & Mentor**.

**OR-071** — AI Tutor & Mentor includes **Objašnjenja**.

**OR-072** — AI Tutor & Mentor includes **Preporuke**.

**OR-073** — AI Tutor & Mentor includes **Personalizacija**.

**OR-074** — AI Tutor & Mentor includes **Pomoć u učenju**.

**OR-075** — AI Tutor & Mentor includes **Razgovor / Q&A**.

**OR-076** — Core services include **3.6 Praktične obuke**.

**OR-077** — Practical training includes **Virtualni lab**.

**OR-078** — Practical training includes **Simulatori**.

**OR-079** — Practical training includes **CAD/CAM/CAE**.

**OR-080** — Practical training includes **Industrijski scenariji**.

**OR-081** — Practical training includes **Praktični zadaci**.

**OR-082** — Core services include **3.7 Ispiti i certifikacija**.

**OR-083** — Exams/certification includes **Stručni ispit**.

**OR-084** — Exams/certification includes **Praktični ispit**.

**OR-085** — Exams/certification includes **Rezultati**.

**OR-086** — Exams/certification includes **Verifikacija**.

**OR-087** — Exams/certification includes **Certifikati**.

**OR-088** — Core services include **3.8 Zapošljavanje**.

**OR-089** — Employment includes **Povezivanje sa poslodavcima**.

**OR-090** — Employment includes **Ponude**.

**OR-091** — Employment includes **Probni rad**.

**OR-092** — Employment includes **Evidencija**.

**OR-093** — Core services include **3.9 Povratne informacije**.

**OR-094** — Feedback includes **Od poslodavaca (3m)**.

**OR-095** — Feedback includes **Ocjena kompetencija**.

**OR-096** — Feedback includes **Nedostajuće vještine**.

**OR-097** — Feedback includes **Sigurnost na radu**.

**OR-098** — Core services include **3.10 Analitika i izvještavanje**.

**OR-099** — Analytics/reporting includes **Dashboardi**.

**OR-100** — Analytics/reporting includes **KPI**.

**OR-101** — Analytics/reporting includes **Trendovi**.

**OR-102** — Analytics/reporting includes **Predikcije**.

**OR-103** — Analytics/reporting includes **Izvještaji**.

---

## 5. AI and intelligent layer

**OR-104** — The architecture defines **4. AI I INTELIGENTNI SLOJ**.

**OR-105** — The AI layer contains **4.1 AI Orkestrator**.

**OR-106** — AI Orchestrator includes **Upravljanje zahtjevima**.

**OR-107** — AI Orchestrator includes **Kontekst i memorija**.

**OR-108** — AI Orchestrator includes **Politike i pravila**.

**OR-109** — AI Orchestrator includes **Planiranje akcija**.

**OR-110** — The AI layer contains **4.2 AI Safety Gate**.

**OR-111** — AI Safety Gate includes **Klasifikacija rizika**.

**OR-112** — AI Safety Gate includes **Provjera kompetencija**.

**OR-113** — AI Safety Gate includes **Pravila sigurnosti**.

**OR-114** — AI Safety Gate includes **Dozvola / Blokada**.

**OR-115** — AI Safety Gate includes **Eskalacija čovjeku**.

**OR-116** — The AI layer contains **4.3 AI Model Abstraction Layer**.

**OR-117** — The model abstraction layer shows **Model A (LLM)**.

**OR-118** — The model abstraction layer shows **Model B (LLM)**.

**OR-119** — The model abstraction layer shows an **Open Source Model**.

**OR-120** — The model abstraction layer shows **Specijalizirani modeli (simulacije)**.

**OR-121** — Model Management includes **verzije**.

**OR-122** — Model Management includes **evaluacija**.

**OR-123** — Model Management includes **fine-tuning**.

**OR-124** — Model Management includes **prompt biblioteka**.

**OR-125** — The AI layer contains **4.4 AI Servisi**.

**OR-126** — AI services include **AI Tutor**.

**OR-127** — AI services include **AI Mentor**.

**OR-128** — AI services include **Generator pitanja**.

**OR-129** — AI services include **Analiza odgovora**.

**OR-130** — AI services include **Preporuke sadržaja**.

**OR-131** — AI services include **Sažeci i objašnjenja**.

**OR-132** — The AI layer contains **4.5 Output Validator**.

**OR-133** — Output Validator includes **Provjera tačnosti**.

**OR-134** — Output Validator includes **Provjera izvora**.

**OR-135** — Output Validator includes **Provjera sigurnosti**.

**OR-136** — Output Validator includes **Format i jezik**.

**OR-137** — The AI layer contains **4.6 Analytics Engine**.

**OR-138** — Analytics Engine includes **Učenje analitika**.

**OR-139** — Analytics Engine includes **AI kalibracija**.

**OR-140** — Analytics Engine includes **Predikcije ishoda**.

**OR-141** — Analytics Engine includes **Uspješnost programa**.

---

## 6. Knowledge and review / governance

**OR-142** — The architecture defines **5. ZNANJE I RECENZIJA (KNOWLEDGE GOVERNANCE)**.

**OR-143** — Knowledge governance includes **5.1 Ingestion**.

**OR-144** — Ingestion includes **Uvoz sadržaja**.

**OR-145** — Ingestion includes **Struktura**.

**OR-146** — Ingestion includes **Metapodaci**.

**OR-147** — Knowledge governance includes **5.2 Naučna recenzija**.

**OR-148** — Scientific review includes **Naučni recenzenti**.

**OR-149** — Scientific review includes **Validacija sadržaja**.

**OR-150** — Scientific review includes **Kvalitet i tačnost**.

**OR-151** — Knowledge governance includes **5.3 Stručna recenzija**.

**OR-152** — Professional review includes **Stručnjaci iz prakse**.

**OR-153** — Professional review includes **Primjenjivost**.

**OR-154** — Professional review includes **Standardi struke**.

**OR-155** — Knowledge governance includes **5.4 Sigurnosna recenzija**.

**OR-156** — Security review includes **Sigurnosni eksperti**.

**OR-157** — Security review includes **Procjena rizika**.

**OR-158** — Security review includes **Pravila sigurnog učenja**.

**OR-159** — Knowledge governance includes **5.5 Copyright & Licence**.

**OR-160** — Copyright/licence control includes **Provjera licence**.

**OR-161** — Copyright/licence control includes **Uslovi korištenja**.

**OR-162** — Copyright/licence control includes **Evidencija licenci**.

**OR-163** — Knowledge governance includes **5.6 Odobreno znanje**.

**OR-164** — Approved knowledge includes **Verzije izvora**.

**OR-165** — Approved knowledge includes **Status odobrenja**.

**OR-166** — Approved knowledge includes **Povezani izvori**.

---

## 7. Data layer

**OR-167** — The architecture defines **6. PODATKOVNI SLOJ (DATA LAYER)**.

**OR-168** — The data layer contains **6.1 Users DB**.

**OR-169** — Users DB includes **Korisnici**.

**OR-170** — Users DB includes **Uloge**.

**OR-171** — Users DB includes **Organizacije**.

**OR-172** — Users DB includes **Sesije**.

**OR-173** — The data layer contains **6.2 Competency DB**.

**OR-174** — Competency DB includes **Kompetencije**.

**OR-175** — Competency DB includes **Vještine**.

**OR-176** — Competency DB includes **Nivoi**.

**OR-177** — Competency DB includes **Dokazi**.

**OR-178** — The data layer contains **6.3 Learning DB**.

**OR-179** — Learning DB includes **Kursevi**.

**OR-180** — Learning DB includes **Moduli**.

**OR-181** — Learning DB includes **Lekcije**.

**OR-182** — Learning DB includes **Putanje učenja**.

**OR-183** — The data layer contains **6.4 Assessment DB**.

**OR-184** — Assessment DB includes **Testovi**.

**OR-185** — Assessment DB includes **Pitanja**.

**OR-186** — Assessment DB includes **Odgovori**.

**OR-187** — Assessment DB includes **Rezultati**.

**OR-188** — The data layer contains **6.5 Content/KB DB**.

**OR-189** — Content/KB DB includes **Izvori**.

**OR-190** — Content/KB DB includes **Dokumenti**.

**OR-191** — Content/KB DB includes **Metapodaci**.

**OR-192** — Content/KB DB includes **Verzije**.

**OR-193** — The data layer contains **6.6 Vector DB**.

**OR-194** — Vector DB includes **Embeddings**.

**OR-195** — Vector DB includes **Semantičko pretraživanje**.

**OR-196** — Vector DB includes **RAG indeksi**.

**OR-197** — The data layer contains **6.7 Files / Object Storage**.

**OR-198** — Files/Object Storage includes **Dokumenti**.

**OR-199** — Files/Object Storage includes **Slike**.

**OR-200** — Files/Object Storage includes **Video**.

**OR-201** — Files/Object Storage includes **Certifikati**.

**OR-202** — The data layer contains **6.8 Audit Ledger (Immutable)**.

**OR-203** — Immutable Audit Ledger includes **Svi događaji**.

**OR-204** — Immutable Audit Ledger includes **AI razgovori**.

**OR-205** — Immutable Audit Ledger includes **Procjene**.

**OR-206** — Immutable Audit Ledger includes **Odluke**.

**OR-207** — The data layer shows cross-cutting **Backups**.

**OR-208** — The data layer shows **Replication**.

**OR-209** — The data layer shows **Encryption at rest**.

**OR-210** — The data layer shows **Data Retention Policy**.

**OR-211** — The data layer shows **Disaster Recovery**.

---

## 8. External systems and integrations

**OR-212** — The architecture defines **7. EKSTERNI SISTEMI I INTEGRACIJE**.

**OR-213** — External systems include **Obrazovne ustanove**.

**OR-214** — Educational institutions are described as **Škole, fakulteti, centri za obuku (LMS, SIS)**.

**OR-215** — External systems include **Institucije vlasti**.

**OR-216** — Government institutions are described as **Ministarstva, zavodi, agencije**.

**OR-217** — The government-institution area references registries such as **MUP, Poreska uprava...**.

**OR-218** — External systems include **Tržište rada / Zavodi za zapošljavanje**.

**OR-219** — The labour-market area includes **Podaci o tržištu, deficitarnim zanimanjima**.

**OR-220** — External systems include **Poslodavci / Kompanije**.

**OR-221** — Employer integrations include **Povratne ocjene, kompetencije, zapošljavanje**.

**OR-222** — External systems include **Ispitne institucije**.

**OR-223** — Examination integrations include **Termini ispita, rezultati, certifikati**.

**OR-224** — External systems include **eID / Digitalni potpisi**.

**OR-225** — eID/digital signatures include **eIDAS, kvalifikovani potpisi, identifikacija**.

**OR-226** — External systems include **Platni sistemi**.

**OR-227** — Payment integrations include **Uplate, refundacije, finansijski moduli**.

**OR-228** — External systems include **Nacionalni registri kvalifikacija**.

**OR-229** — National qualification registers include **SOK / EQF / NQF** and **standardi kvalifikacija**.

---

## 9. Process flow

**OR-230** — The architecture defines **8. PROCES UČENJA – TOK PODATAKA**.

**OR-231** — The process begins with **Početna procjena**.

**OR-232** — The next process stage is **Personalizirani plan**.

**OR-233** — The process includes **Učenje / Lekcije**.

**OR-234** — The process includes **Vježbe / Simulacije**.

**OR-235** — The process includes **Procjena**.

**OR-236** — The process includes **Praktična obuka**.

**OR-237** — The process includes **Završna procjena**.

**OR-238** — The process includes **Stručni ispit**.

**OR-239** — The process includes **Certifikat**.

**OR-240** — The process includes **Zapošljavanje**.

**OR-241** — The process includes **3 mj. review**.

**OR-242** — The process includes a subsequent **Certifikat** stage as displayed in the source flow.

**OR-243** — The process includes **Povratna informacija**.

**OR-244** — The process diagram shows a **Kontinuirano poboljšanje (Feedback Loop)**.

---

## 10. Security and compliance

**OR-245** — The architecture defines **9. SIGURNOST I USKLAĐENOST**.

**OR-246** — The security/compliance area references **GDPR / ZKP usklađenost**.

**OR-247** — The security/compliance area references **Enkripcija (TLS, AES-256)**.

**OR-248** — The security/compliance area includes **Penetraciona testiranja**.

**OR-249** — The security/compliance area includes **Monitoring i SOC**.

**OR-250** — The security/compliance area includes **Backup i DR plan**.

---

## 11. System principles

**OR-251** — The source defines a **PRINCIPI SISTEMA** area.

**OR-252** — One principle is **Čovjek u centru**.

**OR-253** — One principle is **Sigurnost i privatnost**.

**OR-254** — One principle is **Transparentnost i odgovornost**.

**OR-255** — One principle is **Interoperabilnost i jedinstveni standardi**.

**OR-256** — One principle is **Naučna i stručna validacija**.

**OR-257** — One principle is **Kontinuirano poboljšanje**.

---

## 12. Legend and communication semantics

**OR-258** — The architecture defines a **LEGENDA** for system relationships and flows.

**OR-259** — The legend identifies **Sinkrona komunikacija (API)**.

**OR-260** — The legend identifies **Asinkrona komunikacija**.

**OR-261** — The legend identifies **Tok podataka**.

**OR-262** — The legend identifies **Povratna petlja / Feedback**.

**OR-263** — The legend visually distinguishes **Korisnici i kanali**.

**OR-264** — The legend visually distinguishes **Sigurnosni sloj**.

**OR-265** — The legend visually distinguishes **Poslovni servisi**.

**OR-266** — The legend visually distinguishes **AI sloj**.

**OR-267** — The legend visually distinguishes **Znanje i recenzija**.

**OR-268** — The legend visually distinguishes **Podatkovni sloj**.

**OR-269** — The legend visually distinguishes **Proces učenja**.

**OR-270** — The legend visually distinguishes **Sigurnost i usklađenost**.

---

## 13. Source footer / stated system positioning

**OR-271** — The source footer states: **ZNANJE JE JAVNO DOBRO**.

**OR-272** — The source footer states: **KOMPETENCIJA JE BUDUĆNOST**.

**OR-273** — The source footer states: **SIGURNOST JE PRIORITET**.

**OR-274** — The source displays **Verzija: 1.0**.

**OR-275** — The source displays **Datum: 19.05.2026.**.

---

## 14. Source-boundary notes

The following items are explicitly **not finalized by this extraction** and remain for later validation/consolidation:

- final legal competences of institutions;
- final governance bodies and mandates;
- final interpretation of national/entitiy institutional roles;
- final API contracts and API schemas;
- final identity and authorization model;
- final database schemas and data models;
- final retention periods;
- final security control catalogue;
- final AI model-selection policy;
- final AI risk taxonomy and safety thresholds;
- final certification legislation and procedures;
- final interoperability standards and implementation profiles;
- final technology stack;
- final infrastructure/procurement architecture;
- final implementation budget and financing model;
- final operational procedures.

These are deliberately left outside the original-source extraction unless and until another source establishes them.

---

## 15. Controlled status

| Control item | Status |
|---|---|
| Original source located | YES |
| Original source visually inspected | YES |
| Original source content extracted | YES |
| Source-ID assigned | YES — AILCS-SRC-005 |
| Original requirements normalized into OR records | YES |
| P1–P4 mapping | PENDING |
| Cross-source consolidation | PENDING |
| Conflict resolution with other AILCS sources | PENDING |
| Reconstruction register closure | NO |
| Final AILCS documentation | NO |

**Control rule:** This document is an evidence-preserving extraction of `AILCS-SRC-005`. It is not a final AILCS specification.