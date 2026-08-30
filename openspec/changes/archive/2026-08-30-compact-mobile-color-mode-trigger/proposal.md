## Why

On compact mobile screens, the selected color-mode label consumes useful horizontal space in the top-right utility area even though the control is already identifiable by its icon and accessible name. Keeping the trigger icon-only on compact mobile makes the utility lighter while preserving labeled choices when the user opens the mode menu.

## What Changes

- On viewports at or below the existing 760px compact-mobile breakpoint, hide the selected mode's visible text in the color-mode trigger and retain its icon.
- Keep the trigger's accessible label and tooltip descriptive of the selected mode.
- Keep Bright, Automatic, and Dark menu options visible with both icon and text when the menu is opened.
- Preserve the current immediate menu close after a mode is selected.
- Leave desktop and wider tablet trigger presentation unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `global-color-mode-selector`: Restrict the icon-only trigger presentation to compact mobile while preserving labeled menu options and accessibility semantics.

## Impact

- `web/styles.css`: Add compact-mobile-only trigger text visibility and sizing rules.
- `web/app.js`: Preserve or adjust the trigger markup so its visible label can be hidden without removing the accessible name.
- `tests/test_web_contract.py`: Add contract assertions for mobile-only icon presentation and labeled menu alternatives.
- `openspec/specs/global-color-mode-selector/spec.md`: Add the compact-mobile presentation requirement.
- No API, data, dependency, persistence, or desktop-layout changes.