# Design

## Context

See [proposal.md](proposal.md) for motivation. The Pages publisher builds a detached worktree, clears its contents, copies a curated `$requiredWebFiles` list, and then calculates the cache generation. The cache helper maintains its own `$PwaCacheSensitivePaths` list. Those lists can drift: `redundancy.js` is cache-sensitive but currently not staged, and the existing app-import test does not match imports with a `?v=` suffix.

## Goals / Non-Goals

**Goals:**
- Ensure every cache-sensitive asset exists in the staged Pages tree before cache generation runs.
- Make the publisher contract test recognize local JavaScript imports with optional query strings and detect drift between cache-sensitive and staged asset lists.
- Keep existing asset paths and cache-generation inputs unchanged.

**Non-Goals:**
- Replace the publisher's curated staging model or redesign cache generation.
- Change service-worker caching policy, generated cache identities, or deployment workflow.
- Add a new dependency or introduce spec-level behavior beyond the existing PWA publication contracts.

## Decisions

- Keep `$requiredWebFiles` as the publisher's explicit staging allowlist and add `redundancy.js` to it. This preserves the current copy process and published path while ensuring the required input exists before hashing.
- Strengthen the existing web contract test to handle optional query strings on relative JavaScript imports. Also compare the cache-sensitive paths declared by `pwa-cache-generation.ps1` with the publisher's staging list. This tests the actual source of the CI failure and prevents future list drift; relying only on imported modules would miss non-module shell assets.
- Leave the cache helper's required asset list unchanged. The failure is caused by incomplete staging, not an incorrect set of cache inputs.

## Risks / Trade-offs

- The publisher and cache helper retain separate lists → A contract test compares their required paths so omissions fail before deployment.
- Regex-based source checks can be brittle → Limit parsing to the declared PowerShell array blocks and allow the import query suffix explicitly.
