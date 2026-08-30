## Why

The mobile navigation became translucent when the shared navigation background token was introduced, changing the bright-mode shade from the established solid white treatment. Restore the historical bright appearance while giving dark mode an equivalent solid dark surface so the fixed navigation remains visually distinct and consistent with the surrounding theme.

## What Changes

- Restore a solid white background for the mobile navigation in Bright mode.
- Use the established solid dark navigation surface for mobile navigation in Dark mode.
- Add a Dark-mode-only 9px gradient edge above the mobile navigation, transitioning from a lighter dark-slate border tone to transparency over the frame.
- Preserve the existing mobile geometry, active-tab styling, restrained shadow, and flat Bright-mode navigation surface.
- Update the web contract coverage to assert the mobile theme-specific surfaces.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `bottom-navigation`: Define theme-appropriate solid mobile navigation surfaces while preserving existing placement, geometry, accessibility, and visual separation behavior.
- `dark-navigation-gradient`: Add a Dark-mode-only mobile gradient edge between the navigation bar and the surrounding frame.

## Impact

- `web/styles.css` mobile navigation background and Dark-mode edge-gradient rules.
- `tests/test_web_contract.py` navigation styling contract assertions.
- No runtime APIs, external dependencies, or data formats are affected.
