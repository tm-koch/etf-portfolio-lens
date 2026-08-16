## 1. Compact Mobile Styling

- [x] 1.1 Update the mobile navigation row variable and button geometry to a stable 64px height while preserving safe-area padding and content clearance.
- [x] 1.2 Reduce mobile navigation icons to 18px, labels to 0.75rem, the icon-label gap to 3px, and the item gap to 2px.
- [x] 1.3 Set inactive mobile navigation labels and icons to regular muted styling, and set only the active label and icon to bold accent-blue styling.
- [x] 1.4 Preserve the existing mobile full-width placement, transparent active background, restrained shadow, focus visibility, and desktop navigation rules.

## 2. Verification

- [x] 2.1 Verify the navigation remains compact, readable, and non-wrapping at 320px, 375px, 430px, and 760px widths.
- [x] 2.2 Verify each destination button remains at least 44px tall and page content remains reachable above the fixed navigation, including safe-area clearance.
- [x] 2.3 Verify inactive destinations are muted and regular weight while the active destination is blue and bold for both label and icon.
- [x] 2.4 Verify desktop navigation styling is unchanged and keyboard activation still updates the active panel and `aria-current="page"`.
