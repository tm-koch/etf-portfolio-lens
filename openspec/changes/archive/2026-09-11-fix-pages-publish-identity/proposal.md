## Why

The GitHub Pages publication workflow currently fails when `publish-gh-pages.ps1` commits the assembled site because the temporary worktree has no Git author identity. The workflow must configure a deterministic automation identity before invoking the publisher, while keeping the publisher itself usable for manual invocations.

## What Changes

- Configure the GitHub Actions bot name and noreply email in the Actions checkout before invoking the Pages publisher.
- Preserve the existing `gh-pages` branch publication, force-with-lease push, and source repository identity isolation.
- Add regression coverage that verifies the workflow configures identity before invoking the publisher.
- Keep the identity configuration scoped to the Actions checkout rather than changing global developer Git configuration or manual publisher behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `pwa-publishing`: A Pages publication SHALL configure a valid automation Git identity before creating its generated-site commit.

## Impact

- Affected workflow: `.github/workflows/live-market-data.yml`.
- Affected publishing contract tests, likely in `tests/test_web_contract.py`.
- No changes to the live-data artifact, workflow triggers, repository source history, public Pages paths, or developer Git configuration.
