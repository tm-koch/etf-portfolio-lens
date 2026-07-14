## 1. Normalize weight units in the backend

- [x] 1.1 Update the holdings normalization path so parsed provider weights are converted to percentage numbers before they are stored on the canonical holding model.
- [x] 1.2 Ensure aggregate generation uses the same percentage unit for `sector_weights`, `region_weights`, and `currency_weights`.
- [x] 1.3 Confirm the serialized snapshot output still uses the `weight_pct` field name everywhere the unit changes apply.

## 2. Update validation and fixtures

- [x] 2.1 Add or update backend tests so a representative snapshot asserts `weight_pct` values are percentage numbers rather than fractions.
- [x] 2.2 Regenerate or refresh sample snapshot data used by tests so the published JSON reflects the new unit contract.
- [x] 2.3 Verify the MEUD snapshot shows currency and region weights as percentages, including the known `0.2517` example becoming `25.17`.

## 3. Check downstream compatibility

- [x] 3.1 Verify the web consumer renders the updated snapshot values correctly without additional unit conversion.
- [x] 3.2 Run the focused ingestion test suite against the changed snapshots and confirm no unit-related regressions remain.
