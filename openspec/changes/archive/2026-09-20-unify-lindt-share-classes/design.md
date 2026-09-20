## Context

The security master has two distinct Lindt instruments: `CH0010570759` (`LISN`) named `Chocoladefabriken Lindt & Spruengli AG N`, and `CH0010570767` (`LISP`) named `Chocoladefabriken Lindt & Spruengli AG Part`. Normalization currently derives a company ID from each canonical name, producing two IDs. The web aggregation path uses `holding.security.company_id` as its primary key, so the share classes remain separate in company exposure views.

The existing override registry already supports exact-ISIN identity corrections, and normalized snapshots preserve the raw provider row in `provenance.source_fields`. This change can therefore be implemented as identity data plus regression coverage, without changing aggregation or frontend code.

## Goals / Non-Goals

**Goals:**

- Assign both verified Lindt share-class ISINs to one stable company ID: `chocoladefabriken-lindt-spruengli-ag`.
- Use `Chocoladefabriken Lindt & Spruengli AG` as the canonical display name for both instruments.
- Preserve each share class's ISIN, ticker, source fields, weights, prices, and provenance.
- Make current published snapshots aggregate both share classes under one company key.
- Validate that unrelated securities do not receive the Lindt identity.

**Non-Goals:**

- Do not merge the two securities into one instrument or alter their tickers, ISINs, prices, or share counts.
- Do not change frontend aggregation logic or introduce name-based grouping.
- Do not rewrite historical snapshots unless a separate historical-data migration is requested.
- Do not apply the alias to other Lindt entities or securities without verified ISINs.

## Decisions

1. **Use two exact-ISIN override entries.** Each share class has a distinct ISIN, so the override registry needs one selector for `CH0010570759` and one for `CH0010570767`. Exact ISIN matching is safer than ticker or name matching and preserves the distinction between instruments.

2. **Share one company ID and canonical name.** Both overrides set `company_id` to `chocoladefabriken-lindt-spruengli-ag` and `canonical_name` to `Chocoladefabriken Lindt & Spruengli AG`. This directly aligns with the web's existing company aggregation key.

3. **Leave security-master and provider data untouched.** The override changes normalized identity fields only. Raw provider names remain in `source_fields`, and the source/security-master match remains visible in provenance.

4. **Regenerate only current catalog-backed snapshots.** The current catalog points to `2026-09-20`; regenerate the current snapshots containing either ISIN and validate the catalog references. Historical snapshots remain immutable to avoid rewriting prior observations.

5. **Test at normalization and snapshot boundaries.** Add focused tests for both exact ISINs, shared identity, preserved source fields, and unrelated-ISIN isolation. Validate generated snapshots contain separate instruments with a shared company key.

## Risks / Trade-offs

- [Risk] A future security-master naming change could reintroduce a different identity if the override is removed. → Mitigation: keep the verified exact-ISIN entries in the version-controlled override registry.
- [Risk] Historical snapshots will continue to show separate company IDs. → Mitigation: document current-snapshot scope and treat any historical rewrite as a separate migration decision.
- [Risk] Grouping distinct share classes may obscure share-class composition in company-level views. → Mitigation: retain the original ticker and ISIN on every holding and only unify the company aggregation key.

## Migration Plan

1. Add both exact-ISIN overrides and focused regression tests.
2. Regenerate current snapshots for all catalog-backed ETFs containing either Lindt share class.
3. Validate shared company IDs, canonical names, preserved provenance, and unchanged instrument fields.
4. Run focused and full test suites.
5. Roll back by removing the overrides and regenerating a future snapshot; do not mutate historical snapshots.

## Open Questions

None. The two ISINs and requested canonical company name are confirmed.
