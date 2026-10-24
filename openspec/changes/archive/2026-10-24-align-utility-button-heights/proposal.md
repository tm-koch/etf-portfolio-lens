# Proposal

## Why

The newly added report-export button has a different outer height from the neighboring language and color-mode controls, making the top utility row look uneven. The PWA install action uses separate sizing rules and should align whenever it is visible.

## What Changes

- Give the language, color-mode, report-export, and visible PWA install controls matching outer box heights at desktop and mobile breakpoints.
- Preserve each control's existing width, icon or label presentation, interaction, and visibility behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `global-color-mode-selector`: Define consistent outer heights and vertical alignment for the top-right utility controls.
- `pwa-install-promotion`: Require the visible install action to match the neighboring utility controls' height.

## Impact

- `web/styles.css`: Utility button dimensions and responsive overrides.
- `tests/test_web_contract.py`: Responsive utility-control sizing assertions.
- OpenSpec deltas for the existing utility-control and PWA install-promotion capabilities.
