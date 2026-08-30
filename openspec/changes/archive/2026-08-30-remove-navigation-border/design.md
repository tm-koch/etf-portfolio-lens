## Context

The primary navigation uses the shared `.card` class, which supplies a `1px solid var(--border)` outline. The mobile override also declares a top border with the same token. Because the navigation has its own theme surface, this inherited border appears as a light-grey edge that is visually separate from the bar. Existing mobile shadow and dark-mode gradient styles already provide a restrained boundary.

## Goals / Non-Goals

**Goals:**

- Remove the visible navigation border at desktop and mobile widths.
- Keep the navigation background, positioning, spacing, safe-area footprint, shadow, and dark-mode gradient unchanged.
- Update the contract test and bottom-navigation delta spec to make the borderless boundary explicit.

**Non-Goals:**

- Do not change navigation destinations, active-state styling, or keyboard/accessibility behavior.
- Do not change the shared `.card` border used by other surfaces.
- Do not replace or redesign the existing shadow or dark-mode gradient.

## Decisions

### Explicitly override the shared card border

Set the primary navigation border to `0` in its base rule and remove the mobile `border-top` declaration. An explicit navigation rule is preferable to changing `.card`, because other cards rely on the shared border and the navigation intentionally has a distinct visual treatment.

**Alternative considered:** Set the border color equal to the navigation background. This retains unnecessary layout geometry and can still produce an edge when the background is translucent, so removing the border is more direct.

### Preserve existing separation treatments

Leave the mobile upward shadow and dark-only 9px gradient unchanged. Together with the solid mobile navigation surface, they provide visual separation without introducing a second color at the bar edge.

**Alternative considered:** Remove all edge treatment. This would reduce legibility where content scrolls behind the fixed mobile bar and is outside the requested scope.

### Validate through focused web contracts

Update the existing web contract assertions to verify that the navigation explicitly has no border while retaining the current background, shadow, gradient, and responsive rules.

## Risks / Trade-offs

- [Risk] The borderless desktop navigation may have less separation from a similarly colored page surface. -> Mitigation: retain the existing desktop shadow and theme background.
- [Risk] Removing the mobile top border could reduce contrast over scrolled content. -> Mitigation: retain the solid mobile surface, restrained upward shadow, and dark-mode gradient.
- [Risk] A shared `.card` rule could reintroduce the border during future refactoring. -> Mitigation: keep the navigation-specific `border: 0` explicit and cover it in the contract test.

## Migration Plan

No data or deployment migration is required. Apply the CSS and test/spec updates together; rollback consists of reverting the navigation-specific border overrides.

## Open Questions

None.