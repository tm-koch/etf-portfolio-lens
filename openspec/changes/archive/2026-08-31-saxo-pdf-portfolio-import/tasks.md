## 1. Importer Foundation

- [x] 1.1 Add a pinned PDF.js browser dependency and worker configuration compatible with the static GitHub Pages deployment.
- [x] 1.2 Add Portfolio-tab drag-and-drop and file-selection controls with accessible status and error surfaces.
- [x] 1.3 Define normalized imported-position and parser-result models separate from the persisted portfolio state.

## 2. Saxo PDF Parsing

- [x] 2.1 Extract PDF page text incrementally in the browser and detect Saxo Bank report markers.
- [x] 2.2 Identify the CHF and EUR `Bestände` sections and parse ISIN-anchored ETF rows with German numeric formatting.
- [x] 2.3 Validate extracted ISIN, shares, price, currency, and market value fields and retain row-level warnings for incomplete data.
- [x] 2.4 Match extracted rows against the current catalog by normalized ISIN and mark unknown rows as unmatched and non-applicable.
- [x] 2.5 Add parser tests covering the supplied Saxo CHF/EUR text shape, duplicate/malformed rows, unsupported documents, and unmatched ISINs.

## 3. Review And Portfolio Replacement

- [x] 3.1 Build an editable import review dialog showing match status, inclusion, shares, price, currency, calculated value, and CHF-normalized value.
- [x] 3.2 Recalculate `shares * price` and fixed EUR-to-CHF normalization immediately after review edits.
- [x] 3.3 Apply only valid included catalog matches and replace the existing portfolio atomically on confirmation; preserve it on cancel or invalid confirmation.
- [x] 3.4 Persist imported valuation fields with backward-compatible local-storage normalization and restore them on reload.

## 4. Value-Based Portfolio Calculations

- [x] 4.1 Extend share-link encoding, decoding, and validation to preserve optional imported valuation fields without breaking older links.
- [x] 4.2 Update Portfolio weights, comparison rollups, and aggregated company exposure to use valid CHF-normalized values with the documented share-count fallback.
- [x] 4.3 Update Portfolio copy and rendered values so imported monetary weighting and the fixed EUR=CHF assumption are understandable.

## 5. Verification And Documentation

- [x] 5.1 Add web contract and behavior tests for import controls, review editing, replacement semantics, persistence, sharing, and value-based weighting.
- [x] 5.2 Run focused importer tests and the full existing test suite.
- [ ] 5.3 Verify desktop and mobile file selection, review interaction, unmatched-row handling, cancellation, replacement, reload persistence, and the supplied Saxo report shape in a browser.
- [x] 5.4 Document the supported Saxo PDF format, local-only processing, fixed currency assumption, and future broker-extension boundary.
