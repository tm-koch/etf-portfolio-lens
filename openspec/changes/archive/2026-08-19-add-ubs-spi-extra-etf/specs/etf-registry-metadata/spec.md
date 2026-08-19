## ADDED Requirements

### Requirement: UBS SPI Extra registry metadata
The ETF registry SHALL include the canonical identity and fixture metadata for UBS SPI® Extra ETF in addition to its existing ETF entries.

#### Scenario: New UBS identity is represented
- **WHEN** registry metadata is read for ISIN `CH1553162921`
- **THEN** the entry uses ticker `SPIEXT`, name `UBS SPI® Extra ETF`, provider `UBS`, and the English UBS product page as `source_url`

#### Scenario: Existing registry entries remain available
- **WHEN** the registry is loaded after the new entry is added
- **THEN** all existing ETF entries remain present and unchanged
