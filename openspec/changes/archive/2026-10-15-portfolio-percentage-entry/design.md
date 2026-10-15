## Context

The Portfolio tab persists a `portfolioMode` of `full` or `percentage`. Full mode uses share counts and optional valuation data; percentage mode already powers private shared portfolios using relative units stored in the existing `shares` field. Existing helpers derive position weights, and the percentage renderer avoids absolute valuation resolution. The missing capability is a local, user-selectable way to enter a portfolio directly as relative weights.

## Goals / Non-Goals

**Goals:**
- Let users choose shares-based entry or relative allocation entry and persist that choice.
- Convert a populated shares-based portfolio to its currently derived normalized weights when entering allocation mode.
- Reuse existing percentage-mode calculations and privacy-safe private-share serialization.
- Avoid fabricating share counts when leaving relative allocation mode.

**Non-Goals:**
- Convert relative weights into actual shares or monetary values.
- Add a target-investment-amount workflow or new valuation service.
- Change existing share-link formats or imported-portfolio semantics.

## Decisions

- **Reuse the existing `percentage` portfolio mode.** The mode already suppresses valuation UI, computes weights from relative units, and supports private links. A separate mode or second weight field would duplicate behavior and complicate persistence.
- **Convert on entry using existing weight derivation.** For a shares-based portfolio, calculate each position's current weight with the existing valuation-aware weighting logic, then persist only its ISIN and relative weight units. This preserves its current distribution while dropping absolute valuation fields from percentage mode. An empty portfolio remains empty.
- **Treat entered values as relative weights.** The entered units need not total 100; all displayed weights and analysis normalize each position by the sum of non-negative units. The editor should communicate relative allocation semantics and retain decimal entry.
- **Zero shares when leaving allocation mode.** There is no unique mapping from relative weights to absolute share counts. Selecting Shares immediately retains every selected ETF but sets its share count to zero. This avoids inventing quantities and avoids an interruptive confirmation; the relative distribution is intentionally discarded.
- **Keep persisted and shared formats compatible.** Continue storing `mode: 'percentage'` and `{ isin, shares }` relative units, so existing private links remain valid. Existing legacy portfolio records without a mode continue to load as full portfolios.

## Risks / Trade-offs

- [Switching back discards relative weights] → Retain every selected ETF and show zero in each Shares input so the new state is explicit without a modal prompt.
- [The input field can be mistaken for literal percentages] → Label it as allocation and explain that entered values are relative weights normalized for analysis; show the normalized Weight column.
- [Weight conversion depends on available valuations] → Reuse the current weighting fallback behavior, which falls back to share counts when a usable valuation is unavailable.
- [Existing percentage mode has private-sharing language] → Keep user-selected local allocation and shared private portfolios on the same calculation path, but ensure hints identify relative units rather than claiming the local portfolio came from a private link.

## Migration Plan

No data migration is required. Existing saved portfolios and share payloads retain their current shapes; legacy entries default to shares mode. The selected mode continues to persist through the existing portfolio state record. Rollback can remove the selector and transition behavior while retaining compatibility with persisted percentage-mode and private-link data.

## Open Questions

- None. Returning to shares mode intentionally retains the selected ETFs at zero shares; target-amount conversion is outside this change.
