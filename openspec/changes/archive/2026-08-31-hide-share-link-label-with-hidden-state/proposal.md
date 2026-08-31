## Why

The share-link label still appears before a share URL exists because its component CSS sets `display: grid`, overriding the browser's default hidden-element styling. This leaves a visible `Share link` caption beside an empty hidden input and makes the sharing area appear partially active.

## What Changes

- Ensure a share-link label with the `hidden` attribute has no rendered layout or visible text.
- Preserve the existing behavior that reveals the label and URL input after a valid share URL is generated.
- Add regression coverage for CSS-enforced hidden behavior and visible post-share fallback behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-sharing`: Require the hidden share-link label to remain visually absent until a generated URL is available.

## Impact

- Affected presentation rules in `web/styles.css`.
- Affected frontend contract tests in `tests/test_web_contract.py`.
- No changes to share URL encoding, application state, clipboard behavior, markup structure, or external dependencies.
