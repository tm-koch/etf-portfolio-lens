## Context

The backend currently parses provider holdings into `NormalizedHolding`, enriches them through a downloaded ticker CSV, and writes snapshots. Matching is primarily identifier-based, but exchange labels vary by provider and ticker values are only locally unique. The frontend currently falls back to ISIN, ticker, or name while aggregating companies, so conflicting source records can produce order-dependent names and incorrect merges.

The change crosses parsing, matching, snapshot modeling, CLI configuration, fixture data, and frontend aggregation. It must preserve raw provider values for auditability while producing stable canonical identity data for downstream consumers.

## Goals / Non-Goals

**Goals:**

- Resolve holdings with deterministic, auditable precedence across overrides and the security master.
- Normalize exchange aliases without losing the original source value.
- Represent exact traded instruments separately from canonical companies.
- Persist resolved identity and canonical names in snapshots.
- Provide strict validation that fails a run before partial publication.
- Make aggregation independent of selected ETF insertion order.
- Cover known ambiguous and conflicting records with regression tests.

**Non-Goals:**

- Building a general-purpose global security master.
- Automatically guessing a company identity from an unreliable ticker or free-form name.
- Replacing provider holdings files or changing exposure calculations.
- Introducing a mandatory external company-ID service or network dependency beyond the existing security master.

## Decisions

### Override-first resolution

Add a version-controlled override document with explicit match selectors for ISIN, ticker plus normalized exchange or country, and holding name. An override may correct identifiers and provide canonical identity and missing enrichment fields. The resolver applies the most specific valid override first, then fills only remaining fields from the security master.

Alternatives considered: modifying the downloaded ticker CSV is not reproducible and loses the distinction between upstream data and local correction; security-master-only matching cannot repair a wrong source ISIN such as the ACWD/CHSPI conflict.

### Canonical exchange codes

Introduce a normalized exchange-code vocabulary and alias mapping. Matching uses the internal code, while raw exchange text remains in `source_fields`. Country is a secondary disambiguator where an exchange is absent or insufficient.

Alternatives considered: exact exchange-string matching is brittle; ignoring exchange causes globally duplicated tickers to become ambiguous.

### Stable instrument and company identities

Store the source/exact instrument fields together with `company_id` and `canonical_name` on resolved holdings. `company_id` is assigned from an explicit override or an authoritative security-master field when available; otherwise a deterministic internal ID is generated only from a validated canonical record and persisted in the snapshot. No ID is inferred from ticker alone.

Alternatives considered: using ISIN as company identity incorrectly separates share classes and cannot consolidate corrected or alternate instruments; deriving identity live in the browser makes results non-reproducible.

### Strict validation as an opt-in CLI mode

Add an opt-in strict flag. Normal mode retains current warning behavior. Strict mode collects all unresolved, ambiguous, or required-field failures, reports them together, and raises before writing successful snapshots or updating the catalog.

Alternatives considered: always-strict ingestion would block useful exploratory fixture runs; stopping at the first error hides the full correction workload.

### Canonical aggregation in the web layer

The frontend aggregates by persisted `company_id`, displays `canonical_name`, and applies deterministic secondary sorting by company ID/name after exposure. Selected ETF columns may retain user order for presentation, but the set of rows and values must not depend on that order.

Alternatives considered: alphabetical selection among conflicting names only hides the identity error; sorting by position order preserves the underlying bug.

## Risks / Trade-offs

- [Risk] Override selectors can themselves be too broad or contradictory. -> Validate selector uniqueness and reject conflicting override definitions before ingestion.
- [Risk] A source may contain a wrong ISIN that appears valid in the security master. -> Allow higher-specificity source-context/name overrides and record the correction in diagnostics.
- [Risk] Existing snapshots lack canonical fields. -> Version the snapshot schema or support a clear legacy-read path while regenerating published snapshots.
- [Risk] A generated internal ID may become unstable if canonical names change. -> Prefer explicit IDs and persist generated IDs through the override registry before relying on them across historical runs.
- [Risk] Strict mode may expose many existing data-quality issues. -> Report all failures with ETF, source row, attempted strategies, and missing fields so corrections can be added incrementally.

## Migration Plan

1. Add the override document and exchange alias configuration with initial entries for known collisions.
2. Implement resolver and snapshot fields while retaining non-strict warning behavior.
3. Regenerate fixture snapshots and validate that canonical names and IDs are present.
4. Switch frontend aggregation to canonical identity with a compatibility fallback only for legacy snapshots.
5. Run strict ingestion against all fixtures, correct or explicitly classify failures, then enable strict mode in publishing automation.
6. Roll back by using the previous ingestion command and frontend revision; no destructive data migration is required because snapshots are regenerated artifacts.

## Open Questions

- Which authoritative external company identifier, if any, should be adopted when the security master gains one (for example LEI)?
- Should strict mode require every classification field, or only resolvable identity plus the fields required by current reports?
- Should corrected source identifiers be retained as separate instrument fields in addition to the canonical instrument fields?
