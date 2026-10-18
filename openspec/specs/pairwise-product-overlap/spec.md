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
Developer settings SHALL provide a persisted near-identical overlap threshold, defaulting to 90%, and accept only finite values from 0% through 100%. A pair SHALL be marked near-identical when its overlap is at or above the configured threshold.

#### Scenario: Default threshold marks a high-overlap pair
- **WHEN** no valid threshold preference has been saved and a pair overlap is at least 90%
- **THEN** the pair SHALL be marked near-identical

#### Scenario: Threshold changes update selected pairs
- **WHEN** the developer changes the valid threshold or the selected portfolio ETFs change
- **THEN** near-identical heatmap marks SHALL update to reflect the current value and selection

#### Scenario: Invalid threshold is entered
- **WHEN** the configured threshold is non-finite or outside 0% to 100%
- **THEN** the invalid value SHALL NOT be applied and the last valid value or default SHALL remain active

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
