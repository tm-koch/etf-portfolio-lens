# Proposal

## Why

Switching the interface language rebuilds the navigation buttons, after which the selected destination loses its visible emphasis. Subsequent destination selections update the content panel but still fail to show the selected state, leaving users without reliable visual feedback.

## What Changes

- Preserve the selected destination's visual and accessible active state when navigation is rerendered for a language change.
- Add regression coverage for switching language and then selecting another destination.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bottom-navigation`: Require the active destination's selected style and accessibility state to remain correct across runtime language changes.

## Impact

- `web/app.js`: navigation rendering and selected-state synchronization.
- `tests/test_web_runtime.py` or existing focused web tests: locale-switch navigation regression coverage.
- `openspec/specs/bottom-navigation/spec.md`: active-destination requirement scenario.
