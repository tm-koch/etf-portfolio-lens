# ubs-spi-extra-etf Specification

## Purpose
TBD - created by archiving change add-ubs-spi-extra-etf. Update Purpose after archive.
## Requirements
### Requirement: UBS SPI Extra registry identity
The system SHALL identify UBS SPI® Extra ETF with ISIN `CH1553162921`, ticker `SPIEXT`, provider `UBS`, canonical name `UBS SPI® Extra ETF`, the supplied English UBS product page URL, expected format `xls`, parser ID `ubs_xml_xls_v1`, and its local holdings fixture.

#### Scenario: Registry entry is loadable
- **WHEN** the ETF registry is loaded
- **THEN** it contains one entry for ISIN `CH1553162921` with the specified identity and parser metadata

### Requirement: UBS SPI Extra fixture ingestion
The ingestion pipeline SHALL parse the supplied UBS SPI® Extra workbook through the existing UBS XML-spreadsheet path and produce normalized holdings and aggregates without changing the snapshot schema.

#### Scenario: Complete holdings are parsed
- **WHEN** the ETF is ingested with fixtures enabled
- **THEN** the generated snapshot contains 179 holdings and a holdings weight total within the existing aggregation tolerance of 100 percent

#### Scenario: Footer content is excluded
- **WHEN** the workbook parser reaches the first completely empty row after the holdings table
- **THEN** rows containing UBS source text, disclaimers, or other footer content are not normalized as holdings

### Requirement: UBS SPI Extra frontend availability
The published catalog SHALL expose a successful UBS SPI® Extra snapshot using the registry identity and a valid dated snapshot path.

#### Scenario: Catalog contains the ETF
- **WHEN** the catalog is regenerated from successful fixture ingestion
- **THEN** it contains `CH1553162921`, ticker `SPIEXT`, name `UBS SPI® Extra ETF`, provider `UBS`, and a snapshot path under `/data/raw/<run-date>/snapshots/CH1553162921.json`

#### Scenario: Existing frontend workflows load the ETF
- **WHEN** the frontend loads the regenerated catalog and referenced snapshot
- **THEN** UBS SPI® Extra is available to the existing Portfolio, Compare, and Explore workflows without ETF-specific frontend code

