# Design

## Context

`renderNavigation()` replaces the navigation container's button elements during a locale switch. `setTab()` currently retains and updates button references captured during bootstrap, so after replacement those references no longer represent the rendered controls. The locale-switch flow already calls `setTab(state.activeTab)` after rebuilding navigation.

## Goals / Non-Goals

**Goals:**
- Apply active classes and `aria-current` to the currently rendered navigation buttons whenever the active destination is set.
- Preserve the selected destination through runtime locale changes and subsequent destination clicks.
- Cover the rerender-and-select sequence with a focused regression test.

**Non-Goals:**
- Change destination selection, persistence, locale switching, or panel activation behavior.
- Change navigation styling or translation resources.

## Decisions

- Make `setTab()` query `.tab-button` elements from `elements.navigationItems` when applying the active state. The navigation container is stable while its child buttons are replaced, so this avoids stale references without adding another synchronization step to every renderer.
- Keep `state.activeTab` as the source of truth. The existing locale-switch flow calls `setTab(state.activeTab)` after rendering, which will apply the persisted in-memory selection to the new buttons.
- Test that an active destination remains styled and exposed through `aria-current="page"` after a locale switch, and that selecting a different destination afterward updates the new button and active panel. Prefer the existing web test harness; no new dependency is needed.

An alternative is to refresh the cached `elements.tabButtons` inside `renderNavigation()`. Querying from `setTab()` is preferred because it ties state application to the live DOM and remains correct if another caller replaces the buttons.

## Risks / Trade-offs

- [Risk] A future navigation renderer could move buttons outside `elements.navigationItems` → Keep the query scoped to the stable navigation container and update the test if that ownership changes.
- [Trade-off] `setTab()` performs a small DOM query each time a destination is selected → The navigation contains only a few buttons, so this cost is negligible and avoids reference invalidation.
