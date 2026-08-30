## 1. Desktop Layout

- [x] 1.1 Inspect the existing desktop Home hero and Portfolio heading geometry and select spacing values that clear the rendered color-mode control at representative wide desktop widths.
- [x] 1.2 Add desktop-only top spacing for Home's hero metadata/status region so it begins below the color-mode control without changing the primary title alignment.
- [x] 1.3 Add desktop-only top spacing for Portfolio's heading-side persistence note so it begins below the color-mode control without changing the primary title alignment.
- [x] 1.4 Inspect Compare and Explore heading geometry and select spacing values consistent with the existing desktop clearance.
- [x] 1.5 Add desktop-only top spacing for Compare and Explore heading-side explanatory text without changing their primary title alignment.

## 2. Contract Coverage

- [x] 2.1 Add focused assertions in `tests/test_web_contract.py` for the desktop-only clearance selectors and the unchanged mobile breakpoint boundary.
- [x] 2.2 Confirm the existing global color-mode behavior, accessibility semantics, and navigation contracts remain covered without altering unrelated expectations.
- [x] 2.3 Extend focused assertions for the Compare and Explore desktop clearance selectors.

## 3. Verification

- [x] 3.1 Run the focused web contract tests and fix any failures caused by the new layout rules.
- [x] 3.2 Use the local browser at a wide desktop viewport to verify Home and Portfolio secondary content do not overlap the selector and remain readable.
- [x] 3.3 Use the local browser at a compact mobile viewport to verify the selector trigger, panel flow, and fixed bottom navigation retain their existing geometry.
- [x] 3.4 Use the local browser at a wide desktop viewport to verify Compare and Explore secondary content do not overlap the selector and remain readable.
