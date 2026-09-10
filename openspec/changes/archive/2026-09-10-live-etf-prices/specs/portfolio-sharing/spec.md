## ADDED Requirements

### Requirement: Share valuation mode without leaking private values
Full portfolio share payloads SHALL preserve the selected valuation mode and imported fallback fields when present, while private payloads SHALL continue to contain only ISINs and relative weighting units. Live quotes and FX rates SHALL be resolved from the recipient's latest published data and SHALL NOT be embedded in private payloads.

#### Scenario: Full link preserves hybrid mode
- **WHEN** a user shares a full portfolio configured for latest or hybrid valuation
- **THEN** the versioned payload preserves the valuation mode and any imported fallback fields so the recipient can recalculate from current published data

#### Scenario: Private link excludes market data
- **WHEN** a user creates a private share link
- **THEN** the payload contains no prices, currencies, FX rates, monetary values, quote timestamps, or provider information

#### Scenario: Older full link remains readable
- **WHEN** a recipient opens an existing full link without valuation-mode fields
- **THEN** the application treats it as legacy imported valuation data and loads it without rejecting the portfolio
