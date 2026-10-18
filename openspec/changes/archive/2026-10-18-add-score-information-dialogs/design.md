# Design

## Context

Explore already presents redundancy, pairwise overlap, and diversification as separate analysis sections, with localized descriptions and native dialogs elsewhere in the interface. Their definitions differ: redundancy aggregates duplicate portfolio-weighted contributions across selected ETFs; pairwise overlap compares shared disclosed weights for one ETF pair; diversification is the inverse HHI of normalized company exposure. See `proposal.md` and the three capability deltas for the behavior contract.

## Goals / Non-Goals

**Goals:**
- Give each analysis section a compact, accessible entry point to its own explanation.
- Explain the calculations in plain language without implying that pairwise overlap and portfolio redundancy are the same measure.
- Spell out “Herfindahl-Hirschman Index” and clarify that the diversification score is an effective number, not a count of actual holdings.
- Keep all explanatory content localized and usable on narrow screens.

**Non-Goals:**
- Change score calculations, availability rules, thresholds, or displayed values.
- Add a new general-purpose help system or a new dependency.
- Change the existing heatmap legend or near-identical threshold behavior.

## Decisions

### Use one reusable native dialog

Place an icon-only information button in each section heading and use one native `<dialog>` whose title and body are selected from the activating section. Reuse the existing dialog treatment and Lucide icon library. Each button has a localized accessible name; the dialog has a heading, a close control, and returns focus to its opener when closed. Native dialog behavior supplies modal focus handling and Escape dismissal; the content area can scroll on small screens.

**Alternative considered:** Use three inline popovers. Rejected because the rating bands and coverage caveats make the content too long for a compact popover, particularly on mobile, and separate popover behavior would duplicate interaction code.

### Keep each explanation specific to its measure

The redundancy explanation describes the per-security calculation as total selected-ETF portfolio contribution minus the largest single-ETF contribution. A short 70%/30% identical-holdings example illustrates why the smaller contribution is counted as redundant. The pairwise explanation describes each cell as a comparison of two ETFs, uses the smaller reported shared weight, and explains that incomplete disclosed holdings are not renormalized. The diversification explanation names the Herfindahl-Hirschman Index, describes squared normalized company shares and the inverse, and distinguishes effective number from actual company count.

**Alternative considered:** Use one shared explanation for all three. Rejected because it would blur portfolio-wide duplication, per-pair overlap, and company-level diversification.

### Localize complete explanation content

Treat English copy as the source wording and provide translated labels and explanatory content for every supported locale. Keep the rating ranges and numeric examples consistent with the existing calculations. Automated contract checks should verify that the HHI expansion is present in English and that each information control maps to the correct content.

**Alternative considered:** Show English explanations in every locale. Rejected because it would make the new controls inconsistent with the rest of Explore.

## Risks / Trade-offs

- The full diversification explanation is longer than the other two → use short paragraphs and a compact rating-band list; allow the dialog body to scroll on narrow or short viewports.
- The effective number can be mistaken for a literal company count → explicitly state that it is an equivalent concentration measure, not the actual number of holdings.
- Redundancy wording can sound like simple ETF-pair overlap → define the portfolio-weighted calculation and include the 70%/30% example.

## Migration Plan

No data migration or calculation change is required. Update the Explore controls, shared dialog content, and locale strings together. Rollback consists of removing the controls and dialog content; the three existing score calculations remain unchanged.
