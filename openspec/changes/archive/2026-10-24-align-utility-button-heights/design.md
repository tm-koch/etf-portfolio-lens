# Design

## Context

The controls share `.app-utility-content` but have separate sizing rules. The report button currently has a fixed 42px height, the mobile language and color-mode triggers use 37px, and the install action relies on padding and its current content. See [proposal.md](proposal.md) for motivation and the spec deltas for the required alignment behavior.

## Goals / Non-Goals

**Goals:**
- Give the utility controls a consistent outer height at each responsive breakpoint.
- Keep the install action aligned when visible without changing when it appears.

**Non-Goals:**
- Change control widths, labels, icons, focus treatment, interaction, or visibility behavior.
- Reposition the utility bar or alter navigation and page layout.

## Decisions

- Define a shared CSS height token for utility triggers and apply it to the language, color-mode, report-export, and install buttons. Use `box-sizing: border-box` so borders are included in the shared outer height.
- Set the token at the existing desktop and mobile breakpoints, anchoring its value to the established language/color-mode trigger dimensions. Keep each button's current width, padding/layout, and content visibility rules; center the contents within the shared box.
- Add responsive contract checks for the four controls, including the install action when visible. A browser check should compare computed outer heights at widths on both sides of the 760px breakpoint and verify top/bottom alignment.

Alternative considered: change only the report button's current height. That would leave the independently sized install control vulnerable to the same mismatch and retain duplicated dimensions; one shared token gives all utility triggers a single sizing rule.

## Risks / Trade-offs

- [A visible install label may not fit a shared fixed height] → Preserve its existing horizontal layout and verify the label remains vertically centered and unclipped at desktop widths.
- [Breakpoint-specific dimensions may drift from the reference controls] → Keep the values on one shared token and test computed dimensions at desktop and mobile widths.
