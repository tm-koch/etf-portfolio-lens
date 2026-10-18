# Design

## Context

The Explore view already aggregates selected ETF holdings into portfolio-weighted company exposure and renders a separate redundancy score box with a segmented bullet bar. The existing aggregation uses available snapshots and stable holding identity fallbacks; pairwise overlap coverage is computed from disclosed holding weights but is specific to ETF pairs. See `proposal.md` for motivation and `specs/portfolio-diversification-score/spec.md` for the behavior contract.

## Goals / Non-Goals

**Goals:**
- Calculate a deterministic effective number of companies from current look-through exposure.
- Keep scores useful when only part of the selected portfolio's holdings are disclosed, while clearly communicating coverage.
- Match the redundancy score box's layout and interaction conventions.

**Non-Goals:**
- Change the redundancy metric, its availability rules, or its thresholds.
- Add user-configurable diversification thresholds; the supplied rating boundaries are fixed.
- Change published catalog or snapshot schemas.

## Decisions

### Calculate the metric from aggregate company exposure

Use the existing selected-position aggregation as the source of company weights. Normalize each aggregated company weight by the total available company exposure, calculate HHI as the sum of squared normalized weights, then present its inverse. A separate pure calculation module, parallel to the existing redundancy calculation module, keeps the math independently testable without coupling diversification to redundancy behavior.

**Alternative considered:** Calculate HHI per ETF and combine scores. Rejected because it would not describe the selected portfolio's combined look-through exposure and would ignore cross-ETF company weights.

### Calculate coverage from disclosed holding weights

For each selected positive-allocation ETF, sum available holding exposure percentages and multiply by that ETF's normalized portfolio allocation. Sum these contributions for portfolio coverage, bounded to 0-100% for display. A selected ETF with no usable snapshot contributes zero coverage. Continue to calculate the score over the disclosed company exposure; show a coverage warning whenever the resulting coverage is incomplete.

**Alternative considered:** Reuse pairwise overlap coverage records. Rejected because those records are pair-specific and are not available or necessary for a single portfolio-wide coverage value.

### Expand the score scale above 40

Keep a 0-40 baseline scale and set the maximum to the effective number when it exceeds 40. Position the marker against that maximum while retaining the fixed rating boundaries at 5, 10, 20, and 40. This prevents scores such as 50 from being clipped while preserving the attachment's interpretation of 40 as the threshold for Highly Diversified.

**Alternative considered:** Clip the bar at 40 and show `40+`. Rejected because it would not position a score of 50 at its actual value as requested.

### Follow the redundancy score presentation

Render a new box after pairwise product overlap, with the exact title `Diversification score (1/HHI)`, a prominent numeric effective number, and a localized color-coded verdict badge matching the redundancy score treatment. Keep the segmented bullet bar free of textual rating-band labels; retain the marker, endpoints, and accessible scale label. Localize all visible and assistive text in the supported locales. At smartphone widths, the partial-coverage warning may be visually hidden but remains available to assistive technology.

**Alternative considered:** Place the metric beside redundancy. Rejected because the requested position is below product overlap and the current Explore layout presents its analysis boxes in sequence.

### Keep score markers and scale endpoints distinct

Use each score's existing localized rating string as the marker's native hover tooltip, and expose the existing localized rating label from every colored bar section on hover. Align each maximum endpoint label with the track's right edge without an extra horizontal inset. The 14px vertical track-to-endpoint gap keeps the marker from colliding with its number; apply this shared endpoint treatment to both score bars.

Keep endpoint values below the tracks with the existing left/right alignment. Use a 14px gap between each track and its endpoint row to clear the marker's 7px lower overhang. Do not show a separate written rating-label row beneath the redundancy bar; its segments expose those labels on hover instead.

## Risks / Trade-offs

- Partial holdings may not represent the undisclosed portion's company distribution; the effective number can therefore differ from the whole portfolio's true breadth. The coverage warning makes this limitation explicit.
- Ambiguous or unmatched company identities can split one issuer into multiple exposure keys and inflate the effective number. Reuse the existing identity resolution and retain current data-quality warnings; improving identity matching is outside this change.
- A scale that expands beyond 40 makes bar lengths less comparable across portfolio selections. Keep the numeric value and fixed rating visible so the dynamic endpoint does not obscure interpretation.
- Small rounding differences in disclosed weights can produce coverage just below 100%. Treat coverage at or above 99.995% as complete to match two-decimal warning precision; larger shortfalls remain visible and trigger the warning.

## Migration Plan

No data migration or catalog schema change is required. Deploy the client-side calculation, UI, localization, and focused tests together. Rollback consists of removing the new Explore box and calculation module; existing redundancy and pairwise-overlap behavior remains unchanged.