## Why

The mobile navigation currently occupies more vertical space than necessary and gives inactive destinations the same bold emphasis as the selected destination. A more compact bar will preserve access to the three primary destinations while making the active destination easier to distinguish.

## What Changes

- Reduce the mobile navigation row height and internal padding.
- Reduce mobile navigation icon size, label font size, and icon-label spacing.
- Render inactive mobile labels and icons with the existing muted color and regular font weight.
- Render only the active mobile label and icon in accent blue with bold font weight.
- Preserve the existing icon-over-label arrangement, full-width fixed placement, safe-area handling, content clearance, and keyboard accessibility.
- Leave desktop navigation styling and destination behavior unchanged.

## Capabilities

### New Capabilities

### Modified Capabilities

- `bottom-navigation`: Add compact mobile sizing and distinguish active and inactive typography while preserving responsive placement and accessibility requirements.

## Impact

- `web/styles.css`: Update mobile-only navigation dimensions, spacing, icon sizing, label sizing, and font-weight rules.
- `openspec/specs/bottom-navigation/spec.md`: Add requirements for compact mobile geometry and active/inactive typography.
- No JavaScript, API, dependency, URL, persistence, or desktop layout changes.
