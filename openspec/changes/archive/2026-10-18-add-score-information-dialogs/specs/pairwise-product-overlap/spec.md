# Spec Delta

## ADDED Requirements

### Requirement: Explain pairwise product overlap
Explore SHALL provide an accessible information control in the pairwise product overlap section. When activated, its explanation SHALL state that each cell compares one ETF pair and adds the smaller disclosed weight for each shared underlying security or company. It SHALL clarify that overlap uses disclosed weights as reported, is not renormalized for incomplete holdings, and that coverage is shown for both ETFs.

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
