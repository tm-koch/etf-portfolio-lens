# Tasks

## 1. Pairwise Holdings Breakdown

- [x] 1.1 Derive per-company contributions from the two selected ETF snapshots using existing identity and aggregation rules; add focused tests verifying both weights and minimum-weight contributions match the pairwise metric.
- [x] 1.2 Sort contributions deterministically, apply the configured maximum (default 20), and calculate any remaining contribution; test ordering, tie-breaking, configurable limits, fewer-than-limit cases, and reconciliation to the precomputed pair total.

## 2. Developer Maximum Setting

- [x] 2.1 Add a default-20 maximum preference with finite positive-integer validation and load/save behavior; test defaulting, valid persistence, and malformed or invalid values.
- [x] 2.2 Add the numeric developer control, state updates, and validation feedback; verify initialization, valid changes, and invalid-value retention in frontend tests.
- [x] 2.3 Localize the setting label and validation feedback in every supported locale; verify locale-key parity and existing web contract tests.

## 3. Drill-Down Interface

- [x] 3.1 Add two accessible ETF selectors limited to current portfolio ETFs, including distinct selections and reset behavior when portfolio selection changes; verify selector options and invalidated-pair handling in frontend tests.
- [x] 3.2 Refine the standalone card with a concise title, side-by-side selectors, endpoint-adjacent percentages, and theme-aware butterfly colors; verify layout and unchanged total.
- [x] 3.3 Localize the concise card title and keep all locale contracts passing.
- [x] 3.4 Show weights without percent suffixes with a bottom unit note, summarize undisplayed overlap contribution, and scale the longest bar to the available width; localize and test.
- [x] 3.5 Place the pairwise info-dialog icon in the top-right of the card header and verify dialog opening and focus return.
- [x] 3.6 Provide separate heatmap and drill-down dialogs, with an info icon in each card header.
- [x] 3.7 Verify pairwise content visibility on smartphone-sized screens; ensure Explore is active and ETFs are selected before expecting pairwise data.
- [x] 3.8 Place the unit note and remaining overlap contribution together in the footer, remove the visible center marker, and scale bars across the space left after number labels.
- [x] 3.9 Keep the footer text left-aligned and tightly joined, and add a small clear gap between the opposing bars without an axis marker.
- [x] 3.10 Remove the per-ETF remaining-share box while retaining the combined remaining overlap contribution in the footer.

## 4. Integration Verification

- [x] 4.1 Run the focused pairwise frontend and web runtime tests, then verify selectors, theme colors, and developer setting at 320px and 375px without horizontal page overflow.
- [x] 4.2 Verify percentage-unit labeling, remaining overlap contribution, proportional bar scaling, locale parity, and responsive layout.
- [x] 4.3 Verify the remaining-contribution footer, bottom percentage note, info-dialog trigger/focus, and responsive layout.
- [x] 4.4 Verify both dialogs open independently with focus restoration and both cards remain visible at smartphone widths.
- [x] 4.5 Verify the footer row, marker-free chart, full available bar track, and overflow behavior from phone to desktop widths.
- [x] 4.6 Verify the center gap and compact footer at phone and desktop widths without clipping or overflow.
- [x] 4.7 Verify no per-ETF remaining-share box is rendered and the contribution remains visible across supported locales.
