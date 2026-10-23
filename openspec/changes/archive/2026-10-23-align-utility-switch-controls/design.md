# Design

## Context

The language and color-mode triggers are in the same utility row and share base button styles. At 390px, the current language button measures about 45.2 by 40.4 CSS pixels, while the icon-only color-mode button measures about 42.6 by 36.6. At wide viewports both are about 40px tall, but their widths follow different localized labels. See `proposal.md` for motivation and the delta specs for the required behavior.

## Goals / Non-Goals

**Goals:**
- Give the two collapsed triggers identical outer dimensions and top/bottom alignment at widths of 760px or less.
- Keep the language code and color icon centered and fully visible in the shared compact box.
- Preserve full localized labels on wider viewports and existing focus, tooltip, menu, and selection behavior.

**Non-Goals:**
- Reposition the utility row or change the install control, menu dimensions, menu placement, or bottom navigation.
- Change language or color-mode behavior, persistence, or accessible names.

## Decisions

- Use CSS-only overrides for the existing language and color-mode buttons inside the current 760px breakpoint. The controls already share button classes, so no markup or JavaScript changes are needed.
- Set both compact triggers to one shared inline and block size, based on the current color-mode icon box (approximately 43 by 37 CSS pixels; use stable integer dimensions near that footprint). Use border-box sizing, remove content-driven padding as needed, and center the icon or two-character language code.
- Keep the wide-viewport buttons content-sized. Their labels differ in localized length, so equal widths there would either waste space or risk truncating the existing full labels; their current common height and utility-row alignment remain unchanged.
- Verify geometry at 390px and 760px, and confirm the wide presentation at 761px and 1440px. Also verify the existing accessible names and menu behavior remain intact.

## Risks / Trade-offs

- **Fixed compact dimensions could clip a glyph or reduce the tap target** → Check all three language codes and the color icon at the compact breakpoints; keep the target at least as large as the existing color-mode control and preserve its focus outline.
- **Breakpoint-specific overrides could drift from shared styles** → Keep the dimensions together in the existing mobile media block and add a focused regression check.

## Migration Plan

No data or preference migration is needed. The CSS change is reversible by removing the compact trigger-size overrides.
