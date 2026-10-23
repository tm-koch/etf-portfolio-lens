# Design

## Context

The compact Explore table renders a visual header as a sibling of the horizontally scrollable body table. The visual header is sticky at `top: 0`; on wide screens, the primary navigation is also sticky at `top: 0` and has a higher stacking order. The header's existing table wrapper bounds its sticky range, and JavaScript synchronizes its horizontal position with the body table. See `proposal.md` for the motivation and the spec delta for observable behavior.

## Goals / Non-Goals

**Goals:**
- Keep the visual header visible below desktop navigation while preserving its current table-boundary and horizontal-scroll behavior.
- Preserve mobile behavior, where navigation is fixed to the bottom and the header can stick at the viewport top.

**Non-Goals:**
- Change the table's data, loading, semantics, or column sizing.
- Redesign or reposition primary navigation.
- Change sticky behavior for other tables or the standard Explore presentation.

## Decisions

- Use a shared CSS custom property for the desktop navigation's sticky height and use it as the compact table header's `top` offset. Keep the value aligned with the navigation's current 82px height (62px tab-button minimum height plus 20px vertical navigation padding), rather than raising the header's stacking order over the navigation.
- Override the header offset to `0` at the mobile breakpoint because mobile navigation is bottom-fixed. This avoids reserving a top gap where no top navigation is present.
- Keep the current header/body sibling structure and horizontal scroll synchronization. Moving the header into the horizontally overflowing element could make that element the sticky scroll container and would couple vertical stickiness to horizontal scrolling.
- Update the focused `test_web_contract.py` assertions for the shared desktop offset and mobile reset. Validate the layout at desktop and mobile widths to check the rendered header position, navigation clearance, table-end boundary, and horizontal alignment.

## Risks / Trade-offs

- [Navigation dimensions change without the shared offset being updated] → Keep the height in a shared CSS variable and assert the offset behavior in the contract test; verify the header against the rendered navigation at representative desktop widths.
- [CSS contract checks pass while real sticky positioning is still obscured] → Include a browser viewport check with page scrolling and horizontal table scrolling in the implementation verification.