## Context

Selected ETF positions use the same semantic table markup across viewport sizes, with CSS grid rules changing the presentation. Wide mode gives the Shares input a fixed `84px` width, while the mobile override currently sets the input to `width: 100%`, causing the control to expand with its grid column. The mobile card should remain responsive, but the Shares control should retain the same visual width as its wide counterpart.

## Goals / Non-Goals

**Goals:**

- Keep the Shares input at the existing `84px` width in both wide and mobile layouts.
- Preserve the mobile position card's responsive outer width and existing Shares, Weight, and Remove arrangement.
- Add focused contract coverage for the shared fixed width.

**Non-Goals:**

- Changing card height, row structure, typography, or spacing.
- Changing position data, editing behavior, valuation calculations, or accessibility markup.
- Introducing a new CSS variable or component abstraction for one shared dimension.

## Decisions

- **Override mobile width with the existing fixed value.** The mobile `.position-input` rule will use `width: 84px` instead of `width: 100%`. This reuses the established wide-mode dimension and keeps the change limited to the mismatch identified by the user.
- **Retain mobile grid flexibility around the input.** The mobile grid columns and card width remain unchanged, so the card can still fit narrow viewports while the input no longer stretches unnecessarily.
- **Test the CSS contract rather than browser geometry.** The existing web contract suite already checks responsive position rules. It will assert the mobile fixed-width declaration and preserve the existing wide-width assertion.

## Risks / Trade-offs

- [Risk] A fixed `84px` input could consume more horizontal space on exceptionally narrow devices. -> Mitigation: the mobile control row already uses flexible grid columns, and `84px` is the established wide-mode control size.
- [Risk] A future change to the wide input width could make the mobile width inconsistent again. -> Mitigation: keep the mobile declaration explicit in the contract test alongside the wide declaration.

## Migration Plan

No data or deployment migration is required. Apply the CSS and contract-test change together; rollback consists of restoring the mobile `width: 100%` rule if narrow-device testing exposes a layout issue.

## Open Questions

None. The existing wide-mode width of `84px` is the intended shared dimension.