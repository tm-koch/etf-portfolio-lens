## Why

Dark mode currently presents the primary navigation as a flat panel, while the bright experience uses a light gradient to separate the navigation from the surrounding frame. Adding a restrained dark gradient will restore that visual separation without changing navigation behavior or layout.

## What Changes

- Add a dark-mode gradient edge beginning at the sticky primary navigation separator.
- Use theme-aware gradient colors that remain distinct from the dark page frame and readable behind navigation controls.
- Preserve the existing bright navigation appearance, responsive layout, and active-tab styling.
- Verify the gradient at desktop and mobile navigation breakpoints.

## Capabilities

### New Capabilities

- `dark-navigation-gradient`: Visual separation for the primary navigation in dark mode.

### Modified Capabilities

<!-- No existing capability requirements change. -->

## Impact

- `web/styles.css` dark-mode navigation styling and theme tokens.
- Web contract coverage for the dark navigation gradient.
- No backend, API, data, or dependency changes.
