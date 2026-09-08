# ubs-smim-smi-etfs Specification

## Purpose
TBD - created by archiving change add-ubs-smim-smi-etfs. Update Purpose after archive.
## Requirements
### Requirement: Register UBS SMIM and SMI ETFs
The ETF registry SHALL contain entries for UBS SMIM ETF CHF dis (`CH0111762537`) and UBS SMI ETF CHF acc (`CH1447931341`) with their canonical fund-page URLs, provider `UBS`, expected format `xls`, parser ID `ubs_xml_xls_v1`, and local fixture paths.

#### Scenario: UBS SMIM registry entry is available
- **WHEN** the registry is loaded and queried for `CH0111762537`
- **THEN** it returns the UBS SMIM ETF metadata with `expected_format` equal to `xls` and `parser_id` equal to `ubs_xml_xls_v1`

#### Scenario: UBS SMI registry entry is available
- **WHEN** the registry is loaded and queried for `CH1447931341`
- **THEN** it returns the UBS SMI ETF metadata with `expected_format` equal to `xls` and `parser_id` equal to `ubs_xml_xls_v1`

### Requirement: Ingest the supplied UBS constituent workbooks
The ingestion pipeline SHALL parse the supplied SMIM and SMI workbooks through the existing UBS XML-in-XLS parser, retain every constituent row before the provider footer, and preserve provider ISIN, currency, price, and weight fields in normalized holdings provenance.

#### Scenario: SMIM fixture produces complete holdings
- **WHEN** fixture ingestion processes `CH0111762537`
- **THEN** the snapshot contains 30 holdings, all retained holdings have an ISIN and weight, and the weights total approximately 100%

#### Scenario: SMI fixture produces complete holdings
- **WHEN** fixture ingestion processes `CH1447931341`
- **THEN** the snapshot contains 20 holdings, all retained holdings have an ISIN and weight, and the weights total approximately 100%

#### Scenario: UBS legal footer is excluded
- **WHEN** either UBS fixture is parsed
- **THEN** no normalized holding is created from the provider legal disclaimer or source attribution text after the holdings table

### Requirement: Preserve offline and live source workflows
The integration SHALL use local fixtures when fixture mode is enabled and SHALL retain the canonical UBS product-page URL as the source URL for live ingestion. A live response that is HTML without a resolvable workbook link SHALL fail through the existing explicit download error path rather than being passed to the holdings parser.

#### Scenario: Fixture mode does not require UBS access
- **WHEN** either new ETF is ingested with fixture mode enabled
- **THEN** the pipeline reads its configured local fixture and does not request the UBS product page

#### Scenario: Live source metadata is preserved
- **WHEN** live ingestion successfully resolves a UBS workbook
- **THEN** the snapshot records the configured UBS product-page URL as `source_url` and records the downloaded workbook path as the resolved source

#### Scenario: Cookie-gated page is rejected clearly
- **WHEN** a UBS product page returns HTML without a downloadable XLS/XLSX/CSV link
- **THEN** ingestion raises the existing download error before invoking the holdings table parser and does not publish a partial snapshot

