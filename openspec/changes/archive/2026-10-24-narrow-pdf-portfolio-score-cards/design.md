# Design

## Context

See `proposal.md` for motivation and `specs/portfolio-pdf-export/spec.md` for the observable width and alignment contract. The PDF renderer already lays out exposure rollups in three equal columns; score cards currently use half the printable width.

## Goals / Non-Goals

**Goals:**
- Match score-card width and horizontal spacing to one exposure-rollup column.
- Keep the existing score order, content, and side-by-side arrangement.

**Non-Goals:**
- Change score calculations, verdicts, labels, or vertical sizing.
- Rework other report-card layouts.

## Decisions

- Use the same three-column width calculation and gap as the exposure-rollup cards. This keeps the score cards aligned to the first two rollup columns and avoids introducing a second sizing convention.
- Preserve the current horizontal order and badge placement. Verify both unavailable values and populated score verdicts at the narrower width so text remains legible and does not overlap.
- Keep the implementation local to PDF score-card rendering rather than introducing a shared layout abstraction for two nearby calculations.

## Risks / Trade-offs

- [Localized labels or verdict badges may collide at the narrower width] → Exercise populated and unavailable score output in the renderer runtime test and assert card geometry and text placement.

## Migration Plan

No data migration or preference change is required. The new geometry takes effect in newly generated reports; existing PDFs remain unchanged. Rollback consists of restoring the prior half-width calculation.
