## Context

The current UBS XML-spreadsheet parser identifies the holdings header and then iterates over subsequent rows. It currently skips empty rows and continues parsing later rows, which allows disclaimer/footer text after the holdings table to be considered for row parsing. For CH0130595124, the first empty row is the logical end of the holdings table.

## Goals / Non-Goals

**Goals:**
- Stop parsing the UBS holdings table at the first empty row.
- Prevent disclaimer/footer rows after the holdings table from entering the holdings output.
- Preserve all valid holdings that appear before the termination row.

**Non-Goals:**
- Do not redesign the table parser for all file types.
- Do not add heuristics based on disclaimer text content.
- Do not change matching, enrichment, or snapshot schema behavior beyond the parsed row set.

## Decisions

1. Treat the first completely empty row as a hard table terminator for the UBS holdings source.
   - Rationale: the source file structure already signals the end of the holdings table with a blank row, so this is the most reliable boundary.
   - Alternative considered: continue skipping empty rows and rely on later filters. Rejected because it allows footer/disclaimer rows to flow through parsing and makes the boundary ambiguous.

2. Apply the rule in the row-to-table parsing layer rather than downstream normalization.
   - Rationale: once disclaimer rows are parsed into dictionaries, downstream code must still inspect and discard them. Stopping at the parser layer keeps the raw parsed table faithful to the source structure.
   - Alternative considered: filter the unwanted rows during normalization. Rejected because normalization should not need source-layout knowledge.

3. Keep the change source-specific to the UBS holdings path.
   - Rationale: other source adapters may use empty rows differently, so the termination rule should not become a blanket behavior for every spreadsheet.
   - Alternative considered: change all spreadsheet parsing to stop at the first blank row. Rejected because it could truncate valid holdings in other sources that use spacer rows.

## Risks / Trade-offs

- [A future UBS file may contain a legitimate spacer row before the end of holdings] → Keep the rule scoped to the verified CH0130595124 UBS path and validate against the fixture before broadening it.
- [Other .xls sources might also inherit the helper if the implementation is shared] → Preserve source-specific selection at the adapter level so the termination rule only applies where intended.
- [Dropping rows earlier may make debugging harder if the termination row is accidental] → Keep the raw download retained and rely on fixture-based tests to confirm the parser boundary.

## Migration Plan

1. Update the UBS parser path to stop collecting rows after the first empty row.
2. Validate the CH0130595124 snapshot to confirm disclaimer rows are no longer present as holdings.
3. Run the full ingestion test suite to ensure existing source behavior remains unchanged.
4. If another UBS source shows the same table-ending pattern, apply the same rule only after fixture validation.

## Open Questions

- Should this termination rule be applied only to CH0130595124, or to all UBS XML-spreadsheet holdings files that use the same layout?
