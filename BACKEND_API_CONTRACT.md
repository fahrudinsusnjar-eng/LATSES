# TRAMP Backend API Contract

The Android client never pretends that a source was checked.

## POST /v1/analyze
Input:
- question
- jurisdiction
- date
- language

Output:
- claims[]
- required_context[]
- candidate_sources[]
- evidence[]
- conflicts[]
- uncertainty[]
- decision_state

## GET /v1/sources/{sourceId}
Returns the current source metadata and retrieval status.

## POST /v1/verify
Input:
- claim
- sourceId
- documentUrl

Output:
- verified
- evidence
- publicationDate
- effectiveDate
- version
- uncertainty

A production backend must use HTTPS, cache raw source responses, retain retrieval timestamps and preserve the evidence used for each answer. No fabricated live verification is permitted.
