## MODIFIED Requirements

### Requirement: Canonical weight units
The ingestion backend SHALL write `weight_pct` values in the canonical snapshot using the unit semantics required by the source parser.

#### Scenario: Percent-based parser
- **WHEN** a parser emits weights already expressed as percentages
- **THEN** the backend SHALL preserve the raw numeric percentage value without multiplying it by 100

#### Scenario: Fraction-based parser
- **WHEN** a parser emits weights as fractions between 0 and 1
- **THEN** the backend SHALL convert the value to a percentage before storing it as `weight_pct`

#### Scenario: Source-specific normalization
- **WHEN** the backend normalizes a holding
- **THEN** it SHALL choose the weight conversion based on the parser ID for that source

### Requirement: Aggregate totals stay bounded
The ingestion backend SHALL validate that the sum of weights for each topic does not exceed 100 percent beyond a small rounding tolerance.

#### Scenario: Holdings total validation
- **WHEN** the backend finishes normalizing holdings for a source
- **THEN** the sum of holding weights for that source SHALL be less than or equal to 100 percent plus tolerance

#### Scenario: Sector total validation
- **WHEN** the backend computes sector rollups
- **THEN** the sum of sector weights SHALL be less than or equal to 100 percent plus tolerance

#### Scenario: Region total validation
- **WHEN** the backend computes region rollups
- **THEN** the sum of region weights SHALL be less than or equal to 100 percent plus tolerance

#### Scenario: Currency total validation
- **WHEN** the backend computes currency rollups
- **THEN** the sum of currency weights SHALL be less than or equal to 100 percent plus tolerance
