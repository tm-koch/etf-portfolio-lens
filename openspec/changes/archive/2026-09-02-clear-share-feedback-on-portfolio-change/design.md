## Context

A valid private portfolio share link sets `state.shareFeedback` to a message explaining that the loaded shares are relative allocation units. The feedback is rendered in the Portfolio sharing area and currently remains visible after local edits because portfolio mutation handlers update and persist `state.portfolio` without invalidating the feedback.

The application intentionally gives a share URL precedence over local storage during startup. A user edit must therefore dismiss the current-session message without changing the URL fragment or altering refresh behavior.

## Goals / Non-Goals

**Goals:**

- Clear the current share-loading feedback after a confirmed portfolio mutation.
- Cover PDF replacement, ETF addition, share-count changes, and ETF removal consistently.
- Preserve the share URL fragment and existing startup precedence so refresh reloads the original shared portfolio.
- Add focused static contract coverage for the invalidation behavior.

**Non-Goals:**

- Removing or rewriting the share URL after edits.
- Changing portfolio persistence, private weighting, share encoding, or startup loading.
- Clearing feedback for actions that do not mutate the portfolio, such as opening or cancelling the PDF review dialog.

## Decisions

- **Centralize feedback invalidation in a small helper.** A helper will clear the relevant share feedback state and refresh its DOM rendering. This keeps all mutation handlers consistent and avoids duplicating state-reset details.
- **Invoke invalidation only after real mutations.** The helper will be called by the successful PDF confirmation, ETF addition, share update, and ETF removal paths. Duplicate ETF additions and invalid imports will not clear feedback because they do not change the portfolio.
- **Keep the URL unchanged.** The hash remains the source of truth on a later reload, matching the agreed behavior that the original shared portfolio and loading message return after refresh.
- **Retain generated-share feedback semantics unless overwritten by a mutation.** The same feedback state is used for share-link results, so a later portfolio change clears stale sharing status rather than displaying it against a different portfolio.

## Risks / Trade-offs

- [Risk] A share-link message disappears immediately after an edit, reducing provenance context in the current session. -> Mitigation: the original share URL remains available and refresh behavior is unchanged.
- [Risk] A mutation handler could omit invalidation in the future. -> Mitigation: contract tests assert the helper is present at each portfolio mutation boundary.
- [Risk] Clearing all share feedback also hides a recently generated share-link result after a subsequent edit. -> Mitigation: this is intentional because the generated result describes the previous portfolio state.

## Migration Plan

No data migration or deployment migration is required. Deploy the frontend change and contract tests together. Rollback consists of reverting the frontend commit; stored portfolios and URL payloads remain backward compatible.

## Open Questions

None. The URL-preserving refresh behavior is an explicit requirement.
