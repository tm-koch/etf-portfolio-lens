# Proposal

## Why

The PDF report contains portfolio analytics and exposure insights, but its only entry point is an icon in the global utility bar. A labeled export action in Explore makes the report easier to discover in the context where users review those insights.

## What Changes

- Keep the existing global export icon and its behavior.
- Add a labeled portfolio-PDF action near the top of the Explore / Aggregated portfolio view, before the insight sections.
- Open the existing Export dialog from either entry point, with the current portfolio selected by default.
- Localize the new action and keep it usable on desktop and mobile layouts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portfolio-pdf-export`: Allow users to open the existing Export view from both the global utility icon and a contextual Explore action, without changing its scope defaults or report-generation behavior.

## Impact

- `web/index.html` and `web/styles.css`: Explore action-row structure and responsive presentation.
- `web/app.js`: Connect the contextual action to the existing export-dialog flow.
- `web/locales/*.json`: Localized action labels.
- `tests/`: Export entry-point and responsive/localization contract coverage.
- `openspec/specs/portfolio-pdf-export/spec.md`: Export-view entry-point requirement.
