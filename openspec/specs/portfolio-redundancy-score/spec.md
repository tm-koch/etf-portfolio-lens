# portfolio-redundancy-score Specification

## Purpose
The portfolio redundancy score summarizes the share of portfolio exposure duplicated across selected ETFs. It gives users a single, dynamically scaled Explore indicator for aggregate look-through overlap.

## Requirements

### Requirement: Calculate aggregate look-through redundancy
The redundancy score SHALL sum, for each underlying security, its total portfolio contribution minus its largest contribution from any one selected ETF. Each contribution SHALL use the ETF's current normalized portfolio allocation multiplied by that security's weight within the ETF.

#### Scenario: Two equally weighted ETFs have identical holdings
- **WHEN** two selected ETFs have equal portfolio allocations and identical underlying security weights
- **THEN** the redundancy score SHALL be 50% of the portfolio

#### Scenario: Three equally weighted ETFs have identical holdings
- **WHEN** three selected ETFs have equal portfolio allocations and identical underlying security weights
- **THEN** the redundancy score SHALL be 66.7% of the portfolio, subject to display precision

#### Scenario: Unequal ETF allocations affect the score
- **WHEN** two ETFs have identical holdings but portfolio allocations of 70% and 30%
- **THEN** the redundancy score SHALL be 30% of the portfolio

#### Scenario: A security held by only one ETF
- **WHEN** an underlying security contributes to the portfolio through only one selected ETF
- **THEN** that security SHALL contribute 0% to the redundancy score

### Requirement: Scale the score to the selected ETF count
The score bar maximum SHALL be `100% * (1 - 1/n)`, where `n` is the number of positive-allocation ETFs with usable holdings included in the calculation. Zero-allocation positions SHALL NOT affect the score or scale, and the score SHALL remain within that scale.

#### Scenario: One ETF has usable holdings
- **WHEN** exactly one selected ETF has usable holdings
- **THEN** the maximum SHALL be 0% and the displayed redundancy score SHALL be 0%

#### Scenario: Four ETFs determine the scale maximum
- **WHEN** four selected ETFs have usable holdings
- **THEN** the score bar maximum SHALL be 75%

#### Scenario: No selected ETF has usable holdings
- **WHEN** no selected ETF has usable holdings available for calculation
- **THEN** the score SHALL be presented as unavailable rather than as a measured 0% score

#### Scenario: A positively weighted ETF has no usable holdings
- **WHEN** any selected ETF with a positive portfolio allocation has no usable holdings available
- **THEN** the score SHALL be presented as unavailable rather than calculated from incomplete portfolio coverage

#### Scenario: A selected ETF has zero allocation
- **WHEN** a selected ETF has a zero portfolio allocation and the other positive-allocation ETFs have usable holdings
- **THEN** the zero-allocation ETF SHALL NOT affect the score or the scale maximum

### Requirement: Present the score separately in Explore
The Explore tab SHALL show the redundancy score in its own responsive box after Rollups and before Top companies, using the existing application font and a bullet bar with left-aligned Low, Moderate, and High labels aligned to their bands.

#### Scenario: Score appears between Rollups and Top companies
- **WHEN** the user views the Explore tab with a calculated score
- **THEN** the score SHALL appear in a separate box after Rollups and before Top companies, and SHALL NOT be rendered as part of the Top companies section

#### Scenario: One-ETF scale is zero-width
- **WHEN** the score scale maximum is 0% for a single ETF
- **THEN** the box SHALL clearly show a 0% score and SHALL NOT imply any positive overlap range

#### Scenario: Viewport narrows
- **WHEN** the Explore tab is viewed on a narrow viewport
- **THEN** the score, band labels, and bar SHALL remain readable without horizontal overflow or overlapping content

### Requirement: Configure redundancy classification thresholds
The developer settings SHALL provide low/moderate and moderate/high thresholds in percentage points, defaulting to 10% and 25%. The application SHALL classify scores below the first threshold as Low, scores from the first threshold up to but not including the second as Moderate, and scores at or above the second threshold as High.

#### Scenario: Default thresholds classify the score
- **WHEN** no valid developer threshold preferences have been saved
- **THEN** the low/moderate threshold SHALL be 10% and the moderate/high threshold SHALL be 25%

#### Scenario: Developer changes valid thresholds
- **WHEN** the developer saves finite thresholds between 0% and 100% with the low/moderate value less than the moderate/high value
- **THEN** the score bands SHALL use the saved absolute percentage thresholds

#### Scenario: Developer enters invalid thresholds
- **WHEN** a threshold is non-finite, outside 0% to 100%, or the low/moderate threshold is not less than the moderate/high threshold
- **THEN** the invalid values SHALL NOT be applied to score classification

#### Scenario: Thresholds exceed the current bar maximum
- **WHEN** a valid configured threshold is greater than the current ETF-count-based bar maximum
- **THEN** score classification SHALL still use the configured absolute percentage values without extending the bar beyond its maximum

### Requirement: Do not show near-identical ETF pairs
The redundancy score calculation SHALL remain independent of pairwise overlap classification. The redundancy score box SHALL show a localized warning with a warning icon and affected product names at its bottom when any selected pair meets the configured near-identical threshold, and SHALL NOT show that warning when no selected pair meets the threshold.

#### Scenario: Score is rendered without pair detection
- **WHEN** no selected ETF pair meets the configured near-identical threshold
- **THEN** the redundancy score box SHALL NOT show near-identical pair labels, warnings, or recommendations

#### Scenario: Selected pair meets the threshold
- **WHEN** one or more selected ETF pairs have pairwise overlap at or above the configured near-identical threshold
- **THEN** the bottom of the redundancy score box SHALL show a localized warning with a warning icon and the affected product names, without changing the aggregate redundancy score

### Requirement: Explain aggregate portfolio redundancy
Explore SHALL provide an accessible information control in the redundancy score section. When activated, its explanation SHALL state that for each underlying security the score adds portfolio-weighted contributions across selected ETFs and subtracts the largest single-ETF contribution; the remaining amount is counted as duplicated exposure. It SHALL explain that the score is unavailable when a selected positive-allocation ETF lacks usable holdings.

#### Scenario: User opens redundancy information
- **WHEN** the user activates the redundancy score information control
- **THEN** the explanation SHALL describe the aggregate-contribution-minus-largest-contribution calculation and clarify that the score represents duplicated portfolio exposure

#### Scenario: User interprets unequal overlapping positions
- **WHEN** two ETFs have identical holdings and portfolio allocations of 70% and 30%
- **THEN** the explanation SHALL make clear that the 30% contributed by the smaller ETF is counted as redundant exposure

#### Scenario: Redundancy cannot be calculated
- **WHEN** a selected ETF with positive allocation has no usable holdings
- **THEN** the explanation SHALL identify incomplete holdings data as a reason the score may be unavailable
