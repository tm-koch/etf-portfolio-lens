## 1. Comparison chart layout

- [x] 1.1 Refactor the shared comparison chart configuration so sector, region, and currency use one consistent donut sizing model.
- [x] 1.2 Increase the donut ring thickness so the comparison charts read wider without changing the underlying data.
- [x] 1.3 Move legend rendering into a dedicated layout area so legend height no longer shrinks the donut drawing space.

## 2. Responsive presentation

- [x] 2.1 Update the comparison tab styles to reserve enough space for the legend and keep it fully visible at desktop widths.
- [x] 2.2 Add responsive behavior for narrower viewports so the legend remains readable without clipping.

## 3. Verification

- [x] 3.1 Verify sector, region, and currency comparison charts render with the same visible donut size.
- [x] 3.2 Verify the comparison legends remain fully visible in the browser at desktop and mobile widths.
- [x] 3.3 Confirm the change does not affect the comparison data order, labels, or tooltip content.
