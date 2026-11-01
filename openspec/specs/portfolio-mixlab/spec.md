# portfolio-mixlab Specification

## Purpose
MixLab lets users compare illustrative ETF mixes locally, balancing exposure similarity, fees, diversification, and fund count while making data quality and assumptions visible.

## Requirements

### Requirement: Provide a dedicated Lab destination
The application SHALL provide a primary navigation destination labelled Lab that opens the MixLab interface and remains available when the portfolio is empty.

#### Scenario: Open Lab from primary navigation
- **WHEN** a user activates Lab
- **THEN** the MixLab panel becomes active and the existing portfolio remains unchanged

#### Scenario: Open Lab with an empty portfolio
- **WHEN** a user opens Lab without selected portfolio positions
- **THEN** the custom fund-sleeve mode remains available and the consolidation mode explains that a portfolio is required

#### Scenario: Show the applicable consolidation state
- **WHEN** a user opens consolidation with or without portfolio positions
- **THEN** MixLab shows only the empty-portfolio message or the current-portfolio summary that applies, without reserving space for the hidden state

#### Scenario: Match Explore card spacing
- **WHEN** consolidation state cards are rendered in the Lab panel
- **THEN** their vertical gap matches the 18px spacing between cards in Explore

### Requirement: Consolidate a current portfolio by country exposure
MixLab SHALL derive a country-bucket exposure target from the selected portfolio and compare candidate mixes against that target using proportional overlap. The default minimum overlap SHALL be 97% and users SHALL be able to change it.

#### Scenario: Build target from a shares-based portfolio
- **WHEN** a user runs consolidation with valued portfolio positions
- **THEN** the target country exposures use each position's normalized portfolio weight and disclosed underlying country weights

#### Scenario: Build target from a percentage-only portfolio
- **WHEN** a user runs consolidation in relative-allocation mode
- **THEN** the target country exposures use the normalized relative allocation weights without requiring share counts

#### Scenario: Candidate is within exposure tolerance
- **WHEN** a candidate's proportional overlap meets or exceeds the selected threshold
- **THEN** the result identifies it as meeting the exposure constraint

#### Scenario: Candidate is outside exposure tolerance
- **WHEN** a candidate's proportional overlap is below the selected threshold
- **THEN** it is not presented as a qualifying consolidation

### Requirement: Use exclusive and auditable country buckets
Country exposure SHALL use a versioned mapping in which each recognized country belongs to at most one geographic bucket, with Switzerland separate from other Europe and an explicit unclassified bucket.

#### Scenario: Classify a recognized country
- **WHEN** a holding has a recognized country identifier
- **THEN** its weight contributes to exactly one country bucket

#### Scenario: Preserve unclassified exposure
- **WHEN** a holding has no recognized country identifier or bucket mapping
- **THEN** its weight contributes to unclassified exposure and is not silently discarded

#### Scenario: Show mapping methodology
- **WHEN** a user inspects MixLab assumptions
- **THEN** the country classification source, mapping version or date, and treatment of unclassified exposure are disclosed

### Requirement: Build custom mixes from fund sleeves
MixLab SHALL allow users to enter percentage allocations across explicitly classified fund sleeves. Sleeve allocations SHALL total 100% to run a comparison and SHALL be distinguished from the resulting look-through country exposures.

#### Scenario: Enter custom sleeve allocations
- **WHEN** a user enters non-negative sleeve weights totaling 100%
- **THEN** MixLab searches eligible catalog products for a mix matching those sleeve allocations

#### Scenario: Sleeve allocations do not total 100%
- **WHEN** entered sleeve weights total less or more than 100%
- **THEN** MixLab identifies the total and does not run the comparison until it equals 100%

#### Scenario: World and regional sleeves overlap
- **WHEN** a custom mix includes World and one or more regional sleeves
- **THEN** the interface explains that sleeves are investment allocations that may overlap and shows the candidate's resulting look-through exposures separately

#### Scenario: Distinguish developed World from all-country World
- **WHEN** a catalog contains developed-world and all-country-world products
- **THEN** MixLab presents them as distinct sleeve classifications and does not infer the distinction from a ticker alone

#### Scenario: Label the sleeve allocation card
- **WHEN** custom sleeve allocation controls are rendered
- **THEN** the card title appears inside the card border and labels the control group

### Requirement: Balance TER and effective-company breadth
MixLab SHALL let users balance weighted TER against the effective number of underlying companies with a slider. It SHALL calculate effective company breadth from aggregated look-through company weights and SHALL use fewer ETFs as a tie-breaker between otherwise equivalent candidates.

#### Scenario: Prioritize lower TER
- **WHEN** the slider is set to its lower-TER endpoint
- **THEN** qualifying candidates are ranked primarily by lower weighted TER

#### Scenario: Prioritize effective-company breadth
- **WHEN** the slider is set to its higher-diversification endpoint
- **THEN** qualifying candidates are ranked primarily by higher effective number of companies

#### Scenario: Candidates have equivalent objective scores
- **WHEN** two qualifying candidates have equivalent weighted objective scores
- **THEN** the candidate with fewer ETFs ranks first

### Requirement: Apply enabled TER and diversification limits
MixLab SHALL provide independently enabled maximum weighted TER and minimum effective-company limits, report each limit's state for displayed candidates, and use available current-portfolio metrics as their initial values.
The maximum-TER label SHALL identify the value as a percentage. TER input precision SHALL be limited to three decimal places and minimum effective-company precision to one decimal place.

#### Scenario: Initialize limits from the current portfolio
- **WHEN** a current portfolio has weighted TER and effective-company metrics available and the user has not edited the limit values
- **THEN** the maximum TER and minimum effective-company inputs use those portfolio metrics while their constraint checkboxes remain disabled

#### Scenario: Preserve edited limit values
- **WHEN** the user edits either portfolio-derived limit and then changes the portfolio
- **THEN** MixLab preserves that edited value and may refresh the other untouched limit

#### Scenario: Refresh untouched limit defaults
- **WHEN** the portfolio changes and a limit value has not been edited
- **THEN** MixLab refreshes that limit from the corresponding available current-portfolio metric

#### Scenario: Apply limit input precision
- **WHEN** a user commits a limit value with more decimal places than allowed
- **THEN** the maximum TER value is rounded to at most three decimal places and the minimum effective companies value to at most one decimal place

#### Scenario: Enter fractional limit values
- **WHEN** a user types a fractional maximum TER or minimum effective companies value within the allowed precision
- **THEN** the decimal value remains editable and is accepted without being rewritten during typing

#### Scenario: Enforce enabled limits
- **WHEN** one or both limits are enabled
- **THEN** only candidates satisfying every enabled limit are labelled qualifying

#### Scenario: No candidate satisfies all enabled limits
- **WHEN** no candidate satisfies the exposure requirement and all enabled limits
- **THEN** MixLab reports that no qualifying mix was found and shows closest alternatives with each unmet constraint identified

#### Scenario: Limits are disabled
- **WHEN** a limit is disabled
- **THEN** its value does not exclude candidates from the qualifying results

### Requirement: Filter distribution policy explicitly
MixLab SHALL offer Both, Accumulating, and Distributing distribution-policy choices, defaulting to Both. A selected single policy SHALL exclude candidates that do not match it.

#### Scenario: Default to both policies
- **WHEN** a user opens MixLab without a saved filter
- **THEN** both accumulating and distributing products are eligible

#### Scenario: Restrict to one distribution policy
- **WHEN** a user selects Accumulating or Distributing
- **THEN** only catalog products with that policy are eligible and the selected policy is visible in results

### Requirement: Estimate annual TER costs
MixLab SHALL show weighted TER and estimated annual TER cost for candidate mixes. Percentage-only portfolios SHALL have an editable portfolio-value input defaulting to CHF 10,000, and savings SHALL be shown only when a current-portfolio TER baseline is available.

#### Scenario: Estimate costs for a percentage-only portfolio
- **WHEN** a percentage-only portfolio is compared
- **THEN** the annual cost estimate uses the entered CHF portfolio value, defaulting to CHF 10,000

#### Scenario: Current TER baseline is unavailable
- **WHEN** no reliable TER is available for every current portfolio position
- **THEN** MixLab shows the candidate TER and annual cost estimate but does not claim annual savings

#### Scenario: Show signed annual cost change
- **WHEN** a current-portfolio TER baseline is available
- **THEN** MixLab shows candidate annual TER cost minus baseline annual TER cost, with a negative value indicating a cost improvement

#### Scenario: Display fee estimate caveat
- **WHEN** MixLab displays annual cost or savings estimates
- **THEN** it identifies TER as an estimate and states that taxes and trading costs are excluded

### Requirement: Disclose exposure coverage and retain snapshot provenance
MixLab SHALL show classified country-exposure coverage for the target and each candidate, including unclassified weight. Source snapshot dates MAY remain in the underlying data for provenance but SHALL NOT be rendered in MixLab result cards. A candidate SHALL NOT be labelled as meeting exposure tolerance when the target or candidate has less than 95% classified country exposure.

#### Scenario: Exposure coverage meets minimum
- **WHEN** target and candidate each have at least 95% classified exposure
- **THEN** MixLab may label the proportional-overlap result as a qualifying exposure match

#### Scenario: Exposure coverage is below minimum
- **WHEN** target or candidate has less than 95% classified exposure
- **THEN** MixLab shows the coverage and SHALL NOT claim that the exposure tolerance is met

#### Scenario: Snapshot dates differ
- **WHEN** the target portfolio and candidate snapshots have different source dates
- **THEN** MixLab shows the exposure coverage without displaying snapshot dates in result cards

### Requirement: Show weighted portfolio TER on Home
The Home summary SHALL display weighted portfolio TER when every selected position has verified TER metadata and valid portfolio weights. It SHALL display estimated annual CHF cost only for a value-based portfolio with complete CHF valuations, except that an empty portfolio SHALL show zero TER and zero annual CHF cost. Percentage-only portfolios SHALL show weighted TER and mark the absolute CHF cost unavailable. Missing TER SHALL NOT be treated as zero for a non-empty portfolio.

#### Scenario: Portfolio is empty
- **WHEN** no portfolio positions are selected
- **THEN** the Home summary shows 0% weighted TER and CHF 0.00 annual TER cost

#### Scenario: Valued portfolio has complete TER metadata
- **WHEN** every selected position has a valid CHF valuation and TER
- **THEN** the Home summary shows value-weighted TER and annual CHF cost

#### Scenario: Portfolio uses percentage allocations
- **WHEN** the selected portfolio uses relative percentage allocations
- **THEN** the Home summary shows TER weighted by those allocations and indicates that annual CHF cost is unavailable

#### Scenario: TER or valuation data is incomplete
- **WHEN** a selected position lacks TER metadata or a required CHF valuation
- **THEN** the affected Home summary metric is unavailable rather than estimated as zero

### Requirement: Keep MixLab outside PDF reports
MixLab inputs, settings, and modeled alternatives SHALL NOT be added to the existing PDF report.

#### Scenario: Generate a PDF after using MixLab
- **WHEN** a user generates a portfolio or catalog PDF after using MixLab
- **THEN** the PDF contains no MixLab inputs, results, or recommendations

### Requirement: Include weighted portfolio TER in PDF summaries
The PDF portfolio summary SHALL show weighted TER derived from verified metadata and valid portfolio weights. An empty portfolio SHALL show zero TER, while incomplete TER data SHALL be unavailable. The metric SHALL be independent of MixLab inputs and results.

#### Scenario: PDF portfolio has complete TER data
- **WHEN** a user exports a portfolio with valid weights and verified TER for every selected position
- **THEN** the PDF TER card shows the portfolio's weighted TER

#### Scenario: PDF portfolio is empty
- **WHEN** a user exports an empty portfolio
- **THEN** the PDF TER card shows 0% weighted TER

#### Scenario: PDF portfolio TER data is incomplete
- **WHEN** a non-empty portfolio has missing or unverified TER metadata
- **THEN** the PDF TER card shows weighted TER as unavailable rather than treating missing TER as zero

### Requirement: Show annual TER cost in PDF
The PDF TER card SHALL show estimated annual CHF cost only when the portfolio has verified TER data and complete CHF valuations. Percentage-only portfolios SHALL show the cost as unavailable.

#### Scenario: PDF TER cost has complete valuations
- **WHEN** every selected position has verified TER and a positive CHF valuation
- **THEN** the PDF TER card shows the estimated annual CHF cost

#### Scenario: PDF TER cost has incomplete valuations
- **WHEN** any selected position has an unavailable CHF valuation or the portfolio uses percentages
- **THEN** the PDF TER card shows annual CHF cost as unavailable

#### Scenario: PDF portfolio is empty for TER cost
- **WHEN** a user exports an empty portfolio
- **THEN** the PDF TER card shows CHF 0.00 annual cost

#### Scenario: PDF portfolio uses percentage allocations
- **WHEN** a user exports a percentage-only portfolio with complete TER metadata
- **THEN** the PDF TER card shows weighted TER and marks annual CHF cost unavailable

#### Scenario: PDF summary content clears the footer
- **WHEN** a PDF summary includes weighted TER and annual-cost detail
- **THEN** the summary metric cards and following analytics sections do not overlap the page footer
