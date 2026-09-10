## Context

The Pages publisher builds a detached worktree, stages the generated static site, and commits it before pushing `HEAD:gh-pages`. In GitHub-hosted runners, the checkout does not guarantee a usable Git author identity for that detached worktree. The current commit therefore fails with `Author identity unknown` even though the workflow has permission to write repository contents.

The failure occurs inside the publisher rather than in the workflow's source checkout. The fix must work for scheduled and manual invocations, remain valid for local `-NoPush` runs, and avoid changing global Git configuration on shared developer machines or the runner.

## Goals / Non-Goals

**Goals:**

- Configure a deterministic automation identity in the Actions checkout before invoking the publisher.
- Allow the existing Pages publication to commit and push successfully on GitHub Actions.
- Keep identity configuration in the workflow and test the ordering contract.
- Preserve existing branch routing, artifact validation, cache generation, cleanup, and push behavior.

**Non-Goals:**

- Changing the source checkout's Git identity or committing generated data to `main`.
- Changing GitHub Actions permissions, authentication, or branch protection.
- Introducing user-configurable commit identity parameters.
- Changing the generated site's content or commit message.

## Decisions

### Configure identity in the workflow

After checkout and before invoking the publisher, run `git config user.name 'github-actions[bot]'` and `git config user.email '41898282+github-actions[bot]@users.noreply.github.com'` in the Actions workspace.

This keeps the manual publisher behavior unchanged while ensuring the workflow-owned invocation has an identity. The commands use repository-local configuration by default and do not mutate developer Git configuration.

### Keep the existing bot identity convention

Use the standard GitHub Actions bot name and noreply address already used by repository automation history. This produces recognizable publication commits without exposing a personal identity or introducing a secret.

### Test ordering and locality through the contract

Extend the publishing contract test to assert both identity commands and their placement before the publish step. The test should also ensure the implementation continues to use the temporary publisher and does not configure identity in the reusable script.

## Risks / Trade-offs

- [Identity commands can fail] An unavailable Git executable could make configuration fail. -> Let the workflow fail before publication starts.
- [Bot identity is fixed] All automated Pages commits use one shared identity. -> This is intentional for generated deployment output and matches GitHub's standard Actions bot convention.
- [Local publication behavior remains unchanged] Manual `-NoPush` runs continue to use the caller's Git identity. -> This preserves the script's independent manual workflow.

## Migration Plan

1. Add the two repository-local Git configuration commands to the workflow after checkout and before publication.
2. Add contract assertions for both commands and their ordering.
3. Run the focused publishing/web contract tests and the complete test suite.
4. Trigger the workflow manually and verify the generated `gh-pages` commit is authored by `github-actions[bot]`.
5. Roll back by removing the two local configuration commands if publication identity policy changes; no data migration is required.

## Open Questions

- None. The repository's existing GitHub Actions bot identity is the appropriate automation identity.
