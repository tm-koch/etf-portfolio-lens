## 1. Restore Mobile Card Boundary

- [x] 1.1 Remove the mobile-only suppression that prevents each `.position-row` from rendering its bottom border, while preserving cell-level border suppression and the existing mobile grid.
- [x] 1.2 Verify at a phone-sized viewport that each selected-position row has continuous top, right, bottom, and left edges and no horizontal overflow.

## 2. Add Regression Coverage

- [x] 2.1 Add a focused web contract assertion for the mobile position-row border requirement and retain checks for the existing mobile grid areas.
- [x] 2.2 Run the focused web contract tests and inspect the rendered mobile card with the local browser/server when available.

## 3. Validate Compatibility

- [x] 3.1 Run the full test suite and confirm desktop/tablet position layout behavior remains covered and unchanged.
- [x] 3.2 Review the final diff for unrelated styling or generated-file changes.
