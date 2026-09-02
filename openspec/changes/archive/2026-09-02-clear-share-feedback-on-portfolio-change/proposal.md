## Why

When a private portfolio is opened from a share link, the application continues displaying the "Private portfolio loaded" feedback after the user changes the portfolio. This makes stale sharing context look current and obscures the fact that the edited portfolio is now local working state.

## What Changes

- Clear share-loading feedback after an actual portfolio mutation, including PDF replacement, adding an ETF, changing share counts, and removing an ETF.
- Keep the share URL fragment unchanged so refreshing the page continues to reload the original portfolio shared through the link.
- Preserve the existing private-portfolio weighting behavior and share-link generation behavior.
- Add contract coverage for feedback invalidation at each portfolio mutation boundary.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-sharing`: A loaded shared-portfolio status message is cleared after the portfolio is changed, while the original URL remains authoritative on refresh.

## Impact

- `web/app.js` portfolio mutation handlers and share-feedback state.
- `tests/test_web_contract.py` static contract coverage.
- `openspec/specs/portfolio-sharing/` through a delta specification.
- No API, persistence format, dependency, or URL encoding changes.
