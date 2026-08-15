## 1. Stable Mobile Geometry

- [x] 1.1 Define a mobile navigation row-height custom property based on the current intended navigation footprint.
- [x] 1.2 Set the mobile navigation and its inner destination row to explicit stable heights without dynamic safe-area values on Firefox Android.
- [x] 1.3 Set mobile destination buttons to the explicit row height instead of relying on intrinsic sizing or minimum height.
- [x] 1.4 Align mobile body bottom clearance with the stable Firefox Android footprint and add safe-area expansion only for stable WebKit mobile platforms.
- [x] 1.5 Preserve fixed positioning, edge-to-edge styling, active colors, accessibility, and unchanged desktop rules.
- [x] 1.6 Keep the mobile navigation on the basic opaque paint path without special compositor or containment hints that can cause scroll jitter.

## 2. Verification

- [ ] 2.1 Verify the navigation row and total navigation height remain stable during Firefox Android upward and downward scrolling.
- [ ] 2.2 Verify the icon-to-bottom spacing does not expand when the Firefox browser toolbar changes state.
- [ ] 2.3 Verify content remains reachable with and without a device bottom safe-area inset.
- [x] 2.4 Verify desktop Firefox responsive emulation and desktop navigation remain unchanged.
- [x] 2.5 Verify destination switching and active navigation behavior remain functional after the geometry changes.
