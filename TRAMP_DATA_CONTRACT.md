# TRAMP Data Contract

A live result is never verified merely because a URL exists.

Minimum evidence: source ID, institution, jurisdiction, URL, publication/effective date or version, retrieval timestamp, evidence excerpt or structured field, verification status, uncertainty/conflict note.

Decision states:
INPUT → NEEDS_CONTEXT → NEEDS_SOURCE → UNVERIFIED → VERIFIED

Flow entities:
FundingOpportunity, FinancialFlow, TradeFlow, MigrationFlow, HealthEvent, ClimateSignal.

The Android client is the presentation layer. A backend connector must retrieve current official documents, preserve evidence and return traceable records. The client must not fabricate live values.