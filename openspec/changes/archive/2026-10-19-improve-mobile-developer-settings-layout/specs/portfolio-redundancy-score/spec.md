# Spec Delta

## MODIFIED Requirements

### Requirement: Configure redundancy classification thresholds
The developer settings SHALL provide low/moderate and moderate/high thresholds in percentage points, defaulting to 10% and 25%. The application SHALL classify scores below the first threshold as Low, scores from the first threshold up to but not including the second as Moderate, and scores at or above the second threshold as High. The two threshold fields SHALL remain side by side at smartphone viewport widths.

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

#### Scenario: Threshold fields remain paired on smartphones
- **WHEN** the developer settings are viewed at a smartphone viewport width
- **THEN** the low/moderate and moderate/high threshold fields SHALL appear side by side
