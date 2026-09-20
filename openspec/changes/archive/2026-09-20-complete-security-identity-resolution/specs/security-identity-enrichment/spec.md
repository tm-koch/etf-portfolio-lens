## ADDED Requirements

### Requirement: Resolve reviewed provider identities by exact ISIN
The resolver SHALL apply verified review mappings for provider holdings that lack source ISINs, including canonical company identity where supplied, without relying on ticker-only inference.

#### Scenario: Reviewed missing-ISIN holding receives identity
- **WHEN** a provider holding matches a reviewed mapping for `AGS`, `DSFIR`, `INPST`, `OCTV SDB`, or `SN.`
- **THEN** the normalized holding SHALL contain the supplied exact ISIN and SHALL retain the provider identifier and raw source fields

#### Scenario: QIA resolves as Qiagen
- **WHEN** a provider row has ticker `QIA`, name `QIAGEN` or `QIAGEN NV`, and Deutsche Börse Xetra / Germany context
- **THEN** the resolver SHALL assign ISIN `NL0015002SN0` and canonical identity `Qiagen NV`

#### Scenario: Liquidity funds remain excluded from company identity
- **WHEN** a provider row has identifier `ICSEAGD` or `ICSSAGD`
- **THEN** the resolver SHALL retain the row but SHALL exclude it from company identity aggregation and SHALL NOT fabricate a company identity

### Requirement: Preserve provider and security-master venue provenance
The resolver SHALL preserve provider exchange and country independently from security-master venue metadata and SHALL record a discrepancy when a verified ISIN has a different security-master venue label.

#### Scenario: QIA venue discrepancy remains auditable
- **WHEN** `QIA` is resolved with provider context Deutsche Börse Xetra / Germany and ISIN `NL0015002SN0`
- **THEN** the snapshot SHALL retain the provider venue and SHALL record that the security-master venue label is LSE

### Requirement: Keep unresolved decisions explicit
The resolver SHALL leave holdings unresolved or ambiguous when no verified exact ISIN decision exists for the four name-only collisions or ticker/context conflicts.

#### Scenario: Ticker conflict is not guessed
- **WHEN** a reviewed ticker/context conflict has no verified ISIN mapping
- **THEN** the resolver SHALL retain the holding with an explicit ambiguous diagnostic rather than selecting a security-master record arbitrarily
