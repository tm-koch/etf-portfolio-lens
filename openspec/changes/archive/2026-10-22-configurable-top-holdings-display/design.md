# Design

## Context

See `proposal.md` for motivation and the capability deltas for observable behavior. The Explore list already shares one ranked aggregation between the standard cards and compact table, renders unfiltered rows in batches, and searches the full ranking. The compact table's horizontal-overflow wrapper currently contains its header, which prevents reliable viewport-relative sticky behavior during page scrolling.

## Goals / Non-Goals

**Goals:**
- Reuse the existing ranked data and incremental loading for both presentations.
- Keep search independent from the unfiltered display cap.
- Keep the preview header aligned during horizontal table scrolling and bounded by the table during page scrolling.

**Non-Goals:**
- Change ranking, exposure calculations, or search matching.
- Add a user-facing portfolio preference or change backend data.
- Replace normal page scrolling with an internally scrolling table.

## Decisions

- Store a non-negative integer maximum in browser storage using the existing developer-preference pattern. Treat missing or invalid values as `0`; use zero as the unlimited sentinel. Keep the batch size independent from the maximum, and stop incremental loading when the positive maximum or ranked-list end is reached.
- Apply the maximum only to the unfiltered ranked rendering path in both presentations. Keep the complete ranked list as the source for matching and preserve original ranks, so a search can return a holding below the unfiltered limit. This avoids changing search semantics or truncating matches.
- Separate the compact table's visual sticky header from the horizontally scrolling body wrapper. Keep the sticky layer in a page-scrolling container bounded by the table section, and synchronize its horizontal offset with the body scroller. Use the same explicit column sizing for both layers; retain accessible header semantics in the primary table and keep any visual duplicate out of the accessibility tree.
- Prefer the separated header layer over moving vertical scrolling into the table wrapper, because the requested behavior is tied to normal page scrolling. A CSS-only sticky header inside the existing horizontal-overflow wrapper would still be constrained by that wrapper's scrollport.

## Risks / Trade-offs

- [Header and body columns can drift after resizing or content changes] -> Generate both layers from the same column definitions and update their measured widths when the table layout changes.
- [A duplicated visual header can create confusing screen-reader output] -> Preserve one semantic header in the primary table and mark only the visual duplicate as decorative.
- [A malformed or negative stored value could hide all rows or cause invalid limits] -> Validate the stored value as a non-negative integer and fall back to zero.
- [The sticky layer can overlap adjacent page content near the table boundary] -> Bound it by the table section and verify its start/end transitions during page-scroll browser tests.

## Migration Plan

No data migration is required. Existing users without a saved maximum receive the unlimited default. Rollback can remove the new setting and sticky-header layer; the additional browser-storage key can remain unused.
