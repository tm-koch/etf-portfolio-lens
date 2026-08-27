## Context

The static frontend currently defines a Warnings subcard at the bottom of the Explore `/aggregated` panel. `web/app.js` looks up that element and `renderWarnings()` fills it, while the About this build dialog separately renders the same current-selection warning collection into `#build-warning-list`. The build dialog also has optional details, warnings, and developer settings sections with independent top borders; hidden optional details can therefore leave an empty separator above warnings. The requested behavior is to remove the Explore surface, retain build diagnostics, and leave one separator before the bottom warnings section.

## Goals / Non-Goals

**Goals:**

- Remove the Explore warning markup from the aggregated tab in all presentation modes.
- Remove the now-unused Explore warning element lookup and render call.
- Preserve warning collection and rendering in the About this build dialog.
- Ensure hidden optional build details do not display a separator or occupy layout space, leaving one visible separator before the bottom warnings section.
- Keep the change limited to the frontend contract and its focused tests.

**Non-Goals:**

- Do not change warning detection, aggregation, snapshot validation, or warning text.
- Do not remove warnings from the About this build dialog.
- Do not alter the compact holdings matrix or other Explore content.
- Do not change backend or published catalog data.

## Decisions

- Remove the Explore warning subcard from `web/index.html` rather than hiding it with CSS. The surface is not needed in either Explore mode, so removing its DOM keeps layout, accessibility, and scripting behavior explicit.
- Delete the `elements.warningList` lookup and the Explore call in `renderWarnings()`, but retain `renderBuildWarnings()` and `#build-warning-list`. This preserves the existing diagnostic ownership in the build dialog and avoids duplicating warning logic.
- Update `tests/test_web_contract.py` to assert that the Explore warning ID is absent and the build-dialog warning ID and rendering path remain present. This guards both halves of the requested removal.
- Add a CSS rule for `.build-details-extra[hidden]` so the hidden optional section cannot contribute its border or grid row. Keep the warnings section as the single separator-bearing boundary above warnings.

## Risks / Trade-offs

- [Risk] A future caller may expect `renderWarnings()` to update an Explore warning list. -> Keep the function as the build-dialog refresh path and retain the shared warning collector; the contract test documents the intended remaining surface.
- [Risk] Removing the panel changes the vertical density of Explore. -> This is the requested result and does not affect the exposure content or responsive table behavior.
- [Risk] The dialog may show no separator when optional details are populated. -> Keep the warnings section's top border independent so the boundary remains present in both metadata states.

## Migration Plan

No data or storage migration is required. Deploy the frontend changes together; rollback consists of restoring the Explore markup and its corresponding element/render references.

## Open Questions

None.
