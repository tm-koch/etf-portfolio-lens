## Why

On Firefox for Android, the fixed mobile navigation can jump during upward scrolling and show extra white space below its icons. This is not reproduced by Firefox desktop responsive emulation because it does not reproduce the real browser toolbar and visual-viewport changes, so the navigation needs stable internal geometry for real-device scrolling.

## What Changes

- Give the mobile navigation an explicit, stable total height.
- Give the icon-and-label row an explicit stable height so browser-toolbar changes do not alter internal whitespace.
- Keep the mobile navigation as a simple opaque fixed element without special compositor or containment hints that can introduce scroll-layer jitter.
- Preserve safe-area expansion on mobile platforms that expose a stable WebKit safe-area model.
- Keep page bottom clearance aligned with the stable navigation footprint.
- Preserve fixed bottom positioning, destination switching, active styling, and desktop navigation behavior.
- Verify behavior on Firefox Android with the browser toolbar expanded and collapsed during scrolling.

## Capabilities

### New Capabilities

### Modified Capabilities

- `bottom-navigation`: Require stable mobile navigation geometry and content clearance while the browser visual viewport changes during real-device scrolling.

## Impact

- `web/styles.css`: Add stable mobile navigation geometry and remove special mobile compositor and containment hints.
- Browser verification: test Firefox Android scrolling with dynamic browser chrome and compare desktop responsive emulation behavior.
- No changes to navigation state, URLs, persistence, destination content, APIs, or dependencies.
