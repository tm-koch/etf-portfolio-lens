## Context

The backend is a registry-driven Python ingestion pipeline. iShares holdings exports are fetched as CSV and parsed by the existing `ishares_csv_v1` parser, then normalized through the security master and scoped overrides before dated snapshots and the web catalog are generated.

The supplied CSSMIM endpoint returns a valid CSV response, and `data/example/CSSMIM_holdings.csv` uses the same iShares table shape as existing fixtures. A temporary strict pipeline run produced 34 holdings totaling 100.0%, with all company rows resolved and cash/derivative rows excluded from company identity requirements.

## Goals / Non-Goals

**Goals:**

- Register iShares SMIM® ETF (CH) using ISIN `CH0019852802`, ticker `CSSMIM`, and the verified holdings endpoint.
- Preserve all valid fixture holdings and provider source fields.
- Verify strict identity enrichment, including existing scoped overrides and non-company exclusions.
- Publish a dated snapshot and catalog entry using the existing generation workflow.

**Non-Goals:**

- Add a new parser or fetcher.
- Change the security-master schema or general matching algorithm.
- Alter frontend warning semantics or portfolio behavior.
- Add live-only behavior that cannot be exercised offline.

## Decisions

1. **Reuse the existing iShares CSV parser.** The live response has content type `text/csv` and the expected `Ticker`, `Name`, `Sector`, and `Asset Class` headers. Reusing `ishares_csv_v1` avoids provider-specific branching and preserves the established parser contract. A custom parser was considered unnecessary because the fixture and live response match existing iShares exports.

2. **Use a registry entry as the integration boundary.** The entry will contain the fund identity, direct CSV URL, `csv` format, `ishares_csv_v1` parser ID, and fixture path. This keeps source selection, fixture mode, and catalog identity aligned with existing ETFs.

3. **Rely on existing enrichment behavior and overrides.** The verified fixture resolves through the repository security master and existing overrides for `HBAN`, `BAER`, `RO`, and `SCHP`. Cash, collateral, and futures rows remain normalized but do not require fabricated company identity. No new override is planned unless validation exposes a missing identity.

4. **Validate before publishing generated outputs.** Focused tests will cover fixture shape, row count, weight total, strict identity status, snapshot provenance, and catalog linkage. The full test suite will run before generated snapshot/catalog artifacts are accepted.

## Risks / Trade-offs

- **[Provider export changes its headers or row shape]** → Keep fixture coverage and parser structure assertions; live ingestion will fail explicitly if the expected table cannot be found.
- **[Security-master names drift from provider names]** → Preserve scoped override support and require strict-mode validation to expose unresolved company rows.
- **[Generated output date changes on regeneration]** → Generate all artifacts in one dated run and ensure catalog paths reference that same run date.
- **[Fixture represents a later or earlier portfolio date than live data]** → Treat the fixture as deterministic test data and preserve its as-of value in snapshot provenance; live refresh remains the normal production path.
