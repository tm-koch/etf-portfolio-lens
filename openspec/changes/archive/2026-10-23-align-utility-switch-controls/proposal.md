# Proposal

## Why

The language and color-mode triggers share the app utility row but their compact button boxes have different widths and heights, making them look like mismatched controls. Matching their compact footprint will create a cleaner, aligned utility area without changing how language or color mode works.

## What Changes

- Give the collapsed language and color-mode triggers identical outer dimensions and vertical alignment at smartphone widths, using the existing compact color-mode trigger as the sizing reference.
- Preserve the full localized language name and icon-plus-label color-mode presentation on wider viewports, with the controls aligned vertically.
- Keep menu contents, keyboard behavior, accessible names, tooltips, and preference persistence unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `web-localization`: Specify the compact language trigger's dimensions and alignment relative to the adjacent color-mode trigger.
- `global-color-mode-selector`: Specify matching compact dimensions and alignment while retaining the existing responsive presentation and accessibility behavior.

## Impact

- Affects the utility-control styles in `web/styles.css` and responsive layout tests.
- No API, dependency, persistence, or menu-behavior changes.
