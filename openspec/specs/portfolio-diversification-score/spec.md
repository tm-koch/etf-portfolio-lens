# portfolio-diversification-score Specification

## Purpose
Summarizes the breadth of a selected portfolio's disclosed look-through company exposure using the effective number of companies and a qualitative diversification rating.

## Requirements

### Requirement: Calculate the effective number of companies
The diversification score SHALL be the inverse HHI of normalized, aggregated company weights in the selected portfolio's disclosed holdings. The system SHALL normalize the available company weights to their total before calculating HHI, and SHALL calculate from partial holdings when some selected portfolio exposure is undisclosed.

#### Scenario: Calculate score from company exposure
- **WHEN** the disclosed portfolio exposure is distributed equally across four distinct companies
- **THEN** the diversification score SHALL be 4

#### Scenario: Calculate from partial holdings coverage
- **WHEN** one or more selected ETFs have partial holdings coverage and at least some company exposure is available
- **THEN** the score SHALL be calculated from the available company exposure normalized to its disclosed total

#### Scenario: No company exposure is available
- **WHEN** no positive disclosed company exposure is available
- **THEN** the score SHALL be unavailable rather than presented as zero

#### Scenario: Zero-allocation ETF is selected
- **WHEN** an ETF has zero portfolio allocation
- **THEN** its holdings SHALL NOT affect the score or holdings coverage

### Requirement: Classify the diversification score
The system SHALL classify effective numbers below 5 as Highly Concentrated, from 5 to below 10 as Concentrated, from 10 to below 20 as Moderately Diversified, from 20 to below 40 as Well Diversified, and 40 or more as Highly Diversified.

#### Scenario: Score is on a rating boundary
- **WHEN** the effective number is exactly 5, 10, 20, or 40
- **THEN** the rating SHALL be Concentrated, Moderately Diversified, Well Diversified, or Highly Diversified, respectively

#### Scenario: Score is below five
- **WHEN** the effective number is less than 5
- **THEN** the rating SHALL be Highly Concentrated

### Requirement: Scale the diversification bullet bar
The score bar SHALL use a maximum of at least 40 and SHALL extend its maximum to the effective number when that number exceeds 40. The bar SHALL show the score marker and the concentration rating bands at the defined effective-number boundaries.

#### Scenario: Effective number exceeds 40
- **WHEN** the effective number is 50
- **THEN** the bar maximum SHALL be 50 and the score marker SHALL be positioned at that value

#### Scenario: Effective number is below 40
- **WHEN** the score is available and the effective number is below 40
- **THEN** the bar maximum SHALL remain 40

### Requirement: Present the score in Explore
The Explore tab SHALL show the diversification score in a separate responsive box below the pairwise product overlap section, following the existing redundancy score presentation pattern and naming the metric "Diversification score (1/HHI)".

#### Scenario: Score is displayed
- **WHEN** the user views Explore with a calculated score
- **THEN** the score value and localized qualitative rating SHALL be shown with the bullet bar

#### Scenario: Viewport narrows
- **WHEN** the Explore tab is viewed on a narrow viewport
- **THEN** the score value, rating, and bullet bar SHALL remain readable without horizontal overflow or overlap

### Requirement: Present the verdict separately from the bullet bar
The score box SHALL show the current localized rating in a color-coded verdict badge beside the score, using the redundancy score's badge treatment. The bullet bar SHALL NOT display text labels for rating bands.

#### Scenario: Verdict is shown without band labels
- **WHEN** a diversification score is available
- **THEN** the color-coded verdict badge SHALL show its rating and the bullet bar SHALL contain no textual rating-band labels

### Requirement: Identify score markers and separate endpoint labels
The redundancy and diversification score markers SHALL expose the current localized rating as a hover tooltip. The maximum endpoint label SHALL align with the track's right edge; vertical spacing SHALL keep it clear of a marker positioned at the maximum.

#### Scenario: Marker is at the maximum
- **WHEN** either score marker is positioned at the scale maximum
- **THEN** its localized rating SHALL be available as a hover tooltip, the maximum endpoint label SHALL align with the track's right edge, and the marker SHALL NOT overlap the label

### Requirement: Identify bullet bar sections on hover
Each redundancy and diversification bullet bar section SHALL expose its localized rating label as a hover tooltip, using the existing rating translations.

#### Scenario: User hovers over a bullet bar section
- **WHEN** the user hovers over a colored section in either score's bullet bar
- **THEN** the tooltip SHALL show the localized label for that section's rating

### Requirement: Keep score endpoints clear of the markers
The redundancy score bar SHALL NOT show written rating labels below the bar. Both score bars SHALL keep endpoint numbers aligned below their respective ends, with the maximum value aligned to the track's right edge, and separated vertically from the marker so the marker does not overlap the numbers.

#### Scenario: Marker reaches the scale maximum
- **WHEN** either score marker is positioned at the scale maximum
- **THEN** the endpoint number SHALL remain aligned beneath the right end of the bar and shall not overlap the marker

### Requirement: Disclose holdings coverage
The system SHALL calculate portfolio holdings coverage by weighting each selected positive-allocation ETF's disclosed holdings weight by its normalized portfolio allocation. Coverage at or above 99.995% SHALL be treated as complete to match two-decimal display precision. When coverage is incomplete, the score box SHALL show a warning with the covered percentage; the warning MAY be visually hidden at smartphone viewport widths while remaining available to assistive technology.

#### Scenario: Coverage is incomplete
- **WHEN** the selected portfolio has less than 100% disclosed holdings coverage and a score can be calculated
- **THEN** the score box SHALL disclose the covered percentage and identify that the score uses partial holdings data

#### Scenario: Coverage is complete
- **WHEN** the selected portfolio has 100% disclosed holdings coverage
- **THEN** the partial-coverage warning SHALL NOT be shown

#### Scenario: Coverage shortfall is within display rounding
- **WHEN** weighted holdings coverage is at least 99.995%
- **THEN** the system SHALL treat coverage as complete and SHALL NOT show the partial-coverage warning

#### Scenario: Smartphone viewport hides the warning
- **WHEN** the score box is displayed at a smartphone viewport width with incomplete coverage
- **THEN** the warning MAY be visually hidden but its partial-coverage status SHALL remain available to assistive technology

### Requirement: Explain the effective-company calculation
Explore SHALL provide an accessible information control in the diversification score section. Its explanation SHALL expand HHI as the Herfindahl-Hirschman Index, describe HHI as the sum of squared normalized disclosed company shares, and explain that the score is its inverse and represents an effective number of equally weighted companies rather than the actual number of companies held.

#### Scenario: User opens diversification information
- **WHEN** the user activates the diversification score information control
- **THEN** the explanation SHALL define the Herfindahl-Hirschman Index and describe the score as the inverse HHI of normalized disclosed company weights

#### Scenario: User interprets the effective number
- **WHEN** the user reads a diversification score of 10
- **THEN** the explanation SHALL say that the disclosed exposure has the same concentration as 10 equally weighted companies and SHALL NOT imply that the portfolio holds only 10 companies

### Requirement: Explain diversification ratings and coverage
The diversification explanation SHALL list the rating bands and clarify that the calculation uses disclosed company exposure when holdings coverage is incomplete; the displayed coverage warning identifies the portion included.

#### Scenario: User reads the rating bands
- **WHEN** the user opens diversification information
- **THEN** the explanation SHALL identify scores below 5 as Highly Concentrated, 5 to below 10 as Concentrated, 10 to below 20 as Moderately Diversified, 20 to below 40 as Well Diversified, and 40 or more as Highly Diversified

#### Scenario: Holdings coverage is incomplete
- **WHEN** the diversification score uses partial holdings data
- **THEN** the explanation SHALL state that only disclosed company exposure is used and that the coverage warning shows how much is included
