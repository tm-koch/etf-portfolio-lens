# Proposal

## Why

In the wide Selected positions view, each fund box sizes its metric columns independently, so Price, Value CHF, and Weight begin at different horizontal positions from row to row. Shared left-aligned columns will make the values easier to scan and compare across funds.

## What Changes

- Align the left edges of Price, Value CHF, and Weight consistently across all selected-position boxes in the wide layout.
- Preserve existing metric labels, values, position controls, percentage-only behavior, and mobile reflow.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `mobile-positions-layout`: Extend wide selected-position behavior to require consistent left alignment of metric columns across fund boxes.

## Impact

- `web/styles.css`: wide selected-position grid layout.
- `tests/test_web_runtime.py` and/or `tests/test_web_contract.py`: regression coverage for shared metric-column alignment.
- `openspec/specs/mobile-positions-layout/spec.md`: add the wide-layout alignment requirement.
