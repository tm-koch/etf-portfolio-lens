## 1. Visual and Layout Refresh

- [x] 1.1 Replace the dark visual theme with a lightweight white UI palette.
- [x] 1.2 Rework the comparison and aggregated sections so sectors, regions, and currencies stack vertically.
- [x] 1.3 Tune spacing and card treatment so the page stays readable on desktop and mobile.

## 2. Chart Stability

- [x] 2.1 Add bounded chart wrappers with explicit height for each doughnut chart.
- [x] 2.2 Verify Chart.js renders the sector, region, and currency doughnuts inside the new containers.
- [x] 2.3 Confirm the chart layout does not introduce horizontal scrolling on narrow screens.

## 3. Local Server Access

- [x] 3.1 Make the development server binding configurable so it can be reached from a browser beyond localhost.
- [x] 3.2 Document the default local URL and the network-accessible binding option.

## 4. GitHub Pages Documentation

- [x] 4.1 Add a deployment note that lists the frontend files and static data files required for GitHub Pages.
- [x] 4.2 Document the expected folder structure for the published site, including the data directory layout.
- [x] 4.3 Verify the documentation matches the file paths used by the frontend at runtime.
