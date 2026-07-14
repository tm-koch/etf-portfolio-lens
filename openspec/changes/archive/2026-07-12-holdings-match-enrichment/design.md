## Context

The current ingestion backend can normalize holdings and enrich missing fields from `data/tickers.csv`, but unresolved holdings are only surfaced through a generic warning. That leaves the generated snapshot without enough information to explain why a holding could not be matched, and it prevents consumers from seeing whether the missing piece was an ISIN, ticker, exchange, or another field.

The immediate goal is to make match outcomes explicit in the output and to fill an absent ISIN when the security master can resolve the holding uniquely from the ticker.

## Goals / Non-Goals

**Goals:**
- Record exactly which input elements were missing for holdings that could not be fully matched.
- Preserve match attempts and fallback order in the output provenance.
- Populate a missing ISIN from `data/tickers.csv` when the ticker uniquely identifies a security master record.
- Keep the current normalization pipeline and snapshot structure stable for already matched holdings.

**Non-Goals:**
- Reworking the full security master model.
- Adding a user interface for reviewing match failures.
- Changing the source registry or download behavior.
- Introducing external matching services or fuzzy matching libraries.

## Decisions

1. **Represent matching as structured provenance**
   - Store match diagnostics in snapshot provenance rather than only in console output.
   - The record should expose missing elements, attempted fallback steps, and the final match status.
   - Alternative considered: keep warnings only in stderr. Rejected because the output file then loses the reason a record remained incomplete.

2. **Allow ticker-only ISIN enrichment when the ticker is unique**
   - If a holding lacks an ISIN but its ticker matches exactly one security master record, copy the ISIN from `data/tickers.csv`.
   - If multiple records share the ticker, do not guess; keep the record unmatched and warn.
   - Alternative considered: require ticker plus exchange for every ISIN fallback. Rejected because the security master already contains enough unique ticker cases to resolve many holdings safely.

3. **Keep match fallback order deterministic**
   - The matching sequence should remain: ISIN, ticker plus exchange, ticker-only unique fallback, aliases.
   - This makes diagnostics comparable across sources and avoids hidden behavior changes.
   - Alternative considered: dynamic scoring across all fields. Rejected because it would be harder to explain why a record matched.

4. **Expose unresolved fields as a concise list**
   - The output should list the missing elements, not a prose explanation.
   - A list such as `["isin", "exchange"]` is easier to test and easier for downstream consumers to parse.
   - Alternative considered: free-form text warnings. Rejected because it is not stable enough for comparisons and tests.

## Risks / Trade-offs

- [Ticker-only fallback could create false positives if ticker duplicates exist] → Restrict fallback to unique ticker matches and warn on ambiguity.
- [More diagnostics increase snapshot size] → Keep the diagnostics object small and limited to missing elements, attempted methods, and status.
- [Downstream consumers may ignore the new diagnostics] → Preserve current fields and add the diagnostics object as an additive change.
- [Some unmatched holdings will still remain unresolved] → Continue to warn in the console so data quality issues remain visible during ingestion.

## Migration Plan

1. Add structured match diagnostics to the normalized holding output.
2. Extend security-master lookup to support unique ticker-only ISIN fallback.
3. Update the ingestion output and tests to verify missing-element reporting.
4. Validate the generated snapshots against the existing ETF fixtures.

Rollback strategy: since the change is additive, revert the diagnostics field and ticker-only fallback while keeping the existing snapshot schema intact if any ambiguity is discovered.

## Open Questions

- Should the diagnostics object live under `provenance` or as a top-level field on each holding?
- Should ambiguous ticker-only matches emit one warning per record or a batch summary at the end of the run?
- Should the fallback attempt order itself be stored in the output or only the final result?
