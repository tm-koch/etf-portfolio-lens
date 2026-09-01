## Why

Users need to share an ETF allocation for discussion or scenario analysis without revealing portfolio size, share counts, prices, or monetary values. A minimal private mode can reuse the existing no-price portfolio behavior by encoding each ETF's portfolio percentage as relative `shares` units, allowing recipients to adjust the values and explore alternatives.

## What Changes

- Add a private percentage-only option to portfolio sharing.
- Convert each selected ETF's current derived portfolio weight into relative `shares` units when creating a private link.
- Strip imported price, currency, value, and CHF-normalized value fields from private share payloads.
- Mark private payloads explicitly so their relative units are not confused with actual share counts.
- Load private links into the existing no-price portfolio editing experience without introducing a separate allocation GUI.
- Allow recipients to edit the existing Shares inputs to explore alternative allocations; calculations normalize the edited units across the selected ETFs.
- Keep absolute-value summary cards visible in private mode, but render share counts and monetary values as `0` or `Not available`.
- Preserve existing full portfolio share links and local portfolios.

## Capabilities

### New Capabilities

- `private-percentage-sharing`: Create, load, validate, and edit private percentage-only portfolio links without sharing absolute valuation data.

### Modified Capabilities

- `portfolio-sharing`: Extend the sharing contract with a private percentage-only payload while preserving existing full portfolio links and startup behavior.

## Impact

- `web/app.js`: portfolio share encoding/decoding, private-weight conversion, mode tracking, weighting behavior, summary rendering, and share feedback.
- `web/index.html`: private share action and any required status or explanatory text.
- `web/styles.css`: only minimal styling if the private share action needs it; the recipient portfolio table remains unchanged.
- `openspec/specs/portfolio-sharing/spec.md`: sharing requirements and payload validation.
- New focused web contract tests for private payloads, redaction, loading, normalization, editing, and summary values.
- No server-side service or new dependency is required.
