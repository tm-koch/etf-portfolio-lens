## ADDED Requirements

### Requirement: Parse USD Saxo positions with source currency preserved
The Saxo import parser SHALL recognize USD in section-level and row-level currency fields and SHALL attach the parsed source currency to the imported position without replacing it with the ETF share-class or registry currency.

#### Scenario: USD section and row are parsed
- **WHEN** a Saxo report contains a USD holdings section and a row for `IE0009HF1MK9`
- **THEN** the imported row contains currency USD, the correct shares, price, and value

#### Scenario: CHF WEBGCHF row remains CHF
- **WHEN** a Saxo report contains the SIX CHF listing `WEBGCHF SW` for `IE0009HF1MK9`
- **THEN** the imported row contains currency CHF and its imported CHF value is not converted through USD/CHF

### Requirement: Keep source-driven display and conversion
Portfolio valuation SHALL determine display currency and FX conversion from the active live quote or imported position source, not from the ETF's fund/share-class currency or constituent currencies.

#### Scenario: CHF live quote for USD share class
- **WHEN** the selected ETF has a valid CHF live quote while its share-class currency is USD
- **THEN** the price displays as CHF and the effective CHF value uses the quote directly

#### Scenario: USD imported source uses USD/CHF
- **WHEN** the selected ETF has an imported USD position and a valid USD/CHF rate
- **THEN** the imported value is converted to CHF using USD/CHF and the source currency remains visible as USD

#### Scenario: Missing required USD FX remains unavailable
- **WHEN** an imported USD position has no valid USD/CHF rate and no usable fallback value
- **THEN** its converted CHF valuation remains unavailable rather than being treated as CHF
