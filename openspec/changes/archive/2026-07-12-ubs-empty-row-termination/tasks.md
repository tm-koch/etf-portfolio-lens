## 1. Parser Update

- [x] 1.1 Update the UBS spreadsheet row parsing logic to stop at the first completely empty row.
- [x] 1.2 Ensure rows after the termination row are ignored and never reach normalization.
- [x] 1.3 Keep valid holdings before the empty row unchanged.

## 2. Verification

- [x] 2.1 Add or update a fixture-based test for CH0130595124 that confirms disclaimer rows after the empty row are excluded.
- [x] 2.2 Add or update a parser-level test that proves the first empty row acts as a hard table terminator.
- [x] 2.3 Run the full ingestion test suite to confirm no other ETF source behavior regresses.
