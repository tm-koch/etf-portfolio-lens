# Tasks

## 1. Sticky Offset and Regression Contract

- [x] 1.1 Add a shared desktop navigation-height CSS variable, use it as the compact Explore header's sticky offset, reset the offset at the mobile breakpoint, and update the focused contract assertions; verify with `python -m unittest discover -s tests -p test_web_contract.py`.

## 2. Viewport Verification

- [x] 2.1 Verify in a browser at desktop and mobile widths that the header remains visible below desktop navigation or at the mobile viewport top, stays aligned during horizontal scrolling, and stops at the end of the table.