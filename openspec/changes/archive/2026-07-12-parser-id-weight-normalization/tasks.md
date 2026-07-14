## 1. Parser-Aware Normalization

- [x] 1.1 Define the parser ID to weight-unit mapping for known ETF sources.
- [x] 1.2 Update normalization to scale only fraction-based sources to percentage values.
- [x] 1.3 Keep percent-based sources unchanged so canonical snapshots preserve their published units.

## 2. Validation and Regression Coverage

- [x] 2.1 Add a backend check that holding, sector, region, and currency weight totals stay within 100 percent plus tolerance.
- [x] 2.2 Add regression tests covering a percent-based source and a fraction-based source.
- [x] 2.3 Regenerate or verify affected snapshots so the published JSON reflects the corrected units.
