## Context

The web application is a serverless static site. Its current portfolio model stores positions with an ISIN, share count, and optional imported price, currency, value, and CHF-normalized value. Portfolio weights are derived centrally from CHF values when available and otherwise from share counts. The Portfolio, Compare, and Explore views consume those derived weights.

The smallest private-sharing implementation should reuse the existing no-imported-price behavior. A private link will encode derived ETF percentages as synthetic share units, remove all absolute valuation fields, and carry an explicit mode marker. The recipient can then use the existing Shares inputs to change relative allocation units and recalculate all views.

## Goals / Non-Goals

**Goals:**

- Share ETF identities and relative allocation percentages without sharing absolute portfolio data.
- Preserve the existing full portfolio sharing behavior and version 1 links.
- Reuse the existing portfolio table, input handling, weighting helpers, and chart aggregation.
- Allow recipients to edit relative units for scenario analysis.
- Keep absolute summary cards visible while displaying `0` or `Not available` for data absent from private payloads.
- Keep the feature serverless and dependency-free.

**Non-Goals:**

- Authentication, access control, expiring links, or server-side privacy guarantees.
- A separate allocation editor or redesigned percentage-specific recipient GUI.
- Importing PDF holdings into private mode.
- Hiding ETF identities or allocation percentages from link recipients.
- Converting a recipient's edited private portfolio into actual share counts.

## Decisions

### Reuse `shares` as relative weighting units

Private payload positions will retain the existing `{ isin, shares }` shape, with `shares` containing the calculated percentage units. The payload will include `mode: "percentage"` so the meaning is explicit. This avoids introducing a second canonical numeric field and allows existing input events and rendering to continue working.

Alternatives considered:

- A separate `weightPct` field would make the data model clearer but would require parallel input, normalization, validation, and calculation paths.
- Overwriting only the rendered Weight cell would make the table disagree with charts and look-through calculations.
- Leaving Shares empty would require a hidden second source of truth and special editing behavior.

### Normalize private units through the existing weighting pipeline

Private positions will not include valuation fields. The weighting helper will use their synthetic `shares` units, and all portfolio calculations will continue to derive normalized weights from the common helper. If a recipient changes one unit, the total is recalculated and the edited units are normalized across the selected positions.

### Redact absolute fields at private-link creation and load

Private encoding will construct a new position array rather than serializing the local positions directly. Only ISIN and synthetic share units will be emitted. Decoding will reject or ignore valuation fields for private payloads so absolute data cannot enter the private state through the private contract.

### Preserve the current GUI with minimal explanatory feedback

The recipient will see the existing no-price table, including the Shares input and `Not imported` valuation cells. Private-mode feedback or hint text will explain that Shares represent relative weighting units, not actual holdings. No separate allocation table is introduced.

### Retain summary cards with unavailable values

The existing absolute cards remain in their current positions. In private mode, the Share units card displays `0` and the Total value card displays `Not available` (or the established zero formatter where the current UI contract requires it). No synthetic percentage units are presented as actual holdings or currency values.

## Risks / Trade-offs

- [Relative units may be mistaken for actual shares] -> Add explicit private-link feedback and portfolio hint text explaining the units.
- [Rounding percentage units may slightly change totals] -> Use sufficient decimal precision in the payload and test that displayed weights remain within an agreed tolerance.
- [Edited units may not sum to exactly 100] -> Treat units as relative values and normalize them for calculations while showing the existing derived Weight column.
- [A URL recipient can still see ETF identities and percentages] -> Describe the feature as private from absolute values, not confidential or access-controlled.
- [Future code may interpret synthetic shares as real holdings] -> Require and preserve the explicit percentage mode marker and centralize mode-aware weighting and summary behavior.
- [Version 1 decoders may not understand the new marker] -> Keep existing version 1 payloads unchanged and use a new supported payload version for private links.

## Migration Plan

1. Add private payload creation and validation alongside the existing version 1 full-share contract.
2. Keep local-storage arrays and version 1 shared links loading as normal portfolios.
3. Load the new private mode into state with valuation fields absent and persist it using the existing local storage mechanism plus mode metadata.
4. Deploy the static site; no backend migration is required.
5. Roll back by removing private-link creation/loading support; existing version 1 links and local portfolios remain unaffected.

## Open Questions

- Whether the private share action should be a second button or a small choice adjacent to the existing Share portfolio action.
- Whether private feedback should call the values `relative units`, `allocation units`, or `percentage units` while retaining the existing Shares label.
- The exact decimal precision and tolerance for private percentage encoding and normalization.
