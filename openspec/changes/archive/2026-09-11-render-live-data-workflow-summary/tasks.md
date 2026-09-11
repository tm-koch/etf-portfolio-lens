## 1. Markdown Report Generation

- [x] 1.1 Add a deterministic formatter that reads the validated live-data artifact and includes its generation timestamp, quote ISINs, and prices with currencies.
- [x] 1.2 Include every FX pair and rate in a separate Markdown table, rendering `Unavailable` for unavailable or missing quote and FX values.
- [x] 1.3 Add unit coverage for available values, unavailable values, stable row ordering, and absence of provider or secret fields.

## 2. GitHub Actions Integration

- [x] 2.1 Add a workflow step after artifact validation that generates the Markdown report from `data/live_prices.json`.
- [x] 2.2 Append the report to `$GITHUB_STEP_SUMMARY` and expose the identical Markdown through a named multiline `$GITHUB_OUTPUT` value.
- [x] 2.3 Keep report generation before GitHub Pages publication and preserve existing failure and secret-handling behavior.

## 3. Workflow Contract Validation

- [x] 3.1 Extend workflow contract tests to require the formatter step, rendered summary destination, named output, and ordering before publication.
- [x] 3.2 Run focused live-data and workflow tests, then run the complete test suite.
- [x] 3.3 Validate the OpenSpec change and confirm all summary scenarios, including unavailable values, are covered.
