## 1. Home Panel Markup

- [x] 1.1 Add a Home panel with the `home` destination key and move the existing ETF Portfolio Lens introduction into it.
- [x] 1.2 Move the summary grid into the Home panel alongside the introduction, retaining the existing metric labels and element id.
- [x] 1.3 Keep the build-information dialog trigger and accessible dialog relationship working from the Home information area.

## 2. Navigation and State

- [x] 2.1 Add Home as the first `NAVIGATION_DESTINATIONS` entry with a Lucide house icon while preserving the existing Portfolio, Compare, and Explore keys.
- [x] 2.2 Change the default active destination to `home` and verify missing or invalid stored destination values fall back to Home.
- [x] 2.3 Verify Home, Portfolio, Compare, and Explore activate only their matching panels and preserve the existing `aggregated` panel mapping.
- [x] 2.4 Verify destination persistence restores all four destinations without changing the URL or browser history.

## 3. Styling and Accessibility

- [x] 3.1 Adjust Home panel and moved overview styles so the existing visual hierarchy remains coherent without undesirable nested-card treatment.
- [x] 3.2 Preserve desktop document-flow navigation after the Home overview and preserve the fixed, full-width mobile navigation geometry and content clearance.
- [x] 3.3 Verify all four destinations retain visible labels, distinct icons when Lucide is available, keyboard operation, and `aria-current="page"` active state.

## 4. Verification

- [x] 4.1 Run the available frontend or repository tests and resolve any Home-navigation regressions.
- [x] 4.2 Manually verify empty and populated Home summaries update after adding, removing, and changing ETF shares.
- [x] 4.3 Verify Home, Portfolio, Compare, and Explore at desktop and mobile widths, including reload persistence and the build-information dialog.
- [x] 4.4 Confirm the final OpenSpec status reports all required artifacts complete.
