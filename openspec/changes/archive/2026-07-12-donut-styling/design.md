## Context

The comparison view renders multi-ring doughnut charts for sector, region, and currency exposure. The current implementation uses a short fixed palette and a dark slice border, which causes repeated colors once the category count grows and makes the slices feel visually heavy against the light UI.

The chart is data-driven and shared across multiple metric types, so the styling should be consistent across all donut rings without changing the underlying values, labels, or ring semantics.

## Goals / Non-Goals

**Goals:**
- Give each visible donut slice a more distinct color using a longer qualitative palette.
- Keep the palette visually harmonious by anchoring it around cool blue hues.
- Increase saturation slightly so adjacent categories remain easy to distinguish.
- Replace the dark slice separator with a white border for clearer segmentation.
- Preserve the existing chart data model and percentage formatting.

**Non-Goals:**
- Redesign the comparison layout or chart card structure.
- Change the exposure calculation pipeline or snapshot format.
- Add user-configurable theme controls or runtime palette editing.

## Decisions

Use a fixed categorical palette with more unique colors than the current eight-color set.
- Rationale: the chart is qualitative, not sequential, so category colors should maximize distinction rather than encode magnitude.
- Alternatives considered: generating colors procedurally at runtime or reusing the existing short palette. Procedural generation risks inconsistent results between rings, while the short palette repeats too early.

Anchor the palette in a cool blue family with neighboring cyan, teal, green, indigo, and violet accents.
- Rationale: a cool-led palette stays cohesive across the three donut metrics and keeps the interface aligned with the product’s calm, analytical tone.
- Alternatives considered: a warm triad or a full rainbow. Warm-led colors would feel louder than necessary, and a rainbow palette can become noisy in dense donuts.

Use white slice borders instead of the current dark border.
- Rationale: white separators read cleanly on the light card surfaces and maintain slice boundaries even when adjacent colors are similarly saturated.
- Alternatives considered: no border or a darker neutral separator. No border makes small slices merge visually, and a dark separator competes with the saturated palette.

Keep label-to-color mapping stable across all comparison donuts.
- Rationale: users should be able to recognize the same category across sector, region, and currency views without relearning the color key.
- Alternatives considered: per-chart palettes. That increases visual variety but makes cross-chart comparison harder.

## Risks / Trade-offs

[Longer palette still repeats if a metric exceeds the palette length] → Choose a palette long enough for observed category counts and preserve the same ordering across charts so repetition is predictable.

[More saturated colors can feel busy on small screens] → Keep luminance balanced and rely on the white border to separate slices instead of pushing saturation too far.

[Cool-led colors may under-emphasize rare warm categories] → Reserve a small number of warm accents for separation rather than making them dominant.
