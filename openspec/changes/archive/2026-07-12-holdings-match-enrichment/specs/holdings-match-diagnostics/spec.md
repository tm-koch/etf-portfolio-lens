## ADDED Requirements

### Requirement: Record match diagnostics for each holding
The system MUST record match diagnostics for each normalized holding, including which required elements were missing and which match strategies were attempted.

#### Scenario: Missing elements are listed in output
- **WHEN** a holding cannot be fully matched or enriched
- **THEN** the system MUST include a list of missing elements such as `isin`, `ticker`, `exchange`, or `name` in the output diagnostics

#### Scenario: Match attempts are recorded
- **WHEN** a holding is processed through the matching pipeline
- **THEN** the system MUST record the match strategies attempted in order

### Requirement: Populate missing ISIN from the security master when ticker match is unique
The system MUST populate a missing ISIN from `data/tickers.csv` when the holding ticker uniquely matches one security master record.

#### Scenario: Unique ticker match fills ISIN
- **WHEN** a holding has no ISIN and its ticker matches exactly one record in the security master
- **THEN** the system MUST copy the matched record's ISIN into the normalized holding output

#### Scenario: Ambiguous ticker match does not guess
- **WHEN** a holding has no ISIN and its ticker matches more than one security master record
- **THEN** the system MUST leave the ISIN unresolved and MUST record an ambiguity warning

### Requirement: Preserve unresolved holdings with explicit status
The system MUST preserve holdings that remain unmatched after enrichment and mark them as unresolved in the output.

#### Scenario: Unresolved holding remains in output
- **WHEN** a holding cannot be matched by ISIN, ticker plus exchange, ticker-only unique fallback, or aliases
- **THEN** the system MUST keep the holding in the output with an unresolved match status

#### Scenario: Unresolved holdings trigger a warning
- **WHEN** a holding remains unresolved after all match strategies are attempted
- **THEN** the system MUST emit a console warning that includes the holding identifier and the missing elements
