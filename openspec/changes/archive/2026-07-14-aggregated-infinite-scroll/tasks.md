## 1. Rendering setup

- [x] 1.1 Render only the top 20 aggregated holdings on initial load.
- [x] 1.2 Add a scroll sentinel or equivalent loading trigger near the end of the list.
- [x] 1.3 Keep ranked holdings order stable as new items append.

## 2. Progressive loading

- [x] 2.1 Append the next batch of holdings when the sentinel enters view.
- [x] 2.2 Stop loading once all holdings are rendered.
- [x] 2.3 Preserve the existing row content and summary panels while appending.

## 3. Validation

- [x] 3.1 Verify the top 20 holdings are shown by default.
- [x] 3.2 Confirm additional holdings appear as the user scrolls downward.
- [x] 3.3 Run a browser smoke check for the aggregated tab.
