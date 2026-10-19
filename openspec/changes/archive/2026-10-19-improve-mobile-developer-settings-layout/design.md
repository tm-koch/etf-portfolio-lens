# Design

## Context

The redundancy and near-identical controls are separate grid sections in the Build & preview developer settings. The redundancy section currently changes to one column below 760px. The near-identical section overrides the shared grid with one column and a maximum width, which also constrains its top border. See proposal.md for motivation and the spec deltas for observable requirements.

## Goals / Non-Goals

**Goals:**
- Keep both redundancy threshold fields in a shared two-column layout at smartphone widths.
- Align the near-identical input to one redundancy input while allowing its section border to span the full content width.

**Non-Goals:**
- Change threshold values, validation, persistence, or score classification.
- Change the Build & preview dialog's overall layout or other developer controls.

## Decisions

- Reuse the existing two-column threshold grid at narrow widths instead of creating a separate mobile arrangement. This keeps the paired thresholds comparable across modes and avoids a viewport-specific stacking rule.
- Let the near-identical section use the same two-column grid tracks as the redundancy section. Its heading and error message continue spanning the full row, while its label and input occupy one grid column. This makes its input match one redundancy field and lets the section's top border extend across the full content width.
- Remove the narrow-screen one-column override and the near-identical section's independent width cap. A separately sized input was considered, but it would duplicate responsive sizing logic and could drift from the redundancy fields.

## Risks / Trade-offs

- **Numeric fields have less horizontal room on the narrowest phones** → Keep the existing compact input styling and verify the dialog at a narrow smartphone viewport; labels may wrap naturally without forcing the inputs onto separate rows.

## Migration Plan

No data or preference migration is needed. Update the developer-settings grid styles and verify the controls at desktop and smartphone widths. Rollback consists of restoring the prior grid overrides.
