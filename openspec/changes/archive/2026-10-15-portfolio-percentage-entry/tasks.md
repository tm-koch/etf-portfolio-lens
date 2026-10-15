## 1. Portfolio Mode Control and State

- [x] 1.1 Add an accessible Shares / Allocation (%) mode control to the Portfolio tab and reflect the active mode.
- [x] 1.2 Implement shares-to-allocation conversion using current derived position weights and persist the normalized relative units without valuation fields.
- [x] 1.3 Switch to shares mode without a prompt, retaining all selected ETFs with share counts set to zero.
- [x] 1.4 Preserve legacy saved-portfolio defaults, selected-mode persistence, private share loading, and imported portfolio behavior.

## 2. Allocation Entry and Presentation

- [x] 2.1 Reuse percentage-mode rendering for local allocation entry, including decimal relative inputs, normalized Weight values, and clear relative-weight guidance.
- [x] 2.2 Ensure adding, editing, and removing positions in allocation mode persists relative units and refreshes dependent analysis without resolving absolute valuations.
- [x] 2.3 Keep valuation controls, provenance, price/value columns, and absolute summary values unavailable in allocation mode, while preserving the full shares-based presentation.

## 3. Verification

- [x] 3.1 Add focused runtime and contract tests for mode selection, conversion, normalized totals other than 100, zero-share transition, and persistence.
- [x] 3.2 Verify existing private-share payloads and imported/share-based portfolio behaviors remain compatible; run the focused web test suite.
