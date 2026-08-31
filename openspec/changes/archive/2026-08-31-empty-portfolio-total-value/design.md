## Context

The Home tab renders five live summary cards from the selected portfolio state. Four cards already display numeric zero for an empty portfolio, but Total value currently bypasses the currency formatter and displays `Unavailable` when no finite imported valuation is present.

The change is limited to presentation logic and its regression contract. Existing populated-portfolio calculations, valuation imports, and currency formatting must remain unchanged.

## Goals / Non-Goals

**Goals:**

- Make an empty portfolio display Total value as `CHF 0.00`.
- Reuse the existing currency formatter so zero uses the same format as populated totals.
- Cover the empty-state behavior with a focused web contract test.

**Non-Goals:**

- Changing how imported valuation data is parsed or calculated.
- Adding valuation estimates from share counts or ETF prices.
- Changing other unavailable states in the application.

## Decisions

Use `formatChfValue(0)` for the empty Total value fallback in `updateSummary()`. This keeps currency formatting in one place and prevents the empty state from diverging from populated values. The alternative, hard-coding `CHF 0.00`, would duplicate formatting behavior and could drift if the formatter changes.

Extend the existing `home-tab` delta contract and web contract test to assert the currency-formatted zero. No new dependency or API is needed.

## Risks / Trade-offs

- [Risk] Positions may exist without imported valuation data and will also use the zero fallback even when share counts are non-zero. -> Mitigation: preserve the current finite-value filtering and limit this change to replacing the existing `Unavailable` fallback; valuation estimation remains out of scope.
- [Risk] A test that only checks source text could miss runtime rendering issues. -> Mitigation: retain the existing web contract suite and verify the exact fallback expression and formatter behavior in the focused test.

## Migration Plan

Update the fallback and regression test, run the focused and full test suites, then deploy through the existing static publishing workflow. Rollback consists of reverting the fallback and its test assertion.

## Open Questions

None.
