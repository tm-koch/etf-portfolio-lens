## Why

The live-market-data workflow currently fetches and publishes the validated artifact but gives reviewers no readable view of the retrieved prices or exchange rates in the GitHub Actions run. A rendered summary will make each refresh auditable at a glance while preserving the existing JSON artifact and secret-handling boundaries.

## What Changes

- Generate a Markdown workflow summary after `data/live_prices.json` has been validated.
- Render one table containing every configured quote's ISIN and price including its currency.
- Render a separate exchange-rate table containing each retrieved FX pair and rate.
- Show `Unavailable` for quotes or FX rates whose artifact status is unavailable rather than omitting them.
- Expose the generated Markdown as a reusable step output while also writing it to GitHub's rendered step summary.
- Include the artifact generation timestamp and preserve the existing publication flow.

## Capabilities

### New Capabilities

### Modified Capabilities

- `scheduled-market-data-publication`: Successful live-data workflow runs also render the validated quote and FX results in the GitHub Actions summary and expose the same Markdown as a step output.

## Impact

- Affects `.github/workflows/live-market-data.yml` and likely adds a small report-generation helper or test fixture.
- Adds workflow contract or unit coverage for Markdown formatting, unavailable-value handling, and GitHub Actions summary/output wiring.
- Does not change `data/live_prices.json`, quote fetching, valuation behavior, publication branching, or secret values.
