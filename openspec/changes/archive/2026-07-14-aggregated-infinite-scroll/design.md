## Context

The aggregated tab already computes and ranks the holdings list. The new requirement is to present that ranked list in a progressive way so the user sees a manageable initial subset and can scroll to reveal the remaining holdings on demand.

This is a front-end interaction change. It should not alter the aggregation data model, the ranking order, or the underlying holdings calculation.

## Goals / Non-Goals

**Goals:**
- Show the top 20 aggregated holdings initially.
- Append additional holdings as the user scrolls downward.
- Preserve the existing ranking order and row content.
- Keep the interaction lightweight and predictable.

**Non-Goals:**
- No changes to aggregation formulas or ranking logic.
- No backend pagination or API changes.
- No redesign of the aggregated analytics cards or warnings panel.

## Decisions

1. Use client-side incremental rendering of the already computed ranked list.
   - Rationale: the full list is already available after aggregation, so incremental display is enough to improve usability without adding data-fetch complexity.
   - Alternatives considered: backend pagination; rejected because there is no remote data source and it would add unnecessary complexity.
   - Alternatives considered: render the full list and rely on browser native scrolling only; rejected because the user explicitly wants a progressive reveal behavior.

2. Trigger loading with a scroll sentinel near the end of the list.
   - Rationale: it avoids manual pagination controls and matches the requested infinite-scroll behavior.
   - Alternatives considered: explicit "Load more" button; rejected because it changes the interaction pattern and adds friction.
   - Alternatives considered: scroll event polling; rejected because it is less efficient and harder to reason about than a sentinel.

3. Keep the batch size fixed at 20 items for the first render and subsequent appends unless the list is exhausted.
   - Rationale: a stable chunk size is easy to reason about and preserves the “top 20 by default” behavior exactly.
   - Alternatives considered: dynamic chunk sizes; rejected because they make the interaction less predictable.

## Risks / Trade-offs

- [Very small viewports may still require a lot of scrolling] → Mitigation: the initial 20-item cap keeps the first paint manageable, and progressive loading prevents the page from becoming too dense at once.
- [Scroll sentinel logic can be fragile if the list layout changes] → Mitigation: keep the sentinel attached to the aggregated list container and verify the behavior in the browser.
- [Users may expect jump-free positioning when new rows append] → Mitigation: append below the current viewport without reordering or replacing existing rows.

## Migration Plan

No migration is required.

1. Update the aggregated holdings rendering to render the first 20 items only.
2. Append more holdings when the scroll sentinel becomes visible.
3. Verify the full ranked list appears by continuous scrolling.
4. Roll back to full rendering if the progressive load introduces instability.
