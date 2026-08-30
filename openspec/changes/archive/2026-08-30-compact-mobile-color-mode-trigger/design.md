## Context

The global color-mode control is positioned in the app-level utility area and its trigger currently renders the selected mode's icon and visible label at every viewport width. The expanded menu already renders all three choices with icons and labels. Compact mobile uses the existing `max-width: 760px` breakpoint, where the trigger label adds unnecessary width but the control still needs an accessible name and discoverable alternatives.

## Goals / Non-Goals

**Goals:**

- Make only the compact-mobile trigger icon-only at widths up to 760px.
- Keep the selected mode available through the trigger's accessible name and tooltip.
- Keep every expanded menu option labeled with its icon and text.
- Preserve immediate menu dismissal, persistence, mode behavior, positioning, and desktop/wider-tablet presentation.

**Non-Goals:**

- Do not change the color-mode state machine, storage key, or theme resolution.
- Do not add a transient post-selection display or leave the menu open after selection.
- Do not hide labels from the menu options or alter menu keyboard semantics.
- Do not change the existing compact-mobile breakpoint or utility placement.

## Decisions

### Hide only the trigger label with responsive CSS

Retain the trigger's selected-mode `<span>` in the DOM and hide that span only inside the existing `max-width: 760px` media query. This keeps the JavaScript rendering path and accessible `aria-label` unchanged while making the trigger visually icon-only on compact mobile.

**Alternative considered:** Render different trigger markup in JavaScript based on viewport width. This duplicates responsive concerns in JavaScript and would require resize synchronization without improving semantics.

### Keep full labels in the expanded menu

Continue rendering each menu option with its icon and visible label. The menu is the user's choice surface, so labels remain available when selecting an alternate mode and satisfy the existing menu radio semantics.

**Alternative considered:** Use icon-only menu options. Familiarity and color-mode icon ambiguity make this less accessible, especially for Automatic versus a specific theme.

### Preserve the trigger accessible name independently of visible text

Keep the dynamic `aria-label` such as `Color mode: Automatic` and the existing tooltip title. Hiding the visual span must not remove the current mode announcement for assistive technology or mouse users.

## Risks / Trade-offs

- [Risk] Users may not recognize the color-mode icon immediately on compact mobile. -> Mitigation: retain the descriptive tooltip, accessible name, and labeled menu options.
- [Risk] The hidden span could accidentally be hidden on desktop during future CSS changes. -> Mitigation: scope the rule to the existing `@media (max-width: 760px)` block and add contract assertions for the media-scoped selector.
- [Risk] A narrow mobile trigger could affect menu alignment. -> Mitigation: preserve the existing relative control and right-aligned menu, then verify at representative compact widths.

## Migration Plan

No data or deployment migration is required. Add the responsive visibility rule and contract coverage; rollback consists of removing the compact-mobile-only rule.

## Open Questions

None.