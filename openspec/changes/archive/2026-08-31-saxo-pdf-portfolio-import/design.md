## Context

The web app is a client-side vanilla JavaScript application. The Portfolio tab currently searches the published ETF catalog, stores positions in local storage, and uses share counts as the weighting proxy for Portfolio, Compare, and Explore calculations. The requested Saxo report contains text-based holdings tables on the CHF and EUR `Bestände` pages, including ISIN, quantity, current price, and market value. The importer must preserve privacy by processing the selected PDF in the browser and must avoid treating uncertain extraction as an automatic portfolio update.

## Goals / Non-Goals

**Goals:**

- Add a browser-native file drop/select workflow in the Portfolio tab.
- Use PDF.js to extract text from the selected PDF without uploading it.
- Detect Saxo Bank reports and parse the two supported holdings sections by ISIN anchors.
- Match rows against the published catalog by normalized ISIN.
- Present an editable review dialog for inclusion, shares, price, and currency before applying anything.
- Replace the existing portfolio atomically with confirmed supported rows.
- Persist imported price, shares, currency, and derived CHF value.
- Use normalized monetary position values as the weighting basis throughout the existing portfolio calculations.
- Keep unmatched and malformed rows visible as review warnings and exclude them from the applied portfolio.

**Non-Goals:**

- Supporting Excel, CSV, scanned/image-only PDFs, or non-Saxo brokers in this change.
- OCR or generic table understanding for arbitrary broker layouts.
- Live foreign-exchange rates; EUR to CHF is fixed at 1.0 for this first version.
- Uploading reports to a backend or storing the original PDF.
- Automatically merging imported rows into the existing portfolio.

## Decisions

1. **Use PDF.js in the browser.** PDF.js is suitable for text extraction and can run with a worker loaded from the same pinned CDN release. A server parser would add privacy and deployment costs, while a generic table library cannot reliably identify broker-specific layouts.

2. **Select the broker before parsing.** The extracted document text must contain Saxo Bank markers such as `Saxo Bank` and the supported holdings headings. The first adapter is Saxo-only; unsupported or unrecognized documents stop with an actionable error instead of being guessed as Saxo.

3. **Use ISINs as row anchors.** A normalized ISIN regex identifies instrument rows, while nearby extracted text and page boundaries provide the instrument name, currency, quantity, current price, and market value. The parser must validate numeric fields and retain source page/row context for review diagnostics.

4. **Use an intermediate import model.** Parsed rows remain separate from `state.portfolio` until confirmation. Each row carries `isin`, `shares`, `price`, `currency`, `value`, `valueChf`, `matchStatus`, and an inclusion flag. The review dialog edits this model and calculates `value = shares * price` and `valueChf` using the fixed currency conversion.

5. **Replace atomically on confirmation.** Confirming the review maps included, catalog-matched rows into the persisted position model and replaces the full existing portfolio in one operation. Canceling or closing the dialog leaves the prior portfolio unchanged.

6. **Make monetary value the weighting basis.** Positions with valid imported prices use `valueChf` for portfolio weights and all downstream exposure calculations. Manually added positions retain a deterministic fallback value based on shares until they receive an imported price, so existing manual workflows remain usable while imported portfolios become financially meaningful.

7. **Version persisted and shared position data.** Add optional imported fields without invalidating old local state or existing share links. New share payloads include imported fields when present; older payloads continue to load with the fallback weighting behavior.

## Risks / Trade-offs

- [PDF text order varies by viewer or export] -> Restrict parsing to Saxo text reports, use ISIN anchors and numeric validation, and require review before applying.
- [A PDF is scanned or has no extractable text] -> Show an unsupported-document error and keep the existing portfolio unchanged; defer OCR.
- [European number formatting is misread] -> Parse German separators explicitly and display every proposed value for user correction.
- [A catalog ETF is absent or its ISIN is malformed] -> Mark the row unmatched, prevent inclusion, and show the raw identifier in the review dialog.
- [Fixed EUR=CHF conversion becomes stale] -> Label the conversion assumption in the review UI and isolate it behind a conversion constant for later replacement.
- [Changing weights alters existing charts and Explore ordering] -> Update focused contract tests and make the value/fallback rule explicit in the UI and specification.
- [Large PDFs consume browser memory] -> Process pages incrementally and discard extracted page text after parsing; never retain the PDF binary after the import completes.

## Migration Plan

1. Add the PDF.js dependency and importer UI behind the Portfolio tab.
2. Extend position normalization to accept optional imported fields while preserving old `{ isin, shares }` local state and share links.
3. Add Saxo parsing, review, replacement, persistence, and value-based weighting tests.
4. Deploy as a backward-compatible frontend change; existing portfolios load with fallback weighting.
5. If the importer must be rolled back, remove the import entry point while retaining the tolerant position normalizer so existing imported local data is not destructive.

## Open Questions

- Whether a future release should replace the fixed EUR=CHF assumption with a user-entered or date-specific exchange rate.
- Whether additional Saxo report languages should be supported after the German report format is stable.
- Whether imported prices should eventually become timestamped valuations rather than the current position-level value.
