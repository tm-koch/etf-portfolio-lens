# Proposal

## Why

In compact Explore preview on wide screens, the table header sticks at the viewport top beneath the higher-stacking sticky primary navigation, which can obscure the entire header. The header should remain visible while scrolling without competing with the navigation.

## What Changes

- Position the compact Explore preview table header below the sticky primary navigation on wide screens.
- Preserve the header's page-scroll boundary, horizontal column alignment, and mobile behavior.
- Update the Explore table styling requirement and add regression coverage for the desktop navigation offset.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `explore-preview-table-styling`: Specify that the sticky header remains visible below the wide-screen navigation and retains the existing table-boundary and horizontal alignment behavior.

## Impact

The compact Explore sticky-header rules in `web/styles.css` and their regression coverage in `tests/test_web_contract.py` are affected. No API or dependency changes are expected.