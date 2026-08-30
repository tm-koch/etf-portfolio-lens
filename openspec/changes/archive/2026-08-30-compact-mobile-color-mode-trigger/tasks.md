## 1. Compact Mobile Trigger

- [x] 1.1 Add a compact-mobile-only CSS rule that hides the color-mode trigger's visible label at widths up to 760px while retaining the selected mode icon.
- [x] 1.2 Preserve the trigger's accessible name, tooltip, menu alignment, and existing desktop/wider-tablet icon-and-text presentation.

## 2. Menu and Contract Coverage

- [x] 2.1 Confirm the rendered menu continues to expose Bright, Automatic, and Dark options with icons, visible text, and menuitemradio semantics.
- [x] 2.2 Update `tests/test_web_contract.py` to cover the mobile-only hidden trigger label and unchanged labeled menu options.
- [x] 2.3 Run the focused web contract tests and verify compact mobile and wider viewport behavior in the browser.

## 3. Specification Validation

- [x] 3.1 Validate the completed OpenSpec change and confirm the delta matches the `global-color-mode-selector` requirement.