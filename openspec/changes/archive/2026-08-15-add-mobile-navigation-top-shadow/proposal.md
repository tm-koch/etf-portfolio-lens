## Why

The mobile navigation's white surface and the page content are currently separated only by a thin border, which makes the transition between the navigation and the site difficult to perceive. A small static shadow above the bar will improve visual separation without restoring the heavy card-like treatment or changing the navigation geometry.

## What Changes

- Add a small, static upward-facing shadow to the mobile navigation.
- Keep the shadow low-opacity and limited to the top boundary.
- Preserve the existing solid background, top border, fixed position, stable height, safe-area handling, and Firefox scroll-stability constraints.
- Keep desktop navigation styling unchanged.
- Do not animate the shadow or alter layout dimensions.

## Capabilities

### New Capabilities

### Modified Capabilities

- `bottom-navigation`: Refine mobile visual separation with a restrained static top shadow while preserving stable navigation behavior.

## Impact

- `web/styles.css`: Update the mobile-only navigation shadow declaration.
- Main bottom-navigation specification: Document the restrained top shadow requirement.
- No JavaScript, dependency, API, persistence, or desktop changes.
