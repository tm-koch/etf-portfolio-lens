## Context

The ingestion backend currently treats all raw weights as if they needed the same conversion. That works for fraction-based sources such as Amundi, but it breaks sources that already provide percentage values such as iShares, SPDR, and UBS. The result is a mixed-unit backend contract that is easy to misuse and hard to validate.

## Goals / Non-Goals

**Goals:**
- Select the correct weight normalization behavior from the parser ID.
- Preserve the existing snapshot schema and field names.
- Ensure holdings and aggregate rollups are internally consistent in percentage units.
- Add a validation guard that detects totals above 100 percent.

**Non-Goals:**
- Renaming snapshot fields.
- Changing source parsers beyond the metadata needed to identify weight semantics.
- Reworking the frontend presentation layer.

## Decisions

Use parser ID as the normalization switch.
- Rationale: the parser already encodes source-specific shape and semantics, so it is the least ambiguous place to decide whether a source weight is already a percentage.
- Alternatives considered: detect units purely from headers or raw numeric ranges. Rejected because both are brittle when sources rename columns or have small holdings that confuse range checks.

Represent source semantics explicitly in backend normalization.
- Rationale: the backend should own the contract for `weight_pct`, and the parser-specific rule keeps consumers from having to guess at units.
- Alternatives considered: converting only at serialization time. Rejected because it leaves internal data inconsistent and easier to misuse.

Validate topic totals after aggregation.
- Rationale: if holdings or one of the aggregate topic rollups exceeds 100 percent, that is a strong indicator of double conversion or malformed source data.
- Alternatives considered: only validating top-level holdings totals. Rejected because sector, region, and currency rollups can still reveal the same bug independently.

## Risks / Trade-offs

[Parser metadata can drift from the real source format] → Keep the normalization mapping small and add a regression test per parser/source pair that exercises the source-weight unit.

[Some sources may change format without changing parser ID] → Add a fallback warning path and keep the validation guard so unexpected totals fail fast.

[Rounding can create totals slightly above 100] → Allow a small tolerance when validating the totals.
