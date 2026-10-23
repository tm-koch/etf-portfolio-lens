# Design

## Context

See [proposal.md](proposal.md) for the motivation and [the spec delta](specs/comparison-donut-spacing/spec.md) for the observable requirement. Each comparison card is a vertical grid of header, chart frame, and legend. The current header-to-frame distance is formed by the card's grid gap and the header's bottom margin; the mobile grid gap is separately configured.

## Goals / Non-Goals

**Goals:**
- Meet the same maximum 8px text-to-frame gap for Sectors, Regions, and Currencies at every supported viewport width.
- Preserve the existing chart-frame-to-legend spacing and chart dimensions.

**Non-Goals:**
- Change donut sizing, legend layout, or card padding.
- Change spacing elsewhere in the comparison panel or other views.

## Decisions

- Adjust only the header-to-frame relationship in the shared comparison card styles. Account for the different desktop and mobile grid gaps so their effective distance is at most 8px.
- Keep the existing card grid gap for the frame-to-legend relationship. Reducing the grid gap globally was considered but would also compress the legend and alter the established chart stack.
- Keep the three comparison cards on the same shared styling path rather than adding per-metric overrides; this prevents spacing drift between Sectors, Regions, and Currencies.

## Risks / Trade-offs

- [Header spacing compensation can drift if the card grid gap changes later] → Keep the relationship centralized in shared comparison styles and cover the effective gap in regression checks.
- [A wrapped description could expose unintended overlap] → Validate the gap with the existing localized text and responsive layouts; the header remains in normal document flow.

## Migration Plan

No data or API migration is required. Update the shared CSS and regression coverage; rollback consists of reverting those scoped changes.
