# Proposal

## Why

The language selector currently exposes only locale abbreviations visually, even on wide screens where full language names would be easy to scan. Showing localized names in the expanded menu at every viewport, while reserving abbreviations for the collapsed mobile control, improves clarity without sacrificing phone-sized utility-bar space.

## What Changes

- Show the selected language's full localized name in the collapsed control on wide viewports.
- Show full localized names for all choices in the expanded menu at every viewport width.
- Show `EN`, `DE`, or `PL` only in the collapsed control at smartphone widths.
- Keep the selector free of a visible arrow or caret, and preserve its menu and accessibility semantics.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `web-localization`: Define the responsive visible-label behavior of the language selector.

## Impact

- `web/app.js` for the selected and option labels.
- `web/styles.css` for responsive visibility at the existing mobile breakpoint.
- Localization and web contract tests for full names, mobile abbreviations, and the no-arrow presentation.