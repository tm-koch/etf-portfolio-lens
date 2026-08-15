## 1. Mobile Navigation Boundary

- [x] 1.1 Replace the mobile navigation's `box-shadow: none` with the restrained static top shadow `0 -2px 8px rgba(22, 34, 58, 0.10)`.
- [x] 1.2 Preserve the existing top border, solid background, fixed geometry, safe-area variables, and no-animation behavior.
- [x] 1.3 Confirm the desktop navigation shadow and styling remain unchanged.

## 2. Verification

- [x] 2.1 Verify the top shadow visibly separates the mobile navigation from page content without becoming prominent.
- [x] 2.2 Verify the shadow does not change navigation height, row height, safe-area spacing, or body bottom clearance.
- [x] 2.3 Verify scrolling and destination switching do not animate or alter the shadow.
- [x] 2.4 Verify desktop navigation appearance remains unchanged.
