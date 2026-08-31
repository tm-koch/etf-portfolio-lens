## Why

The Portfolio tab currently requires manual ETF selection and share entry, which is tedious and error-prone when the broker already provides the current holdings. A client-side Saxo PDF importer will let users transfer supported ETF positions into the app while reviewing and correcting the extracted values before they replace the local portfolio.

## What Changes

- Add a Portfolio-tab PDF drop/select entry point.
- Parse Saxo Bank transaction and balance reports in the browser using PDF.js.
- Restrict the first broker adapter to the Saxo holdings sections `Bestände - (account), CHF` and `Bestände - EUR`.
- Extract ISIN, ETF share count, current price, source currency, and calculated market value.
- Match imported rows to the ETF catalog by ISIN and reject catalog misses as unmatched rows rather than adding unknown positions.
- Show an editable review dialog before applying the import, including inclusion, shares, price, and currency controls plus calculated CHF value.
- Replace the existing portfolio only after the user confirms the reviewed import.
- Persist imported shares and price/currency data across reloads.
- Normalize imported values to CHF using the initial fixed assumption of `1 EUR = 1 CHF`.
- Use imported monetary values, rather than share counts alone, as the portfolio weighting basis for portfolio, comparison, and aggregated exposure views.

## Capabilities

### New Capabilities

- `saxo-pdf-portfolio-import`: Client-side Saxo holdings PDF detection, extraction, review, currency normalization, and portfolio replacement.

### Modified Capabilities

- `portfolio-sharing`: Extend persisted and shareable position data to preserve imported price and currency information while retaining ISIN-based identity validation.
- `compact-explore-preview`: Change portfolio exposure weighting from share-count weighting to imported position market-value weighting when imported values are available.

## Impact

- Frontend markup, styling, and state management in `web/index.html`, `web/styles.css`, and `web/app.js`.
- Browser dependency loading for PDF.js and its worker.
- Portfolio persistence and share-link normalization contracts.
- Portfolio, comparison, and Explore weighting calculations and their tests.
- No broker PDF is uploaded to a server; parsing remains local to the browser.
- Future broker support can be added through additional broker-specific adapters without changing the review/apply contract.
