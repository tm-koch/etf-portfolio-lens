# Design

## Context

See `proposal.md` for motivation. The pair selectors use `.color-mode-button` for shared visual styling, while the mobile utility-bar rule currently assigns a fixed width to that shared class. The drill-down heading also uses a different heading wrapper from neighboring score cards, so its heading margin needs to be normalized independently of the information button.

## Goals / Non-Goals

**Goals:**
- Keep the two pair selectors in equal-width columns at narrow viewport widths.
- Align the drill-down title with neighboring card headings on widescreen without moving the info control from the upper-right.
- Add regression coverage for both viewport cases.

**Non-Goals:**
- Change pair selection behavior, card ordering, or information-dialog behavior.
- Change the global visual treatment of utility-bar controls or other cards.

## Decisions

- Scope the fixed mobile width to utility-bar language and color-mode controls instead of every `.color-mode-button`. This preserves compact utility controls while allowing the pair selector's existing `width: 100%` rule to fill its grid column. Keeping the two-column `minmax(0, 1fr)` grid avoids overflow when ETF tickers are long.
- Normalize the pair drill-down heading margin within its own card/header. Keep the existing flex header and fixed-size info button so the title and icon remain independent, aligned header items. Avoid moving the button into the content flow or changing the shared info-button geometry.
- Prefer focused assertions in the existing web layout/runtime test coverage for the 375px mobile case and a widescreen case. Validate rendered widths/alignment where the browser harness supports it; otherwise assert the relevant scoped CSS contract without introducing a new test framework.

## Risks / Trade-offs

- A selector that is too broad could change unrelated color-mode buttons. Scope the width rule to controls inside the utility bar and verify pair selector sizing at mobile width.
- Heading alignment can be sensitive to default heading margins. Verify both the title inset and info-button placement against neighboring aggregation cards at widescreen width.

## Migration Plan

No data or deployment migration is required. The change is a client-side layout adjustment and can be rolled back by reverting the scoped CSS and its focused regression coverage.