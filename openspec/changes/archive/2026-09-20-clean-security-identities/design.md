## Context

The ingestion pipeline normalizes provider rows, applies identity overrides, consults a bundled CSV security master, and serializes both instrument and company identity into snapshots. The audit found 221 company-like same-ISIN name conflicts, including 202 with one unambiguous ACWD name, 19 without an ACWD occurrence, 50 missing-ISIN warnings, 62 ticker/context conflicts, 12 ambiguous matches, and a larger set of valid source ISINs absent from the security master.

The existing override registry already supports exact-ISIN selectors and complete overrides. The design must preserve provider fields for auditability, avoid merging distinct instruments, and keep cash, collateral, liquidity funds, and futures outside company identity resolution.

## Goals / Non-Goals

**Goals:**

- Establish one canonical company name and stable company ID for verified same-ISIN identity mappings.
- Use the ACWD name as the preferred canonical name for the 202 covered conflicts.
- Provide explicit alternatives for the 19 conflicts without ACWD coverage.
- Represent valid source ISINs absent from the security master as usable ISIN-only identities.
- Reduce misleading warnings while retaining diagnostics for genuine ambiguity and unresolved instruments.
- Preserve raw provider data, source names, instrument ISINs, and override provenance.

**Non-Goals:**

- Do not infer company identity from ticker alone.
- Do not merge different ISINs automatically merely because names look similar.
- Do not fabricate ticker, exchange, sector, or asset metadata for an ISIN-only row.
- Do not force liquidity funds, cash, collateral, or futures into company aggregation.
- Do not rewrite historical snapshots unless explicitly regenerated as part of the rollout.
- Do not replace the bundled security master in this change.

## Decisions

### Exact ISIN overrides are authoritative for verified identities

A complete exact-ISIN override will set `canonical_name` and `company_id`, and may supply verified classification fields when required. The original provider values remain in provenance. Exact ISIN is preferred over ticker, name, or exchange matching because it identifies the instrument without ticker collision risk.

Alternative considered: broad ticker or name aliases. Rejected because the audit contains repeated ticker collisions across European exchanges and different share classes.

### ACWD is the preferred naming source where uniquely available

For each same-ISIN conflict with exactly one ACWD name, the override will use that name as the canonical display name and derive or explicitly assign a stable company ID. The ACWD source name is a naming authority only; it does not replace the source ISIN or instrument-level data.

Alternative considered: choose the longest provider name. Rejected because descriptive length is not a reliable canonicality signal.

### Non-ACWD conflicts require explicit evidence

The 19 conflicts without ACWD coverage will receive overrides only after selecting a documented preferred source, such as the security master, issuer, exchange, or the most complete provider name. They will not be included in the automatic ACWD rule.

Alternative considered: choose the first provider encountered. Rejected because snapshot ordering is not an identity authority.

### ISIN-only is a first-class partial outcome

When a source row has a valid ISIN but no matching security-master record, normalization will retain the source name and ISIN, create a stable fallback identity, and mark the result as ISIN-only. Ticker and exchange remain empty unless supplied by a verified override or another trusted enrichment source.

Alternative considered: add hundreds of records directly to the bundled CSV. Rejected for this change because it couples a generated external dataset to local corrections and does not address provider naming policy.

### Diagnostics distinguish incomplete identity from non-company holdings

Warnings will identify whether a row is overridden, ISIN-only, unmatched, ambiguous, or excluded as non-company. Non-company rows remain available in snapshots and calculations but do not require company identity overrides.

Alternative considered: suppress all warnings for rows with an ISIN. Rejected because an ISIN can still be invalid, ambiguous, or associated with a wrong provider context.

### Rebuild generated outputs after identity data changes

After overrides and normalization changes are implemented, fixture ingestion and catalog generation will be rerun. Tests will assert identity behavior and warning classification; generated timestamp-only changes will not be treated as semantic data changes.

## Risks / Trade-offs

- [Risk] ACWD naming may be less complete than an issuer's legal name. -> Mitigation: preserve raw names and use ACWD only as canonical display text for the explicitly covered conflicts.
- [Risk] An incorrect exact-ISIN override can merge unrelated company identities. -> Mitigation: require verified ISIN evidence, review generated mappings, and test every override against all fixture occurrences.
- [Risk] ISIN-only fallback can make a holding appear resolved while ticker/exchange remain absent. -> Mitigation: expose an explicit partial status and retain missing-field diagnostics.
- [Risk] Security-master updates may change enrichment behavior over time. -> Mitigation: exact overrides take precedence and snapshots retain provenance and source version.
- [Risk] The override file may become large. -> Mitigation: keep it limited to verified exceptions and use a future supplemental security-data source if recurring coverage gaps justify one.
