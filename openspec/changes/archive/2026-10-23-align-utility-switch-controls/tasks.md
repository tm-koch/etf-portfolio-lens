# Tasks

## 1. Compact Utility Trigger Geometry

- [x] 1.1 Update the compact CSS rules so the collapsed language and color-mode triggers share stable width, height, and top/bottom alignment, with the abbreviation and icon centered; verify equal bounding boxes at 390px and 760px.
- [x] 1.2 Extend existing responsive-control regression coverage and verify it with `python -m unittest discover -s tests -p test_web_runtime.py`.

## 2. Wider Viewport and Accessibility Regression

- [x] 2.1 Verify full localized labels and current color-mode text remain visible above 760px, and confirm menus, focus indicators, accessible names, and mobile bottom-navigation separation are unchanged at 761px and 1440px; run `python -m unittest discover -s tests`.
