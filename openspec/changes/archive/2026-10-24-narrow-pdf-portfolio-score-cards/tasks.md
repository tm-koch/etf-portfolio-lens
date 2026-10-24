# Tasks

## 1. Score Card Layout

- [x] 1.1 Update PDF score-card width and horizontal placement to match the three-column exposure rollups; extend the renderer runtime test to verify card width, gap, and alignment against rollup cards.
- [x] 1.2 Verify score labels, values, and populated verdict badges remain legible and do not overlap at the narrower width with localized and unavailable-score cases in the renderer runtime test.

## 2. Integration Validation

- [x] 2.1 Run the focused PDF runtime tests and validate this change with `openspec validate narrow-pdf-portfolio-score-cards --type change`; confirm both pass.
