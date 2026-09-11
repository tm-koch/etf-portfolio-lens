## Context

The live-market-data workflow generates `data/live_prices.json`, validates it with `LivePricesArtifact.from_dict`, and then publishes the GitHub Pages site. The artifact contains normalized quote records keyed by ISIN and FX records keyed by pair, including status fields that distinguish available values from unavailable ones. GitHub Actions provides `$GITHUB_STEP_SUMMARY` for rendered Markdown on a workflow run and `$GITHUB_OUTPUT` for reusable step outputs.

The summary must be based on the validated artifact so the displayed values cannot diverge from the data that is published. It must not expose provider URLs, credentials, raw responses, or other secret-backed configuration.

## Goals / Non-Goals

**Goals:**

- Render a readable Markdown report after artifact validation and before publication.
- Include generation time, every quote ISIN, price with currency, every FX pair, and its rate.
- Render unavailable quote and FX records as `Unavailable` rather than dropping them.
- Write the report to `$GITHUB_STEP_SUMMARY` and expose the same content through a named step output.
- Keep formatting deterministic so it can be covered by focused tests.

**Non-Goals:**

- Changing the live JSON schema or quote/FX fetching behavior.
- Adding provider names, source URLs, raw response data, or secret values to the report.
- Changing publication atomicity or committing generated data to `main`.
- Creating a separate workflow job solely for reporting.

## Decisions

- Generate the report from `data/live_prices.json` after the existing validation step. This ensures the report reflects the exact artifact passed to publication rather than an unvalidated intermediate object.
- Use a small repository-owned formatter, preferably a Python helper that reads the artifact and emits Markdown. This keeps JSON parsing and unavailable-value rules testable without relying on shell-specific JSON tooling.
- Sort quote rows by ISIN and FX rows by pair for stable output, independent of JSON insertion order. Display available prices as `<currency> <price>` and available rates as numeric values; display `Unavailable` when status is not `available` or the value is absent.
- Append the formatter output to `$GITHUB_STEP_SUMMARY` for GitHub's rendered run summary. Write the same Markdown using the multiline delimiter form to `$GITHUB_OUTPUT` under a named output such as `markdown`, allowing later steps to consume it.
- Keep the reporting step after validation and before publication. A formatting failure should fail the workflow before publication rather than produce a misleading successful report.

## Risks / Trade-offs

- [Risk] Markdown tables may become wide with many rows. -> Mitigation: keep the report to the requested columns and use right alignment only for numeric columns.
- [Risk] A future artifact field may contain Markdown-sensitive text. -> Mitigation: the report uses validated ISINs, currencies, pairs, and numeric values only; no free-form provider fields are rendered.
- [Risk] `$GITHUB_OUTPUT` has size limits for very large reports. -> Mitigation: the current configured dataset is small and the output is additionally rendered directly through `$GITHUB_STEP_SUMMARY`; document the named output as a convenience rather than a persistence channel.
- [Risk] A malformed artifact could cause the report to disagree with publication. -> Mitigation: reuse the existing artifact validation and fail the report step if parsing or formatting fails.

## Migration Plan

Add the formatter, focused tests, and one workflow step. Existing consumers of `data/live_prices.json` require no migration. Rollback is a code-only revert that removes the report step and formatter while leaving the artifact publication flow intact.

## Open Questions

None.
