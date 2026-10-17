# Spec Delta

## MODIFIED Requirements

### Requirement: Do not show near-identical ETF pairs
The redundancy score calculation SHALL remain independent of pairwise overlap classification. The redundancy score box SHALL show a localized warning with a warning icon and affected product names at its bottom when any selected pair meets the configured near-identical threshold, and SHALL NOT show that warning when no selected pair meets the threshold.

#### Scenario: Score is rendered without pair detection
- **WHEN** no selected ETF pair meets the configured near-identical threshold
- **THEN** the redundancy score box SHALL NOT show near-identical pair labels, warnings, or recommendations

#### Scenario: Selected pair meets the threshold
- **WHEN** one or more selected ETF pairs have pairwise overlap at or above the configured near-identical threshold
- **THEN** the bottom of the redundancy score box SHALL show a localized warning with a warning icon and the affected product names, without changing the aggregate redundancy score
