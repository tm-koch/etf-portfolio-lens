# Spec Delta

## ADDED Requirements

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
