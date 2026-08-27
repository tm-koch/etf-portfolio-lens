## Why

In the mobile Selected positions cards, the Shares input and Remove icon occupy control boxes while the Weight percentage sits against the top of its cell. Vertically centering the percentage with those controls will make each lower control row read as one intentional unit without changing the desktop table.

## What Changes

- Vertically center the mobile Weight percentage against the Shares input and Remove icon.
- Scope the alignment change to the mobile position reflow so desktop and tablet table behavior remain unchanged.
- Preserve the existing percentage value, accessible Weight label, input behavior, and Remove icon behavior.

## Capabilities

### New Capabilities

<!-- No new capabilities are introduced. -->

### Modified Capabilities

- `mobile-positions-layout`: Align the mobile Weight value with the neighboring Shares and Remove controls.

## Impact

- `web/styles.css`: mobile-only alignment for the position Weight cell.
- Existing web contract and browser checks: verify the mobile geometry and unchanged larger-viewport table layout.
- No data, calculation, backend, dependency, or public API changes.
