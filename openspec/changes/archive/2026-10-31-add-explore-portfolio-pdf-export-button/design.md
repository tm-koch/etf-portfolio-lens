# Design

## Context

The global utility bar already opens an Export dialog that defaults to the current portfolio. The Explore / Aggregated portfolio panel contains the report's analytics, while its panel heading shares the top-right area with the positioned color-mode control. See proposal.md for motivation and specs/portfolio-pdf-export/spec.md for the behavior contract.

## Goals / Non-Goals

**Goals:**
- Make portfolio PDF export discoverable before users reach the Explore insights.
- Preserve the existing global export icon and provide the same dialog and report choices from both entry points.
- Keep the new action localized and visible at desktop and mobile widths.

**Non-Goals:**
- Add a separate report generator, alter PDF contents, or change the export dialog's scope options.
- Remove or reposition the global utility-bar icon.

## Decisions

- Place a dedicated export action row immediately after the Explore panel heading and before the insight layout. This keeps the action associated with the entire portfolio analysis, avoids implying that it exports only one insight card, and avoids competing with the color-mode control in the heading.
- Use a visible localized label such as "Export portfolio PDF" with the existing `file-down` icon. Align it to the right on wide screens; on narrow screens, place it below the heading and let it use the available row width.
- Route both the global icon and the Explore action through the existing export-dialog flow. The dialog continues to select the current portfolio by default and retains the full-catalog option and allocation-only setting.
- Add the contextual action label to all three locale resources. The existing localization requirement already covers translated user-facing text, so no localization spec delta is needed.
- Add focused coverage to the existing web contract/runtime tests for the Explore action, its localized label, and reuse of the export flow; add no new dependency.

The alternative of placing the action inside an insight card is rejected because the PDF spans multiple analytics sections. Placing it beside the Portfolio editor's selected positions would emphasize portfolio construction rather than analysis.

## Risks / Trade-offs

- [Risk] Two entry points could behave differently over time → Keep them wired to the same dialog-opening behavior and cover the contextual action in tests.
- [Trade-off] The additional row adds vertical space above the insights → A single responsive action row keeps the action visible without adding a card or disrupting the existing insight layout.
