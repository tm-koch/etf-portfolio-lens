# Tasks

## 1. Shares-mode validation

- [x] 1.1 Validate manual Shares edits as finite, non-negative integers before persistence; on invalid input, leave state unchanged and restore the prior value. Verify valid integers still update the portfolio and fractional Allocation edits remain supported.
- [x] 1.2 Add focused runtime tests for accepted integer edits, rejected fractional edits, unchanged pre-existing imported/saved values, and decimal Allocation edits; verify the focused runtime tests pass.

## 2. Position-entry field sizing

- [x] 2.1 Increase the shared position input width from 84px to approximately 97px in base and mobile styles; verify both mode inputs use the target width without layout overflow.
- [x] 2.2 Update contract coverage for desktop and mobile input widths; verify the focused web contract tests pass.

## 3. Responsive integration

- [x] 3.1 Verify Shares and Allocation entry on desktop and mobile: whole-share validation applies only in Shares mode, allocation decimals remain editable, and the wider field does not cause horizontal overflow.
