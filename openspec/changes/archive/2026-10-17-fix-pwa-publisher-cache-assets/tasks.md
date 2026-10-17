# Tasks

## 1. Publisher Staging Contract

- [x] 1.1 Add `redundancy.js` to the Pages publisher's required web files and update the app-import contract to recognize optional query-string suffixes; verify the versioned `redundancy.js` import is required in the staged list.
- [x] 1.2 Extend the publisher contract to compare cache-sensitive paths from `pwa-cache-generation.ps1` with the publisher staging allowlist; verify every hashed asset is staged.

## 2. Integration Verification

- [x] 2.1 Run the focused web contract and PWA cache-generation tests; verify cache generation succeeds with the complete staged asset set.
