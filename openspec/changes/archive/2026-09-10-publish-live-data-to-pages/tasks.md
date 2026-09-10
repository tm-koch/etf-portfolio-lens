## 1. Update Workflow Publication Ownership

- [x] 1.1 Remove the generated `data/live_prices.json` commit and `git push` step from `.github/workflows/live-market-data.yml` while preserving generation, validation, triggers, secrets, and the existing Pages publish step.
- [x] 1.2 Verify the workflow passes the validated workspace artifact to the existing publisher and has no path or command that updates `main` with generated live data.

## 2. Strengthen Contract Coverage

- [x] 2.1 Update web/workflow contract tests to assert that live-data refreshes do not contain a generated-artifact commit or push to `main` and that publication remains targeted at `gh-pages`.
- [x] 2.2 Preserve and extend assertions for artifact validation, `data/live_prices.json` publication, and the existing scheduled/manual workflow triggers.

## 3. Validate Deployment Behavior

- [x] 3.1 Run the focused workflow, publishing, and PWA contract tests and repair any regression in the branch-only publication contract.
- [x] 3.2 Run the complete test suite and confirm the working tree contains no unintended generated-data changes after local validation.
- [x] 3.3 Review the final workflow diff to confirm a successful refresh leaves `main` unchanged while the publisher still force-with-lease pushes the assembled site to `origin/gh-pages`.
