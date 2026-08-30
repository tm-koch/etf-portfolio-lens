## Why

The navigation currently inherits a light-grey border from the shared card styling, which makes the bar edge look disconnected from its theme-appropriate surface. Removing that visible border will give the navigation a cleaner edge while retaining the existing shadow and dark-mode gradient for separation from page content.

## What Changes

- Remove the visible border from the primary navigation in desktop and mobile layouts.
- Preserve the navigation's theme-appropriate background, mobile shadow, dark-mode gradient edge, spacing, safe-area behavior, and destination geometry.
- Update the bottom-navigation requirement and contract coverage to describe separation without a visible border.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bottom-navigation`: Change the mobile visual-boundary requirement so the navigation no longer relies on a visible top border.

## Impact

- `web/styles.css`: Adjust primary-navigation border rules and related responsive styling.
- `tests/test_web_contract.py`: Update structural/style contract assertions for the borderless navigation.
- `openspec/specs/bottom-navigation/spec.md`: Synchronize the revised navigation-edge requirement.
- No API, data, dependency, or persistence changes.