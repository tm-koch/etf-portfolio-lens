## Context

At widths covered by the mobile media query, the Selected positions table is converted into a grid of `.position-row` cards. The shared card styles add a border, but the mobile rule explicitly sets `border-bottom: 0`, which removes the row's lower edge even though the row is the visible card boundary. The parent `.subcard` is a separate container and cannot reliably replace each row's missing bottom edge.

## Goals / Non-Goals

**Goals:**

- Make each mobile selected-position row a visibly complete card with all four border edges rendered.
- Preserve the current identity-above-controls grid, sizing, spacing, and control behavior.
- Keep desktop and tablet table styling unchanged.
- Add a focused regression check for the mobile border contract and, where available, rendered mobile geometry.

**Non-Goals:**

- Redesigning the Selected positions component or changing its markup.
- Changing card colors, radius, navigation, or the desktop table border treatment.
- Fixing unrelated missing resources reported by the local browser.

## Decisions

- Keep `.position-row` as the mobile card boundary and remove the mobile-only bottom-border suppression, because the row already owns the complete border and radius declarations.
- Do not add an extra nested wrapper or pseudo-element: that would duplicate the visual boundary and create another sizing/overflow surface.
- Preserve the existing `border-bottom: 0` behavior on mobile row cells, since cell-level table borders are not the card enclosure and would create internal lines.
- Validate the fix with a source contract assertion that the mobile row retains a complete border and with a mobile viewport browser check when the local server is available. The browser check should inspect the row bounding box and computed border widths rather than relying only on a screenshot.

## Risks / Trade-offs

- [Risk] A future table-specific rule may reintroduce a missing edge. -> Mitigation: keep the mobile border requirement explicit in the web contract test.
- [Risk] The mobile card may become one pixel taller. -> Mitigation: accept the intended border enclosure and verify that the controls remain within the card without overflow.
- [Risk] Browser validation may be unavailable in offline/local development. -> Mitigation: retain deterministic CSS contract coverage and record browser validation as an environment-dependent check.

## Migration Plan

1. Update the mobile `.position-row` rule to retain its complete border.
2. Add or update focused web contract coverage.
3. Run the web contract tests and, with the local server running, inspect a phone-sized viewport.
4. Roll back by restoring the mobile border suppression only if a confirmed layout regression requires it.

## Open Questions

None.
