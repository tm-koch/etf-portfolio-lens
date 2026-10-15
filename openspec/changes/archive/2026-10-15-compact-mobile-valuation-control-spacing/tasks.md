# Tasks

## 1. Compact the phone layout

- [x] 1.1 Override `.portfolio-valuation-details` sizing in the existing `max-width: 480px` rule and update the stylesheet cache-busting URL; verify the focused web contract test passes.
- [x] 1.2 Add or update a web contract test for the phone-specific natural-height and full-width sizing; verify it passes with `python -m unittest tests.test_web_contract`.

## 2. Verify responsive rendering

- [x] 2.1 Inspect the selected-positions panel in a browser at 390px and 320px widths; verify the valuation controls follow Entry mode with compact spacing, wrap without horizontal overflow, and retain their status.
- [x] 2.2 Inspect the same panel at a desktop width; verify the desktop valuation layout and spacing remain unchanged.

## 3. Align the valuation status

- [x] 3.1 Keep the Live status on the same mobile row as the valuation selector, vertically align it with the select, and add a contract assertion; verify `python -m unittest tests.test_web_contract` passes.
- [x] 3.2 Verify at 390px and 320px that selector and status share one row without page overflow, then check desktop layout remains unchanged in the browser.
