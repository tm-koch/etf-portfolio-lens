# Spec Delta

## ADDED Requirements

### Requirement: Select a pair from the portfolio ETFs
The pairwise holdings drill-down SHALL offer only ETFs currently selected in the portfolio and SHALL require two distinct ETFs.

#### Scenario: Portfolio selection supplies the available ETFs
- **WHEN** the drill-down is displayed
- **THEN** both ETF selectors SHALL contain only ETFs in the current portfolio selection

#### Scenario: A selected ETF is removed from the portfolio
- **WHEN** a portfolio change removes an ETF currently selected in the drill-down
- **THEN** the drill-down SHALL select a valid distinct pair from the remaining portfolio ETFs

#### Scenario: Fewer than two ETFs are selected
- **WHEN** the portfolio contains fewer than two ETFs
- **THEN** the drill-down SHALL not present an invalid pair comparison

### Requirement: Configure the pairwise holdings display maximum
Developer settings SHALL provide a persisted maximum number of companies for the pairwise holdings drill-down, defaulting to 20, and accept only finite positive integers.

#### Scenario: No valid setting has been saved
- **WHEN** the pairwise holdings drill-down is initialized without a valid saved maximum
- **THEN** its maximum displayed company count SHALL be 20

#### Scenario: A valid maximum is configured
- **WHEN** the developer enters a finite positive integer maximum
- **THEN** the setting SHALL be persisted and applied to the pairwise holdings drill-down

#### Scenario: An invalid maximum is entered
- **WHEN** the developer enters a non-finite, non-integer, zero, or negative maximum
- **THEN** the invalid value SHALL NOT be applied or persisted, and the last valid maximum or default SHALL remain active

### Requirement: Display a standalone pairwise holdings card
The pairwise holdings drill-down SHALL appear in a standalone card separate from the product-overlap heatmap. For an available selected pair, the card SHALL show its label and precomputed overlap total. Its two ETF selectors SHALL remain side by side, and its title SHALL identify the pair drill-down without naming the chart style.

#### Scenario: Drill-down is separate from the heatmap
- **WHEN** the pairwise section is displayed
- **THEN** the pair selectors and holdings detail SHALL appear in their own card, outside the product-overlap heatmap card

### Requirement: Render shared holdings as butterfly bars
For the selected pair, the drill-down SHALL show up to the configured maximum number of shared companies, ranked by smaller disclosed weight. Each row SHALL show the company name and both weights as mirrored bars around a shared center with a small clear gap between them, with each number beside its bar endpoint. The legend SHALL identify each ETF by ticker and color, and colors SHALL adapt to the active theme.

#### Scenario: Both ETF weights use butterfly bars
- **WHEN** a shared company is shown
- **THEN** its first ETF weight SHALL extend left and its second ETF weight SHALL extend right with a small clear gap at their shared center, and a legend SHALL identify each ETF by its ticker and color

#### Scenario: Shared companies are ranked by overlap contribution
- **WHEN** more companies are shared by the selected ETFs than the configured maximum
- **THEN** the drill-down SHALL show the highest contributors up to that maximum, ordered from largest minimum disclosed weight to smallest

#### Scenario: Both ETF weights are visible
- **WHEN** a shared company is shown
- **THEN** the drill-down SHALL display that company's disclosed weight at each butterfly bar endpoint and make clear that the smaller weight is its overlap contribution

#### Scenario: The displayed rows do not include all shared holdings
- **WHEN** shared companies beyond the configured maximum contribute to the pair total
- **THEN** the drill-down SHALL summarize their combined overlap contribution as remaining holdings

### Requirement: Summarize undisplayed overlap contribution
When shared companies remain beyond the configured display maximum, the drill-down SHALL retain the combined remaining overlap contribution and SHALL NOT show separate per-ETF remaining-share totals or undisplayed company names.

#### Scenario: Undisplayed shared holdings remain
- **WHEN** shared companies remain beyond the configured maximum
- **THEN** the drill-down SHALL show only their combined overlap contribution in the footer, without listing company names or per-ETF remaining-share totals

### Requirement: Identify butterfly weight units
Butterfly weight numbers SHALL omit the percent suffix, and a percentage note SHALL appear at the bottom of the drill-down card.

#### Scenario: Bar weights use a clear percentage unit
- **WHEN** the drill-down displays a bar weight
- **THEN** the adjacent number SHALL omit the percent suffix and the bottom note SHALL state that weights are in percent

### Requirement: Scale butterfly bars to available width
Butterfly bars SHALL scale proportionally, with the longest displayed bar using nearly all side width remaining after its adjacent number and gap are reserved. The shared center SHALL be indicated by a narrow transparent gap, not a visible axis marker.

#### Scenario: Largest bar uses the available width
- **WHEN** the drill-down displays one or more shared companies
- **THEN** the largest bar SHALL extend across nearly all chart width remaining after its adjacent number and gap are reserved, with a small center gap and no visible axis marker

#### Scenario: The pair total is available
- **WHEN** the selected pair has an available precomputed overlap result
- **THEN** the drill-down headline SHALL use that result's total overlap value

#### Scenario: The configured maximum changes
- **WHEN** the developer changes the valid maximum
- **THEN** the displayed companies and remaining contribution SHALL update while the pair overlap total remains unchanged

#### Scenario: Fewer companies are shared than the configured maximum
- **WHEN** the selected pair has fewer shared companies than the configured maximum
- **THEN** the drill-down SHALL show all shared companies and SHALL NOT show a remaining-holdings contribution

### Requirement: Present the unit and remainder together
The drill-down SHALL place the localized percentage-unit note and, when present, the remaining overlap contribution together in one compact, left-aligned footer line without an added layout gap. The footer MAY wrap on narrow viewports to avoid clipping or horizontal overflow, and SHALL NOT add a divider marker between the footer and chart.

#### Scenario: Remaining contribution is present
- **WHEN** undisplayed shared holdings contribute to overlap
- **THEN** the percentage-unit note and remaining overlap contribution SHALL appear together on one left-aligned line when the available width permits

#### Scenario: No remaining contribution is present
- **WHEN** all shared holdings are displayed
- **THEN** the footer SHALL show the percentage-unit note without an empty remainder label

### Requirement: Explain the pairwise holdings drill-down
The pairwise heatmap and drill-down SHALL each have a separate localized information dialog opened by an icon in that card's header. The drill-down explanation SHALL describe both ETFs' disclosed weights, rank companies by the smaller weight, and summarize undisplayed shared holdings through their combined remaining overlap contribution.

#### Scenario: User opens either pairwise information dialog
- **WHEN** the user activates an information icon in the heatmap or drill-down header
- **THEN** only the corresponding localized dialog SHALL open, and closing it SHALL return focus to its icon

### Requirement: Keep pairwise content visible on smartphone screens
The pairwise heatmap and drill-down cards SHALL display their content at smartphone viewport widths without horizontal page overflow or reliance on hover.

#### Scenario: User views pairwise content on a smartphone
- **WHEN** the Explore panel is shown at a viewport width of 375 CSS pixels or less
- **THEN** the heatmap and drill-down cards, selectors, and holdings details SHALL remain visible and usable
