## ADDED Requirements

### Requirement: Support verified canonical display aliases
The ingestion backend SHALL support an exact-ISIN identity override that supplies a verified canonical display name and stable company ID for a matched holding while preserving the original provider and security-master values in provenance.

#### Scenario: TSMC uses the verified English alias
- **WHEN** a holding has ISIN `TW0002330008` and the identity override is loaded
- **THEN** the normalized holding uses company ID `taiwan-semiconductor-manufacturing-co` and canonical name `Taiwan Semiconductor Manufacturing Co.`

#### Scenario: Alias override takes precedence over the security master
- **WHEN** the security master matches `TW0002330008` with a different name
- **THEN** the normalized holding retains the override canonical name and is marked as overridden rather than displaying the security-master name

#### Scenario: Original source identity remains auditable
- **WHEN** the TSMC alias is applied
- **THEN** the raw provider fields and security-master provenance remain present and the override does not alter unrelated classification or exposure fields

#### Scenario: Unrelated instruments are unchanged
- **WHEN** a holding has an ISIN other than `TW0002330008`
- **THEN** the TSMC alias is not applied and the holding follows existing identity-enrichment behavior
