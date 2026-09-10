## Why

The import dialog's "Valuation after import" choice is applied only when the PDF import is confirmed, and existing imported positions cannot switch between live and broker-imported valuation afterward. This makes it appear that changing the choice has no effect and prevents users from reviewing or changing the valuation basis for an already imported portfolio.

## What Changes

- Add a portfolio-level valuation mode control for full portfolios with `latest` and `imported` options.
- Apply the selected mode consistently to selected-position prices, CHF values, weights, totals, and comparison-related portfolio calculations.
- Preserve imported broker fields so users can switch back to imported valuation without re-importing the PDF.
- Keep the import review choice as the initial mode for the newly confirmed portfolio.
- Persist the selected valuation mode across reloads and compatible portfolio sharing behavior.
- Add focused tests for switching modes, live quote and FX availability, imported fallback, persistence, and unavailable values.

## Capabilities

### New Capabilities

- `portfolio-valuation-mode`: User-controlled valuation basis for an imported full portfolio.

### Modified Capabilities

- `saxo-pdf-portfolio-import`: The import valuation choice becomes the initial value of a persistent portfolio-level mode, and the mode can be changed after confirmation.
- `portfolio-currency-display`: Portfolio price/value displays and source labels respond to the selected valuation mode.
- `live-market-data`: Hybrid valuation behavior is extended with an explicit user-selected mode while retaining imported fallback data.

## Impact

- Frontend state and persistence in `web/app.js`.
- Effective valuation selection in `web/valuation.js`.
- Portfolio and import controls in `web/index.html` and associated styles.
- Share payload normalization if the selected mode is included in full-portfolio shares.
- Runtime and contract tests covering import, valuation, persistence, and displayed source labels.
