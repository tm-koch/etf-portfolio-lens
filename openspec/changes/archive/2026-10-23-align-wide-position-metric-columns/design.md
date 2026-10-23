# Design

## Context

The wide layout renders each position row as an independent CSS grid. Its metric tracks are content-sized per row, so different ticker names and values shift the Price, Value CHF, and Weight columns. The current mobile layout uses a separate reflow and is out of scope. See proposal.md for motivation and the spec delta for the behavior contract.

## Goals / Non-Goals

**Goals:**
- Give every wide position row the same left-aligned start positions for Price, Value CHF, and Weight.
- Keep identity, Shares, Remove, position editing, valuation display, and mobile reflow behavior intact.

**Non-Goals:**
- Change metric order, labels, value formatting, or percentage-only portfolio behavior.
- Redesign the position boxes or their mobile layout.

## Decisions

- Use one shared set of wide grid tracks for all share-based position rows instead of allowing each row's content to size its metric columns independently. This directly addresses the source of the drift while retaining each row's existing box and Remove area.
- Keep percentage-only rows on their existing reduced-column layout, and keep the mobile breakpoint rules independent. A single shared full-mode track definition for percentage rows would reserve empty Price and Value CHF space and change their established presentation.
- Validate the left edges of both metric labels and values across rows using different names, currencies, value lengths, and unavailable values. Text alignment within independently sized rows alone is insufficient because it does not establish shared column starts.

## Risks / Trade-offs

- **Fixed or constrained tracks may need more horizontal room for some currencies or labels** → Preserve the existing wide wrapper's overflow behavior and verify representative long values without changing the mobile breakpoint.
- **A wide-only selector could accidentally affect compact layouts** → Keep the shared tracks inside the existing wide media query and verify at widths on both sides of the breakpoint.
