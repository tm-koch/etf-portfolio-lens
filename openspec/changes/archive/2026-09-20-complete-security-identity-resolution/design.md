## Context

The normalizer currently attempts exact ISIN, ticker plus exchange, contextual ticker, name, and alias matching. Provider exports can omit ISINs, reuse short tickers across venues, or provide names that correspond to multiple security-master records. The existing override registry and snapshot provenance are the established extension points.

The review queue identified four exact-name collisions, 37 ticker/context conflicts, and a set of missing-ISIN rows with externally supplied mappings. Provider context is authoritative for describing the source row, but the verified ISIN is authoritative for instrument identity. Raw provider fields must remain unchanged for auditability.

## Goals / Non-Goals

**Goals:**

- Resolve reviewed holdings with exact ISIN overrides and stable canonical company identities.
- Keep instrument identity, company aggregation identity, provider context, and security-master provenance distinct.
- Preserve explicit exclusions for liquidity-fund rows.
- Make venue-label discrepancies visible without blocking a verified identity.
- Reduce ambiguous and unmatched diagnostics through fixture-based regression tests.

**Non-Goals:**

- Inferring identities from ticker alone when no verified ISIN or context decision exists.
- Replacing the external security master or changing its venue labels globally.
- Reclassifying non-company instruments as companies.
- Reworking unrelated frontend navigation or valuation behavior.

## Decisions

### Use exact-ISIN overrides as the resolution boundary

Each reviewed provider identity will be represented by an override keyed by the provider context and/or provider holding name, setting the verified ISIN, canonical name, and stable company ID. Exact-ISIN selectors take precedence after an earlier context selector supplies the ISIN. This reuses the existing registry and avoids changing generic matching heuristics.

**Alternative considered:** add ticker aliases to the security master. Rejected because ticker aliases cannot safely distinguish reused listings, share classes, or depositary receipts.

### Preserve provider context separately from identity

Normalization will retain the provider exchange, country, and raw source fields even when the security-master record has a different venue label. For `QIA`, the provider context remains Deutsche Börse Xetra / Germany, the identity is Qiagen NV with ISIN `NL0015002SN0`, and the LSE label is recorded as a provenance discrepancy.

**Alternative considered:** overwrite provider exchange with the security-master exchange. Rejected because it destroys source evidence and can make a correct instrument appear to come from the wrong venue.

### Treat reviewed exclusions as explicit non-company rows

`ICSEAGD` and `ICSSAGD` remain representable in snapshots but are excluded from company identity validation and aggregation. No fabricated company ID or equity identity will be assigned.

**Alternative considered:** map liquidity funds to their provider names as companies. Rejected because it pollutes company exposure results.

### Validate through regenerated fixtures and diagnostics

After overrides are added, rerun fixture ingestion and verify exact identity fields, status transitions, retained source fields, conflict counts, and catalog generation. Tests will cover each distinct resolution pattern rather than only the individual rows.

## Risks / Trade-offs

- [A supplied ISIN may be valid for a different venue or instrument than the provider row] -> Preserve provider context and record the discrepancy; require exact-ISIN review before adding any mapping.
- [A provider identifier may later be reused for a different security] -> Scope overrides with provider name, exchange, country, and holding context where available.
- [Generated snapshots may contain large formatting diffs] -> Regenerate only through the existing fixture pipeline and validate the staged diff before publication.
- [Unresolved rows may remain after the reviewed mappings] -> Keep them as explicit diagnostics and report the residual identifiers rather than silently guessing.

## Migration Plan

1. Add reviewed mappings and explicit exclusions to the version-controlled override document.
2. Extend or adjust normalization provenance only where required to represent source-versus-master venue differences.
3. Regenerate fixture snapshots and the web catalog.
4. Run focused identity tests followed by the full test suite.
5. If validation fails, revert the new override entries and generated artifacts together; do not retain partially regenerated snapshots.

## Open Questions

- Which exact ISIN and canonical identity should resolve the four name-only collisions and the 37 ticker/context conflicts not covered by the current review responses?
- Should the security-master venue label for `NL0015002SN0` be corrected locally, or should the discrepancy remain provenance-only?
