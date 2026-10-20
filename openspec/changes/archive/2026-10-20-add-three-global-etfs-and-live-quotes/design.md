# Design

## Context

See [proposal.md](proposal.md) for motivation and [the spec deltas](specs/) for the required behavior. The ingestion pipeline already parses the supplied iShares CSV fixtures with `ishares_csv_v1` and the UBS OpenXML workbook with `ubs_xml_xls_v1`; the latter is detected by its file signature. Normalization already supports the relevant weight columns and preserves UBS `Securities` labels. The Swiss CSV quote parser accepts CHF, EUR, and USD, but quote URL formatting and validation currently support only ISIN and ticker placeholders.

## Goals / Non-Goals

**Goals:**
- Reuse current parser families and deterministic fixture ingestion.
- Keep UBS Core MSCI World fixture-only so ordinary ingestion never calls its session-gated export control.
- Keep registry share-class currency distinct from intended listing and quote currency.
- Extend the existing Swiss URL-template contract while keeping the normalized quote artifact unchanged.
- Verify catalog generation and leave historical snapshots untouched.

**Non-Goals:**
- Add a new holdings parser or quote adapter.
- Change company identity matching behavior or valuation formulas.
- Rewrite historical snapshots or change the quote artifact schema.

## Decisions

- **Use existing parsers and supplied fixtures.** EIMI and IMEA use `ishares_csv_v1`; UBS uses `ubs_xml_xls_v1`. This matches current registry conventions and avoids a new parsing path. Validate all fixture rows and representative normalized holdings before publishing snapshots.
- **Make the UBS entry fixture-only.** Add explicit registry metadata that causes the pipeline to use its supplied fixture even when the run is not globally in fixture mode. Keep the product page as reference metadata, but do not attempt automated downloads or configure a live quote for this entry. This avoids an authenticated browser-only export flow; a custom token-backed fetcher is intentionally out of scope.
- **Keep instrument, share-class, and listing metadata separate.** Use each ISIN as the stable registry and quote-artifact key. Store the fund currency independently from listing ticker and quote currency; configure quote currencies as EIMI USD, IMEA CHF, and UBS WRDUSW CHF.
- **Add `{currency}` to the current template formatter.** Pass the configured quote currency to template formatting and to template validation. A template without `{currency}` remains valid for existing configurations, while the shared deployment template can use `{isin}{currency}4` for CHF and USD paths. An alternative would be separate secrets or adapter entries per currency; that duplicates configuration and is unnecessary for the existing path pattern.
- **Keep product URLs and fixture paths in the registry.** Verify that the two iShares download URLs return complete CSV data. UBS uses its supplied local fixture and retains its product page as reference metadata.
- **Regenerate only current derived data.** Run fixture ingestion and catalog generation for the additions without modifying files under `data/raw/` that represent existing snapshots.

## Risks / Trade-offs

- [An iShares URL may return HTML or a partial export] → Verify the response format and row completeness before accepting the registry URL; retain fixture-based checks in CI.
- [The external `SWISS_QUOTE_URL_TEMPLATE` value may not contain `{currency}`] → Update the deployed secret value and add tests for both CHF and USD formatting while keeping the secret name stable.
- [UBS holdings may become stale] → Keep the fixture-only status explicit in registry metadata and require a deliberate reviewed fixture replacement to refresh it.
- [New holdings may contain unresolved constituent identities] → Preserve source rows and existing diagnostics; do not add guessed identity overrides as part of ETF registration.

## Migration Plan

1. Add registry entries and fixture-only behavior, configure the two iShares quotes, implement currency placeholder formatting/validation, and add focused tests.
2. Validate the iShares holdings downloads, ingest all supplied fixtures, and regenerate the selectable catalog and current snapshots.
3. Update the external Swiss URL-template secret to include `{currency}`, then run the live quote workflow and verify the iShares quote currencies.
4. Roll back by removing the three new registry and quote entries and reverting the formatter change; existing quote templates without `{currency}` and historical snapshots remain compatible.