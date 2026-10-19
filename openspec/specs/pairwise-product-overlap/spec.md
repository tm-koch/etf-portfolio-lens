# pairwise-product-overlap Specification

## Purpose
Shows which selected ETFs hold the same underlying securities and how much their disclosed fund weights overlap, complementing the portfolio-wide redundancy score with a pair-by-pair view.

## Requirements

### Requirement: Calculate pairwise product overlap
For each unordered ETF pair, overlap SHALL equal the shared disclosed weight without renormalizing incomplete holdings. Holdings with the same ISIN SHALL match exactly. Remaining weights SHALL also match by stable canonical company identity, including when both holdings have different ISINs for the same company. Each matched weight SHALL contribute at most once, and a company's contribution SHALL NOT exceed the smaller total disclosed weight for that company in either ETF.

#### Scenario: Shared security contributes the smaller fund weight
- **WHEN** one ETF holds a security at 6% and another holds it at 4%
- **THEN** that security SHALL contribute 4 percentage points to the pair's overlap

#### Scenario: ISIN is unavailable for a holding
- **WHEN** a shared holding lacks an ISIN in either ETF snapshot but both snapshots identify the same canonical company
- **THEN** the holding SHALL match through that canonical company identity

#### Scenario: Share class ISINs differ for the same company
- **WHEN** holdings in two ETFs have different ISINs but share the same stable canonical company identity
- **THEN** their remaining disclosed weights SHALL contribute to the same company overlap, without double-counting any exact ISIN match

#### Scenario: Holdings coverage is incomplete
- **WHEN** the sum of disclosed holdings in either ETF is below 100%
- **THEN** the pair score SHALL use the disclosed weights as-is and the heatmap SHALL communicate the compared holdings coverage

### Requirement: Keep pairwise data aligned with the published ETF catalog
The published product-overlap data SHALL include one result for each unordered pair in the same successful ETF set and catalog generation, with each ETF's holdings coverage. A pair without usable holdings or stable identity data SHALL be unavailable rather than displayed as zero overlap.

#### Scenario: A new ETF is published
- **WHEN** a catalog refresh successfully publishes an additional ETF with holdings
- **THEN** the pairwise data SHALL include a comparison between it and every other published ETF

#### Scenario: A pair cannot be compared
- **WHEN** either ETF has no usable holdings or the pair has no stable comparison data
- **THEN** the heatmap SHALL show that pair as unavailable rather than as 0% overlap

### Requirement: Present the selected ETF pairs in a lower-triangle heatmap
Explore SHALL show a separate box titled "Pairwise product overlap heatmap" that filters and orders the published matrix by the selected portfolio ETFs and uses a 0% to 100% overlap scale.
All body cells SHALL have a consistent height regardless of content; the header SHALL retain its separate sizing. Column headers and ETF row labels SHALL use the same light neutral background. Diagonal dash cells and unused cells SHALL use a subtly lighter neutral background.

#### Scenario: Selected products determine matrix rows and columns
- **WHEN** the portfolio selection changes
- **THEN** the heatmap SHALL show exactly those ETFs in portfolio order on both axes

#### Scenario: Matrix avoids duplicate pair cells
- **WHEN** the pairwise heatmap is displayed
- **THEN** the diagonal SHALL show a dash, cells above the diagonal SHALL be empty, and each unique pair SHALL appear once below the diagonal

#### Scenario: Matrix body cells have consistent height
- **WHEN** body rows contain overlap, unavailable, diagonal, or empty cells
- **THEN** all body cells SHALL have the same height, independent of their content, without changing the header height

#### Scenario: Matrix labels and unused cells have distinct neutral backgrounds
- **WHEN** the heatmap is displayed
- **THEN** column headers and ETF row labels SHALL share the same light neutral background, while diagonal dash cells and unused cells SHALL appear slightly lighter

#### Scenario: Heatmap matches application styling
- **WHEN** the heatmap is displayed
- **THEN** it SHALL use the existing application font and restrained rounded cell corners

### Requirement: Keep large heatmaps navigable
The heatmap viewport SHALL be bounded and support horizontal and vertical scrolling without page-level horizontal overflow; its ETF header row and first product column SHALL remain fixed while scrolling.

#### Scenario: Matrix exceeds available viewport space
- **WHEN** the selected ETF count exceeds the available width or height
- **THEN** the user SHALL be able to scroll the matrix in the needed direction while retaining visible row and column identities

### Requirement: Keep the mobile heatmap compact and legible
At narrow viewport widths, the heatmap SHALL use compact typography and cells, show tickers without full product names or per-cell coverage text, and preserve those details in accessible labels. The viewport SHALL hide scrollbar tracks while retaining touch, pointer, and keyboard scrolling. A legend SHALL explain the overlap color scale, near-identical outline and active threshold, and disclosed-weight coverage range.

#### Scenario: Mobile matrix shows compact product labels
- **WHEN** the heatmap is displayed at a narrow viewport
- **THEN** row and column labels SHALL show product tickers, full product names and per-cell coverage text SHALL be visually hidden, and cells SHALL use smaller typography and dimensions

#### Scenario: Mobile scrolling remains available
- **WHEN** the matrix is wider or taller than its viewport
- **THEN** users SHALL be able to scroll it by touch, pointer, or keyboard without visible scrollbar tracks or page-level horizontal overflow

#### Scenario: Legend explains matrix encoding
- **WHEN** the heatmap is displayed
- **THEN** a localized legend SHALL identify the 0% to 100% color scale, near-identical outline and configured threshold, and the disclosed fund-weight coverage represented by the data

### Requirement: Align aggregation card headings on mobile
At narrow viewport widths, the Rollups, Pairwise product overlap heatmap, and Top companies card headings SHALL align with the Redundancy score heading in horizontal inset, top spacing, and title size.

#### Scenario: Aggregation card headings share a common alignment
- **WHEN** the aggregation view is displayed at a narrow viewport
- **THEN** the Rollups, Pairwise product overlap heatmap, and Top companies headings SHALL have the same inset, top alignment, and title size as Redundancy score

### Requirement: Configure near-identical pair threshold
Developer settings SHALL provide a persisted near-identical overlap threshold, defaulting to 90%, and accept only finite values from 0% through 100%. A pair SHALL be marked near-identical when its overlap is at or above the configured threshold. The threshold input SHALL match the width of one redundancy threshold input at every viewport width, and the separator before the near-identical threshold section SHALL span the full settings content width.

#### Scenario: Default threshold marks a high-overlap pair
- **WHEN** no valid threshold preference has been saved and a pair overlap is at least 90%
- **THEN** the pair SHALL be marked near-identical

#### Scenario: Threshold changes update selected pairs
- **WHEN** the developer changes the valid threshold or the selected portfolio ETFs change
- **THEN** near-identical heatmap marks SHALL update to reflect the current value and selection

#### Scenario: Invalid threshold is entered
- **WHEN** the configured threshold is non-finite or outside 0% to 100%
- **THEN** the invalid value SHALL NOT be applied and the last valid value or default SHALL remain active

#### Scenario: Near-identical control matches redundancy field width
- **WHEN** the developer settings are viewed at any viewport width
- **THEN** the near-identical threshold input SHALL have the same width as one redundancy threshold input

#### Scenario: Near-identical section divider spans the settings width
- **WHEN** the developer settings are displayed
- **THEN** the separator before the near-identical threshold section SHALL span the full available settings content width

### Requirement: Explain pairwise product overlap
Explore SHALL provide an accessible information control in the pairwise product overlap section. When activated, its explanation SHALL state that each cell compares two ETFs and adds the smaller disclosed weight for each shared underlying security or company. It SHALL clarify that overlap uses disclosed weights as reported, is not renormalized for incomplete holdings, and that coverage is shown for both ETFs. It SHALL distinguish an unavailable result from zero overlap.

#### Scenario: User opens pairwise overlap information
- **WHEN** the user activates the heatmap information control
- **THEN** the explanation SHALL describe the pair-by-pair shared-weight calculation and distinguish it from the portfolio-wide redundancy score

#### Scenario: One ETF reports a larger shared holding
- **WHEN** one ETF reports a shared holding at 6% and the other reports it at 4%
- **THEN** the explanation SHALL make clear that the pairwise overlap contribution is 4 percentage points

#### Scenario: Pair coverage is incomplete
- **WHEN** either ETF has less than 100% disclosed holdings coverage
- **THEN** the explanation SHALL state that the overlap uses disclosed weights without scaling them to 100% and that both ETFs' coverage is shown

#### Scenario: Pair cannot be compared
- **WHEN** the pairwise result is unavailable
- **THEN** the explanation SHALL clarify that unavailable data is distinct from zero overlap

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
Developer settings SHALL provide a persisted maximum number of companies for the pairwise holdings drill-down, defaulting to 10, and accept only finite positive integers.

#### Scenario: No valid setting has been saved
- **WHEN** the pairwise holdings drill-down is initialized without a valid saved maximum
- **THEN** its maximum displayed company count SHALL be 10

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
