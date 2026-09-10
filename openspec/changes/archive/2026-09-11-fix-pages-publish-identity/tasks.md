## 1. Configure Workflow Identity

- [x] 1.1 Add local `user.name` and `user.email` Git configuration commands to `.github/workflows/live-market-data.yml` after checkout and before invoking the publisher.
- [x] 1.2 Use the standard `github-actions[bot]` name and noreply email without changing global Git configuration or workflow branch behavior.

## 2. Add Regression Coverage

- [x] 2.1 Extend the web/publishing contract tests to require both identity configuration commands in the workflow.
- [x] 2.2 Assert the identity configuration appears before the publisher invocation and that the existing `gh-pages` push behavior remains intact.

## 3. Validate the Workflow Fix

- [x] 3.1 Run the focused publishing and web contract tests and repair any regression in the commit-identity contract.
- [x] 3.2 Run the complete test suite and inspect diagnostics for the changed PowerShell and test files.
- [x] 3.3 Review the final diff to confirm the fix is limited to workflow publication identity and regression coverage.
