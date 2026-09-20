## ADDED Requirements

### Requirement: Configure a CHF live quote for the requested SIX listing
The live market-data configuration SHALL support a Swiss quote entry for `IE0009HF1MK9` using the existing Swiss adapter and the requested CHF SIX listing identifier.

#### Scenario: CHF quote configuration is valid
- **WHEN** quote configuration is loaded
- **THEN** the new entry identifies `IE0009HF1MK9`, the Swiss adapter, CHF currency, and the configured provider lookup reference without exposing a URL

#### Scenario: Swiss quote is normalized in CHF
- **WHEN** the configured Swiss source returns a valid price for `WEBGCHF SW`
- **THEN** the published quote is keyed by `IE0009HF1MK9` and has currency CHF

### Requirement: Preserve source currency during valuation
The live-data pipeline SHALL use the currency on the normalized quote for conversion decisions and SHALL not apply USD/CHF to a quote already denominated in CHF.

#### Scenario: CHF live source avoids FX conversion
- **WHEN** the new ETF has a valid CHF live quote and USD/CHF is also available
- **THEN** live valuation uses the CHF price directly without multiplying by USD/CHF

#### Scenario: USD source remains convertible
- **WHEN** the ETF is later configured with a valid USD quote or an imported USD value
- **THEN** the valuation layer uses the existing USD/CHF rate to calculate CHF value

### Requirement: Preserve live-data regression coverage
Live-data configuration tests SHALL include the new ISIN and continue validating the existing quote count, adapter constraints, and USD/CHF artifact behavior.

#### Scenario: Configuration test covers the new quote
- **WHEN** the live quote configuration contract is tested
- **THEN** `IE0009HF1MK9` is present with CHF source metadata and all previous configured entries remain present
