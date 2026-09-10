## Context

The scheduled workflow in `.github/workflows/live-market-data.yml` checks out `main`, generates and validates `data/live_prices.json`, commits that generated file to `main`, and then invokes `scripts/publish-gh-pages.ps1`. The publisher creates a detached worktree from the source revision, assembles the static site, copies the validated live artifact, generates build provenance and the PWA cache version, and pushes the resulting tree to `origin/gh-pages`.

The generated artifact is needed by the published site, but it is deployment output rather than source input. The existing publisher already has the correct Pages branch routing and artifact validation boundary. The change therefore needs to alter workflow ownership of the generated file without creating a second publishing path or weakening failure handling.

## Goals / Non-Goals

**Goals:**

- Generate and validate live data in the Actions workspace.
- Publish the validated artifact only through the existing `gh-pages` publication.
- Ensure a successful refresh does not create a generated-data commit or push to `main`.
- Preserve the existing scheduled/manual triggers, secrets, validation, build provenance, PWA cache generation, and atomic Pages replacement behavior.
- Add focused contract coverage for the branch-only publication invariant.

**Non-Goals:**

- Removing the historical `data/live_prices.json` file from the source repository.
- Changing the public URL or the `data/live_prices.json` path on GitHub Pages.
- Replacing the detached-worktree publisher or changing its force-with-lease strategy.
- Changing quote providers, artifact schema, update cadence, or frontend fallback behavior.

## Decisions

### Reuse the existing publisher as the only deployment boundary

Remove the workflow's generated-artifact commit step and leave the validated file in the runner checkout. Keep `publish-gh-pages.ps1` responsible for copying that workspace artifact into its temporary publication worktree and pushing `HEAD:gh-pages`.

This is preferred over adding a separate checkout or direct file copy to `gh-pages` because the existing publisher already assembles all web assets, validates the artifact, generates provenance, updates the service-worker cache generation, and cleans up its worktree. A second path would duplicate deployment logic and could produce inconsistent Pages trees.

### Keep source revision provenance tied to the checked-out source

The publisher will continue to use `HEAD` for source commit and timestamp metadata. The live artifact's own `generated_at` value remains the authoritative live-data timestamp in the published artifact and build metadata. The source revision does not need to change for every data refresh.

This keeps build provenance meaningful: it identifies the application/catalog source used for the publication while separately recording the newly fetched market-data timestamp.

### Preserve validation before publication

The workflow will retain artifact validation before invoking the publisher, and the publisher will retain its own presence, schema, and prohibited-field checks. If generation or validation fails, no Pages push occurs. The temporary generated file is discarded with the runner after the job, so no failed or partial artifact reaches either branch.

### Test the observable branch contract

Contract tests will inspect the workflow and publisher scripts to verify that the workflow no longer performs a generated-data commit/push to `main`, while the publisher still targets `gh-pages` and includes `live_prices.json`. Existing live-data and PWA validation tests remain unchanged unless their assertions depend on the removed commit behavior.

## Risks / Trade-offs

- [Existing source artifact remains historical] `main` may continue to contain the last committed `data/live_prices.json` value. -> Treat removal of that tracked fallback as a separate change so local runtime behavior and this deployment refactor remain isolated.
- [Runner workspace is the artifact handoff] Publication depends on the generated file remaining at the expected path between workflow steps. -> Keep the existing default output path and validate immediately before publication; add a contract assertion for the workflow-to-publisher handoff.
- [Build provenance source commit does not include live-data changes] A Pages build may show the same source commit across multiple data refreshes. -> Continue recording `data.live.generatedAt` and status in `build-info.json`; do not overload source commit metadata with runtime data identity.
- [Pages branch replacement remains force-based] A concurrent or unrelated update to `gh-pages` could still affect publication. -> Preserve concurrency serialization and `--force-with-lease`; changing branch protection or deployment ownership is outside this change.

## Migration Plan

1. Deploy the workflow change while leaving the existing tracked artifact in `main`.
2. Run the workflow manually and verify that generation and validation succeed, `main` receives no new commit, and `origin/gh-pages` receives the updated artifact and build metadata.
3. Run the existing HTTPS/PWA deployment validation against the Pages URL.
4. Roll back by restoring the removed workflow commit step if branch-only publication fails; the previous Pages publication remains available when the job fails before push.

## Open Questions

- None for the workflow-only implementation. Whether to remove the historical source-branch artifact belongs to a later, separately scoped change.
