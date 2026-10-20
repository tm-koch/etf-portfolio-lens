# Tasks

## 1. Configure the WRDUSW Live Quote

- [x] 1.1 Add `IE00BD4TXV59` to `data/live_price_config.json` with `swiss_csv_v1`, CHF, and the existing Swiss quote-template secret; verify the loaded config contains the entry while the registry remains fixture-only.
- [x] 1.2 Extend live quote configuration tests for the WRDUSW adapter, currency, secret name, and the intentional fixture-only separation; run the focused configuration tests.

## 2. Add Safe Per-ETF Diagnostics

- [x] 2.1 Add ISIN and adapter context to quote fetch/parse failures without logging resolved URLs, credentials, arbitrary exception text, or response bodies; verify a missing-date response reports its ISIN and preserves the prior artifact.
- [x] 2.2 Add opt-in CLI debug logging for quote start and outcome using safe identifiers and stage summaries; test captured logs for expected ISIN context and absence of a secret URL and payload.

## 3. Integrate and Verify the Refresh Workflow

- [x] 3.1 Enable the CLI debug option in the live-market-data GitHub workflow and document the optional flag in the README; verify the documented invocation and workflow command use the supported option.
- [x] 3.2 Run focused live-market-data tests and the full test suite, then run `openspec validate add-wrdusw-live-quote-diagnostics --strict`; verify all checks pass and the output artifact remains unchanged on quote failure.
