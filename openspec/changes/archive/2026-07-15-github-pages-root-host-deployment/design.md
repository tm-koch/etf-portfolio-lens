## Context

The repository already produces a static frontend and published ETF snapshot JSON files. The remaining problem is not data generation; it is choosing a deployment shape that matches the current absolute data URLs in the catalog and the branch-based GitHub Pages workflow.

The `gh-pages` branch already exists as the publish branch, so the deployment design should focus on a repeatable static tree and a root-hosted site layout rather than branch bootstrapping.

## Goals / Non-Goals

**Goals:**
- Publish the static site from the `gh-pages` branch.
- Keep the current root-absolute data URLs valid in the deployed site.
- Include the frontend and the relevant published ETF data files in one publish tree.
- Make the publish process repeatable and easy to execute from PowerShell.

**Non-Goals:**
- No changes to portfolio data generation or normalization.
- No changes to chart logic or frontend interaction behavior.
- No requirement to support repo-subpath Pages hosting for this change.

## Decisions

1. Publish the site as a root-hosted GitHub Pages tree.
   - Rationale: the current catalog data points at `/data/raw/...`, which is compatible with a root-hosted site but not with a repo-subpath deployment.
   - Alternatives considered: rewrite all snapshot URLs for repo-subpath hosting; rejected because it adds unnecessary path translation and complicates the publish flow.

2. Treat `gh-pages` as the single publish branch.
   - Rationale: the branch already exists and maps naturally to a static Pages deployment.
   - Alternatives considered: create a separate build branch or use a docs folder; rejected because it adds branching complexity without improving the static publishing contract.

3. Publish the frontend and data assets together.
   - Rationale: the UI depends on the generated catalog and snapshot files being present in the deployed tree at the same time.
   - Alternatives considered: publish only the frontend and fetch data elsewhere; rejected because the site is designed to be self-contained and static.

## Risks / Trade-offs

- [Root-hosted Pages is less flexible than repo-subpath hosting] → Mitigation: document the expected Pages target clearly and keep the publish tree stable.
- [Publishing data files increases branch size] → Mitigation: publish only the relevant static snapshot artifacts required by the frontend.
- [The workflow still depends on a valid Git remote and Pages configuration] → Mitigation: include those prerequisites in the publish script or documentation.

## Migration Plan

No data migration is required.

1. Confirm the repository publishes from the `gh-pages` branch.
2. Ensure the publish tree contains the frontend and `data/raw/<date>/snapshots` files.
3. Verify the deployed site loads the catalog and snapshot JSON from the Pages root.
4. Roll back by republishing the previous `gh-pages` tree if needed.
