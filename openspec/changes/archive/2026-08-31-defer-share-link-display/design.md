## Context

The Portfolio tab already stores a generated fallback URL in `state.shareFallbackUrl` and renders the URL input from `renderShareFeedback()`. The input is hidden when the URL is empty, but its surrounding label remains visible, leaving an empty `Share link` affordance before the user has requested a link.

The existing sharing flow supports clipboard success, manual fallback when clipboard access is unavailable, and an empty-portfolio error. This change is a presentation-state refinement and must not alter the encoded payload or sharing semantics.

## Goals / Non-Goals

**Goals:**

- Hide the complete share-link label and input until a valid generated URL exists.
- Reveal the label and input together whenever `state.shareFallbackUrl` is populated.
- Keep the empty-portfolio status message independent from the link field.
- Cover initial, successful-share, clipboard-fallback, and empty-portfolio states with regression tests.

**Non-Goals:**

- Changing the share URL format, payload version, or clipboard behavior.
- Adding a server-side sharing service.
- Clearing a previously generated link when the portfolio is edited later.
- Changing the status messages or the accessible share action.

## Decisions

Use the existing `state.shareFallbackUrl` as the single visibility condition. The URL label should be hidden when that value is empty and shown when it contains the generated URL; the input keeps its existing readonly behavior. This avoids introducing another state flag and ensures the label and input cannot become inconsistent.

Keep the status paragraph always available to report empty-portfolio and clipboard outcomes. The manual-copy fallback continues to populate the URL before reporting clipboard failure, so the link is revealed in that case as well.

Add the visibility hook to the existing markup and assert the conditional rendering contract in the current web tests. No CSS-only solution is preferred because the visibility depends on application state rather than a static selector.

## Risks / Trade-offs

- [Risk] A generated link may remain visible after later portfolio edits. -> Mitigation: retain current behavior deliberately; clearing stale links is outside this change and can be specified separately if needed.
- [Risk] Hiding the label could make the fallback URL less discoverable if the input visibility is not updated with it. -> Mitigation: toggle the label and input from the same URL state and test both elements together.

## Migration Plan

Update the markup, render logic, and web contract assertions, then run the focused and full test suites and perform a browser smoke test for empty and populated sharing states. Rollback consists of reverting these small presentation changes.

## Open Questions

None.
