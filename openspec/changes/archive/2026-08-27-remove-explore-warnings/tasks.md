## 1. Remove Explore Warning Surface

- [x] 1.1 Remove the Warnings subcard and `warning-list` element from the Explore `/aggregated` markup.
- [x] 1.2 Remove the Explore warning element lookup and update `renderWarnings()` so it refreshes only the About this build warning list.
- [x] 1.3 Fix the About this build dialog's hidden optional-details styling so it does not create a second separator, leaving one separator above the bottom warnings section.

## 2. Update Verification

- [x] 2.1 Update the web contract tests to assert the Explore warning surface is absent and the build-dialog warning surface remains present.
- [x] 2.2 Extend the web contract tests for the single-separator behavior.
- [x] 2.3 Run the focused web contract tests and browser smoke-check both Explore modes and About this build warnings.
