## Why

Users who want to explore portfolio distribution may know only relative allocations, not share counts or monetary values. The Portfolio tab already supports valuation-independent relative allocations for private shared portfolios, but users cannot directly enter or manage a local portfolio in that mode.

## What Changes

- Add a persistent Shares / Allocation (%) mode control to the Portfolio tab.
- Allow users to enter non-negative relative allocation weights; normalize them for displayed allocation and portfolio analysis without requiring the entered values to total 100.
- When switching from shares to allocation mode, convert the current positions to their derived portfolio weights.
- Reuse the existing percentage-only portfolio presentation and analysis behavior without resolving or showing absolute valuations.
- When leaving allocation mode, retain all selected ETFs and set their share counts to zero without a confirmation prompt.

## Capabilities

### New Capabilities
- `portfolio-allocation-mode`: Select and persist shares-based or relative-allocation entry, including conversion into relative weights and percentage-mode presentation.

### Modified Capabilities
- `portfolio-valuation-mode`: Percentage-mode valuation independence applies to user-selected allocation portfolios as well as private shared portfolios.

## Impact

- `web/app.js`, `web/index.html`, and `web/styles.css` for mode state, entry controls, transitions, and table presentation.
- Existing portfolio persistence, weight calculations, private-share serialization, and portfolio view rendering are reused where appropriate.
- Add or update focused web runtime and contract tests; no backend or dependency changes are expected.
