## 1. Navigation Feedback Styling

- [x] 1.1 Add a scoped tap-highlight override for primary mobile navigation buttons.
- [x] 1.2 Add an intentional `:active` pressed state that remains legible in Bright and Dark modes.
- [x] 1.3 Add or refine `:focus-visible` styling so keyboard focus remains distinct from pressed and active states.
- [x] 1.4 Confirm the existing `.active` styling and synchronous `setTab()` behavior remain unchanged across mobile and desktop navigation.

## 2. Regression Coverage

- [x] 2.1 Extend web contract tests to require the scoped tap-highlight, pressed-state, and focus-visible rules.
- [x] 2.2 Add or update interaction assertions that activating a navigation button updates `.active`, `aria-current`, and the matching panel synchronously.
- [x] 2.3 Run the focused web contract tests and the relevant browser check at a mobile viewport in Bright and Dark modes.

## 3. Release Verification

- [x] 3.1 Verify Chrome Mobile no longer shows the default tap flash and that canceled presses do not change tabs.
- [x] 3.2 Confirm desktop navigation, keyboard navigation, and PWA shell behavior are unchanged before publishing.
