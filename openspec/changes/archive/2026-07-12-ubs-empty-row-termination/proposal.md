## Why

The UBS holdings file for CH0130595124 includes an empty row that marks the end of the actual holdings table, followed by disclaimer text that is not part of the portfolio data. The current parser continues past that break and risks treating post-table rows as holdings-like rows, which can pollute the snapshot output.

## What Changes

- Stop parsing the UBS holdings table once the first empty row in the table is reached.
- Ignore all rows after that termination point for the CH0130595124 UBS source.
- Preserve the current parsing behavior for other ETF sources unless they also use the same table-termination pattern.
- Keep the raw downloaded source file unchanged and continue to retain provenance for parsed holdings.

## Capabilities

### New Capabilities
- `ubs-empty-row-termination`: stop the UBS holdings parser at the first empty row so disclaimer rows after the holdings table are ignored.

### Modified Capabilities
-

## Impact

Affected areas include the UBS parser path, the ingestion snapshot contents for CH0130595124, and the fixture-based tests that validate the end of the holdings table. This change should reduce false holdings and prevent disclaimer text from being parsed as portfolio data.
