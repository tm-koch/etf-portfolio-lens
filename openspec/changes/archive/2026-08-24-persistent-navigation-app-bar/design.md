## Context

The static frontend currently places `.page-frame` around the application shell, with destination panels and the primary navigation styled as cards. The navigation is in document flow after the Home panel on desktop and becomes an edge-to-edge fixed bottom bar at widths up to 760px. Smartphone content still inherits body side padding and card framing, reducing the usable reading width.

The redesign keeps the existing destination registry, panel switching, local persistence, Lucide icons, and mobile safe-area behavior. It changes the layout ownership so navigation is application chrome and destination content is a separate constrained reading column.

## Goals / Non-Goals

**Goals:**

- Place one primary navigation element before destination content in the DOM.
- Present that navigation as a persistent desktop app bar and preserve fixed bottom placement on smartphones.
- Remove the outer page-frame wrapper and its responsibility for separating navigation from content.
- Keep desktop content centered and constrained without wrapping the navigation in that content frame.
- Allow smartphone destination content to use the full viewport width while preserving usable internal padding and fixed-nav clearance.
- Preserve all existing destination behavior, accessibility semantics, visual active states, and persistence.

**Non-Goals:**

- Add URL routing, browser history navigation, or a new application shell framework.
- Change destination names, ordering, panel content, portfolio calculations, chart behavior, or data loading.
- Redesign the destination panels beyond removing outer mobile framing and maintaining readable internal spacing.
- Add dependencies or alter backend and published data formats.

## Decisions

### Use one navigation element for both responsive placements

Keep the existing `nav.primary-navigation` and dynamically rendered destination buttons as the only navigation implementation. Desktop CSS will position it as a sticky, full-width app bar; the mobile media query will continue to position the same element fixed at the viewport bottom. This keeps keyboard behavior, `aria-current`, persistence, and future destination registration consistent.

An alternative is to render separate desktop and mobile navigation elements. That would duplicate interaction semantics and create two sources of truth for active state, so it is rejected.

### Move navigation outside the constrained content column

Place the navigation before a main content container that holds the destination panels. The navigation can span the viewport and have its own boundary, while the content column uses the existing maximum width and desktop spacing. This removes the need for `.page-frame` to enclose both concerns and makes the desktop separation explicit.

An alternative is to keep the current DOM order and visually move the navigation with CSS. That leaves the document reading order inconsistent with the visual order and does not establish a clear app-bar ownership boundary.

### Remove outer mobile framing, retain panel internals

At widths up to 760px, remove body side gutters and suppress the active panel's outer border radius, border, and shadow where they represent the page frame. Preserve panel padding and inner cards so tables, charts, and grouped data remain visually legible. Keep bottom body padding tied to the stable navigation footprint and safe area.

An alternative is to remove all card styling from every nested component. That would flatten useful grouping and is outside the request.

### Use sticky desktop positioning rather than fixed positioning

The desktop app bar will remain in normal layout flow while sticking to the top during scrolling. This preserves natural document height, avoids overlaying the initial content, and still keeps navigation available on long pages. The mobile breakpoint retains fixed positioning because the bottom bar is intended to remain visible while scrolling.

An alternative is a fixed desktop bar with compensating top padding. That adds overlay geometry and risks hiding the beginning of a panel without providing a meaningful benefit.

## Risks / Trade-offs

- [Changing desktop navigation order may conflict with the archived bottom-navigation contract] -> Update the active capability specification and validate visual order, keyboard order, and `aria-current` behavior.
- [Removing mobile outer framing may make wide tables or charts feel visually unbounded] -> Keep a consistent internal content gutter and preserve inner grouping surfaces.
- [A sticky app bar can overlap content at the top of a scroll container] -> Keep it in the document flow, use a stable height, and verify anchor-free tab switching at desktop widths.
- [Removing body padding changes the dialog and background composition] -> Retain dialog-specific width and padding rules and verify all four destinations at desktop and smartphone widths.
- [Safe-area clearance can regress while moving the navigation in the DOM] -> Preserve the existing mobile height variables and verify the final reachable content below long panels.

## Migration Plan

1. Move the existing navigation before the destination panels and replace the outer frame with a content-column container.
2. Update desktop styles for the full-width sticky app bar and constrained content column.
3. Update smartphone styles for full-bleed content, internal gutters, and unchanged fixed bottom-nav clearance.
4. Update the bottom-navigation capability delta and add focused implementation tasks.
5. Validate navigation order, keyboard interaction, tab switching, desktop sticky behavior, smartphone full-bleed layout, chart sizing, and safe-area clearance.

Rollback is a markup and stylesheet reversal; no persisted data, URLs, or backend artifacts require migration.

## Open Questions

None. The desktop navigation is intentionally above the active content and sticky during scrolling; smartphone navigation remains fixed at the bottom.
