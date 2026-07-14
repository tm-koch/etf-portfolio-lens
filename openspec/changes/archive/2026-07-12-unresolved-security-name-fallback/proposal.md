## Why

Some holdings arrive with a valid ISIN but cannot be resolved against the security master, leaving `security.name` null even though the source file still provides a readable name. That makes unresolved holdings harder to inspect and compare, especially when the raw source already contains a useful label.

## What Changes

- Preserve the provider/source security label as a fallback `security.name` when a holding cannot be fully enriched.
- Keep the canonical security fields empty when no match exists, but avoid a blank display name when the source file already provides one.
- Continue to record unresolved holdings and match diagnostics so fallback naming does not hide enrichment failures.
- Do not change matching rules or claim a successful security-master match when enrichment fails.

## Capabilities

### New Capabilities
- `security-name-fallback`: preserve the source-provided name for unresolved holdings when canonical enrichment cannot resolve a security record.

### Modified Capabilities
-

## Impact

Affected areas include the normalization layer, the normalized snapshot output, and the tests that assert unresolved holdings and match diagnostics. No external API changes are expected, but the JSON contract gains a more useful fallback value for unresolved holdings.
