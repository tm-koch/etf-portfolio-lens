## MODIFIED Requirements

### Requirement: Portfolio and ETF contribution columns
The compact holdings matrix SHALL display the holding name, the existing total portfolio contribution, and one column for every selected ETF. Each ETF cell SHALL display that ETF contributor's existing share of the holding total, and SHALL display an em dash when that ETF does not contribute to the holding. The matrix SHALL NOT introduce a separate holding-level exposure data source. Portfolio contribution calculations SHALL weight each selected ETF position by its valid imported CHF-normalized market value; positions without imported valuation data SHALL use the existing share-count fallback. The matrix SHALL initially display the first 20 ranked holdings and SHALL append further ranked holdings in batches as the user scrolls toward the end.

#### Scenario: Shared holding contribution breakdown
- **WHEN** a holding has contributors from multiple selected ETFs
- **THEN** its total column SHALL use the existing aggregated holding calculation and each contributing ETF column SHALL use the existing contributor share-of-holding value

#### Scenario: Imported values determine portfolio weighting
- **WHEN** selected positions have valid imported CHF-normalized market values
- **THEN** their relative portfolio contribution SHALL be calculated from those values rather than share counts alone

#### Scenario: Manual positions retain fallback weighting
- **WHEN** a selected position has no valid imported valuation data
- **THEN** that position SHALL use the existing share-count fallback without preventing other positions from using imported value weighting

#### Scenario: Holding absent from an ETF
- **WHEN** an aggregated holding has no contributor record for a selected ETF
- **THEN** that ETF's cell SHALL display an em dash and SHALL not affect the row's existing total

#### Scenario: ETF columns follow selected positions
- **WHEN** the selected portfolio contains multiple ETFs
- **THEN** the table SHALL provide one distinct column per selected ETF in the selected-position order

#### Scenario: More holdings load while scrolling
- **WHEN** the user scrolls toward the end of the currently rendered compact rows and more ranked holdings remain
- **THEN** the application SHALL append the next batch of ranked rows without replacing the existing rows
