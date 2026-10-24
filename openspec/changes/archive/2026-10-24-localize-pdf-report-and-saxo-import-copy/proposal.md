# Proposal

## Why

PDF section headings currently remain English in German and Polish reports, and the Top Companies table uses per-ETF portfolio contributions instead of the normalized contributor shares shown on the website. The Saxo import instruction also calls the source document a holdings report rather than using Saxo's transaction-and-balance-report terminology.

## What Changes

- Localize the PDF's numbered top-level section headings in English, German, and Polish while retaining the ETF Portfolio Lens brand name.
- Localize the footer's generation-time label using the same wording as the cover.
- Show each contributing ETF's percentage share of a company's total exposure in the PDF Top Companies matrix; keep the total portfolio contribution column and em-dash behavior for non-contributors.
- Update the Saxo import instructions to name the transaction and balance report in English, German, and Polish.
- Leave Saxo PDF recognition and parsing behavior unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-pdf-export`: Localize numbered section headings and define ETF contribution cells as each ETF's share of the company's total exposure.
- `saxo-pdf-portfolio-import`: Use the localized transaction-and-balance-report wording in the import instructions without changing parsing behavior.

## Impact

PDF rendering and report analytics in `web/pdf-report-renderer.js`, `web/pdf-export.js`, and `web/report-data.js`; Saxo import instructions in `web/index.html`; English, German, and Polish resources in `web/locales/`; and the related PDF, import-copy, and localization contract/runtime tests. No parser behavior, API, persisted data, dependencies, or portfolio calculations change.