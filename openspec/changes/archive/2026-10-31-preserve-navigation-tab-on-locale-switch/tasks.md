# Tasks

## 1. Preserve Active Navigation State

- [x] 1.1 Add regression coverage for selecting a destination, switching language, and then selecting another destination; verify the test exposes the stale-button behavior with `python -m unittest discover -s tests -p test_web_runtime.py`.
- [x] 1.2 Update `setTab()` to apply active classes and `aria-current` to the current navigation buttons, then verify the regression and runtime test file pass with `python -m unittest discover -s tests -p test_web_runtime.py`.
