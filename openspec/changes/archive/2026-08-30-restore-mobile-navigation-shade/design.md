## Context

The primary navigation uses shared theme tokens for desktop and mobile surfaces. Before commit `73887b6`, the mobile fixed navigation used a solid `#ffffff` background. The later shared-token override makes Bright mode use translucent `var(--card)` and Dark mode use translucent `rgba(23, 30, 40, 0.92)`, which changes the historical mobile appearance and weakens the intended solid separation from content.

The existing bottom-navigation contract requires a solid mobile background, restrained boundary/shadow treatment, and stable geometry. Bright mode visually transitions into the surrounding frame through the page background and shadow, while Dark mode currently lacks an explicit matching edge. This change adds a Dark-mode-only mobile edge gradient without changing the Bright surface or desktop navigation.

## Goals / Non-Goals

**Goals:**

- Restore the historical solid white mobile navigation surface in Bright mode.
- Give Dark mode a corresponding solid dark surface using the established dark navigation surface token.
- Keep desktop navigation, Bright mobile surface, mobile layout geometry, active-state styling, safe-area handling, and shadow unchanged.
- Add focused contract assertions for the theme-specific mobile surfaces.

**Non-Goals:**

- Redesigning navigation layout, typography, icons, or active-state colors.
- Changing the desktop navigation background or gradient.
- Changing color-mode persistence or automatic mode resolution.
- Adding dependencies or browser-specific runtime logic.

## Decisions

1. **Use mobile-only theme overrides.** The mobile rule will retain its fixed positioning and override only its background by effective theme. This keeps the desktop shared token and the existing responsive structure intact.

2. **Use `#ffffff` for Bright mobile navigation.** This exactly restores the surface present at the referenced historical commit and avoids translucency over page content.

3. **Use `var(--card-strong)` for Dark mobile navigation.** This is the established dark elevated surface and is the closest theme-equivalent to the historical bright solid surface. It avoids introducing a duplicate dark color literal while remaining consistent with the existing dark desktop navigation treatment before the gradient refactor.

4. **Tune the Dark-only mobile edge gradient.** Create a mobile-only `::after` edge positioned above the fixed navigation and enable it only under the Dark effective color mode. Give it a 9px height, start at the existing lighter dark-slate `var(--table-header-background)` at the navigation border, and fade to `transparent`, allowing the dark frame background to show naturally; Bright mode remains without an explicit pseudo-element.

5. **Update contract tests rather than adding browser automation.** The repository's web contract tests already assert stylesheet invariants. They can verify the theme-specific declarations without introducing a new test framework or viewport dependency.

## Risks / Trade-offs

- [Theme selector specificity] A later rule could accidentally override the mobile theme surface. -> Keep the overrides adjacent to the existing mobile navigation rule and assert both declarations in the contract test.
- [Gradient contract drift] Existing tests or specs may not distinguish the Dark-only edge from Bright behavior. -> Assert the Dark selector and gradient while asserting no Bright edge selector is introduced.
- [Perceived dark contrast] The gradient could appear too grey against the dark frame. -> Use the existing cool dark-slate table-header tone only at the border and fade to transparency, keeping the transition restrained while preserving the frame's own background.
- [Historical test coupling] Contract tests inspect CSS text and can be sensitive to formatting. -> Make the smallest stylesheet change and update only the affected assertions.

## Migration Plan

1. Add the mobile Bright and Dark background overrides and the Dark-only mobile edge gradient fading to transparency.
2. Update the focused web contract test.
3. Run the focused test and the full available test suite.
4. Roll back by removing the two theme-specific overrides if visual review identifies an issue; no data or persisted-state migration is required.

## Open Questions

None. The historical Bright value and the existing Dark elevated surface provide the required theme pair.
