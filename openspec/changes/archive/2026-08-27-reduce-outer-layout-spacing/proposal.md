## Why

The application currently uses generous page-level gutters and section gaps, which reduces the active area available for portfolio tables, charts, and exposure views. Reducing the outermost spacing by roughly one third will make the app feel denser and expose more useful content without changing the readable spacing inside cards and controls.

## What Changes

- Reduce desktop and tablet page-level outer gutters by approximately one third.
- Reduce the gap between top-level application sections by approximately one third.
- Preserve the existing maximum content width and centered layout.
- Preserve internal card, table, chart, control, and typography spacing.
- Preserve mobile full-width content and fixed bottom-navigation clearance.
- Verify that the denser shell does not cause overlap, clipping, or reduced control usability.

## Capabilities

### New Capabilities

- `outer-layout-density`: Defines the reduced page-shell gutters and top-level spacing while preserving internal component rhythm and responsive behavior.

### Modified Capabilities

None.

## Impact

- `web/styles.css`: page shell, content-column, and top-level layout spacing rules.
- New layout-density specification and implementation tasks.
- Browser verification at desktop, tablet, and mobile-sized viewports.
- No API, data model, dependency, or persistence changes.
