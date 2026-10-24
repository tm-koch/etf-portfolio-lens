# Spec Delta

## MODIFIED Requirements

### Requirement: Display a standalone pairwise holdings card
The pairwise holdings drill-down SHALL appear in a standalone card separate from the product-overlap heatmap. For an available selected pair, the card SHALL show its label and precomputed overlap total. Its two ETF selectors SHALL remain side by side at all supported viewport widths, each using the available width of its column, and its title SHALL identify the pair drill-down without naming the chart style.

#### Scenario: Drill-down is separate from the heatmap
- **WHEN** the pairwise section is displayed
- **THEN** the pair selectors and holdings detail SHALL appear in their own card, outside the product-overlap heatmap card

## ADDED Requirements

### Requirement: Align the pair drill-down card header
At widescreen viewport widths, the pair drill-down title SHALL align with the heading inset and vertical position used by neighboring aggregation cards, while its information control remains anchored at the upper-right of the card header.

#### Scenario: Widescreen card heading alignment
- **WHEN** the aggregation view is displayed at a widescreen viewport width
- **THEN** the pair drill-down title SHALL align with neighboring card headings and the information control SHALL remain at the upper-right of its card header