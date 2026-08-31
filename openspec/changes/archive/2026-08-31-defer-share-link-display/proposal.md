## Why

The Portfolio tab currently reserves visible space for the `Share link` label before a user has generated a link, even though the input is empty and hidden. This creates a confusing partial state and makes the sharing area appear active before the share action has produced anything useful.

## What Changes

- Keep the share-link label and URL input hidden until a valid share URL has been generated.
- Reveal the label and URL together after sharing a populated portfolio, including when clipboard access is unavailable and manual copying is required.
- Keep the link field hidden when sharing an empty portfolio fails to produce a URL.
- Add regression coverage for the initial hidden state and post-share reveal behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-sharing`: Clarify that the fallback share-link field is revealed only after a valid share URL is generated, while preserving the existing share, clipboard, and empty-portfolio behavior.

## Impact

- Affected frontend markup and presentation: `web/index.html` and `web/styles.css`.
- Affected share rendering state: `web/app.js`, specifically `renderShareFeedback()` and `sharePortfolio()`.
- Affected frontend contract tests: `tests/test_web_contract.py`.
- No changes to share payload encoding, URL format, clipboard APIs, persistence, or external dependencies.
