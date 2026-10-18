# Spec Delta

## ADDED Requirements

### Requirement: Explain the effective-company calculation
Explore SHALL provide an accessible information control in the diversification score section. Its explanation SHALL expand HHI as the Herfindahl-Hirschman Index, describe HHI as the sum of squared normalized company shares, and explain that the score is its inverse and represents an effective number of equally weighted companies rather than the actual number of companies held.

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
