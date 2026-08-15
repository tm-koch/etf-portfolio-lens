## 1. Navigation Structure

- [x] 1.1 Replace the existing tab-bar markup with a labeled primary navigation containing Portfolio, Compare, and Explore destination entries.
- [x] 1.2 Add pinned Lucide browser integration and configure suitable icons for the three destination entries.
- [x] 1.3 Keep the visible Explore destination mapped to the existing `aggregated` panel and state key.

## 2. State And Interaction

- [x] 2.1 Define a single destination registry containing internal keys, labels, and icon names for rendering and future extension.
- [x] 2.2 Update destination event handling and active-state rendering to use the registry while preserving existing panel switching behavior.
- [x] 2.3 Persist the active destination in a versioned local-storage key, validate stored values, and default invalid or missing values to Portfolio.
- [x] 2.4 Set `aria-current="page"` and preserve keyboard activation semantics for the active destination.

## 3. Responsive Styling

- [x] 3.1 Style the navigation in normal document flow below the summary cards for desktop widths.
- [x] 3.2 Add a solid, fixed bottom navigation layout for viewports at or below 760px with active-state styling and icon-over-label arrangement.
- [x] 3.3 Add safe-area bottom spacing and page content clearance so mobile content is not obscured by the fixed navigation.
- [x] 3.4 Remove or replace the old tab-bar narrow-screen rules and verify the layout does not overlap charts, tables, or controls.

## 4. Verification

- [x] 4.1 Verify Portfolio, Compare, and Explore switch panels correctly with and without portfolio positions.
- [x] 4.2 Verify the selected destination survives reload without changing the browser URL or history.
- [x] 4.3 Verify desktop, tablet, and mobile layouts, including fixed positioning, solid background, safe-area spacing, and content reachability.
- [x] 4.4 Verify icon failure does not remove destination labels or prevent navigation, and verify keyboard and assistive-technology states.
- [x] 4.5 Verify adding a registry destination with a matching panel uses the same navigation rendering and interaction path.
