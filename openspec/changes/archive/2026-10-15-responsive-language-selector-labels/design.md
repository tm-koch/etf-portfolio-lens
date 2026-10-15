# Design

## Context

The current selector renders locale codes in both the collapsed button and menu options. Full localized language labels already exist, and the app uses a 760px breakpoint for mobile presentation. See `proposal.md` and the `web-localization` delta for the intended behavior.

## Goals / Non-Goals

**Goals:**
- Keep the collapsed control compact on smartphone-width screens while making its selected language explicit on wider screens.
- Keep expanded menu choices equally identifiable at every width.
- Preserve the existing menu interaction and accessible names without a visual arrow.

**Non-Goals:**
- Change locale resolution, persistence, translation content, or menu interaction semantics.
- Add a new breakpoint, dependency, or JavaScript resize handler.

## Decisions

- **Use the existing 760px breakpoint.** CSS will show the selected full name above 760px and the locale abbreviation at 760px and below. This matches existing mobile utility-bar behavior and avoids a second definition of mobile viewport.
- **Keep expanded options as full localized names at all widths.** The option buttons will use the existing translated language labels. Hiding names and showing codes in the menu on phones was considered, but rejected because the user explicitly wants expanded choices to remain full names.
- **Use CSS to switch the collapsed label.** Render a name span and a code span in the trigger, then control their visibility with the existing breakpoint. This avoids JavaScript resize handling and keeps the button's accessible name independent of the visual abbreviation.
- **Do not add a caret or arrow.** The existing button, `aria-haspopup`, expanded state, and menu roles communicate and operate the interaction; a visible disclosure icon is unnecessary.

## Risks / Trade-offs

- [Longer names could widen or clip the menu] → Keep the menu content-sized with its existing minimum width and verify all three labels at desktop and phone widths.
- [A code shown on mobile could replace the accessible language name] → Preserve the full translated `aria-label` on the collapsed control and each menu option.
- [Breakpoint-specific styles could hide the wrong trigger span] → Verify collapsed and expanded states on both sides of the 760px breakpoint.

## Migration Plan

No data migration is required. Existing saved locale preferences and menu behavior remain unchanged. Rollback consists of restoring code-only trigger and menu labels.