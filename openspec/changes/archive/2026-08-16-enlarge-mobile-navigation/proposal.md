## Why

The mobile navigation was recently compacted, but the resulting bar and labels are slightly too small for comfortable scanning and touch-oriented use. A modest size increase will improve legibility while preserving the compact mobile layout and the distinct active state.

## What Changes

- Increase the mobile navigation row from 57.6px to approximately 64px.
- Increase mobile navigation label text from 0.75rem to approximately 0.8rem.
- Preserve the existing 18px icon size, spacing, active/inactive colors, and font-weight distinction.
- Preserve fixed full-width mobile placement, safe-area handling, content clearance, and keyboard accessibility.
- Leave desktop navigation styling and behavior unchanged.

## Capabilities

### New Capabilities

### Modified Capabilities

- `bottom-navigation`: Increase mobile navigation geometry and label sizing while preserving responsive and accessibility requirements.

## Impact

- `web/styles.css`: Update mobile-only navigation row height and label font size.
- `openspec/specs/bottom-navigation/spec.md`: Add the revised mobile sizing requirements.
- No JavaScript, API, dependency, URL, persistence, icon, or desktop layout changes.
