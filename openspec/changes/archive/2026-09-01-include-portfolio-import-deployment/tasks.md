## 1. Publish Asset Set

- [x] 1.1 Add `portfolio-import.js` to the `$webFiles` list in `scripts/publish-gh-pages.ps1`.
- [x] 1.2 Add a regression assertion that every JavaScript module imported by `web/app.js` is included in the publish asset list.

## 2. Verification And Deployment

- [x] 2.1 Run focused deployment and web contract tests plus the full existing test suite.
- [x] 2.2 Run the GitHub Pages publish script and verify the deployed `portfolio-import.js` request succeeds.
- [x] 2.3 Smoke-test deployed navigation, color-mode selection, and Portfolio PDF import controls.
